import { useContext } from "react";
import AuthContext from "../context/AuthContext";


function LoginPage() {
  let {loginUser} = useContext(AuthContext)
  return (
    <div>
        <form onSubmit={loginUser} class="input-form">
            <input class="form-control" type="text" name="username" placeholder='Enter username'/>
            <input class="form-control" type="password" name="password" placeholder='Enter password'/>
            <input type='submit' class="btn btn-primary"/>
        </form>
    </div>
  )
}

export default LoginPage