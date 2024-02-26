import {
  BrowserRouter,
  Route, 
  Routes
} from "react-router-dom";
import './App.css';
import Header from './components/Header'
import Profile from './pages/Profile'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import PrivateRoute from './utils/PrivateRoute'
import {AuthProvider} from './context/AuthContext'
import RegisterPage from "./pages/RegisterPage";
import PersonalTaskPage from "./pages/PersonalTaskPage";
import TaskPage from "./pages/TaskPage";
import EditBoardPage from "./pages/EditBoardPage";
import AddTaskPage from "./pages/AddTask";
import AddBoardPage from "./pages/AddBoard";
import EditTaskPage from "./pages/EditTaskPage";
import ProjectsPage from "./pages/ProjectsPage";
import ProjectBoardPage from "./pages/ProjectPage";
import AddProjectPage from "./pages/AddProject";
import EditProjectPage from "./pages/EditProjectPage";
import ProjectOneBoardPage from "./pages/ProjectOneBoardPage";
import ProjectTask from "./pages/ProjectTask";

function App() {
  return (         
  <div className="app">
        <BrowserRouter>
          <AuthProvider>
              <Header />
              <Routes>
                <Route path="/boards" element={<PrivateRoute> <HomePage /> </PrivateRoute>}/>        
                <Route path="/login" Component={LoginPage}/>
                <Route path="/register" Component={RegisterPage}/>
                <Route path="/profile" element={<PrivateRoute> <Profile /> </PrivateRoute>}/>
                <Route path="/boards/:boardId/tasks" element={<PrivateRoute> <PersonalTaskPage /> </PrivateRoute>} />
                <Route path="/boards/:boardId/tasks/:taskId" element={<PrivateRoute> <TaskPage /> </PrivateRoute>} />
                <Route path="/boards/:boardId/tasks/:taskId/upd" element={<PrivateRoute> <EditTaskPage /> </PrivateRoute>} />
                <Route path="/boards/:boardId/change" element={<PrivateRoute> <EditBoardPage /> </PrivateRoute>} />
                <Route path="/boards/:boardId/tasks/add" element={<PrivateRoute> <AddTaskPage /> </PrivateRoute>} />
                <Route path="/boards/add" element={<PrivateRoute> <AddBoardPage /> </PrivateRoute>} />
                <Route path="/projects" element={<PrivateRoute> <ProjectsPage /> </PrivateRoute>} />
                <Route path="/projects/add" element={<PrivateRoute> <AddProjectPage /> </PrivateRoute>} />
                <Route path="/projects/:projectId/boards" element={<PrivateRoute> <ProjectBoardPage /> </PrivateRoute>} />
                <Route path="/projects/:projectId/change" element={<PrivateRoute> <EditProjectPage /> </PrivateRoute>} />
                <Route path="/projects/:projectId/boards/:boardId" element={<PrivateRoute> <ProjectOneBoardPage /> </PrivateRoute>} />
                <Route path="/projects/:projectId/boards/:boardId/tasks/:teamtaskId" element={<PrivateRoute> <ProjectTask /> </PrivateRoute>} />
              </Routes>
          </AuthProvider>
        </BrowserRouter> 
  </div>
  );
        {/* <Route path="api/task" exact Component={TaskListPage} />
        <Route path="api/task/:id" Component={TaskPage} /> */}
        
}

export default App;