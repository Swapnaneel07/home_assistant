# music_suggester.py
# ---
# Fetches track suggestions from TheAudioDB (Free, No Key Required).

import requests
import random 

# Base URL for TheAudioDB API
BASE_URL = "https://theaudiodb.com/api/v1/json/1" # '1' is the public demo key for all endpoints

def _search_artist(mood_keyword):
    """Searches for an artist based on the mood keyword."""
    # This endpoint searches by artist name. We'll use the keyword as the "name"
    search_url = f"{BASE_URL}/searchartist.php?s={mood_keyword}"
    
    try:
        response = requests.get(search_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Check if any artists were found
        artists = data.get('artists')
        if artists and artists[0]:
            # Use the first result's ID
            return artists[0]['idArtist']
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] TheAudioDB Artist Search failed: {e}")
    
    return None

def _get_top_track(artist_id):
    """Fetches the top track for a given Artist ID."""
    # This endpoint gets the 10 most popular tracks
    tracks_url = f"{BASE_URL}/track-top10.php?s={artist_id}"
    
    try:
        response = requests.get(tracks_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        tracks = data.get('track')
        if tracks:
            # Pick a random track from the top 10
            return random.choice(tracks)
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] TheAudioDB Track Search failed: {e}")
        
    return None


def get_track_suggestion(mood):
    """
    Suggests a track based on the detected mood using TheAudioDB.
    """
    
    # 1. Map sentiment to search terms
    if "Stressed" in mood:
        # Search terms related to soothing genres/artists
        search_query = random.choice(["Chill", "Ambient", "Jazz", "Classical"])
        mood_label = "soothing"
    elif "Happy" in mood:
        # Search terms related to energetic genres/artists
        search_query = random.choice(["Pop", "Dance", "Funk", "Rock"])
        mood_label = "energetic"
    else:
        return "I'm not sure what music to play when your mood is neutral."

    # 2. Search for a matching artist
    artist_id = _search_artist(search_query)

    if not artist_id:
        return f"I couldn't find a good artist for a {mood_label} mood. Try searching for a specific song!"

    # 3. Get a top track for the found artist
    suggested_track = _get_top_track(artist_id)

    if suggested_track:
        title = suggested_track.get('strTrack')
        artist = suggested_track.get('strArtist')
        
        return (
            f"I see you're feeling {mood_label}! I suggest the track: "
            f"'{title}' by {artist}."
        )
    else:
        return f"I found an artist for your {mood_label} mood, but no track data was available."