import React, {useState, useEffect} from 'react';
import ListItem from '../components/ListItem';

const TaskListPage = () => {

    let [tasks, setTasks] = useState([])
    useEffect(() => {
        getTasks()
    }, [])  

    let getTasks = async () => {
        let response = await fetch('api/task/')
        let data = await response.json()
        console.log(data)
        setTasks(data)
    }

  return (

    <div>
        <div>
            {tasks.map((task, index) => (
            <ListItem key={index} task={task} />
            ))}
        </div>
    </div>
  )
}

export default TaskListPage