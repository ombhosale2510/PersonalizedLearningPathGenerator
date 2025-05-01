import React, { useEffect, useState } from 'react';
import { learningPathService } from '../services/api';
import { LearningPath } from '../services/types';
import { Link } from 'react-router-dom';

const LearningPathsPage: React.FC = () => {
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [interests, setInterests] = useState('');
  const [difficulty, setDifficulty] = useState('beginner');

  useEffect(() => {
    fetchLearningPaths();
  }, []);

  const fetchLearningPaths = async () => {
    try {
      setLoading(true);
      const data = await learningPathService.getAllLearningPaths();
      setLearningPaths(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching learning paths:', err);
      setError('Failed to load learning paths. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePath = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      const interestArray = interests.split(',').map(item => item.trim());
      
      await learningPathService.generateLearningPath({
        title,
        description,
        interests: interestArray,
        difficulty_level: difficulty,
        max_courses: 5
      });
      
      // Reset form
      setTitle('');
      setDescription('');
      setInterests('');
      setDifficulty('beginner');
      setShowCreateForm(false);
      
      // Refresh the list
      fetchLearningPaths();
    } catch (err) {
      console.error('Error generating learning path:', err);
      setError('Failed to generate learning path. Please try again.');
      setLoading(false);
    }
  };

  if (loading && learningPaths.length === 0) {
    return <div className="text-center py-10">Loading learning paths...</div>;
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">My Learning Paths</h1>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          {showCreateForm ? 'Cancel' : 'Generate New Path'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {showCreateForm && (
        <div className="bg-gray-100 p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4">Generate New Learning Path</h2>
          <form onSubmit={handleGeneratePath}>
            <div className="mb-4">
              <label htmlFor="title" className="block text-gray-700 font-medium mb-2">Title</label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="description" className="block text-gray-700 font-medium mb-2">Description</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                rows={3}
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="interests" className="block text-gray-700 font-medium mb-2">Interests (comma-separated)</label>
              <input
                type="text"
                id="interests"
                value={interests}
                onChange={(e) => setInterests(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g. Python, Web Development, Data Science"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="difficulty" className="block text-gray-700 font-medium mb-2">Difficulty Level</label>
              <select
                id="difficulty"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <button
              type="submit"
              className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate Learning Path'}
            </button>
          </form>
        </div>
      )}

      {learningPaths.length === 0 ? (
        <p className="text-gray-600">You don't have any learning paths yet. Generate one to get started!</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {learningPaths.map((path) => (
            <div key={path.id} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
              <div className="p-6">
                <h2 className="text-xl font-semibold mb-2">{path.title}</h2>
                <p className="text-gray-700 mb-4">{path.description}</p>
                <p className="text-sm text-gray-600 mb-4">Created: {new Date(path.created_at).toLocaleDateString()}</p>
                
                <Link 
                  to={`/learning-paths/${path.id}`} 
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 inline-block"
                >
                  View Path
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LearningPathsPage;