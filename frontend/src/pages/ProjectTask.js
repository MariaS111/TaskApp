import {useState, useEffect, useContext} from 'react'
import AuthContext from '../context/AuthContext'
import { useParams, useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';


const ProjectTask = () => {
    const { projectId, boardId, teamtaskId } = useParams();
    const [tasks, setTasks] = useState([]);
    let {authTokens, logoutUser} = useContext(AuthContext)
    const [comments, setComments] = useState([]);
    const history = useNavigate();

    useEffect(() => {
        const fetchTask = async () => {
          try {
            const taskResponse = await fetch(
              `http://127.0.0.1:8000/api/projects/project/${projectId}/teamboard/${boardId}/teamtask/${teamtaskId}/`,
              {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json',
                  Authorization: 'Bearer ' + String(authTokens.access),
                },
              }
            );
            const taskData = await taskResponse.json();
            setTasks(taskData);
    
            // Загрузка комментариев для задачи
            const commentsResponse = await fetch(
              `http://127.0.0.1:8000/api/projects/project/${projectId}/teamboard/${boardId}/teamtask/${teamtaskId}/comments/`,
              {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json',
                  Authorization: 'Bearer ' + String(authTokens.access),
                },
              }
            );
            const commentsData = await commentsResponse.json();
            setComments(commentsData);
          } catch (error) {
            console.error('Error fetching task information:', error);
          }
        };
    
        fetchTask();
      }, [projectId, boardId, teamtaskId, authTokens.access]);

const handleDelete = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/projects/project/${projectId}/teamboard/${boardId}/teamtask/${teamtaskId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + String(authTokens.access)
      },
    });

    if (response.ok) {
      console.log('Board deleted successfully');
      history(`/projects/${projectId}/boards/${projectId}`)
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
      <p>Worker: {tasks.worker}</p>
    </div>
    <div class="task-btns">
    <Link to={`/boards/${boardId}/tasks/${tasks.id}/upd`} className="btn btn-primary">
                Change task
      </Link>
      <button className="btn btn-primary" onClick={handleDelete}>
                Delete task
      </button>
      <Link to={`/boards/${boardId}/tasks/${tasks.id}/upd`} className="btn btn-primary">
                Add comment
      </Link>
      </div>

      <div className='comments'>
        <h3>Comments</h3>
        <ul>
        {Array.isArray(comments.results) && comments.results.map(comment => (
            <li key={comment.id}>{comment.content} by {comment.user}</li>
          ))}
        </ul>
      </div>

  </div>
);

}

export default ProjectTask