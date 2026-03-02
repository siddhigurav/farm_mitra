
import React from 'react';
import './CropHistory.css';

const CropHistory = () => {
    // Mock data
    const history = [
        { id: 1, name: 'Grapes', type: 'Thompson Seedless', planted: '2024-03-15', harvested: '2024-08-25', yield: '5 tons' },
        { id: 2, name: 'Guava', type: 'Allahabad Safeda', planted: '2024-04-10', harvested: '2024-09-10', yield: '2 tons' },
    ];

    return (
        <div className="crop-history-container">
            <h2>Crop History</h2>
            <table className="crop-history-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Crop Name</th>
                        <th>Crop Type</th>
                        <th>Planting Date</th>
                        <th>Harvest Date</th>
                        <th>Yield</th>
                    </tr>
                </thead>
                <tbody>
                    {history.map(item => (
                        <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.name}</td>
                            <td>{item.type}</td>
                            <td>{item.planted}</td>
                            <td>{item.harvested}</td>
                            <td>{item.yield}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default CropHistory;
