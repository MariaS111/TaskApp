import React, {useContext} from 'react';
import {
  Link
} from "react-router-dom";
import AuthContext from '../context/AuthContext';

const Header = () => {
  let {user, logoutUser, continueWithGithub} = useContext(AuthContext)
  return (
    <div class="header">
         <Link  to="/boards" class="icon-link" >My Boards</Link>
         <Link  to="#" class="icon-link" >Team Boards</Link>
         <Link  to="/projects" class="icon-link" >Projects</Link>
            {user ? (
             <div class="horizontal">
              <Link to="/profile" class="icon-link">Profile</Link>
              <a onClick={logoutUser} class="icon-link">Logout</a> 
              </div>
            ): (
              <div class="horizontal">
                {/* <button type="button" class="btn btn-primary">Login with GitHub</button> */}
                <Link to="/login" class="icon-link">Login</Link> 
                <Link to="/register" class="icon-link">Registration</Link>
              </div>
            )}
    </div>
   
  )
}

export default Header