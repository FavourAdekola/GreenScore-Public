# Recycling Detection System with Leaderboard

This project is a recycling detection system with a leaderboard that encourages users to recycle by assigning points for recycled items. Each user has a unique QR code, and the points accumulated are stored and displayed on a leaderboard. The backend is built in Python and MongoDB Atlas is used as the database.

## Features

- **User Registration**: Users can register with unique QR codes associated with each account.
- **Google Login**: Optional integration for users to log in with Google.
- **QR Code Generation**: A unique QR code is generated for each user upon registration.
- **Points System**: Users earn points for each recycled item.
- **Leaderboard**: Users can view rankings based on points, encouraging competition and environmental engagement.

## Tech Stack

- **Backend**: Python with Flask (or FastAPI)
- **Database**: MongoDB Atlas
- **QR Code Generation**: Python `qrcode` library
- **Authentication**: Google OAuth (optional)

## License

This project is licensed under the MIT License.