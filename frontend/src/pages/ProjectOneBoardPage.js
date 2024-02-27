import {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'
import { useParams } from 'react-router-dom';
import { Link, useNavigate } from 'react-router-dom';


const ProjectOneBoardPage = () => {
    const { boardId, projectId } = useParams();
    const [board, setBoard] = useState({});
    const [tasks, setTasks] = useState([]);
    const history = useNavigate();
    let {authTokens, logoutUser} = useContext(AuthContext)

useEffect(() => {
  // Получаем информацию о доске
  const fetchBoardInfo = async () => {
    try {
      const boardResponse = await fetch(`http://django:8000/api/projects/project/${projectId}/teamboard/${boardId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':'Bearer ' + String(authTokens.access)
        },
      });
      const boardData = await boardResponse.json();
      setBoard(boardData);
    } catch (error) {
      console.error('Error fetching board information:', error);
    }
  };

  // Получаем список тасков для доски
  const fetchTasks = async () => {
    try {
      const tasksResponse = await fetch(`http://django:8000/api/projects/project/${projectId}/teamboard/${boardId}/teamtask`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':'Bearer ' + String(authTokens.access)
        },
      });
      const tasksData = await tasksResponse.json();
      setTasks(tasksData.results);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  fetchBoardInfo();
  fetchTasks();
}, [boardId, projectId]);


const handleDelete = async () => {
  try {
    const response = await fetch(`http://django:8000/api/projects/project/${projectId}/teamboard/${boardId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + String(authTokens.access)
      },
    });

    if (response.ok) {
      console.log('Board deleted successfully');
      history(`/boards`)
      // После успешного удаления, переход на другую страницу
    } else {
      console.error('Failed to delete board');
    }
  } catch (error) {
    console.error('Error deleting board:', error);
  }
};

return (
  <div class="whole-width">
    <div className="board-info">
      <h2>{board.title}</h2>
      <p>{board.description}</p>
      <p>{board.admins}</p>
      <p>{board.participants}</p>
      <div class="board-actions">
      <Link to={`/boards/${board.id}/tasks/add`} className="btn btn-primary">
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
      </button>
      </div>
    </div>
    
    <div className="tasks-list">
      <h3>Tasks</h3>
      <div class="div boards">
        {tasks.map(task => (
          <div class="div card text-center" key={task.id}>
            <div class="div card-body">
            <h5 class="card-title">{task.title}</h5>
            <p class="card-text">{task.description}</p>
            {/* Добавьте другие поля задачи, которые вам нужны */}
            <Link to={`/projects/${projectId}/boards/${boardId}/tasks/${task.id}`} className="btn btn-primary">
                Show more...
            </Link>
          </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);

}

export default ProjectOneBoardPage