import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">Learning Path Generator</Link>
        
        <div className="flex space-x-4">
          <Link to="/courses" className="hover:text-gray-300">Courses</Link>
          
          {isAuthenticated ? (
            <>
              <Link to="/learning-paths" className="hover:text-gray-300">My Learning Paths</Link>
              <Link to="/enrollments" className="hover:text-gray-300">My Enrollments</Link>
              <div className="flex items-center">
                <span className="mr-2">Hi, {user?.username}</span>
                <button 
                  onClick={logout} 
                  className="bg-red-600 px-3 py-1 rounded hover:bg-red-700"
                >
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-gray-300">Login</Link>
              <Link to="/register" className="hover:text-gray-300">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;