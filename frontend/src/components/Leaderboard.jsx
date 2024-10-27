import React, { useState, useEffect, useMemo, useCallback } from 'react';
import axios from 'axios';
import './Leaderboard.css';

const LeaderboardItem = React.memo(({ user, index }) => {
  const getPlaceClass = useMemo(() => {
    if (index === 0) return 'first-place';
    if (index === 1) return 'second-place';
    if (index === 2) return 'third-place';
    return '';
  }, [index]);

  return (
    <div 
      className={`leaderboard-item ${getPlaceClass}`}
    >
      <div className="rank">
        {index + 1}.
      </div>
      
      <div className="avatar">
        <img 
          src={user.picture} 
          alt={user.name}
        />
      </div>
      
      <div className="user-name">
        {user.name}
      </div>
      
      <div className="points">
        {user.points} pts
      </div>
    </div>
  );
});

const Leaderboard = () => {
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLeaderboard = useCallback(async () => {
    try {
      const { data: newData } = await axios.get('https://greenscore.onrender.com/api/leaderboard');
      
      setLeaderboardData(prevData => {
        // Only update if data has actually changed
        if (JSON.stringify(prevData) === JSON.stringify(newData)) {
          return prevData;
        }
        
        // Update only changed items
        return newData.map(newUser => {
          const prevUser = prevData.find(p => p.google_id === newUser.google_id);
          if (prevUser && prevUser.points === newUser.points) {
            return prevUser; // Reuse existing user object if points haven't changed
          }
          return newUser;
        });
      });

      setLoading(false);
    } catch (err) {
      console.error('Error fetching leaderboard:', err);
      setError('Failed to load leaderboard');
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLeaderboard();
    const interval = setInterval(fetchLeaderboard, 3000);
    return () => clearInterval(interval);
  }, [fetchLeaderboard]);

  if (loading) {
    return <div className="loading">Loading leaderboard...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="leaderboard-container">
      <h2 className="leaderboard-title">
        Top Recyclers
      </h2>
      
      <div className="leaderboard-list">
        {leaderboardData.map((user, index) => (
          <LeaderboardItem 
            key={user.google_id}
            user={user}
            index={index}
          />
        ))}
      </div>
    </div>
  );
};

export default Leaderboard;