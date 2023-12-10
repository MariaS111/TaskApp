import {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'
import { useParams } from 'react-router-dom';
import { Link, useNavigate } from 'react-router-dom';


const ProjectBoardPage = () => {
    const { projectId } = useParams();
    const [project, setProject] = useState({});
    const [boards, setBoards] = useState([]);
    const history = useNavigate();
    let {authTokens, logoutUser} = useContext(AuthContext)

useEffect(() => {
  // Получаем информацию о доске
  const fetchProjectInfo = async () => {
    try {
      const boardResponse = await fetch(`http://127.0.0.1:8000/api/projects/project/${projectId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':'Bearer ' + String(authTokens.access)
        },
      });
      const projectData = await boardResponse.json();
      setProject(projectData);
    } catch (error) {
      console.error('Error fetching board information:', error);
    }
  };

  // Получаем список тасков для доски
  const fetchBoards = async () => {
    try {
      const tasksResponse = await fetch(`http://127.0.0.1:8000/api/projects/project/${projectId}/teamboard/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':'Bearer ' + String(authTokens.access)
        },
      });
      const boardsData = await tasksResponse.json();
      setBoards(boardsData.results);
      console.log("wtf")
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  fetchProjectInfo();
  fetchBoards();
}, [projectId]);


const handleDelete = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/projects/project/${projectId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + String(authTokens.access)
      },
    });

    if (response.ok) {
      console.log('Project deleted successfully');
      history(`/projects`)
      // После успешного удаления, переход на другую страницу
    } else {
      console.error('Failed to delete project');
    }
  } catch (error) {
    console.error('Error deleting project:', error);
  }
};

return (
  <div class="whole-width">
    <div className="board-info">
      <h2>{project.title}</h2>
      <p>{project.description}</p>
      <p>{project.user}</p>
      <p>{project.watchers}</p>
      <div class="board-actions">
      {/* <Link to={`/boards/${board.id}/tasks/add`} className="btn btn-primary">
                Add new task
      </Link>
      <Link to={`/boards/${board.id}/change`} className="btn btn-primary">
                Change board information
      </Link>
      <Link to={`/boards/${board.id}/done`} className="btn btn-primary">
                Show done tasks
      </Link>
      <button className="btn btn-primary" onClick={handleDelete}>
                Delete board 
      </button> */}
      </div>
    </div>
    
    <div className="tasks-list">
      <h3>TeamBoards</h3>
      <div class="tasks">
        {boards.map(board => (
          <div class="card text-center" key={board.id}>
            <h5 class="card-title">{board.title}</h5>
            <p class="card-text">{board.description}</p>
            {/* Добавьте другие поля задачи, которые вам нужны */}
            <Link to={`/projects/${project.id}/boards/${board.id}`} className="btn btn-primary">
                Show more...
            </Link>
          </div>
        ))}
      </div>
    </div>
  </div>
);

}

export default ProjectBoardPage