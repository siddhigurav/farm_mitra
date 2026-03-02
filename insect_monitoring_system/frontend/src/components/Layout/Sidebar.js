import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2>Smart Insect Detector</h2>
            </div>
            <ul className="sidebar-menu">
                <li><Link to="/dashboard">Dashboard</Link></li>
                <li><Link to="/dashboard/add-crop">Add Crop</Link></li>
                <li><Link to="/dashboard/crop-history">Crop History</Link></li>
                <li><Link to="/dashboard/profile">Profile</Link></li>
                <li><button onClick={handleLogout} className="logout-button">Logout</button></li>
            </ul>
        </div>
    );
};

export default Sidebar;