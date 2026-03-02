// Main JavaScript for Smart Farming Dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const addCropForm = document.getElementById('add-crop-form');
    const cropList = document.getElementById('crop-list');
    const approvalList = document.getElementById('approval-list');
    const detectionList = document.getElementById('detection-list');
    const sensorData = document.getElementById('sensor-data');
    const cropCount = document.getElementById('crop-count');
    const pestCount = document.getElementById('pest-count');
    const approvalCount = document.getElementById('approval-count');
    const usernameElement = document.getElementById('username');
    const logoutLink = document.getElementById('logout-link');
    
    // Event listener for adding crops
    if (addCropForm) {
        addCropForm.addEventListener('submit', handleAddCrop);
    }
    
    // Event listener for logout
    if (logoutLink) {
        logoutLink.addEventListener('click', handleLogout);
    }
    
    // Initialize the dashboard
    loadUserProfile();
    loadCrops();
    loadApprovals();
    loadDetections();
    loadSensorData();
    
    // Function to load user profile
    async function loadUserProfile() {
        try {
            const response = await fetch('/api/profile');
            if (response.ok) {
                const user = await response.json();
                if (usernameElement) {
                    usernameElement.textContent = user.username;
                }
            } else {
                // Redirect to login if not authenticated
                window.location.href = '/login';
            }
        } catch (error) {
            console.error('Error loading user profile:', error);
        }
    }
    
    // Function to handle logout
    async function handleLogout(e) {
        e.preventDefault();
        
        try {
            const response = await fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                // Clear any stored credentials
                localStorage.clear();
                sessionStorage.clear();
                // Redirect to login page
                window.location.href = '/login';
            }
        } catch (error) {
            console.error('Error logging out:', error);
            // Even if there's an error, redirect to login
            window.location.href = '/login';
        }
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
        
        // Create crop data object
        const cropData = {
            crop_name: cropName,
            crop_variety: cropVariety,
            planting_date: plantingDate,
            area_in_hectares: parseFloat(areaHectares),
            irrigation_type: irrigationType
        };
        
        // Disable submit button during submission
        const submitButton = addCropForm.querySelector('.submit-btn');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Adding...';
        submitButton.disabled = true;
        
        try {
            const response = await fetch('/api/crops', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(cropData)
            });
            
            if (response.ok) {
                const newCrop = await response.json();
                addCropToUI(newCrop);
                addCropForm.reset();
                updateStats();
                showNotification('Crop added successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification('Error: ' + error.error, 'error');
            }
        } catch (error) {
            console.error('Error adding crop:', error);
            showNotification('Error adding crop. Please try again.', 'error');
        } finally {
            // Re-enable submit button
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    }
    
    // Function to add crop to UI
    function addCropToUI(crop) {
        const cropElement = document.createElement('div');
        cropElement.className = 'crop-item';
        cropElement.innerHTML = `
            <h4>${crop.crop_name} - ${crop.crop_variety}</h4>
            <div class="crop-details">
                <p><strong>Planting Date:</strong> ${crop.planting_date}</p>
                <p><strong>Area:</strong> ${crop.area_in_hectares} hectares</p>
                <p><strong>Irrigation:</strong> ${crop.irrigation_type}</p>
                <span class="crop-tag">${crop.crop_name}</span>
            </div>
        `;
        cropList.appendChild(cropElement);
        
        // Add animation class
        setTimeout(() => {
            cropElement.style.opacity = '1';
            cropElement.style.transform = 'translateY(0)';
        }, 10);
    }
    
    // Function to load crops
    async function loadCrops() {
        try {
            const response = await fetch('/api/crops');
            if (response.ok) {
                const crops = await response.json();
                cropList.innerHTML = '';
                crops.forEach(crop => {
                    addCropToUI(crop);
                });
                updateStats();
            } else {
                console.error('Error loading crops');
            }
        } catch (error) {
            console.error('Error loading crops:', error);
            showNotification('Error loading crops', 'error');
        }
    }
    
    // Function to load pest detections
    async function loadDetections() {
        try {
            const response = await fetch('/api/detections');
            if (response.ok) {
                const detections = await response.json();
                detectionList.innerHTML = '';
                
                detections.forEach(detection => {
                    const detectionElement = document.createElement('div');
                    detectionElement.className = 'detection-item';
                    detectionElement.dataset.id = detection.id;
                    
                    // Determine severity class
                    let severityClass = '';
                    if (detection.severity === 'High') {
                        severityClass = 'severity-high';
                    } else if (detection.severity === 'Medium') {
                        severityClass = 'severity-medium';
                    } else {
                        severityClass = 'severity-low';
                    }
                    
                    detectionElement.innerHTML = `
                        <h4>${detection.name} Detected</h4>
                        <div class="detection-details">
                            <p><strong>Crop:</strong> ${detection.crop}</p>
                            <p><strong>Timestamp:</strong> ${detection.timestamp}</p>
                            <p><strong>Severity:</strong> <span class="${severityClass}">${detection.severity}</span></p>
                            <div class="remedy">
                                <strong>Recommended Remedy:</strong> ${detection.remedy}
                            </div>
                            <button class="done-btn" onclick="markDetectionAsDone(${detection.id})">Done</button>
                        </div>
                    `;
                    detectionList.appendChild(detectionElement);
                });
            } else {
                console.error('Error loading detections');
            }
        } catch (error) {
            console.error('Error loading detections:', error);
            detectionList.innerHTML = '<p>Error loading pest detections.</p>';
        }
    }
    
    // Function to load farmer approvals
    async function loadApprovals() {
        try {
            const response = await fetch('/api/farmer_approvals');
            if (response.ok) {
                const approvals = await response.json();
                approvalList.innerHTML = '';
                
                approvals.forEach(approval => {
                    const approvalElement = document.createElement('div');
                    approvalElement.className = 'approval-item';
                    
                    // Determine status class
                    const statusClass = approval.status === 'approved' ? 'status-approved' : 'status-pending';
                    const statusText = approval.status === 'approved' ? 'Approved' : 'Pending Approval';
                    
                    approvalElement.innerHTML = `
                        <h4>${approval.type} Request</h4>
                        <p><strong>Crop:</strong> ${approval.crop}</p>
                        <p>${approval.details}</p>
                        <p class="approval-status ${statusClass}">Status: ${statusText}</p>
                        ${approval.status !== 'approved' ? 
                            `<button class="approve-btn" onclick="approveRequest(${approval.id}, '${approval.type}')">Approve</button>` : 
                            ''}
                    `;
                    approvalList.appendChild(approvalElement);
                });
                
                updateStats();
            } else {
                console.error('Error loading approvals');
            }
        } catch (error) {
            console.error('Error loading approvals:', error);
            approvalList.innerHTML = '<p>Error loading approvals.</p>';
        }
    }
    
    // Function to load sensor data
    async function loadSensorData() {
        try {
            // In a real app, this would fetch from IoT devices
            // For now, we'll use sample data
            sensorData.innerHTML = `
                <div class="sensor-grid">
                    <div class="sensor-item">
                        <h4>Soil Moisture</h4>
                        <div class="sensor-value">65%</div>
                    </div>
                    <div class="sensor-item">
                        <h4>pH Level</h4>
                        <div class="sensor-value">6.8</div>
                    </div>
                    <div class="sensor-item">
                        <h4>Temperature</h4>
                        <div class="sensor-value">24°C</div>
                    </div>
                    <div class="sensor-item">
                        <h4>Humidity</h4>
                        <div class="sensor-value">72%</div>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error loading sensor data:', error);
            sensorData.innerHTML = '<p>Error loading sensor data. IoT devices may be offline.</p>';
        }
    }
    
    // Function to update stats
    async function updateStats() {
        try {
            const response = await fetch('/api/stats');
            if (response.ok) {
                const stats = await response.json();
                cropCount.textContent = stats.total_crops;
                pestCount.textContent = stats.pests_detected;
                approvalCount.textContent = stats.pending_approvals;
            }
        } catch (error) {
            console.error('Error updating stats:', error);
        }
    }
    
    // Function to show notifications
    function showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.padding = '15px 20px';
        notification.style.borderRadius = '5px';
        notification.style.color = 'white';
        notification.style.fontWeight = '500';
        notification.style.zIndex = '1000';
        notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        notification.style.maxWidth = '300px';
        notification.style.cursor = 'pointer';
        notification.style.transition = 'all 0.3s ease';
        
        if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #4CAF50, #8BC34A)';
        } else {
            notification.style.background = 'linear-gradient(135deg, #f44336, #e91e63)';
        }
        
        // Add hover effect
        notification.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        notification.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        
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
    
    // Global function for approving requests
    window.approveRequest = async function(approvalId, type) {
        try {
            const response = await fetch(`/api/approve_request/${approvalId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({type: type})
            });
            
            if (response.ok) {
                const result = await response.json();
                showNotification(result.message, 'success');
                // Reload approvals to show updated status
                loadApprovals();
            } else {
                const error = await response.json();
                showNotification('Error: ' + error.error, 'error');
            }
        } catch (error) {
            console.error('Error approving request:', error);
            showNotification('Error approving request. Please try again.', 'error');
        }
    };
    
    // Global function for marking detections as done
    window.markDetectionAsDone = async function(detectionId) {
        try {
            const response = await fetch(`/api/detections/${detectionId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const result = await response.json();
                showNotification(result.message, 'success');
                // Remove the detection element from UI
                const detectionElement = document.querySelector(`.detection-item[data-id="${detectionId}"]`);
                if (detectionElement) {
                    detectionElement.style.opacity = '0';
                    detectionElement.style.transform = 'translateX(100px)';
                    setTimeout(() => {
                        if (detectionElement.parentNode) {
                            detectionElement.parentNode.removeChild(detectionElement);
                        }
                        // Update stats
                        updateStats();
                    }, 300);
                }
            } else {
                const error = await response.json();
                showNotification('Error: ' + error.error, 'error');
            }
        } catch (error) {
            console.error('Error marking detection as done:', error);
            showNotification('Error marking detection as done. Please try again.', 'error');
        }
    };
    
    // Initialize stats
    updateStats();
});