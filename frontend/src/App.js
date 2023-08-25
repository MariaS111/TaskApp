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


function App() {
  return (         
  <div className="app">
        <BrowserRouter>
          <AuthProvider>
              <Header />
              <Routes>
                <Route path="/" element={<PrivateRoute> <HomePage /> </PrivateRoute>}/>        
                <Route path="/login" Component={LoginPage}/>
                <Route path="/register" Component={RegisterPage}/>
                <Route path="/profile" element={<PrivateRoute> <Profile /> </PrivateRoute>}/>
              </Routes>
          </AuthProvider>
        </BrowserRouter> 
  </div>
  );
        {/* <Route path="api/task" exact Component={TaskListPage} />
        <Route path="api/task/:id" Component={TaskPage} /> */}
        
}

export default App;