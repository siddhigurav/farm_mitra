import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useTranslation } from 'react-i18next';
import './Sidebar.css';

const Sidebar = () => {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const { t, i18n } = useTranslation();

    const changeLang = (lang) => {
        i18n.changeLanguage(lang);
        localStorage.setItem('i18nextLng', lang);
        document.documentElement.lang = lang;
    };

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2>{t('app_name')}</h2>
            </div>
            <ul className="sidebar-menu">
                <li><Link to="/dashboard">{t('overview')}</Link></li>
                <li><Link to="/dashboard/live">{t('live_camera')}</Link></li>
                <li><Link to="/dashboard/analytics">{t('analytics')}</Link></li>
                <li><Link to="/dashboard/irrigation">{t('irrigation')}</Link></li>
                <li><Link to="/dashboard/crops">{t('crops')}</Link></li>
                <li><Link to="/dashboard/add-crop">{t('add_crop')}</Link></li>
                <li><Link to="/dashboard/crop-history">{t('crop_history')}</Link></li>
                <li><Link to="/dashboard/profile">{t('profile')}</Link></li>
                <li><Link to="/dashboard/settings">{t('settings')}</Link></li>
                <li><button onClick={handleLogout} className="logout-button">{t('logout')}</button></li>
            </ul>
            <div className="sidebar-footer">
                <div className="lang-switcher">
                    <button onClick={() => changeLang('en')}>EN</button>
                    <button onClick={() => changeLang('hi')}>हिं</button>
                    <button onClick={() => changeLang('mr')}>मर</button>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;