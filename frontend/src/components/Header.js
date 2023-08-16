import React, {useContext} from 'react';
import {
  Link
} from "react-router-dom";
import AuthContext from '../context/AuthContext';

const Header = () => {
  let {user, logoutUser} = useContext(AuthContext)
  return (
    <div>
        <h1>Notes</h1>
        <Link to='/'>Home</Link>
        <span> | </span>
        {
        !user ? <Link to='/login'>Login</Link> : (<p onClick={logoutUser}>Logout</p>)
        }
        {user && <p>Hello {user.username}</p>}
    </div>
  )
}

export default Header