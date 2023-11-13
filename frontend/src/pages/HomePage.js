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
      <div class="boards">   
        {Array.isArray(boards.results) && boards.results.map(board => (
                //   <li key={board.id} >{board.title}</li>
            
          <div key={board.id} class="card text-center">
            {/* <div class="card-header">
                Featured
            </div> */}
            <div class="card-body">
                <h5 key={board.id} class="card-title">{board.title}</h5>
                <p key={board.id} class="card-text">{board.description}</p>
                <a href="#" class="btn btn-primary">Show...</a>
            </div>
            {/* <div class="card-footer text-body-secondary">
                2 days ago
            </div> */}
            </div>
             ))}
      </div>
  )
}

export default HomePage