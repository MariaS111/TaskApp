import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { useParams, useHistory, useNavigate } from 'react-router-dom';

const EditTaskPage = ({ match }) => {
    const { boardId, taskId} = useParams();
    let {authTokens, logoutUser} = useContext(AuthContext)
    const history = useNavigate();
    const [taskStatus, setTaskStatus] = useState('');

    const [taskData, setTaskData] = useState({
    title: '',
    description: '',
    start_date: '',
    end_date: '',
    status: '',
  });

  useEffect(() => {
    const fetchTaskData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/board/${boardId}/task/${taskId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization':'Bearer ' + String(authTokens.access)
          },
        });

        if (response.ok) {
          const data = await response.json();
          setTaskData({
            id: data.id,
            title: data.title,
            description: data.description,
            start_date: data.start_date,
            end_date: data.end_date,
            status: data.status, 
          });
          setTaskStatus(data.status); // Добавленный код
        } else {
          console.error('Failed to fetch board data');
        }
      } catch (error) {
        console.error('Error fetching board data:', error);
      }
    };

    fetchTaskData();
  }, [taskId]);


  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setTaskData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleCheckboxChange = () => {
    setTaskData((prevData) => ({
      ...prevData,
      status: prevData.status === 'D' ? '' : 'D',
      
    }));
    history(`/boards/${boardId}/tasks/`);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/board/${boardId}/task/${taskId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + String(authTokens.access)
        },
        body: JSON.stringify(taskData),
      });

      if (response.ok) {
        console.log('Board data updated successfully');
        // После успешного обновления, переход на страницу /boards/${boardId}
        history(`/boards/${boardId}/tasks/${taskId}`);
      } else {
        console.error('Failed to update board data');
      }
    } catch (error) {
      console.error('Error updating board data:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} class="input-form for-task">
        <h2>Edit Task</h2>
        <input class="form-control" type="text" name="title" value={taskData.title} onChange={handleInputChange} />
        <textarea class="form-control" name="description" value={taskData.description} onChange={handleInputChange} />
        <input class="form-control" type="text" name="start_date" value={taskData.start_date} onChange={handleInputChange} />
        <input class="form-control" type="text" name="end_date" value={taskData.end_date} onChange={handleInputChange} />
        <div>
            <input
              type="checkbox"
              name="status"
              checked={taskData.status === 'D'}
              onChange={handleCheckboxChange}
            />
            Done
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </form>
    </div>
  );
};

export default EditTaskPage;
