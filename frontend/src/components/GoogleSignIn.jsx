// Frontend: GoogleSignIn.jsx
import React from 'react';
import { useGoogleLogin, GoogleOAuthProvider } from '@react-oauth/google';
import config from "../config";

const GoogleSignIn = ({ setUser }) => {  // Add setUser prop
  const GOOGLE_CLIENT_ID = context.env.GOOGLE_CLIENT_ID;  // Replace with your actual Google Client ID
    console.log(GOOGLE_CLIENT_ID)
    console.log(context.env.GOOGLE_CLIENT_ID)

  const login = useGoogleLogin({
    onSuccess: async (response) => {
      try {
        // First, get user info using the access token
        const userInfoResponse = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
          headers: { Authorization: `Bearer ${response.access_token}` },
        });
        
        const userInfo = await userInfoResponse.json();
        
        // Send user info to your backend
        const backendResponse = await fetch(`${config.apiUrl}/auth/google`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            google_id: userInfo.sub,
            email: userInfo.email,
            name: userInfo.name,
            picture: userInfo.picture
          }),
        });
        
        const data = await backendResponse.json();
        console.log('Signed in user:', data);
        
        // Update both localStorage and parent component's state
        localStorage.setItem('user', JSON.stringify(data));
        setUser(data);  // Set the user state in parent component
        
      } catch (error) {
        console.error('Error signing in:', error);
      }
    },
    onError: () => console.log('Login Failed'),
    scope: 'email profile'
  });

  return (
    <GoogleOAuthProvider clientId={process.env.GOOGLE_CLIENT_ID}>
      <div className="flex justify-center items-center p-4">
        <button
          onClick={() => login()}
          className="flex items-center gap-2 bg-white text-gray-700 px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-50 transition-colors"
        >
          
          Sign in with Google
        </button>
      </div>
    </GoogleOAuthProvider>
  );
};

export default GoogleSignIn;