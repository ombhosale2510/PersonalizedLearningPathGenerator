import axios from 'axios';
import { 
    AuthResponse, 
    Course, 
    Enrollment, 
    LearningPath, 
    User 
} from './types';

// Base API URL - adjust this based on where your Flask API is running
const API_URL = 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add interceptor to include the auth token in requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token && config.headers) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Auth Services
export const authService = {
    register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
        const response = await api.post<AuthResponse>('/api/auth/register', {
            username,
            email,
            password
        });
        return response.data;
    },

    login: async (username: string, password: string): Promise<AuthResponse> => {
        const response = await api.post<AuthResponse>('/api/auth/login', {
            username,
            password
        });
        return response.data;
    },

    getProfile: async (): Promise<User> => {
        const response = await api.get<User>('/api/auth/profile');
        return response.data;
    }
};

// Course Services
export const courseService = {
    getAllCourses: async (): Promise<Course[]> => {
        const response = await api.get<Course[]>('/api/courses');
        return response.data;
    },

    getCourseById: async (id: number): Promise<Course> => {
        const response = await api.get<Course>(`/api/courses/${id}`);
        return response.data;
    },

    createCourse: async (course: Partial<Course>): Promise<Course> => {
        const response = await api.post<Course>('/api/courses', course);
        return response.data;
    },

    updateCourse: async (id: number, course: Partial<Course>): Promise<{ message: string }> => {
        const response = await api.put<{ message: string }>(`/api/courses/${id}`, course);
        return response.data;
    },

    deleteCourse: async (id: number): Promise<{ message: string }> => {
        const response = await api.delete<{ message: string }>(`/api/courses/${id}`);
        return response.data;
    },

    enrollInCourse: async (courseId: number): Promise<any> => {
        const response = await api.post<any>(`/api/courses/${courseId}/enroll`);
        return response.data;
    },

    getEnrollments: async (): Promise<Enrollment[]> => {
        const response = await api.get<Enrollment[]>('/api/enrollments');
        return response.data;
    }
};

// Learning Path Services
export const learningPathService = {
    getAllLearningPaths: async (): Promise<LearningPath[]> => {
        const response = await api.get<LearningPath[]>('/api/learning-paths');
        return response.data;
    },

    getLearningPathById: async (id: number): Promise<LearningPath> => {
        const response = await api.get<LearningPath>(`/api/learning-paths/${id}`);
        return response.data;
    },

    createLearningPath: async (path: { 
        title: string, 
        description: string, 
        course_ids?: number[] 
    }): Promise<LearningPath> => {
        const response = await api.post<LearningPath>('/api/learning-paths', path);
        return response.data;
    },

    updateLearningPath: async (
        id: number, 
        path: { 
            title?: string, 
            description?: string, 
            course_ids?: number[] 
        }
    ): Promise<{ message: string }> => {
        const response = await api.put<{ message: string }>(`/api/learning-paths/${id}`, path);
        return response.data;
    },

    deleteLearningPath: async (id: number): Promise<{ message: string }> => {
        const response = await api.delete<{ message: string }>(`/api/learning-paths/${id}`);
        return response.data;
    },

    generateLearningPath: async (options: {
        title: string,
        description: string,
        interests: string[],
        difficulty_level?: string,
        max_courses?: number
    }): Promise<LearningPath> => {
        const response = await api.post<LearningPath>('/api/learning-paths/generate', options);
        return response.data;
    }
};