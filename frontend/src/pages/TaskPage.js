import React, { useState, useEffect }  from 'react'
import { useParams } from 'react-router-dom'

const TaskPage = () => {
  const {id} = useParams()
  let [task, setTask] = useState(null)

  useEffect(() => {
      getTask()
  }, [{id}])

  let getTask = async () => {
    if ({id} === 'new') return

    let response = await fetch(`api/task/${id}/`)
    let data = await response.json()
    setTask(data)
}

    let updateTask = async () => {
        fetch(`api/task/${id}/`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(task)
        })
    }


    let handleChange = (value) => {
      setTask(task => ({ ...task, 'title': value }))
      console.log('Handle Change:', task)
  }
    
  return (
    <div>
        <h2>{task?.title}</h2>
        <h2>{task?.description}</h2>
        <h2>{task?.start_date}</h2>
        <h2>{task?.end_date}</h2>
        {/* <textarea onChange={(e) => { handleChange(e.target.value) }} value={task?.description}></textarea> */}
    </div>
  )
}

export default TaskPage