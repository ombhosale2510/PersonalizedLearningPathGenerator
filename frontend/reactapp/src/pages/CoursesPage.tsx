import React, { useEffect, useState } from 'react';
import { courseService } from '../services/api';
import { Course } from '../services/types';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const CoursesPage: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const data = await courseService.getAllCourses();
        setCourses(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching courses:', err);
        setError('Failed to load courses. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const handleEnroll = async (courseId: number) => {
    try {
      await courseService.enrollInCourse(courseId);
      alert('Successfully enrolled in the course!');
    } catch (err) {
      console.error('Error enrolling in course:', err);
      alert('Failed to enroll in the course. Please try again.');
    }
  };

  if (loading) return <div className="text-center py-10">Loading courses...</div>;
  
  if (error) return (
    <div className="text-center py-10">
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md mx-auto" role="alert">
        <span className="block sm:inline">{error}</span>
      </div>
    </div>
  );

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Available Courses</h1>
      
      {courses.length === 0 ? (
        <p className="text-gray-600">No courses available at the moment.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <div key={course.id} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
              <div className="p-6">
                <h2 className="text-xl font-semibold mb-2">{course.title}</h2>
                <div className="flex items-center text-sm text-gray-600 mb-2">
                  <span className="capitalize bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                    {course.difficulty}
                  </span>
                  <span className="ml-2">{course.duration_hours} hours</span>
                </div>
                <p className="text-gray-700 mb-4 line-clamp-3">{course.description}</p>
                
                <div className="mt-4 flex justify-between">
                  <Link 
                    to={`/courses/${course.id}`} 
                    className="text-blue-600 hover:text-blue-800"
                  >
                    View Details
                  </Link>
                  
                  {isAuthenticated && (
                    <button 
                      onClick={() => handleEnroll(course.id)} 
                      className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 text-sm"
                    >
                      Enroll Now
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CoursesPage;