import {
  BrowserRouter as Router,
  Route, 
  Routes
} from "react-router-dom";
import './App.css';
import Header from './components/Header'
import TaskListPage from './pages/TaskListPage'
import TaskPage from "./pages/TaskPage";


function App() {
  return (
    <Router>
        <div className="container">
          <div className="app">
          <Header />
          <Routes>
            <Route path="/" exact Component={TaskListPage} />
            <Route path="/tasks/:id" Component={TaskPage} />
          </Routes>
          </div>
        </div>
    </Router>
  );
}

export default App;