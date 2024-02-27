import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import { useParams, useNavigate} from 'react-router-dom';
import {useState} from 'react'


function AddTaskPage() {
    let { authTokens, logoutUser } = useContext(AuthContext);
    const { boardId } = useParams();
    const history = useNavigate()
    const [taskData, setTaskData] = useState({
      title: '',
      description: '',
      start_date: '',
      end_date: '',
    });

  const addTask = async (e) => {
    e.preventDefault();
    console.log(taskData)
    try {
      const response = await fetch(`http://django:8000/api/board/${boardId}/task/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + String(authTokens.access),
        },
        body: JSON.stringify(taskData),
      });

      if (response.ok) {
        history(`/boards/${boardId}/tasks`)
        console.log('Task added successfully');
        // Дополнительные действия после успешного добавления задачи
      } else {
        console.error('Failed to add task');
      }
    } catch (error) {
      console.error('Error adding task:', error);
    }
};
  
const handleInputChange = (e) => {
    setTaskData({
      ...taskData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div class="div">
        <form onSubmit={addTask} class="input-form for-task">
            <input class="form-control" type="text" name="title" placeholder='Enter title' onChange={handleInputChange} />
            <input class="form-control" type="text" name="description" placeholder='Enter description' onChange={handleInputChange} />
            <input class="form-control" type="text" name="start_date" placeholder='Enter start date (format yy-mm-dd hh:mm)' onChange={handleInputChange} />
            <input class="form-control" type="text" name="end_date" placeholder='Enter end date (format yy-mm-dd hh:mm)' onChange={handleInputChange} />
            <button type='submit' class="btn btn-primary">Send</button>
        </form>
    </div>
  )
}

export default AddTaskPage