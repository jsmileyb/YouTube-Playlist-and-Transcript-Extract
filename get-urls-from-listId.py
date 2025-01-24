from googleapiclient.discovery import build
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import re

def sanitize_filename(filename):
    # Remove invalid characters from filename
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_playlist_metadata(youtube, playlist_id):
    request = youtube.playlists().list(
        part="snippet,contentDetails,status",
        id=playlist_id
    )
    response = request.execute()
    
    if not response['items']:
        raise ValueError("Playlist not found or is private")
        
    playlist = response['items'][0]
    return {
        "playlist_id": playlist_id,
        "title": playlist['snippet']['title'],
        "description": playlist['snippet']['description'],
        "channel_title": playlist['snippet']['channelTitle'],
        "channel_id": playlist['snippet']['channelId'],
        "published_at": playlist['snippet']['publishedAt'],
        "video_count": playlist['contentDetails']['itemCount'],
        "privacy_status": playlist['status']['privacyStatus'],
        "extracted_at": datetime.now().isoformat()
    }

def get_playlist_videos(youtube, playlist_id):
    video_data = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_title = item["snippet"]["title"]
            video_description = item["snippet"]["description"]
            video_data.append({
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "video_id": video_id,
                "title": video_title,
                "description": video_description,
                "position": item["snippet"]["position"],
                "published_at": item["snippet"]["publishedAt"]
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_data

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data saved to {output_file}")

def get_playlist_id():
    print("\n=== YouTube Playlist Data Extractor ===")
    playlist_ids = os.getenv("YOUTUBE_PLAYLIST_IDS")
    if not playlist_ids:
        print("Error: YOUTUBE_PLAYLIST_IDS not found in .env file")
        exit(1)
    
    # Split the comma-separated string into a list and clean whitespace
    playlist_ids = [pid.strip() for pid in playlist_ids.split(',')]
    
    # Handle if IDs are full URLs instead of just IDs
    cleaned_ids = []
    for pid in playlist_ids:
        if "youtube.com" in pid:
            pid = pid.split("list=")[-1].split("&")[0]
        cleaned_ids.append(pid)
    
    return cleaned_ids

# Example usage
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    API_KEY = os.getenv("YOUTUBE_API_KEY")
    
    if not API_KEY:
        print("Error: YouTube API key not found in .env file")
        exit(1)

    playlist_ids = get_playlist_id()
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    # Create a list to store all playlist data
    all_playlists_data = []
    
    for playlist_id in playlist_ids:
        try:
            # Get playlist metadata first
            playlist_metadata = get_playlist_metadata(youtube, playlist_id)
            
            # Get video data
            video_data = get_playlist_videos(youtube, playlist_id)
            
            # Combine metadata and video data
            playlist_data = {
                "playlist_metadata": playlist_metadata,
                "videos": video_data
            }
            
            all_playlists_data.append(playlist_data)
            
            print(f"\nSuccessfully extracted data for {len(video_data)} videos!")
            print(f"Playlist: {playlist_metadata['title']}")
            print(f"Channel: {playlist_metadata['channel_title']}")
            
        except Exception as e:
            print(f"\nError processing playlist {playlist_id}: {str(e)}")
            print("Continuing with next playlist...")
    
    # Create single output file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"exports/playlist-metadata/{timestamp}_all_playlists.json"
    
    # Ensure directory exists
    os.makedirs("exports/playlist-metadata", exist_ok=True)
    
    # Save all data to single file
    save_to_json(all_playlists_data, output_file)
    print(f"\nAll playlist data saved to {output_file}")

