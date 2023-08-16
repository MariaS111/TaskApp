import {
  BrowserRouter,
  Route, 
  Routes
} from "react-router-dom";
import './App.css';
import Header from './components/Header'
import TaskListPage from './pages/TaskListPage'
import TaskPage from "./pages/TaskPage";
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import PrivateRoute from './utils/PrivateRoute'
import {AuthProvider} from './context/AuthContext'
// "scripts": {
//   "start": "react-scripts start",
//   "build": "react-scripts build",
//   "test": "react-scripts test",
//   "eject": "react-scripts eject"
// },


function App() {
  return (         
  <div className="app">
        <BrowserRouter>
          <AuthProvider>
              <Header />
              <Routes>
                <Route path="/" element={<PrivateRoute> <HomePage /> </PrivateRoute>}/>        
                <Route path="/login" Component={LoginPage}/>
              </Routes>
          </AuthProvider>
        </BrowserRouter> 
  </div>
  );
        {/* <Route path="api/task" exact Component={TaskListPage} />
        <Route path="api/task/:id" Component={TaskPage} /> */}
        
}

export default App;