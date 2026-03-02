import React from 'react';
import { Link } from 'react-router-dom';
import './Auth.css';

const Signup = () => {
    // In a real app, you would handle user creation here
    return (
        <div className="auth-container">
            <form className="auth-form">
                <h2>Signup</h2>
                <div className="form-group">
                    <label>Full Name</label>
                    <input type="text" required />
                </div>
                <div className="form-group">
                    <label>Email</label>
                    <input type="email" required />
                </div>
                <div className="form-group">
                    <label>Password</label>
                    <input type="password" required />
                </div>
                <Link to="/login" className="btn btn-success btn-block">Sign Up</Link>
                <p className="auth-switch">
                    Already have an account? <Link to="/login">Log in</Link>
                </p>
            </form>
        </div>
    );
};

export default Signup;