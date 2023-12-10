import {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'
import { useParams, useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';


const TaskPage = () => {
    const { taskId , boardId} = useParams();
    const [tasks, setTasks] = useState([]);
    let {authTokens, logoutUser} = useContext(AuthContext)
    const history = useNavigate();

useEffect(() => {
  const fetchTask = async () => {
    try {
      const boardResponse = await fetch(`http://127.0.0.1:8000/api/board/${boardId}/task/${taskId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization':'Bearer ' + String(authTokens.access)
        },
      });
      const boardData = await boardResponse.json();
      setTasks(boardData);
    } catch (error) {
      console.error('Error fetching board information:', error);
    }
  };

  fetchTask();
}, [taskId]);

const handleDelete = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/board/${boardId}/task/${taskId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + String(authTokens.access)
      },
    });

    if (response.ok) {
      console.log('Board deleted successfully');
      history(`/boards/${boardId}/tasks`)
    } else {
      console.error('Failed to delete board');
    }
  } catch (error) {
    console.error('Error deleting board:', error);
  }
};

return (
  <div>
    <div>
      <h2>{tasks.title}</h2>
      <p>{tasks.description}</p>
      <p>{tasks.start_date}</p>
      <p>{tasks.end_date}</p>
      <p>{tasks.updated}</p>
      <p>{tasks.status}</p>
    </div>

    <Link to={`/boards/${boardId}/tasks/${tasks.id}/upd`} className="btn btn-primary">
                Change task
      </Link>
      <button className="btn btn-primary" onClick={handleDelete}>
                Delete task
      </button>
  </div>
);

}

export default TaskPage