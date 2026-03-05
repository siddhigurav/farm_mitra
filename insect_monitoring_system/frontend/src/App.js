import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CropProvider } from './context/CropContext';
import DashboardLayout from './components/Layout/DashboardLayout';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import Dashboard from './components/Dashboard/Dashboard';
import AddCrop from './components/Dashboard/AddCrop/AddCrop';
import CropHistory from './components/Dashboard/CropHistory/CropHistory';
import Overview from './pages/Overview';
import LiveCamera from './pages/LiveCamera';
import Analytics from './pages/Analytics';
import Irrigation from './pages/Irrigation';
import CropManagement from './pages/CropManagement';
import Profile from './components/Profile/Profile';
import Settings from './pages/Settings';
import './App.css';

const PrivateRoute = ({ children }) => {
    const { user } = useAuth();
    return user ? children : <Navigate to="/login" />;
};

function App() {
    return (
        <AuthProvider>
            <CropProvider>
                <Router>
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route 
                            path="/dashboard/*" 
                            element={
                                <PrivateRoute>
                                    <DashboardRoutes />
                                </PrivateRoute>
                            }
                        />
                        <Route path="*" element={<Navigate to="/login" />} />
                    </Routes>
                </Router>
            </CropProvider>
        </AuthProvider>
    );
}

const DashboardRoutes = () => {
    return (
        <DashboardLayout>
            <Routes>
                <Route path="/" element={<Overview />} />
                <Route path="/live" element={<LiveCamera />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/irrigation" element={<Irrigation />} />
                <Route path="/crops" element={<CropManagement />} />
                <Route path="/add-crop" element={<AddCrop />} />
                <Route path="/crop-history" element={<CropHistory />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/settings" element={<Settings />} />
            </Routes>
        </DashboardLayout>
    );
}

export default App;