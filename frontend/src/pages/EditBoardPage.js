import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { useParams, useHistory, useNavigate } from 'react-router-dom';

const EditBoardPage = ({ match }) => {
    const { boardId} = useParams();
    let {authTokens, logoutUser} = useContext(AuthContext)
    const history = useNavigate();
    const [boardData, setBoardData] = useState({

    title: '',
    description: '',
  });

  useEffect(() => {
    const fetchBoardData = async () => {
      try {
        const response = await fetch(`http://django:8000/api/board/${boardId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization':'Bearer ' + String(authTokens.access)
          },
        });

        if (response.ok) {
          const data = await response.json();
          setBoardData({
            id: data.id,
            title: data.title,
            description: data.description,
          });
        } else {
          console.error('Failed to fetch board data');
        }
      } catch (error) {
        console.error('Error fetching board data:', error);
      }
    };

    fetchBoardData();
  }, [boardId]);


  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBoardData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/board/${boardId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + String(authTokens.access)
        },
        body: JSON.stringify(boardData),
      });

      if (response.ok) {
        console.log('Board data updated successfully');
        // После успешного обновления, переход на страницу /boards/${boardId}
        history(`/boards/${boardId}/tasks`);
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
      <h2>Edit Board</h2>
        <label>Title:</label>
        <input class="form-control" type="text" name="title" value={boardData.title} onChange={handleInputChange} />
        <label>Description:</label>
        <textarea class="form-control" name="description" value={boardData.description} onChange={handleInputChange} />

        <button type="submit" class="btn btn-primary">Save Changes</button>
      </form>
    </div>
  );
};

export default EditBoardPage;
