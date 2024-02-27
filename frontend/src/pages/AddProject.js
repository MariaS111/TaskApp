import { useContext, useState } from "react";
import AuthContext from "../context/AuthContext";
import { useParams, useNavigate} from 'react-router-dom';

function AddProjectPage() {
  let { authTokens, logoutUser } = useContext(AuthContext);
  const history = useNavigate()
  const [boardData, setBoardData] = useState({
    title: '',
    description: '',
  });

  const addBoard = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://django:8000/api/projects/project/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + String(authTokens.access),
        },
        body: JSON.stringify(boardData),
      });

      if (response.ok) {
        console.log('Board added successfully');
        history(`/projects/`)
        // Дополнительные действия после успешного добавления доски
      } else {
        console.error('Failed to add board');
      }
    } catch (error) {
      console.error('Error adding board:', error);
    }
  };

  const handleInputChange = (e) => {
    setBoardData({
      ...boardData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="div">
      <form onSubmit={addBoard} className="input-form">
        <input className="form-control" type="text" name="title" placeholder='Enter title' onChange={handleInputChange} />
        <input className="form-control" type="text" name="description" placeholder='Enter description' onChange={handleInputChange} />
        <button type='submit' className="btn btn-primary">Send</button>
      </form>
    </div>
  );
}

export default AddProjectPage;
