import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/pages/Login"; // Import the Login component
import Register from "./components/pages/Register"; // Import the Register component
import Dashboard from "./components/pages/Dashboard"; // Import the Dashboard component

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<Login />} /> {/* Default route */}
      </Routes>
    </Router>
  );
};

export default App;
