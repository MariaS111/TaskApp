import { useContext } from "react";
import AuthContext from "../context/AuthContext";


function RegisterPage() {
  let {registerUser} = useContext(AuthContext)
  return (
    <div class="div">
        <form onSubmit={registerUser} class="input-form register-form">
            <input class="form-control" type="text" name="username" placeholder='Enter username'/>
            <input class="form-control" type="password" name="password" placeholder='Enter password'/>
            <input class="form-control" type="password" name="password2" placeholder='Enter password again'/>
            <input class="form-control" type="text" name="email" placeholder='Enter email'/>
            <input class="form-control" type="text" name="first_name" placeholder='Enter first name'/>
            <input class="form-control" type="text" name="last_name" placeholder='Enter last name'/>
            <input type='submit' class="btn btn-primary"/>
        </form>
    </div>
  )
}

export default RegisterPage