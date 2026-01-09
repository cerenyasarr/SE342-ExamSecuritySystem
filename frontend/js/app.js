// Mock Authentication & Navigation
const App = {
    login: (e) => {
        e.preventDefault();
        const role = document.getElementById('role').value;
        const user = document.getElementById('username').value;

        localStorage.setItem('user_role', role);
        localStorage.setItem('username', user);

        window.location.href = 'dashboard.html';
    },

    checkAuth: () => {
        const role = localStorage.getItem('user_role');
        if (!role) {
            window.location.href = 'login.html';
        }

        // Show/Hide elements based on role
        if (role === 'Proctor') {
            document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'none');
        } else if (role === 'Admin') {
            document.querySelectorAll('.proctor-only').forEach(el => el.style.display = 'none');
        }

        const usernameDisplay = document.getElementById('username-display');
        if (usernameDisplay) usernameDisplay.textContent = localStorage.getItem('username');
    },

    logout: () => {
        localStorage.clear();
        window.location.href = 'login.html';
    },

    // Mock ML Verification
    verifyIdentity: () => {
        const resultPanel = document.getElementById('ml-result');
        const status = document.getElementById('status-text');

        resultPanel.style.display = 'block';
        status.innerHTML = '<span class="loading">Analyzing...</span>';

        setTimeout(() => {
            const isMatch = Math.random() > 0.2; // 80% success
            if (isMatch) {
                status.innerHTML = '<span class="status-success">✓ Match Confirmed (98.5%)</span>';
            } else {
                status.innerHTML = '<span class="status-danger">⚠ Identity Mismatch (45.2%)</span>';
            }
        }, 1500);
    }
};
