import {createContext, useState, useEffect} from 'react';
import jwt_decode from "jwt-decode";
import {useNavigate} from 'react-router-dom';
import { upload } from '@testing-library/user-event/dist/upload';

const AuthContext = createContext()

export default AuthContext;

export const AuthProvider = ({children}) => {
    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    let [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null);
    let [loading, setLoading] = useState(true)

    const history = useNavigate();

    let loginUser = async (e) => {
        e.preventDefault()
        let responce = await fetch('http://127.0.0.1:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'username': e.target.username.value, 'password': e.target.password.value})
        })

        let data = await responce.json()

        if (responce.status === 200) {
            setAuthTokens(data);
            setUser(jwt_decode(data.access));
            localStorage.setItem('authTokens', JSON.stringify(data));
            history('/')
        }
        else {
            alert("Invalid username or password!\nTry again!")
        }

    }

    let logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        history('/login')
    }

    let updateToken = async () => {
        console.log("Updated")
        let responce = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'refresh':authTokens?.refresh})
        })

        let data = await responce.json()

        if (responce.status === 200) {
            setAuthTokens(data);
            setUser(jwt_decode(data.access));
            localStorage.setItem('authTokens', JSON.stringify(data));
        }
        else {
            logoutUser()
        }

        if (loading){
            setLoading(false);
        }
    }

    useEffect (() => {
        if (loading){
            updateToken()
        }
        let fourminutes = 1000 * 60 * 4
        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, fourminutes)
        return () => clearInterval(interval)

    }, [authTokens, loading])

    let contextData = {
        loginUser: loginUser,
        authTokens:authTokens,
        user:user,
        logoutUser: logoutUser,
    }

    return <AuthContext.Provider value={contextData}>
        {loading ? null : children}
    </AuthContext.Provider>
}