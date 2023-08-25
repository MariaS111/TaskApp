import {createContext, useState, useEffect} from 'react';
import jwt_decode from "jwt-decode";
import {useNavigate} from 'react-router-dom';
import { upload } from '@testing-library/user-event/dist/upload';
import LoginPage from '../pages/LoginPage';

const AuthContext = createContext()

export default AuthContext;

export const AuthProvider = ({children}) => {
    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    let [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null);
    let [loading, setLoading] = useState(true)

    const history = useNavigate();

    let loginUser = async (e) => {
        e.preventDefault()
        let responce = await fetch('http://127.0.0.1:8000/api/users/token/', {
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

    
    let registerUser = async (e) => {
        e.preventDefault()
        let responce = await fetch('http://127.0.0.1:8000/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'username': e.target.username.value, 'password': e.target.password.value, 'password2': e.target.password2.value,
            'email': e.target.email.value, 'first_name': e.target.first_name.value, 'last_name': e.target.last_name.value})
        })

        let data = await responce.json()
        
        if (responce.status === 201) {
            await loginUser(e)
            history('/')
        }
        else {
            alert(`Invalid information or you don't fill all fields!\n${responce.statusText}\nTry again!`)
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
        let responce = await fetch('http://127.0.0.1:8000/api/users/token/refresh/', {
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
        let thirtyminutes = 1000 * 60 * 30
        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, thirtyminutes)
        return () => clearInterval(interval)

    }, [authTokens, loading])

    let contextData = {
        loginUser: loginUser,
        authTokens:authTokens,
        user:user,
        logoutUser: logoutUser,
        registerUser: registerUser,
    }

    return <AuthContext.Provider value={contextData}>
        {loading ? null : children}
    </AuthContext.Provider>
}