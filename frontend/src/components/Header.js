import React, {useContext} from 'react';
import {
  Link
} from "react-router-dom";
import AuthContext from '../context/AuthContext';

const Header = () => {
  let {user, logoutUser, continueWithGithub} = useContext(AuthContext)
  return (
    <div>
      <h1>Task App</h1>
      <Link to="/" >Home</Link>
            {user ? (
              <div class='span'>
                 <a  onClick={logoutUser}>Logout</a> 
                 <Link to="/profile">Profile</Link>
              </div>
            ): (
              <div class='span'>
                <button>Login with GitHub</button>
                <Link to="/login" >Login</Link> 
                <Link to="/register" >Registration</Link>
              </div>
            )}
        {user && <p>Hello {user.username}</p>}
    </div>
  )
}

export default Header