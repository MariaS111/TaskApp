import {useState, useEffect, useContext} from 'react'
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext'

const ProjectsPage = () => {
  let [projects, setProjects] = useState([])
  let {authTokens, logoutUser} = useContext(AuthContext)

  useEffect(()=> {
      getProjects()
  }, [])


  let getProjects = async() =>{
      let response = await fetch('http://localhost:8000/api/projects/project', {
          method:'GET',
          headers:{
              'Content-Type':'application/json',
              'Authorization':'Bearer ' + String(authTokens.access)
          }
      })
      let data = await response.json()

      if(response.status === 200){
          setProjects(data)
      }else if(response.statusText === 'Unauthorized'){
          logoutUser()
      }
      
  }

  return (
      <div class="div boards">
        <Link to={`/projects/add`} className="btn btn-primary">
                Add new project
        </Link>
        <div class="div boards">   
        {Array.isArray(projects.results) && projects.results.map(project => (
            
          <div key={project.id} class="div card text-center">
            <div class="div card-body">
                <h5 key={project.id} class="card-title">{project.title}</h5>
                <p key={project.id} class="card-text">{project.description}</p>
                {/* <a href="#" class="btn btn-primary">Show...</a> */}
                <Link to={`/projects/${project.id}/boards`} className="btn btn-primary">
                Show more...
                </Link>

            </div>
            </div>
             ))}
      </div>
      </div>
  )
}

export default ProjectsPage