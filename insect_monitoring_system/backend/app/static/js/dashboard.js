/*
 * Smart Farming Dashboard JavaScript
 * Handles interactivity and dynamic content
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const addCropForm = document.getElementById('add-crop-form');
    const cropList = document.getElementById('crop-list');
    const detectionList = document.getElementById('detection-list');
    const cropCountElement = document.getElementById('crop-count');
    const pestCountElement = document.getElementById('pest-count');
    const approvalCountElement = document.getElementById('approval-count');
    const logoutLink = document.getElementById('logout-link');
    const dailyTipElement = document.getElementById('daily-tip');
    
    // Navigation elements
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Daily tips for farmers (translations will be applied)
    const dailyTips = {
        en: [
            "Water your crops early in the morning to reduce evaporation loss.",
            "Rotate your crops each season to maintain soil health.",
            "Check your irrigation system regularly for leaks to conserve water.",
            "Apply organic compost to improve soil fertility naturally.",
            "Monitor weather forecasts to plan your farming activities.",
            "Keep records of your crop yields to identify patterns and improvements.",
            "Use companion planting to naturally deter pests.",
            "Test your soil pH annually to ensure optimal growing conditions."
        ],
        mr: [
            "बाष्पभट्टी कमी करण्यासाठी सकाळी लवकरच पीकांचे पाणी द्या.",
            "मातीचे आरोग्य टिकवण्यासाठी प्रत्येक हंगामी पीके फिरवा.",
            "पाणी वाचवण्यासाठी नियमितपणे सिंचन प्रणाली तपासा.",
            "मातीची सुरक्षितता सुधारण्यासाठी सेंद्रीय खत लावा.",
            "शेतीची योजना बनवण्यासाठी हवामान अहवाल निरीक्षण करा.",
            "सुधारणा ओळखण्यासाठी पीक उत्पादनाचे नोंदणी ठेवा.",
            "कीटकांवर प्राकृतिकरित्या नियंत्रण मिळवण्यासाठी सहपालन लावा.",
            "योग्य वाढीची परिस्थिती सुनिश्चित करण्यासाठी वार्षिक मातीची pH चाचणी करा."
        ],
        hi: [
            "वाष्पीकरण को कम करने के लिए सुबह अपनी फसलों को पानी दें।",
            "मिट्टी के स्वास्थ्य को बनाए रखने के लिए प्रत्येक मौसम में अपनी फसलों को घुमाएं।",
            "पानी को संरक्षित करने के लिए अपनी सिंचाई प्रणाली को नियमित रूप से रिसाव के लिए जांचें।",
            "मिट्टी की उर्वरता को सुधारने के लिए कार्बनिक खाद का उपयोग करें।",
            "अपनी खेती की योजना बनाने के लिए मौसम पूर्वानुमान की निगरानी करें।",
            "पैटर्न और सुधार की पहचान करने के लिए अपनी फसल की पैदावार का रिकॉर्ड रखें।",
            "कीड़ों को प्राकृतिक रूप से भगाने के लिए सहचर खेती का उपयोग करें।",
            "इष्टतम विकास शर्तों को सुनिश्चित करने के लिए प्रति वर्ष अपनी मिट्टी का pH परीक्षण करें।"
        ]
    };
    
    // Initialize dashboard
    initializeDashboard();
    
    // Event Listeners
    if (addCropForm) {
        addCropForm.addEventListener('submit', handleAddCrop);
    }
    
    if (logoutLink) {
        logoutLink.addEventListener('click', handleLogout);
    }
    
    // Set up navigation
    setupNavigation();
    
    // Set up daily tip
    updateDailyTip();
    
    // Add event listeners for existing crop cards
    document.querySelectorAll('.view-details').forEach(button => {
        button.addEventListener('click', function() {
            const cropId = this.getAttribute('data-crop-id');
            fetchCropDetails(cropId);
        });
    });
    
    // Add event listeners for existing remedy sections
    document.querySelectorAll('.remedy-header').forEach(header => {
        header.addEventListener('click', function() {
            toggleRemedySection(this);
        });
    });
    
    // Function to initialize dashboard
    function initializeDashboard() {
        // Load initial data
        loadPestDetections();
        updateStats();
        
        // Check for saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
        
        // Set up periodic updates
        setInterval(updateStats, 30000); // Update stats every 30 seconds
        setInterval(updateDailyTip, 300000); // Update tip every 5 minutes
    }
    
    // Function to handle adding a new crop
    async function handleAddCrop(event) {
        event.preventDefault();
        
        // Get form values
        const cropName = document.getElementById('crop-name').value;
        const cropVariety = document.getElementById('crop-variety').value;
        const plantingDate = document.getElementById('planting-date').value;
        const areaHectares = document.getElementById('area-hectares').value;
        const irrigationType = document.getElementById('irrigation-type').value;
        
        // Validate form
        if (!cropName || !cropVariety || !plantingDate || !areaHectares || !irrigationType) {
            showNotification(getTranslation('pleaseFillAllFields'), 'error');
            return;
        }
        
        // Create crop data object
        const cropData = {
            crop_name: cropName,
            crop_variety: cropVariety,
            planting_date: plantingDate,
            area_in_hectares: parseFloat(areaHectares),
            irrigation_type: irrigationType
        };
        
        // Disable submit button during submission
        const submitButton = addCropForm.querySelector('.btn-primary');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + getTranslation('adding');
        submitButton.disabled = true;
        
        try {
            // Send data to server
            const response = await fetch('/api/crops', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(cropData)
            });
            
            if (response.ok) {
                const newCrop = await response.json();
                
                // Add crop to UI
                addCropToUI(newCrop);
                
                // Reset form
                addCropForm.reset();
                
                // Update stats
                updateStats();
                
                // Show success message
                showNotification(getTranslation('cropAddedSuccessfully'), 'success');
            } else {
                const errorData = await response.json();
                showNotification(errorData.error || getTranslation('errorAddingCrop'), 'error');
            }
        } catch (error) {
            console.error('Error adding crop:', error);
            showNotification(getTranslation('errorAddingCrop'), 'error');
        } finally {
            // Re-enable submit button
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }
    
    // Function to add crop to UI
    function addCropToUI(crop) {
        const cropElement = document.createElement('div');
        cropElement.className = 'crop-card fade-in';
        cropElement.innerHTML = `
            <div class="crop-icon">
                <i class="fas fa-seedling"></i>
            </div>
            <div class="crop-info">
                <h3>${crop.crop_name} - ${crop.crop_variety}</h3>
                <p><i class="fas fa-calendar-day"></i> ${getTranslation('planted')}: ${crop.planting_date}</p>
                <p><i class="fas fa-ruler-combined"></i> ${getTranslation('area')}: ${crop.area_in_hectares} ${getTranslation('hectares')}</p>
                <p><i class="fas fa-tint"></i> ${getTranslation('irrigation')}: ${crop.irrigation_type}</p>
            </div>
            <button class="btn-secondary view-details" data-crop-id="${crop.id}">
                <i class="fas fa-eye"></i> ${getTranslation('viewDetails')}
            </button>
        `;
        cropList.prepend(cropElement);
        
        // Add event listener to the new button
        const viewDetailsButton = cropElement.querySelector('.view-details');
        viewDetailsButton.addEventListener('click', function() {
            const cropId = this.getAttribute('data-crop-id');
            fetchCropDetails(cropId);
        });
    }
    
    // Function to fetch crop details and show in modal
    async function fetchCropDetails(cropId) {
        try {
            const response = await fetch(`/api/crops/${cropId}`);
            if (response.ok) {
                const crop = await response.json();
                showCropDetails(crop);
            } else {
                showNotification(getTranslation('errorFetchingCropDetails'), 'error');
            }
        } catch (error) {
            console.error('Error fetching crop details:', error);
            showNotification(getTranslation('errorFetchingCropDetails'), 'error');
        }
    }
    
    // Function to show crop details in a modal
    function showCropDetails(crop) {
        // Create modal element
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i class="fas fa-seedling"></i> ${getTranslation('cropDetails')}</h2>
                    <span class="close">&times;</span>
                </div>
                <div class="modal-body">
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-signature"></i> ${getTranslation('cropName')}:</strong>
                        <span>${crop.crop_name}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-edit"></i> ${getTranslation('variety')}:</strong>
                        <span>${crop.crop_variety}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-calendar-day"></i> ${getTranslation('plantingDate')}:</strong>
                        <span>${crop.planting_date}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-ruler-combined"></i> ${getTranslation('area')}:</strong>
                        <span>${crop.area_in_hectares} ${getTranslation('hectares')}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-tint"></i> ${getTranslation('irrigationType')}:</strong>
                        <span>${crop.irrigation_type}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-heart"></i> ${getTranslation('growthStage')}:</strong>
                        <span>${getTranslation('vegetative')}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-sun"></i> ${getTranslation('sunlightRequirement')}:</strong>
                        <span>${getTranslation('fullSun')}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-tint"></i> ${getTranslation('waterRequirement')}:</strong>
                        <span>${getTranslation('moderate')}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-leaf"></i> ${getTranslation('fertilizerRecommendation')}:</strong>
                        <span>${getTranslation('balancedNPK')}</span>
                    </div>
                    <div class="crop-detail-item">
                        <strong><i class="fas fa-cut"></i> ${getTranslation('pruningSchedule')}:</strong>
                        <span>${getTranslation('pruneAfterHarvest')}</span>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="btn-primary close-modal">${getTranslation('close')}</button>
                </div>
            </div>
        `;
        
        // Add modal to document
        document.body.appendChild(modal);
        
        // Add event listeners for closing
        const closeButtons = modal.querySelectorAll('.close, .close-modal');
        closeButtons.forEach(button => {
            button.addEventListener('click', function() {
                document.body.removeChild(modal);
            });
        });
        
        // Close modal when clicking outside
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }
    
    // Function to load pest detections
    function loadPestDetections() {
        // Fetch pest detections from server
        fetch('/api/detections')
            .then(response => response.json())
            .then(detections => {
                // Clear existing detections
                detectionList.innerHTML = '';
                
                // Add detections to UI
                detections.forEach(detection => {
                    addDetectionToUI(detection);
                });
            })
            .catch(error => {
                console.error('Error loading detections:', error);
            });
    }
    
    // Function to add detection to UI
    function addDetectionToUI(detection) {
        // Determine severity class and icon
        let severityClass = '';
        let severityIcon = '';
        let pestIcon = '';
        
        switch (detection.severity) {
            case 'High':
                severityClass = 'severity-high';
                severityIcon = '<i class="fas fa-exclamation-triangle"></i>';
                pestIcon = '<i class="fas fa-bug"></i>';
                break;
            case 'Medium':
                severityClass = 'severity-medium';
                severityIcon = '<i class="fas fa-exclamation-circle"></i>';
                pestIcon = '<i class="fas fa-spider"></i>';
                break;
            case 'Low':
                severityClass = 'severity-low';
                severityIcon = '<i class="fas fa-info-circle"></i>';
                pestIcon = '<i class="fas fa-bug-slash"></i>';
                break;
        }
        
        const detectionElement = document.createElement('div');
        detectionElement.className = 'detection-card fade-in';
        detectionElement.innerHTML = `
            <div class="detection-header">
                <div class="detection-icon">${pestIcon}</div>
                <div class="detection-title">${detection.name} ${getTranslation('detected')}</div>
                <div class="severity-badge ${severityClass}">
                    ${severityIcon} ${detection.severity}
                </div>
            </div>
            <div class="detection-details">
                <p><i class="fas fa-seedling"></i> ${getTranslation('crop')}: ${detection.crop}</p>
                <p><i class="fas fa-clock"></i> ${getTranslation('time')}: ${new Date(detection.timestamp).toLocaleString()}</p>
            </div>
            <div class="remedy-section">
                <div class="remedy-header">
                    <h4><i class="fas fa-prescription-bottle"></i> ${getTranslation('recommendedRemedy')}</h4>
                    <i class="fas fa-chevron-down"></i>
                </div>
                <div class="remedy-content">
                    <p>${detection.remedy}</p>
                    <button class="btn-primary done-btn" data-detection-id="${detection.id}">
                        <i class="fas fa-check"></i> ${getTranslation('done')}
                    </button>
                </div>
            </div>
        `;
        
        detectionList.appendChild(detectionElement);
        
        // Add event listener for collapsible remedy section
        const remedyHeader = detectionElement.querySelector('.remedy-header');
        remedyHeader.addEventListener('click', function() {
            toggleRemedySection(this);
        });
        
        // Add event listener for Done button
        const doneButton = detectionElement.querySelector('.done-btn');
        doneButton.addEventListener('click', function() {
            const detectionId = this.getAttribute('data-detection-id');
            markDetectionAsDone(detectionId, detectionElement);
        });
    }
    
    // Function to toggle remedy section
    function toggleRemedySection(header) {
        const remedyContent = header.nextElementSibling;
        remedyContent.classList.toggle('active');
        const chevronIcon = header.querySelector('i.fa-chevron-down, i.fa-chevron-up');
        if (remedyContent.classList.contains('active')) {
            chevronIcon.classList.remove('fa-chevron-down');
            chevronIcon.classList.add('fa-chevron-up');
        } else {
            chevronIcon.classList.remove('fa-chevron-up');
            chevronIcon.classList.add('fa-chevron-down');
        }
    }
    
    // Function to mark detection as done
    async function markDetectionAsDone(detectionId, detectionElement) {
        try {
            const response = await fetch(`/api/detections/${detectionId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                // Remove the detection element from UI
                detectionElement.classList.add('fade-out');
                setTimeout(() => {
                    detectionElement.remove();
                    updateStats();
                }, 300);
                
                showNotification(getTranslation('pestDetectionMarkedAsDone'), 'success');
            } else {
                showNotification(getTranslation('errorMarkingDetectionAsDone'), 'error');
            }
        } catch (error) {
            console.error('Error marking detection as done:', error);
            showNotification(getTranslation('errorMarkingDetectionAsDone'), 'error');
        }
    }
    
    // Function to update stats
    function updateStats() {
        // Fetch stats from server
        fetch('/api/stats')
            .then(response => response.json())
            .then(stats => {
                cropCountElement.textContent = stats.total_crops;
                pestCountElement.textContent = stats.pests_detected;
                approvalCountElement.textContent = stats.pending_approvals;
            })
            .catch(error => {
                console.error('Error updating stats:', error);
                // Fallback to counting elements
                const cropCount = document.querySelectorAll('.crop-card').length;
                const pestCount = document.querySelectorAll('.detection-card').length;
                cropCountElement.textContent = cropCount;
                pestCountElement.textContent = pestCount;
            });

        // Fetch current weather
        fetch('/api/weather/current')
            .then(response => response.json())
            .then(weather => {
                const weatherWidget = document.querySelector('.weather-widget');
                if (weatherWidget) {
                    const icon = getWeatherIcon(weather.description);
                    weatherWidget.innerHTML = `
                        <i class="${icon}"></i>
                        <span>${weather.temperature}°C, ${weather.description}</span>
                    `;
                }

                // Update sensor cards
                const tempCard = document.querySelector('.sensor-card h3 i.fa-thermometer-half').parentElement.parentElement;
                const humidityCard = document.querySelector('.sensor-card h3 i.fa-wind').parentElement.parentElement;
                if (tempCard) {
                    tempCard.querySelector('.sensor-value').textContent = `${weather.temperature}°C`;
                    const tempPercent = Math.min(100, Math.max(0, (weather.temperature / 50) * 100));
                    tempCard.querySelector('.progress-fill').style.width = `${tempPercent}%`;
                }
                if (humidityCard && weather.humidity) {
                    humidityCard.querySelector('.sensor-value').textContent = `${weather.humidity}%`;
                    humidityCard.querySelector('.progress-fill').style.width = `${weather.humidity}%`;
                }
            })
            .catch(error => {
                console.error('Error fetching weather:', error);
            });
    }
    
    // Function to get weather icon based on description
    function getWeatherIcon(description) {
        const desc = description.toLowerCase();
        if (desc.includes('clear') || desc.includes('sun')) return 'fas fa-sun';
        if (desc.includes('cloud') || desc.includes('overcast')) return 'fas fa-cloud';
        if (desc.includes('rain') || desc.includes('drizzle') || desc.includes('shower')) return 'fas fa-cloud-rain';
        if (desc.includes('thunder') || desc.includes('storm')) return 'fas fa-bolt';
        if (desc.includes('snow') || desc.includes('hail')) return 'fas fa-snowflake';
        if (desc.includes('fog') || desc.includes('mist')) return 'fas fa-smog';
        return 'fas fa-sun'; // default
    }
    
    // Function to get translation
    function getTranslation(key) {
        const savedLanguage = localStorage.getItem('language') || 'en';
        if (typeof translations !== 'undefined' && translations.getTranslation) {
            return translations.getTranslation(key, savedLanguage);
        }
        return key; // Fallback to key if translation not available
    }
    
    // Function to set up navigation
    function setupNavigation() {
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all links
                navLinks.forEach(navLink => navLink.classList.remove('active'));
                
                // Add active class to clicked link
                this.classList.add('active');
                
                // Get the page from data attribute
                const page = this.getAttribute('data-page');
                
                // Handle navigation
                if (page === 'profile') {
                    window.location.href = '/profile';
                } else if (page === 'settings') {
                    window.location.href = '/settings';
                } else if (page === 'dashboard') {
                    window.location.href = '/';
                }
            });
        });
    }
    
    // Function to handle logout
    function handleLogout(e) {
        e.preventDefault();
        
        // Show confirmation dialog
        if (confirm(getTranslation('confirmLogout'))) {
            fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    // Clear any stored credentials
                    localStorage.clear();
                    sessionStorage.clear();
                    
                    // Redirect to login page
                    window.location.href = '/login';
                } else {
                    showNotification(getTranslation('errorLoggingOut'), 'error');
                }
            })
            .catch(error => {
                console.error('Error logging out:', error);
                showNotification(getTranslation('errorLoggingOut'), 'error');
            });
        }
    }
    
    // Function to show notifications
    function showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} fade-in`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            ${message}
        `;
        
        // Style the notification
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.padding = '15px 20px';
        notification.style.borderRadius = '8px';
        notification.style.color = 'white';
        notification.style.fontWeight = '500';
        notification.style.zIndex = '1000';
        notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        notification.style.maxWidth = '300px';
        notification.style.cursor = 'pointer';
        notification.style.display = 'flex';
        notification.style.alignItems = 'center';
        notification.style.gap = '10px';
        
        if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #4CAF50, #8BC34A)';
        } else {
            notification.style.background = 'linear-gradient(135deg, #f44336, #e91e63)';
        }
        
        // Add click to dismiss
        notification.addEventListener('click', function() {
            this.style.opacity = '0';
            setTimeout(() => {
                if (this.parentNode) {
                    this.parentNode.removeChild(this);
                }
            }, 300);
        });
        
        // Add to document
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }
        }, 5000);
    }
});

// Global function for viewing crop details (can be called from HTML)
function viewCropDetails(cropId) {
    // In a real app, this would fetch crop details from the server
    alert(`Viewing details for crop ID: ${cropId}`);
}