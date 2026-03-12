// ========================================
// FitLife AI - Dashboard JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();
});

function initializeDashboard() {
    loadStats();
    loadExercises();
    loadHealthData();
    loadRecommendations();
    setupFormListeners();
}

// ==================== Forms ====================

function setupFormListeners() {
    // Exercise Form
    const exerciseForm = document.getElementById('exercise-form');
    if (exerciseForm) {
        exerciseForm.addEventListener('submit', handleAddExercise);
        
        // Update intensity display
        const intensityInput = document.getElementById('exercise-intensity');
        if (intensityInput) {
            intensityInput.addEventListener('input', (e) => {
                document.querySelector('.intensity-value').textContent = e.target.value;
            });
        }
    }
    
    // Health Form
    const healthForm = document.getElementById('health-form');
    if (healthForm) {
        healthForm.addEventListener('submit', handleAddHealthData);
        
        // Update stress display
        const stressInput = document.getElementById('health-stress');
        if (stressInput) {
            stressInput.addEventListener('input', (e) => {
                document.querySelector('.stress-value').textContent = e.target.value;
            });
        }
    }
    
    // Request Analysis Button
    const analysisBtn = document.getElementById('request-analysis');
    if (analysisBtn) {
        analysisBtn.addEventListener('click', handleAnalyzeWithAI);
    }
    
    // Schedule Exercise Modal
    const scheduleForm = document.getElementById('schedule-form');
    if (scheduleForm) {
        scheduleForm.addEventListener('submit', handleScheduleExercise);
    }
}

// ==================== Exercise Handlers ====================

async function handleAddExercise(e) {
    e.preventDefault();
    
    const exerciseData = {
        name: document.getElementById('exercise-name').value,
        exercise_type: document.getElementById('exercise-type').value,
        duration: parseInt(document.getElementById('exercise-duration').value),
        intensity: parseInt(document.getElementById('exercise-intensity').value),
        calories: parseInt(document.getElementById('exercise-calories').value) || 0,
        notes: document.getElementById('exercise-notes').value,
        muscle_groups: []
    };
    
    const response = await FitLifeAPI.apiCall('/api/exercises', 'POST', exerciseData);
    
    if (response) {
        FitLifeAPI.showToast('✅ تم إضافة التمرين بنجاح!', 'success');
        e.target.reset();
        loadExercises();
        loadStats();
    }
}

async function loadExercises() {
    const response = await FitLifeAPI.apiCall('/api/exercises');
    
    if (!response) return;
    
    const exercisesList = document.getElementById('recent-exercises');
    if (!exercisesList) return;
    
    if (response.exercises.length === 0) {
        exercisesList.innerHTML = '<p class="empty-message">لا توجد تمارين مسجلة بعد</p>';
        return;
    }
    
    exercisesList.innerHTML = response.exercises.map(exercise => `
        <div class="exercise-item">
            <h4><i class="fas fa-dumbbell"></i> ${exercise.name}</h4>
            <p>
                <strong>النوع:</strong> ${exercise.type} | 
                <strong>المدة:</strong> ${exercise.duration} دقيقة | 
                <strong>الشدة:</strong> ${exercise.intensity}/10
            </p>
            <p><strong>السعرات:</strong> ${exercise.calories}</p>
            <small>${FitLifeAPI.formatDate(exercise.date)}</small>
            ${exercise.notes ? `<p><em>${exercise.notes}</em></p>` : ''}
        </div>
    `).join('');
}

async function handleScheduleExercise(e) {
    e.preventDefault();
    
    const scheduleData = {
        exercise_name: document.getElementById('schedule-exercise').value,
        scheduled_date: document.getElementById('schedule-date').value
    };
    
    const response = await FitLifeAPI.apiCall('/api/schedule/exercise', 'POST', scheduleData);
    
    if (response) {
        FitLifeAPI.showToast('✅ تم جدولة التمرين بنجاح!', 'success');
        FitLifeAPI.closeModal('schedule-modal');
        e.target.reset();
    }
}

// ==================== Health Data Handlers ====================

async function handleAddHealthData(e) {
    e.preventDefault();
    
    const healthData = {
        weight: parseFloat(document.getElementById('health-weight').value) || null,
        heart_rate: parseInt(document.getElementById('health-heart-rate').value) || null,
        blood_pressure: document.getElementById('health-bp').value,
        body_fat: parseFloat(document.getElementById('health-body-fat').value) || null,
        sleep_hours: parseFloat(document.getElementById('health-sleep').value) || null,
        stress_level: parseInt(document.getElementById('health-stress').value) || null,
        energy_level: 5,
        injuries: null,
        pain_points: null,
        general_notes: ''
    };
    
    const response = await FitLifeAPI.apiCall('/api/health-data', 'POST', healthData);
    
    if (response) {
        FitLifeAPI.showToast('✅ تم حفظ البيانات الصحية بنجاح!', 'success');
        e.target.reset();
        loadStats();
    }
}

// ==================== AI Recommendations ====================

async function loadRecommendations() {
    const response = await FitLifeAPI.apiCall('/api/ai/recommendations');
    
    if (!response) return;
    
    const recommendationsList = document.getElementById('recommendations-list');
    if (!recommendationsList) return;
    
    if (response.recommendations.length === 0) {
        recommendationsList.innerHTML = '<p class="empty-message">لا توجد توصيات حتى الآن</p>';
        return;
    }
    
    recommendationsList.innerHTML = response.recommendations.slice(0, 3).map(rec => `
        <div class="recommendation-item">
            <h4>
                ${getCategoryIcon(rec.category)} ${rec.title}
            </h4>
            <p>${rec.description}</p>
            <div class="confidence-badge">ثقة: ${Math.round(rec.confidence * 100)}%</div>
            ${rec.requires_doctor ? '<p style="color: #f5576c;">⚠️ استشر طبيباً متخصصاً</p>' : ''}
            <small>${FitLifeAPI.formatDate(rec.date)}</small>
        </div>
    `).join('');
}

function getCategoryIcon(category) {
    const icons = {
        'muscle_development': '💪',
        'injury_diagnosis': '🏥',
        'health_tips': '💡',
        'general_advice': '📋',
        'ai_recommendation': '🤖'
    };
    return icons[category] || '💬';
}

async function handleAnalyzeWithAI() {
    const btn = document.getElementById('request-analysis');
    btn.disabled = true;
    btn.textContent = 'جاري التحليل...';
    
    const response = await FitLifeAPI.apiCall('/api/ai/analyze', 'POST', {});
    
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-brain"></i> طلب تحليل ذكي شامل';
    
    if (response) {
        FitLifeAPI.showToast('✅ تم إجراء التحليل الذكي بنجاح!', 'success');
        loadRecommendations();
        
        // عرض النتائج
        if (response.recommendations && response.recommendations.length > 0) {
            showAnalysisResults(response);
        }
    }
}

function showAnalysisResults(analysis) {
    let resultHTML = '<h3>نتائج التحليل الذكي</h3>';
    
    if (analysis.health_status) {
        resultHTML += `
            <div style="margin: 1rem 0; padding: 1rem; background: rgba(102,126,234,0.1); border-radius: 8px;">
                <h4>حالتك الصحية</h4>
                <p><strong>BMI:</strong> ${analysis.health_status.bmi?.toFixed(1) || 'غير متوفر'}</p>
                <p><strong>التصنيف:</strong> ${analysis.health_status.bmi_category}</p>
                <p><strong>تكرار التمارين:</strong> ${analysis.health_status.exercise_frequency} تمرين</p>
            </div>
        `;
    }
    
    if (analysis.recommendations && analysis.recommendations.length > 0) {
        resultHTML += '<h4>التوصيات</h4>';
        analysis.recommendations.forEach(rec => {
            resultHTML += `
                <div style="margin: 0.5rem 0; padding: 0.8rem; background: rgba(240,147,251,0.1); border-radius: 6px; border-right: 3px solid #f093fb;">
                    <strong>${rec.title}</strong><br>
                    <small>${rec.description}</small>
                </div>
            `;
        });
    }
    
    // عرض النتائج في modal أو تنبيه
    FitLifeAPI.showToast('تم جمع بيانات التحليل - راجع التوصيات أعلاه', 'success');
}

// ==================== Statistics ====================

async function loadStats() {
    const response = await FitLifeAPI.apiCall('/api/stats/summary');
    
    if (!response) return;
    
    // Update Stats Cards
    document.getElementById('weekly-exercises').textContent = response.total_exercises || 0;
    document.getElementById('total-calories').textContent = (response.total_calories || 0).toLocaleString('ar-SA');
    
    if (response.latest_health) {
        document.getElementById('heart-rate').textContent = response.latest_health.heart_rate || '--';
    }
    
    // Calculate health score (placeholder)
    const healthScore = calculateHealthScore(response);
    document.getElementById('health-score').textContent = healthScore;
}

function calculateHealthScore(stats) {
    // نموذج بسيط لحساب درجة الصحة
    let score = 70;
    
    if (stats.total_exercises > 3) score += 10;
    if (stats.total_exercises > 7) score += 10;
    if (stats.total_calories > 500) score += 5;
    
    return Math.min(100, score);
}

// ==================== Utilities ====================

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

// Real-time data updates
function startAutoRefresh() {
    setInterval(() => {
        loadStats();
    }, 30000); // كل 30 ثانية
}

// Start auto refresh when dashboard loads
if (document.body.contains(document.getElementById('exercise-form'))) {
    startAutoRefresh();
}

console.log('✅ Dashboard initialized successfully');
