import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import random
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser  # This will open the song in Spotify or a web browser

# Updated Playlists for Indian Moods
playlists = {
    "Happy": [
        "Tum Hi Ho by Arijit Singh",
        "Dil Dhadakne Do by Priyanka Chopra",
        "Gallan Goodiyan by Shankar-Ehsaan-Loy",
        "Tamma Tamma Again by Bappi Lahiri",
        "Kar Gayi Chull by Badshah",
    ],
    "Sad": [
        "Channa Mereya by Arijit Singh",
        "Agar Tum Saath Ho by Alka Yagnik & Arijit Singh",
        "Tujhe Kitna Chahne Lage by Arijit Singh",
        "Jeene Laga Hoon by Atif Aslam",
        "Tum Jo Aaye by Rahat Fateh Ali Khan",
    ],
    "Neutral": [
        "Pehli Nazar Mein by Atif Aslam",
        "Shape of You (Indian Remix) by Ed Sheeran",
        "Raabta by Arijit Singh",
        "Phoolon Ka Taron Ka by Kishore Kumar",
        "Ae Mere Humsafar by Alka Yagnik & Udit Narayan",
    ],
    "Angry": [
        "Nashe Si Chadh Gayi by Arijit Singh",
        "Jab Tak Hai Jaan by Javed Ali",
        "Munni Badnam Hui by Mamta Sharma",
        "Dilliwali Girlfriend by Arijit Singh",
        "Chalti Hai Kya 9 Se 12 by Neha Kakkar",
    ],
    "Surprise": [
        "Swag Se Swagat by Vishal Dadlani & Neha Bhasin",
        "London Thumakda by Labh Janjua",
        "Badtameez Dil by Benny Dayal & Shefali Alvares",
        "Dil Dhadakne Do by Priyanka Chopra & Farhan Akhtar",
        "Nashe Mein by Udit Narayan & Sadhana Sargam",
    ],
}

# Spotify API setup (replace with your actual credentials)
client_id = "bfd2cd4330324a0893be5fa98f4579d1"  # Replace with your Client ID
client_secret = "21671da3d8474619aebec0179d9270fe"  # Replace with your Client Secret

# Authenticate using the client credentials flow
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to search for songs based on a query (mood or keyword)
def search_spotify(query):
    results = sp.search(q=query, type='track', limit=5)  # Limit to 5 results
    if not results['tracks']['items']:  # Check if no songs were found
        return [f"No songs found for '{query}'"]
    
    songs = []
    for track in results['tracks']['items']:
        song_url = track['external_urls']['spotify']
        song_name = track['name'] + " by " + track['artists'][0]['name']
        songs.append((song_name, song_url))
    
    return songs

# Function to get songs based on mood
def get_songs_for_mood(mood):
    mood_keywords = {
        "Happy": "upbeat",
        "Sad": "melancholy",
        "Neutral": "chill",
        "Angry": "rock",
        "Surprise": "unexpected"
    }
    
    query = mood_keywords.get(mood, "neutral")  # Default to "neutral" if mood is not recognized
    return search_spotify(query)

# Function to open a song URL in a web browser (Spotify or Spotify client)
def play_song_on_spotify(song_url):
    webbrowser.open(song_url)

# Function to display playlist and play music
def display_playlist(mood, playlist):
    result_window = tk.Toplevel(root)
    result_window.title(f"Playlist for {mood}")
    result_window.geometry("500x500")
    result_window.configure(bg='#282828')  # Dark background for better contrast

    tk.Label(result_window, text=f"Detected Mood: {mood}", font=("Arial", 18, "bold"), fg="#1DB954", bg="#282828").pack(pady=10)
    tk.Label(result_window, text="Generated Playlist:", font=("Arial", 14), fg="#1DB954", bg="#282828").pack(pady=5)

    # Scrollable frame for the playlist
    canvas = tk.Canvas(result_window)
    scrollbar = tk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg="#282828")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollbar.pack(side="right", fill="y")
    canvas.pack(padx=10, pady=10, fill="both", expand=True)

    for song, url in playlist:
        song_button = tk.Button(scrollable_frame, text=song, font=("Arial", 12), fg="#ffffff", bg="#1DB954", width=40, height=2, bd=0,
                                relief="flat", command=lambda u=url: play_song_on_spotify(u))
        song_button.pack(pady=5)
        song_button.bind("<Enter>", lambda e: e.widget.config(bg="#1ed760"))  # Change color on hover
        song_button.bind("<Leave>", lambda e: e.widget.config(bg="#1DB954"))  # Reset color on hover leave

    tk.Button(result_window, text="Close", font=("Arial", 14), fg="#ffffff", bg="#FF0000", command=result_window.destroy).pack(pady=10)

# Main GUI Window
root = tk.Tk()
root.title("Mood-Based Music Playlist Generator")
root.geometry("500x600")
root.configure(bg='#121212')

# Title Label with background
title_font = tkfont.Font(family='Helvetica', size=20, weight="bold")
tk.Label(root, text="Mood-Based Music Playlist Generator", font=title_font, fg="#1DB954", bg='#121212').pack(pady=20)

# Instruction Label
tk.Label(root, text="Select your mood to generate a playlist:", font=("Arial", 14), fg="#ffffff", bg='#121212').pack(pady=10)

# Mood Buttons with hover effects
moods = ["Happy", "Sad", "Neutral", "Angry", "Surprise"]
for mood in moods:
    mood_button = tk.Button(root, text=mood, font=("Arial", 14), width=20, height=2, fg="#ffffff", bg="#1DB954", relief="flat",
                            command=lambda m=mood: display_playlist(m, get_songs_for_mood(m)))
    mood_button.pack(pady=10)
    mood_button.bind("<Enter>", lambda e: e.widget.config(bg="#1ed760"))  # Change color on hover
    mood_button.bind("<Leave>", lambda e: e.widget.config(bg="#1DB954"))  # Reset color on hover leave

# Run the GUI
root.mainloop()
