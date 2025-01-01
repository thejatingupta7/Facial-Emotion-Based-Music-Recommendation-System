
# Music Recommendation Based on Facial Emotion Recognition
![image](https://github.com/user-attachments/assets/e94da5f7-3866-45a1-af2c-d8ed0cbbeb39)
## Overview
This project combines **Facial Emotion Recognition (FER)** and a **Music Recommendation System** to create personalized Spotify playlists based on a user's detected emotion. The system detects a user's emotion from an image or video and recommends top songs matching the user's mood.

### Key Components
1. **Facial Emotion Recognition**: Classifies a user's face into one of 7 emotions using** DeepFace's emotion model**:
   - Happy
   - Sad
   - Angry
   - Disgust
   - Surprise
   - Neutral
   - Fear

2. **Recommendation System**: Uses the user's detected mood and other options that the user can choose from to recommend songs that match the detected emotion.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/thejatingupta7/Facial-Emotion-Based-Music-Recommendation-System.git
cd Facial-Emotion-Based-Music-Recommendation-System
```

### 2. Install Dependencies
Ensure Python 3.7+ is installed and run the following:
```bash
pip install -r requirements.txt
```

### 3. Set Up Spotify API 
![image](https://github.com/user-attachments/assets/c46597b2-2bf3-4934-b293-3525eb96db4c)
1. Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
3. Note the **Client ID** and **Client Secret**.
4. Update the Spotify API credentials in `xapp.py`:
```python
# Spotify API Initialization
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
```

### 4. Run the Application
1. Run the Streamlit app `xapp.py`.
2. Make sure to be in the project terminal location.
3. Command:
```bash
streamlit run xapp.py
```


https://github.com/user-attachments/assets/e599cc0e-ddba-42a6-8ecd-4fdbcca97154


---

## Technologies Used
- **Python Libraries**: TensorFlow, Keras, OpenCV, Spotipy, Scikit-learn, Streamlit
- **Spotify API**: For retrieving song metadata and features
- **Machine Learning Techniques**: CNNs for emotion detection, classification for music mood prediction

---

## Credits
- Repository Author: [Jatin Gupta](https://github.com/thejatingupta7)

---

## License
This project is licensed under the Apache 2.0 License. See `LICENSE` for details.
