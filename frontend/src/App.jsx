// src/App.jsx
import React, { useState } from 'react';
import GoogleSignIn from './components/GoogleSignIn';
import UserDashboard from './components/UserDashboard';
import Leaderboard from './components/Leaderboard';
import { GoogleOAuthProvider } from '@react-oauth/google';
import "./App.css"

function App() {
    const [user, setUser] = useState(null);

    return (
      <GoogleOAuthProvider clientId="767027653029-vu6grvaeh28h8ueuc7emqdhm7tbliud5.apps.googleusercontent.com">
        <div className="App">

            <h1>GreenScore</h1>
            {!user ? (
                <GoogleSignIn setUser={setUser} />
            ) : (
                <>
                    <UserDashboard user={user} />
                    <Leaderboard />
                </>
            )}
        </div>
        </GoogleOAuthProvider>
    );
}

export default App;
