import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import cv2
from deepface import DeepFace

# Spotify API credentials
SPOTIFY_CLIENT_ID = ""  # Replace with your Spotify client ID
SPOTIFY_CLIENT_SECRET = ""  # Replace with your Spotify client secret

# Initialize Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# Load OpenCV's Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to get songs by mood using Spotify API
def get_songs_by_mood(mood):
    try:
        results = sp.search(q=mood, type="track", limit=50)
        songs = []
        for item in results['tracks']['items']:
            song = {
                'name': item['name'],
                'artist': ", ".join(artist['name'] for artist in item['artists']),
                'album_image_url': item['album']['images'][0]['url'] if item['album']['images'] else None,
                'spotify_url': item['external_urls']['spotify'] if 'external_urls' in item else None
            }
            songs.append(song)
        return songs
    except Exception as e:
        st.error(f"Error fetching songs: {e}")
        return []

# Function to get albums by mood using Spotify API
def get_albums_by_mood(mood):
    try:
        results = sp.search(q=mood, type="album", limit=50)
        albums = []
        for item in results['albums']['items']:
            album = {
                'name': item['name'],
                'artist': ", ".join(artist['name'] for artist in item['artists']),
                'image_url': item['images'][0]['url'] if item['images'] else None,
                'spotify_url': item['external_urls']['spotify'] if 'external_urls' in item else None
            }
            albums.append(album)
        return albums
    except Exception as e:
        st.error(f"Error fetching albums: {e}")
        return []

# Function to search for songs using Spotify API
def search_songs(query):
    try:
        results = sp.search(q=query, type="track", limit=50)
        songs = []
        for item in results['tracks']['items']:
            song = {
                'name': item['name'],
                'artist': ", ".join(artist['name'] for artist in item['artists']),
                'album_image_url': item['album']['images'][0]['url'] if item['album']['images'] else None,
                'spotify_url': item['external_urls']['spotify'] if 'external_urls' in item else None
            }
            songs.append(song)
        return songs
    except Exception as e:
        st.error(f"Error fetching songs: {e}")
        return []

# Function to detect mood using webcam and DeepFace
def detect_mood():
    cap = cv2.VideoCapture(0)
    st.text("Starting webcam for mood detection. Please wait...")
    mood = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture frame. Exiting...")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = rgb_frame[y:y + h, x:x + w]
            try:
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                mood = result[0]['dominant_emotion']
                break
            except Exception as e:
                st.error(f"Error analyzing emotion: {e}")
                mood = ""

        if mood:
            break

    cap.release()
    cv2.destroyAllWindows()
    return mood

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    st.title("Mood-Based Song Recommendation")

    # Sidebar
    with st.sidebar:
        st.header("Options")

        # Search bar
        search_query = st.text_input("Search for a song:")

        mood = "Calm"
        # Mood detection button
        if st.button("Detect Mood via Webcam"):
            detected_mood = detect_mood()
            if detected_mood:
                st.success(f"Detected Mood: {detected_mood}")
                mood = detected_mood
            else:
                st.warning("Could not detect mood. Please try again.")
                

        # Song or Album selection
        option = st.radio("What would you like to explore?", ["Songs", "Albums"])

        # Region selection
        region = st.text_input("Enter a region (e.g., US, UK, IN):", value="US")

        # Language selection
        language = st.text_input("Enter a language (e.g., English, Spanish, Hindi):", value="English")

        # Culture options (dummy for now)
        culture = st.selectbox("Choose a culture:", ["Western", "Asian", "African", "Latin", "Middle Eastern"])

    # Main content
    if search_query:
        st.subheader(f"Search Results for: {search_query}")
        items = search_songs(search_query)
    else:
        st.subheader(f"{option} for the Mood: {mood}")
        if option == "Songs":
            items = get_songs_by_mood(mood)
        elif option == "Albums":
            items = get_albums_by_mood(mood)
        else:
            items = []

    # Display the songs or albums in a scrollable grid
    if items:
        cols_per_row = 5  # Number of columns per row
        rows = -(-len(items) // cols_per_row)  # Calculate the number of rows needed

        for row in range(rows):
            cols = st.columns(cols_per_row)
            for col_index in range(cols_per_row):
                item_index = row * cols_per_row + col_index
                if item_index < len(items):
                    item = items[item_index]

                    with cols[col_index]:
                        try:
                            if item.get('album_image_url') or item.get('image_url'):
                                image_url = item.get('album_image_url') or item.get('image_url')
                                st.markdown(f'<a href="{item["spotify_url"]}" target="_blank"><img src="{image_url}" width="100%"></a>', unsafe_allow_html=True)
                        except Exception as e:
                            # Display default image with the same URL redirect as the album
                            st.markdown(f'<a href="{item["spotify_url"]}" target="_blank"><img src="img.png" width="100%"></a>', unsafe_allow_html=True)
                        st.write(f"**{item['name']}**")
                        if 'artist' in item:
                            st.write(f"{item['artist']}")
    else:
        st.warning("No results found.")

if __name__ == "__main__":
    main()
