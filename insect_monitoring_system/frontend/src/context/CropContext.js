
import React, { createContext, useState, useContext } from 'react';

const CropContext = createContext(null);

const initialCrops = [
    { id: 1, crop_name: 'Grapes', crop_variety: 'Thompson Seedless', planting_date: '2024-03-15' },
    { id: 2, crop_name: 'Guava', crop_variety: 'Allahabad Safeda', planting_date: '2024-04-10' },
];

export const CropProvider = ({ children }) => {
    const [crops, setCrops] = useState(initialCrops);

    const addCrop = (crop) => {
        setCrops(prevCrops => [...prevCrops, { ...crop, id: prevCrops.length + 1 }]);
    };

    return (
        <CropContext.Provider value={{ crops, addCrop }}>
            {children}
        </CropContext.Provider>
    );
};

export const useCrops = () => {
    return useContext(CropContext);
};
