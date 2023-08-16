import {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'

const HomePage = () => {
  let [tasks, setTasks] = useState([])
  let {authTokens, logoutUser} = useContext(AuthContext)

  useEffect(()=> {
      getNotes()
  }, [])


  let getNotes = async() =>{
      let response = await fetch('http://127.0.0.1:8000/api/task/', {
          method:'GET',
          headers:{
              'Content-Type':'application/json',
              'Authorization':'Bearer ' + String(authTokens.access)
          }
      })
      let data = await response.json()

      if(response.status === 200){
          setTasks(data)
      }else if(response.statusText === 'Unauthorized'){
          logoutUser()
      }
      
  }

  return (
      <div>
          <p>You are logged to the home page!</p>
          {/* {console.log(tasks.results)} */}
          <ul>
              {Array.isArray(tasks.results) && tasks.results.map(task => (
                  <li key={task.id} >{task.title}</li>
              ))}
          </ul>
      </div>
  )
}

export default HomePage