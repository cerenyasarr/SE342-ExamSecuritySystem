/**
 * API Configuration for Exam Security System
 * Compatible with new schema (schema.sql)
 */

const API_CONFIG = {
    BASE_URL: 'https://se342-examsecuritysystem-3.onrender.com',

    ENDPOINTS: {
        // Auth endpoints
        AUTH: {
            LOGIN: '/api/auth/login',
            REGISTER: '/api/auth/register',
            ME: '/api/auth/me'
        },

        // Users endpoints (students + system users)
        USERS: {
            BASE: '/api/users',
            STUDENTS: '/api/users/students',
            STUDENT_BY_ID: (id) => `/api/users/students/${id}`,
            BY_ID: (id) => `/api/users/${id}`
        },

        // Students endpoints
        STUDENTS: {
            BASE: '/api/students',
            BY_ID: (id) => `/api/students/${id}`
        },

        // Courses endpoints
        COURSES: {
            BASE: '/api/courses',
            BY_ID: (id) => `/api/courses/${id}`
        },

        // Rooms endpoints
        ROOMS: {
            BASE: '/api/rooms',
            BY_ID: (id) => `/api/rooms/${id}`
        },

        // Exams endpoints
        EXAMS: {
            BASE: '/api/exams',
            BY_ID: (id) => `/api/exams/${id}`,
            STATUS: (id) => `/api/exams/${id}/status`,
            ENROLLMENTS: (id) => `/api/exams/${id}/enrollments`,
            SEATS: (id) => `/api/exams/${id}/seats`
        },

        // Student-Exam (Enrollment) endpoints
        STUDENT_EXAMS: {
            BASE: '/api/student-exams',
            BY_ID: (id) => `/api/student-exams/${id}`,
            CHECKIN: '/api/student-exams/checkin',
            VERIFY_FACE: '/api/student-exams/verify-face',
            EXAM_STATUS: (examId) => `/api/student-exams/exam/${examId}/status`,
            ASSIGN_SEATS: (examId) => `/api/student-exams/exam/${examId}/assign-seats`
        },

        // Violations endpoints
        VIOLATIONS: {
            BASE: '/api/violations',
            BY_ID: (id) => `/api/violations/${id}`,
            BY_EXAM: (examId) => `/api/violations/exam/${examId}`,
            TYPES: '/api/violations/types'
        }
    }
};

/**
 * API Request Helper
 * Automatically includes JWT token if available
 */
async function apiRequest(endpoint, options = {}) {
    const url = API_CONFIG.BASE_URL + endpoint;

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Add JWT token if available
    const token = localStorage.getItem('token');
    if (token) {
        defaultOptions.headers['Authorization'] = `Bearer ${token}`;
    }

    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    try {
        const response = await fetch(url, finalOptions);
        return response;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

/**
 * API Helper Methods
 */
const API = {
    get: (endpoint) => apiRequest(endpoint, { method: 'GET' }),
    post: (endpoint, data) => apiRequest(endpoint, { method: 'POST', body: JSON.stringify(data) }),
    put: (endpoint, data) => apiRequest(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (endpoint) => apiRequest(endpoint, { method: 'DELETE' })
};
