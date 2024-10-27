// utils/pointsService.js
import axios from 'axios';

export const updateUserPoints = async (googleId, points) => {
    try {
        const response = await axios.post(`http://localhost:5000/api/user/${googleId}/points`, {
            points: points
        });
        return response.data;
    } catch (error) {
        console.error('Error updating points:', error);
        throw error;
    }
};

export const addPoints = async (googleId, pointsToAdd) => {
    try {
        // First get current points
        const currentResponse = await axios.get(`http://localhost:5000/api/user/${googleId}/points`);
        const currentPoints = currentResponse.data.points;
        
        // Then update with new total
        const newPoints = currentPoints + pointsToAdd;
        const response = await updateUserPoints(googleId, newPoints);
        return response;
    } catch (error) {
        console.error('Error adding points:', error);
        throw error;
    }
};
