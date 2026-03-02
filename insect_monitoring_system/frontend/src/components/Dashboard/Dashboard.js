
import React from 'react';
import { Link } from 'react-router-dom';
import { useCrops } from '../../context/CropContext';
import './Dashboard.css';

const Dashboard = () => {
    const { crops } = useCrops();

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h1>Dashboard</h1>
                <Link to="/dashboard/add-crop" className="add-crop-button">Add New Crop</Link>
            </div>
            <div className="dashboard-summary">
                <div className="summary-card">
                    <h3>Total Crops</h3>
                    <p>{crops.length}</p>
                </div>
                <div className="summary-card">
                    <h3>Alerts</h3>
                    <p>0</p> {/* Placeholder */}
                </div>
            </div>
            <div className="crop-list">
                <h3>Your Crops</h3>
                <div className="row">
                    {crops.length > 0 ? (
                        crops.map(crop => (
                            <div className="col-md-4" key={crop.id}>
                                <div className="card mb-4">
                                    <div className="card-body">
                                        <h5 className="card-title">{crop.crop_name}</h5>
                                        <h6 className="card-subtitle mb-2 text-muted">{crop.crop_variety}</h6>
                                        <p className="card-text">Planting Date: {crop.planting_date}</p>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p>You haven't added any crops yet.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
