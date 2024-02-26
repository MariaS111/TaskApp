import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import { useParams, useNavigate } from 'react-router-dom';


const EditProjectPage = () => {
    const { projectId } = useParams();
    const { authTokens } = useContext(AuthContext);
    const history = useNavigate();
  
    const [projectData, setProjectData] = useState({
      title: '',
      description: '',
      watchers: [],  
    });
  
    const [allUsers, setAllUsers] = useState([]);
  
    useEffect(() => {
      const fetchProjectData = async () => {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/projects/project/${projectId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + String(authTokens.access),
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            setProjectData({
              id: data.id,
              title: data.title,
              description: data.description,
              watchers: [data.watchers],  // Преобразование в массив id пользователей
            });
          } else {
            console.error('Failed to fetch project data');
          }
        } catch (error) {
          console.error('Error fetching project data:', error);
        }
      };
  
      const fetchAllUsers = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/users/all_users', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + String(authTokens.access),
            },
          });
  
          if (response.ok) {
            const users = await response.json();
            setAllUsers(users);
          } else {
            console.error('Failed to fetch users data');
          }
        } catch (error) {
          console.error('Error fetching users data:', error);
        }
      };
  
      fetchProjectData();
      fetchAllUsers();
    }, [projectId, authTokens.access]);
  
    const handleInputChange = (e) => {
      const { name, value } = e.target;
      setProjectData((prevData) => ({
        ...prevData,
        [name]: value,
      }));
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        console.log(allUsers.results);
         console.log(projectData.user);

        const response = await fetch(`http://127.0.0.1:8000/api/projects/project/${projectId}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access),
          },
          body: JSON.stringify(projectData),
        });
        console.log(projectData)
        if (response.ok) {
          console.log('Project data updated successfully');
          history(`/projects/${projectId}/boards`);
        } else {
          console.error('Failed to update project data');
        }
      } catch (error) {
        console.error('Error updating project data:', error);
      }
    };
  
    return (
      <div>
        <form onSubmit={handleSubmit} className='form'>
          <h2>Edit Project</h2>
          <label>Title:</label>
          <input className="form-control" type="text" name="title" value={projectData.title} onChange={handleInputChange} />
          <label>Description:</label>
          <textarea className="form-control" name="description" value={projectData.description} onChange={handleInputChange} />
  
          <label>Watchers:</label>
          <select 
            className="form-control select"
            name="watchers"
            value={projectData.watchers}
            onChange={handleInputChange}
            multiple 
          >
        {Array.isArray(allUsers?.results) && allUsers.results.map(user => (
    <option key={user.id} value={user.id}>
      {user.username}
    </option>
  ))}
          </select>
          <button type="submit" className="btn btn-primary">
            Save Changes
          </button>
          
        </form>
      </div>
    );
  };
  
  export default EditProjectPage;
  