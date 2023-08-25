import { useContext } from "react";
import AuthContext from "../context/AuthContext";


function RegisterPage() {
  let {registerUser} = useContext(AuthContext)
  return (
    <div>
        <form onSubmit={registerUser}>
            <input type="text" name="username" placeholder='Enter username'/>
            <input type="password" name="password" placeholder='Enter password'/>
            <input type="password" name="password2" placeholder='Enter password again'/>
            <input type="text" name="email" placeholder='Enter email'/>
            <input type="text" name="first_name" placeholder='Enter first name'/>
            <input type="text" name="last_name" placeholder='Enter last name'/>
            <input type='submit'/>
        </form>
    </div>
  )
}

export default RegisterPage