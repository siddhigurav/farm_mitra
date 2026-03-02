
import React from 'react';
import './Profile.css';

const Profile = () => {
    // Mock user data
    const user = {
        name: 'John Doe',
        email: 'john.doe@example.com',
        farmName: 'Green Valley Farms',
        crops: ['Grapes', 'Guava'],
    };

    return (
        <div className="profile-container">
            <div className="profile-card">
                <h2>User Profile</h2>
                <div className="profile-info">
                    <p><strong>Name:</strong> {user.name}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Farm Name:</strong> {user.farmName}</p>
                    <p><strong>Crops:</strong> {user.crops.join(', ')}</p>
                </div>
            </div>
        </div>
    );
};

export default Profile;
