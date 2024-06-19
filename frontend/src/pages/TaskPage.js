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
      const boardResponse = await fetch(`http://localhost:8000/api/board/${boardId}/task/${taskId}`, {
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
    const response = await fetch(`http://localhost:8000/api/board/${boardId}/task/${taskId}/`, {
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

const getStatusLabel = (status) => {
  switch (status) {
    case 'F':
      return 'Future';
    case 'O':
      return 'Overdue';
    case 'PR':
      return 'In Progress';
    case 'D':
      return 'Done';
    default:
      return 'Unknown';
  }
};


return (
  <div>
    <div>
      <h2>{tasks.title}</h2>
      <p>{tasks.description}</p>
      <p>Start Date: {tasks.start_date}</p>
      <p>End Date: {tasks.end_date}</p>
      <p>Last Updated: {tasks.updated}</p>
      <p>Status: {getStatusLabel(tasks.status)}</p>
    </div>
    <div class="task-btns">
    <Link to={`/boards/${boardId}/tasks/${tasks.id}/upd`} className="btn btn-primary">
                Change task
      </Link>
      <button className="btn btn-primary" onClick={handleDelete}>
                Delete task
      </button>
      </div>
  </div>
);

}

export default TaskPage