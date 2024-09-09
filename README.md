# FaceID
Face Recognition Attendance System is a Python-based facial recognition system using OpenCV for detection and face_recognition for recognition, with a Telegram bot for data management and IT support.

## Project Overview
This project aims to develop a program that tracks employee attendance by recording entry times and dates using facial recognition technology.

- Employees can register their data (face image and name) through a Telegram bot.
- The system includes an alert mechanism in case an unauthorized person attempts entry.
- Notifications are sent to the manager when an unauthorized access attempt occurs.
- All data is stored in a CSV file in an organized and structured format for easy access and management.
- Upon user registration via the bot, their image is stored locally, the model is trained on the new data, and a confirmation notification is sent.

## Libraries and Requirements
- OpenCV
- face-recognition library
- scikit-learn
- pyTelegramBotAPI (requires an access key to activate the bot)

## Folders
- train_dir: Contains subfolders for each employee with their training images.
- model: Stores pre-trained model weights.
- Known_people: Contains images of known people. The program captures a photo every 10 frames when it detects a face.
- unknown_people: Stores images of unknown people, captured every 10 frames when a face is detected.
- Cash_vid: Contains 2-second videos used to register a new employee via the bot.
- Cash_telephoto: Contains cached photos extracted from the videos.
- Cash_photo: Stores cached photos captured every 10 frames.

## Scripts
- train.py: Trains the model using the user images dataset.
- split_video.py: Slices the video received from the Telegram bot to register employees in the database.
- test_recognizer.py: Tests the model's prediction accuracy.
- telebot_faceID.py: Handles the Telegram bot for new employee registration.
- attendance.py: Saves data in the attendance sheet.
- recognizer.py: Main program to verify the identity of incoming employees.
