import {useState, useEffect, useContext} from 'react'
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext'

const HomePage = () => {
  let [boards, setBoards] = useState([])
  let {authTokens, logoutUser} = useContext(AuthContext)

  useEffect(()=> {
      getBoards()
  }, [])


  let getBoards = async() =>{
      let response = await fetch('http://django:8000/api/board/', {
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
      <div class="div boards">
        <Link to={`/boards/add`} className="btn btn-primary">
                Add new board
        </Link>
        <div class="div boards">   
        {Array.isArray(boards.results) && boards.results.map(board => (
            
          <div key={board.id} class="div card text-center">
            <div class="div card-body">
                <h5 key={board.id} class="card-title">{board.title}</h5>
                <p key={board.id} class="card-text">{board.description}</p>
                {/* <a href="#" class="btn btn-primary">Show...</a> */}
                <Link to={`/boards/${board.id}/tasks`} className="btn btn-primary">
                Show more...
                </Link>

            </div>
            </div>
             ))}
      </div>
      </div>
  )
}

export default HomePage