export interface User {
    id: number;
    username: string;
    email: string;
    created_at?: string;
}

export interface AuthResponse {
    message: string;
    access_token: string;
    user: User;
}

export interface Course {
    id: number;
    title: string;
    description: string;
    difficulty: 'beginner' | 'intermediate' | 'advanced';
    duration_hours: number;
    created_at?: string;
    topics?: string[];
}

export interface Enrollment {
    enrollment_id: number;
    course_id: number;
    course_title: string;
    enrolled_at: string;
    completed_at: string | null;
    progress_percentage: number;
}

export interface LearningPathItem {
    order: number;
    course_id: number;
    course_title: string;
    difficulty?: string;
    duration_hours?: number;
}

export interface LearningPath {
    id: number;
    user_id: number;
    title: string;
    description: string;
    created_at: string;
    courses: LearningPathItem[];
}