// ============================================
// EXAM SECURITY SYSTEM - Main Application
// Compatible with new schema (schema.sql)
// ============================================

const App = {
    login: async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const submitBtn = e.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Giriş yapılıyor...';
        submitBtn.disabled = true;

        try {
            const response = await API.post(API_CONFIG.ENDPOINTS.AUTH.LOGIN, {
                username: username,
                password: password
            });

            const data = await response.json();

            if (response.ok) {
                // Store token and user info
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user', JSON.stringify(data.user));

                // Get role from response (role_name or role_id)
                const userRole = data.user.role_name || data.user.role_id || 'proctor';
                localStorage.setItem('user_role', userRole);
                localStorage.setItem('username', data.user.full_name || data.user.username);

                console.log('[AUTH] Login successful, role:', userRole);
                console.log('[AUTH] Token stored:', data.access_token ? 'Yes' : 'No');

                App.showSuccess('Giriş başarılı!');
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 500);
            } else {
                App.showError(data.error || 'Giriş başarısız. Lütfen tekrar deneyin.');
            }
        } catch (error) {
            console.error('Login error:', error);
            App.showError('Sunucu bağlantı hatası. Backend çalışıyor mu?');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    },

    checkAuth: () => {
        const token = localStorage.getItem('token');
        const role = localStorage.getItem('user_role');

        console.log('[AUTH] Checking auth - Token:', token ? 'exists' : 'missing', ', Role:', role);

        // Check if on login page
        const isLoginPage = window.location.pathname.includes('login.html');

        if (!token || !role) {
            if (!isLoginPage) {
                console.log('[AUTH] No token/role, redirecting to login');
                window.location.href = 'login.html';
            }
            return false;
        }

        // Role-based UI visibility
        const roleLower = role.toLowerCase();
        console.log('[AUTH] User role:', roleLower);

        if (roleLower === 'proctor') {
            // Proctor can't see admin-only elements
            document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'none');
        } else if (roleLower === 'admin') {
            // Admin can see everything, optionally hide proctor-only
            document.querySelectorAll('.proctor-only').forEach(el => el.style.display = 'none');
        }
        // If neither, show everything (for compatibility)

        // Display username
        const usernameDisplay = document.getElementById('username-display');
        if (usernameDisplay) {
            usernameDisplay.textContent = localStorage.getItem('username') || 'User';
        }

        // Display role badge if element exists
        const roleDisplay = document.getElementById('role-display');
        if (roleDisplay) {
            roleDisplay.textContent = role.toUpperCase();
        }

        return true;
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('user_role');
        localStorage.removeItem('username');
        window.location.href = 'login.html';
    },

    // ============ UTILITY FUNCTIONS ============

    showError: (message) => {
        App.showToast(message, 'error');
    },

    showSuccess: (message) => {
        App.showToast(message, 'success');
    },

    showToast: (message, type = 'success') => {
        // Remove existing toasts
        const existingToast = document.querySelector('.toast');
        if (existingToast) existingToast.remove();

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span style="margin-right: 0.5rem;">${type === 'success' ? '✓' : '⚠'}</span>
            ${message}
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    // ============ DATA LOADING ============

    loadRooms: async (selectId) => {
        try {
            const response = await API.get(API_CONFIG.ENDPOINTS.ROOMS.BASE);
            const rooms = await response.json();

            const select = document.getElementById(selectId);
            if (select) {
                select.innerHTML = '<option value="">Select Room...</option>';
                rooms.forEach(room => {
                    select.innerHTML += `<option value="${room.room_id}">${room.room_name} (Cap: ${room.capacity})</option>`;
                });
            }
            return rooms;
        } catch (error) {
            console.error('Error loading rooms:', error);
            return [];
        }
    },

    loadExams: async (selectId, status = null) => {
        try {
            let url = API_CONFIG.ENDPOINTS.EXAMS.BASE;
            if (status) url += `?status=${status}`;

            const response = await API.get(url);
            const exams = await response.json();

            const select = document.getElementById(selectId);
            if (select) {
                select.innerHTML = '<option value="">Select Exam...</option>';
                exams.forEach(exam => {
                    select.innerHTML += `<option value="${exam.exam_id}">${exam.exam_title} - ${exam.course_code}</option>`;
                });
            }
            return exams;
        } catch (error) {
            console.error('Error loading exams:', error);
            return [];
        }
    },

    loadStudents: async (containerId = null) => {
        try {
            const response = await API.get(API_CONFIG.ENDPOINTS.USERS.STUDENTS);
            const students = await response.json();

            if (containerId) {
                const container = document.getElementById(containerId);
                if (container) {
                    container.innerHTML = students.map(s => `
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <td style="padding: 1rem;">${s.student_number}</td>
                            <td style="padding: 1rem;">${s.full_name}</td>
                            <td style="padding: 1rem;">
                                <span class="status-badge status-success">Registered</span>
                            </td>
                            <td style="padding: 1rem;">
                                <button class="btn btn-danger" onclick="App.deleteStudent('${s.student_id}')"
                                    style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Remove</button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
            return students;
        } catch (error) {
            console.error('Error loading students:', error);
            return [];
        }
    },

    loadViolationTypes: async (selectId) => {
        try {
            const response = await API.get(API_CONFIG.ENDPOINTS.VIOLATIONS.TYPES);
            const types = await response.json();

            const select = document.getElementById(selectId);
            if (select) {
                select.innerHTML = '';
                types.forEach(type => {
                    select.innerHTML += `<option value="${type.code}">${type.name}</option>`;
                });
            }
            return types;
        } catch (error) {
            console.error('Error loading violation types:', error);
            return [];
        }
    },

    // ============ EXAM MANAGEMENT ============

    createExam: async (e) => {
        e.preventDefault();

        const form = e.target;
        const courseCode = form.querySelector('[name="course_code"]').value;
        const examTitle = form.querySelector('[name="exam_title"]').value;
        const roomId = form.querySelector('[name="room_id"]').value;
        const date = form.querySelector('[name="exam_date"]').value;
        const startTime = form.querySelector('[name="start_time"]').value;
        const duration = parseInt(form.querySelector('[name="duration"]').value);

        const startDateTime = new Date(`${date}T${startTime}`);
        const endDateTime = new Date(startDateTime.getTime() + duration * 60000);

        try {
            const response = await API.post(API_CONFIG.ENDPOINTS.EXAMS.BASE, {
                course_code: courseCode,
                exam_title: examTitle,
                room_id: roomId || null,
                start_time: startDateTime.toISOString(),
                end_time: endDateTime.toISOString()
            });

            if (response.ok) {
                App.showSuccess('Exam created successfully!');
                form.reset();
            } else {
                const data = await response.json();
                App.showError(data.error || 'Failed to create exam');
            }
        } catch (error) {
            console.error('Error creating exam:', error);
            App.showError('Connection error');
        }
    },

    // ============ STUDENT MANAGEMENT ============

    deleteStudent: async (studentId) => {
        if (!confirm('Are you sure you want to remove this student?')) return;

        try {
            const response = await API.delete(API_CONFIG.ENDPOINTS.USERS.STUDENT_BY_ID(studentId));

            if (response.ok) {
                App.showSuccess('Student removed successfully');
                App.loadStudents('students-tbody');
            } else {
                const data = await response.json();
                App.showError(data.error || 'Failed to remove student');
            }
        } catch (error) {
            console.error('Error deleting student:', error);
            App.showError('Connection error');
        }
    },

    // ============ VIOLATIONS ============

    loadViolations: async (containerId, examId = null) => {
        try {
            let url = API_CONFIG.ENDPOINTS.VIOLATIONS.BASE;
            if (examId) url = API_CONFIG.ENDPOINTS.VIOLATIONS.BY_EXAM(examId);

            const response = await API.get(url);
            const data = await response.json();
            const violations = examId ? data.violations : data;

            const container = document.getElementById(containerId);
            if (container && violations) {
                if (violations.length === 0) {
                    container.innerHTML = '<p style="text-align: center; color: var(--text-dim);">No violations found.</p>';
                    return;
                }

                container.innerHTML = violations.map(v => `
                    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid var(--danger); border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between;">
                            <h3 style="color: var(--danger);">${v.violation_type}</h3>
                            <span>${v.reported_at ? new Date(v.reported_at).toLocaleTimeString() : '-'}</span>
                        </div>
                        <p style="margin: 0.5rem 0;"><strong>Student:</strong> ${v.student_name || 'Unknown'}</p>
                        <p>${v.description || 'No description'}</p>
                    </div>
                `).join('');
            }
            return violations;
        } catch (error) {
            console.error('Error loading violations:', error);
            return [];
        }
    },

    // ============ EXAM STATUS ============

    loadExamStatus: async (examId, containerId) => {
        try {
            const response = await API.get(API_CONFIG.ENDPOINTS.STUDENT_EXAMS.EXAM_STATUS(examId));
            const data = await response.json();

            const totalEl = document.getElementById('stat-total');
            const pendingEl = document.getElementById('stat-pending');
            const rateEl = document.getElementById('stat-rate');

            if (totalEl) totalEl.textContent = data.attended || 0;
            if (pendingEl) pendingEl.textContent = data.pending || 0;
            if (rateEl) rateEl.textContent = `${data.attendance_rate || 0}%`;

            const container = document.getElementById(containerId);
            if (container && data.students) {
                container.innerHTML = data.students.map(s => `
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 1rem;">-</td>
                        <td style="padding: 1rem;">${s.student_name}</td>
                        <td style="padding: 1rem;">${s.seat_label || '-'}</td>
                        <td style="padding: 1rem;">
                            <span style="color: ${s.status === 'attended' ? 'var(--success)' : 'var(--text-dim)'};">
                                ${s.status}
                            </span>
                        </td>
                    </tr>
                `).join('');
            }

            return data;
        } catch (error) {
            console.error('Error loading exam status:', error);
            return null;
        }
    },

    processCheckin: async (studentId, examId) => {
        try {
            const response = await API.post(API_CONFIG.ENDPOINTS.STUDENT_EXAMS.CHECKIN, {
                student_id: studentId,
                exam_id: examId
            });

            const data = await response.json();

            if (response.ok && data.success) {
                App.showSuccess('Check-in successful!');
                return data;
            } else {
                App.showError(data.error || 'Check-in failed');
                return null;
            }
        } catch (error) {
            console.error('Error processing checkin:', error);
            App.showError('Connection error');
            return null;
        }
    },

    // ============ SEATING ============

    autoAssignSeats: async (examId) => {
        try {
            const response = await API.post(API_CONFIG.ENDPOINTS.STUDENT_EXAMS.ASSIGN_SEATS(examId), {});

            if (response.ok) {
                const data = await response.json();
                App.showSuccess(data.message || 'Seats assigned successfully');
                return data.students;
            } else {
                const data = await response.json();
                App.showError(data.error || 'Failed to assign seats');
                return null;
            }
        } catch (error) {
            console.error('Error auto-assigning seats:', error);
            App.showError('Connection error');
            return null;
        }
    },

    loadSeatingGrid: async (examId, containerId) => {
        try {
            const response = await API.get(API_CONFIG.ENDPOINTS.EXAMS.ENROLLMENTS(examId));
            const enrollments = await response.json();

            const container = document.getElementById(containerId);
            if (container) {
                const seats = {};
                enrollments.forEach(e => {
                    if (e.assigned_row && e.assigned_col) {
                        const key = `R${e.assigned_row}C${e.assigned_col}`;
                        seats[key] = e;
                    }
                });

                const rows = 5;
                const cols = 6;
                let html = '';

                for (let r = 1; r <= rows; r++) {
                    for (let c = 1; c <= cols; c++) {
                        const seatId = `R${r}C${c}`;
                        const enrollment = seats[seatId];
                        const cssClass = enrollment ? 'seat selected' : 'seat';
                        const label = enrollment ? `<small style="color: var(--success)">${enrollment.student_name?.split(' ')[0] || 'Assigned'}</small>` : '<small>Empty</small>';

                        html += `<div class="${cssClass}">${seatId}<br>${label}</div>`;
                    }
                }

                container.innerHTML = html;
            }

            return enrollments;
        } catch (error) {
            console.error('Error loading seating grid:', error);
            return [];
        }
    },

    // ============ MOCK ML VERIFICATION ============

    verifyIdentity: () => {
        const resultPanel = document.getElementById('ml-result');
        const status = document.getElementById('status-text');

        if (resultPanel) resultPanel.style.display = 'block';
        if (status) status.innerHTML = '<span class="loading">Analyzing...</span>';

        setTimeout(() => {
            const isMatch = Math.random() > 0.2;
            if (status) {
                if (isMatch) {
                    status.innerHTML = '<span class="status-success">✓ Match Confirmed (98.5%)</span>';
                } else {
                    status.innerHTML = '<span class="status-danger">⚠ Identity Mismatch (45.2%)</span>';
                }
            }
        }, 1500);
    }
};
