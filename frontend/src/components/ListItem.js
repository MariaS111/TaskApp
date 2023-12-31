import React from 'react'
import { Link } from 'react-router-dom'

const ListItem = ({task}) => {
  return (
    <Link to={`api/task/${task.id}`}>
        <h3>{task.title}</h3>
    </Link>
  )
}

export default ListItem