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
      <div>
        <img src={profile.userprofile.profile_image} class='profile-image' alt="Profile Image"></img>
          <ul>
              <li>{profile.username}</li>
              <li>{profile.first_name}</li>
              <li>{profile.last_name}</li>
              <li>{profile.email}</li>
              <li>{profile.is_verified ? 'Email is verified' : 'Email not verified'}</li>
          </ul>
      </div>
  )
}

export default Profile