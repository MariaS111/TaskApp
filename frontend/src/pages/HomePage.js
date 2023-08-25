import {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'

const HomePage = () => {
  let [boards, setBoards] = useState([])
  let {authTokens, logoutUser} = useContext(AuthContext)

  useEffect(()=> {
      getBoards()
  }, [])


  let getBoards = async() =>{
      let response = await fetch('http://127.0.0.1:8000/api/board/', {
          method:'GET',
          headers:{
              'Content-Type':'application/json',
              'Authorization':'Bearer ' + String(authTokens.access)
          }
      })
      let data = await response.json()

      if(response.status === 200){
          setBoards(data)
      }else if(response.statusText === 'Unauthorized'){
          logoutUser()
      }
      
  }

  return (
      <div>
          <ul>
              {Array.isArray(boards.results) && boards.results.map(board => (
                  <li key={board.id} >{board.title}</li>
              ))}
          </ul>
      </div>
  )
}

export default HomePage