import {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'

const Profile = () => {
  let [profile, setProfile] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    userprofile: {
      profile_image: ''
    }
  });
  let {authTokens, logoutUser} = useContext(AuthContext)

  useEffect(()=> {
      getProfile()
  }, [])


  let getProfile = async() =>{
      let response = await fetch('http://127.0.0.1:8000/api/users/profile', {
          method:'GET',
          headers:{
              'Content-Type':'application/json',
              'Authorization':'Bearer ' + String(authTokens.access)
          }
      })
      let data = await response.json()

      if(response.status === 200){
          setProfile(data)
      }else if(response.statusText === 'Unauthorized'){
          logoutUser()
      }
      console.log(data.userprofile.profile_image)
  }

  return (
      <div class="profile">
        <img src={profile.userprofile.profile_image} class='profile-image' alt="Profile Image"></img>
          <ul class="list-group">
              <li class="list-group-item">Username: {profile.username}</li>
              <li class="list-group-item">First name: {profile.first_name}</li>
              <li class="list-group-item">Last name: {profile.last_name}</li>
              <li class="list-group-item">Email: {profile.email}</li>
              <li class="list-group-item">{profile.is_verified ? 'Email is verified' : 'Email not verified'}</li>
          </ul>
          <div class="btns">
            <button class="btn btn-primary">Change profile information</button>

          </div>
      </div>
  )
}

export default Profile