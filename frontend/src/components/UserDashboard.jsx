// components/UserDashboard.jsx
import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { updateUserPoints, addPoints } from '../utils/pointsService';
import {QRCodeSVG} from 'qrcode.react';
import QRCodePopup from './QRCodePopup';

const UserDashboard = ({ user }) => {
    const [points, setPoints] = useState(0);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const fetchPoints = async () => {
            try {
                const response = await axios.get(`https://greenscore.onrender.com/api/user/${user.google_id}/points`);
                setPoints(response.data.points);
            } catch (error) {
                console.error("Error fetching points:", error);
            }
        };

        if (user.google_id) {
            fetchPoints();
        }
    }, [user.google_id]);

    const handleRecycleItem = async () => {
        try {
            // Add 1 point for recycling
            const result = await addPoints(user.google_id, 1);
            setPoints(result.points); // Update local state
            alert('Thank you for recycling! +1 point');
        } catch (error) {
            console.error('Error updating points:', error);
        }
    };

    const handleResetPoints = async () => {
        try {
            const result = await updateUserPoints(user.google_id, 0);
            setPoints(result.points);
            alert('Points have been reset');
        } catch (error) {
            console.error('Error resetting points:', error);
        }
    };

    return (
        <div>
            <h2>Welcome, {user.name}!</h2>
            <p>Your Green Score: {points}</p>
            <QRCodePopup QRId={user.google_id}/>
            {/* Example buttons for testing */}
            <button 
                onClick={() => handleRecycleItem()}
                className="bg-green-500 text-white px-4 py-2 rounded mr-2"
            >
                Simulate Recycling (+1 Green Score)
            </button>
            
            <button 
                onClick={() => handleResetPoints()}
                className="bg-red-500 text-white px-4 py-2 rounded"
            >
                Reset Green Score
            </button>
        </div>
    );
};

export default UserDashboard;