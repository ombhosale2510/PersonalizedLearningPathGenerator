import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Personalized Learning Path Generator</h1>
        <p className="text-xl text-gray-600">Discover your optimal learning journey tailored to your interests and goals</p>
      </div>

      <div className="bg-gray-100 p-8 rounded-lg shadow-md max-w-3xl mx-auto">
        {isAuthenticated ? (
          <div>
            <h2 className="text-2xl font-semibold mb-4">Welcome back, {user?.username}!</h2>
            <p className="mb-6">Continue your learning journey or discover new paths.</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link to="/learning-paths" className="bg-blue-600 text-white py-3 px-6 rounded-lg text-center hover:bg-blue-700 transition">
                My Learning Paths
              </Link>
              <Link to="/courses" className="bg-green-600 text-white py-3 px-6 rounded-lg text-center hover:bg-green-700 transition">
                Browse Courses
              </Link>
            </div>
          </div>
        ) : (
          <div>
            <h2 className="text-2xl font-semibold mb-4">Start Your Learning Journey Today</h2>
            <p className="mb-6">Create a personalized learning path based on your interests and goals.</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link to="/register" className="bg-blue-600 text-white py-3 px-6 rounded-lg text-center hover:bg-blue-700 transition">
                Sign Up
              </Link>
              <Link to="/login" className="border border-blue-600 text-blue-600 py-3 px-6 rounded-lg text-center hover:bg-blue-50 transition">
                Login
              </Link>
            </div>
          </div>
        )}
      </div>

      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-3">Personalized Paths</h3>
          <p>Get course recommendations tailored to your interests and skill level.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-3">Track Progress</h3>
          <p>Monitor your learning journey and stay motivated with progress tracking.</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-3">Diverse Courses</h3>
          <p>Access a wide range of courses across different subjects and difficulty levels.</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;