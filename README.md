[![Watch the Video](https://img.youtube.com/vi/3ZCa5jKGV6cs/0.jpg)](https://www.youtube.com/watch?v=3ZCa5jKGV6c)
# GreenScore

## Inspiration

The main inspiration behind the idea was a previous plan to build a recycling recognizer AI model as well as a desire to build a more lighthearted hackathon project that did not necessarily aim to change the world or any processes we know of. We essentially wanted to just have fun and make a game, so combining the two ideas we constructed a recycling game, GreenScore.

## What it does

GreenScore is a Recycling game platform that tracks users' recycling habits by awarding points "Green Score" for scanning recyclable materials at AI-powered trash cans. The power behind the trashcans uses Tensorflow to build a model and train it off of a database of trash and recyclable material. Then, it will predict whether a camera frame has recyclable material present or not. If it does, points will be awarded to the currently assigned user, who is determined by scanning a user-specific QR code before scanning in their items.

## How we built it

GreenScore was constructed with 3 main components in mind:

### Backend
We utilized libraries for Flask, google-oauth2, and Pymongo to accomplish the tasks on the three functions summarizing the backend.

``authentication`` - it handles Google authentication with the MongoDB Atlas users database. 

``user_point_functions`` - it retrieves the user's points and updates the user's points in the database

``leaderboard`` - it retrieves the top 10 leaderboard positions and all the information for each of the users. 

### Front End
We utilized Vite, React, Javascript, CSS, HTML to construct the front end of our site which helps us display the leaderboard as well as a user's unique QR Code and their "Green Score" 

### AI Model and Camera

GreenScore's AI model is built from Python and its TensorFlow API. A model was constructed from multiple TensorFlow layers and then trained from a [Garbage Classification](https://www.kaggle.com/datasets/mostafaabla/garbage-classification/data) database modified for our intended recycling use case. Afterward, we constructed a camera input system utilizing the OpenCV API. Here we took in frame inputs to predict whether or not an item held in front of the camera was recyclable or not. Additionally, functionality for scanning QR codes was added which will perform an API call to the backend to select which user to award points to for recyclable material.

## Challenges we ran into

The biggest problem we ran into for this project was identifying how exactly to go about constructing our AI model. There were hundreds of datasets to choose from, different model configurations such as detection, classification, and segmentation, and so much more that made the possibilities nearly endless. For our use case, we settled on a classification-focused AI model, but understand the strength of mixing approaches to obtain stronger and more accurate results in the future. Our choice was informed by trial and error, as well as a bit of research. 

Additionally, this project being our first-ever hosted website, we had issues placing our project on the cloud and enabling it to function across devices and users. We didn't understand where to get a domain name and were not inclined to spend money at this stage, but eventually, we found GitHub pages to be a solution. We were not familiar with the different cloud computing platforms available to us, but we landed on Cloudflare to help host our front end and Render.com for our back end. 

## Accomplishments that we're proud of

As with any project, we are overly glad to have thought of an idea and bring it to fruition. We spent hours planning and understanding our scope and stuck to the overarching plan, persevering through our many obstacles, to bring us a usable product. 

## What we learned

The biggest thing we learned was how to set up cloud applications, from hosting a website to working with cloud tools such as Cloudflare, mongoDB, and Render.com to help piece everything together. Additionally, for the AI model, although we had experience with PyTorch originally, we decided to learn TensorFlow to see how it compared to the other API. On the camera side, we had to learn about computer vision and how to utilize OpenCV to access our computer's webcam to make predictions per frame with our AI model. 

## What's next for GreenScore

GreenScore is far from being its completed idea and it has areas to advance on a business scale as well as a technical scale. We intend to build the software into recycling bin devices to have public areas in which recycling can be scanned and awarded points to users. We would partner with public institutions and services such as waste management plants and universities to bring these bins across the US as well as incentivize recycling beyond just adding to the leaderboard. We know that recycling plants already award money to individuals who bring in aluminum cans and other recyclable material, so the ultimate plan would be to split the user's "green score" which would be used to determine leaderboard placement and their redeemable points. For our AI model, we have massive room for improvement to help decrease Type I and Type II errors. We are looking into mixing different model types such as detection, segmentation, and classification to help in only analyzing the recyclable elements of a frame. Additionally, we can always train the model off of a stronger dataset to help in more niche recycling cases. 
