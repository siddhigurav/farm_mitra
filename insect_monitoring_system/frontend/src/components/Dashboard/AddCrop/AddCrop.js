
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCrops } from '../../context/CropContext';
import './AddCrop.css';

const AddCrop = () => {
    const [crop_name, setCropName] = useState('');
    const [crop_variety, setCropVariety] = useState('');
    const [planting_date, setPlantingDate] = useState('');
    const { addCrop } = useCrops();
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        addCrop({ crop_name, crop_variety, planting_date });
        navigate('/dashboard');
    };

    return (
        <div className="add-crop-container">
            <h2>Add New Crop</h2>
            <form className="add-crop-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Crop Name</label>
                    <input type="text" value={crop_name} onChange={(e) => setCropName(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label>Crop Variety</label>
                    <input type="text" value={crop_variety} onChange={(e) => setCropVariety(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label>Planting Date</label>
                    <input type="date" value={planting_date} onChange={(e) => setPlantingDate(e.target.value)} required />
                </div>
                <button type="submit">Add Crop</button>
            </form>
        </div>
    );
};

export default AddCrop;
