import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the JWT token exists in localStorage
    const token = localStorage.getItem("access_token");

    if (token) {
      // If token exists, user is authenticated
      setIsAuthenticated(true);
    } else {
      // If token doesn't exist, redirect to login page
      navigate("/login");
    }
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 p-4">
      <div className="bg-white p-8 rounded-xl shadow-lg max-w-md w-full text-center">
        {isAuthenticated ? (
          <h1 className="text-3xl font-bold text-green-600">Login Successful!</h1>
        ) : (
          <h1 className="text-xl font-semibold text-red-600">You are not authenticated</h1>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
