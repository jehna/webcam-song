import cv2
from openai import OpenAI
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os
import base64
from pathlib import Path

dotenv.load_dotenv()

# This was very much made super quickly using ChatGPT, so don't expect much.

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Replace these with your own credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

scope = 'user-modify-playback-state user-read-currently-playing user-read-playback-state'  # Add 'playlist-modify-public' scope

def authenticate_spotify():
  # Check if cache file exists
  cache_file = Path(__file__).parent.parent / ".login-cache"
  print(cache_file)
  if not os.path.exists(cache_file):
    print("Next up we will pop up a browser window for you to log in to Spotify and authorize the app. The redirect will result in a page that's not found. Take the URL of that page and paste it here. OK?")
    input("Press Enter to open the browser...")

  return spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    cache_path=cache_file,
    show_dialog=True))

def queue_song(sp: spotipy.Spotify, song_uri):
    sp.add_to_queue(song_uri)
    print(f'Successfully queued: {song_uri}')

def play_song(sp: spotipy.Spotify, song_uri):
    sp.start_playback(uris=[song_uri])
    print(f'Successfully started playing: {song_uri}')

def capture_image() -> str:
    # Open the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture device.")
        return

    print("3...")
    time.sleep(1)  # Wait for 1 second
    print("2...")
    time.sleep(1)  # Wait for 1 second
    print("1...")
    time.sleep(1)  # Wait for 1 second
    # Read a frame from the webcam
    ret, frame = cap.read()
    print("Looks awesome!")

    cap.release()
    if ret:
        # Save the frame as an image file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"/tmp/image-{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved: {filename}")
        return filename
    else:
        raise "Error: Could not read frame."

    # Release the webcam

def get_song_name(image_path: str) -> str:
    base64_image = encode_image(image_path)
    response = openai_client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            },
            {
              "type": "text",
              "text": "Can you look at this picture and tell me what the perfect music would be for this specific mood and situation? Assume that the person is doing something at a computer if they're looking at the camera. Please answer with only the artist and the song name. No yapping."
            }
          ]
        }
      ],
      max_tokens=50,
      temperature=0.85
    )
    return response.choices[0].message.content

def currently_playing(sp: spotipy.Spotify):
    queue = sp.queue()["queue"]
    return len(queue)

def remove_image(image_path):
    os.remove(image_path)

def main():
    sp = authenticate_spotify()
    while True:
        queue_length = currently_playing(sp)
        if queue_length != 11:
          iamge_path = capture_image()
          song_name = get_song_name(iamge_path)
          print(song_name)
          song_uri = sp.search(song_name, type='track')['tracks']['items'][0]['uri']
          if queue_length == 10:
            queue_song(sp, song_uri)
          else:
             play_song(sp, song_uri)
          remove_image(iamge_path)
        time.sleep(60)

if __name__ == "__main__":
    main()
