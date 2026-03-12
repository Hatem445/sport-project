// ========================================
// FitLife AI - Main JavaScript
// ========================================

// Utility Functions
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = 'toast show ' + type;
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

function getFormData(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    return Object.fromEntries(formData);
}

// Navigation Setup
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    updateDate();
    setInterval(updateDate, 1000);
});

function setupNavigation() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/logout');
                if (response.ok) {
                    window.location.href = '/';
                }
            } catch (error) {
                showToast('خطأ في تسجيل الخروج', 'error');
            }
        });
    }
}

function updateDate() {
    const dateElement = document.getElementById('current-date');
    if (!dateElement) return;
    
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    const now = new Date();
    dateElement.textContent = now.toLocaleDateString('ar-SA', options);
}

// API Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        
        if (response.status === 401) {
            window.location.href = '/login';
            return null;
        }
        
        const responseData = await response.json();
        
        if (!response.ok) {
            throw new Error(responseData.error || 'حدث خطأ');
        }
        
        return responseData;
    } catch (error) {
        showToast('❌ ' + error.message, 'error');
        return null;
    }
}

// Format Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('ar-SA', options);
}

function formatDuration(minutes) {
    if (!minutes) return '';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours > 0) {
        return `${hours} ساعة و ${mins} دقيقة`;
    }
    return `${mins} دقيقة`;
}

// Chart Setup Function
function createHealthChart(containerId, data) {
    const ctx = document.getElementById(containerId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [
                {
                    label: 'معدل النبض',
                    data: data.heartRate || [],
                    borderColor: '#f093fb',
                    backgroundColor: 'rgba(240, 147, 251, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'الوزن (كغ)',
                    data: data.weight || [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#a0a0b0',
                        font: { size: 12 }
                    }
                }
            },
            scales: {
                y: {
                    grid: { color: '#2a2a3e' },
                    ticks: { color: '#a0a0b0' }
                },
                x: {
                    grid: { color: '#2a2a3e' },
                    ticks: { color: '#a0a0b0' }
                }
            }
        }
    });
}

// Modal Functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

// Close modal on outside click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('show');
    }
    
    if (e.target.classList.contains('close-btn')) {
        const modal = e.target.closest('.modal');
        if (modal) {
            modal.classList.remove('show');
        }
    }
});

// Notification System
class NotificationManager {
    constructor() {
        this.notifications = [];
        this.unreadCount = 0;
    }
    
    async loadNotifications() {
        // في الإنتاج، اجلب الإشعارات من الخادم
        this.updateBadge();
    }
    
    addNotification(notification) {
        this.notifications.push(notification);
        this.unreadCount++;
        this.updateBadge();
        this.showNotification(notification);
    }
    
    updateBadge() {
        const badge = document.querySelector('.notif-badge');
        if (badge) {
            badge.textContent = this.unreadCount;
            badge.style.display = this.unreadCount > 0 ? 'flex' : 'none';
        }
    }
    
    showNotification(notification) {
        showToast(notification.message || notification.title, notification.type || 'info');
    }
}

const notificationManager = new NotificationManager();

// Export for use in other files
window.FitLifeAPI = {
    apiCall,
    showToast,
    formatDate,
    formatDuration,
    createHealthChart,
    openModal,
    closeModal,
    notificationManager
};
