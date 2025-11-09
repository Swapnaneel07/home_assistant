# music_suggester.py
# ---
# Fetches track suggestions from TheAudioDB (Free Key '123').

import requests
import random 
# Needed for getting the TRIGGER_WORD if we reuse it

# --- CORRECTED BASE URL SETUP ---
# Use the V1 Base URL + the free test key (123)
API_KEY_FREE = "123"
BASE_URL = f"https://www.theaudiodb.com/api/v1/json/{API_KEY_FREE}" 
# Example URL structure: https://www.theaudiodb.com/api/v1/json/123/searchartist.php?s=Coldplay
# -----------------------------------


def _search_artist(mood_keyword):
    """
    Searches for an artist based on the mood keyword using the 'search.php' endpoint,
    which is an alias for artist search.
    
    The free API is limited, so we search the entire database.
    """
    
    # Endpoint to search by artist name. We use 'search.php' as per documentation example.
    search_url = f"{BASE_URL}/search.php?s={mood_keyword}"
    
    try:
        response = requests.get(search_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # The result structure is artists:[{...}]
        artists = data.get('artists')
        if artists and artists[0]:
            # Return the Artist ID (idArtist) from the first result
            return artists[0]['idArtist']
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] TheAudioDB Artist Search failed (URL: {search_url}): {e}")
    
    return None

def _get_top_track(artist_id):
    """Fetches the top track for a given Artist ID."""
    tracks_url = f"{BASE_URL}/track-top10.php?i={artist_id}"
    
    try:
        response = requests.get(tracks_url, timeout=5)
        response.raise_for_status()
        
        # --- NEW JSON ERROR HANDLING ---
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"[ERROR] TheAudioDB Track Search failed to decode JSON (ID: {artist_id}): API returned non-JSON data.")
            return None
        # -------------------------------
        
        tracks = data.get('track')
        if tracks:
            return random.choice(tracks)
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] TheAudioDB Track Search failed (URL: {tracks_url}): {e}")
        
    return None


def get_track_suggestion(mood):
    """
    Suggests a track based on the detected mood using TheAudioDB.
    """
    
    # 1. Map sentiment to search terms
    if "Stressed" in mood:
        search_query = random.choice(["Jazz", "Chill", "Ambient", "Moby", "Enya"])
        mood_label = "soothing"
    elif "Happy" in mood:
        search_query = random.choice(["Pop", "Dance Music", "Funk", "Queen", "Bruno Mars"])
        mood_label = "energetic"
    else:
        return "I'm not sure what music to play when your mood is neutral."

    # 2. Search for a matching artist to get the ID
    artist_id = _search_artist(search_query)

    if not artist_id:
        return f"I couldn't find a good artist for a {mood_label} mood using the search term '{search_query}'. Try a more specific command."

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
        return f"I found the artist {artist_id} but no top track data was available for that mood."
    
