from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# Function to fetch video metadata using YouTube Data API
def fetch_video_metadata(api_key, video_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    try:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        if not response["items"]:
            print(f"No metadata found for video ID: {video_id}")
            return None

        video_info = response["items"][0]
        metadata = {
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "title": video_info["snippet"]["title"],
            "channel": video_info["snippet"]["channelTitle"],
            "upload_date": video_info["snippet"]["publishedAt"],
            "description": video_info["snippet"]["description"],
            "duration": video_info["contentDetails"]["duration"],
            "views": video_info["statistics"].get("viewCount", "N/A"),
            "likes": video_info["statistics"].get("likeCount", "N/A"),
        }
        return metadata
    except Exception as e:
        print(f"Error fetching metadata for video ID {video_id}: {e}")
        return None

# Function to download transcripts and metadata
def download_transcripts(video_urls, output_file, api_key):
    extracted_data = []
    total_videos = len(video_urls)
    
    print(f"\nStarting to process {total_videos} videos...")
    
    for index, url in enumerate(video_urls, 1):
        try:
            video_id = url.split("v=")[1]
            print(f"\nProcessing video {index}/{total_videos}: {url}")
            
            metadata = fetch_video_metadata(api_key, video_id)
            if metadata:
                print(f"✓ Metadata retrieved for: {metadata['title']}")
                
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
                metadata["transcript"] = transcript
                metadata["extraction_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                extracted_data.append(metadata)
                print("✓ Transcript downloaded successfully")
            
            # Calculate and display progress percentage
            progress = (index / total_videos) * 100
            print(f"Progress: {progress:.1f}% ({index}/{total_videos} videos processed)")
            
        except Exception as e:
            print(f"✗ Error processing {url}: {e}")
            print(f"Progress: {(index / total_videos) * 100:.1f}% ({index}/{total_videos} videos processed)")

    # Save as JSON
    print("\nSaving data to file...")
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(extracted_data, file, indent=4, ensure_ascii=False)
    print(f"✓ Data saved to {output_file}")
    print(f"✓ Successfully processed {len(extracted_data)} out of {total_videos} videos")

def get_latest_playlist_file():
    playlist_dir = "exports/playlist-metadata"
    if not os.path.exists(playlist_dir):
        raise FileNotFoundError(f"Directory {playlist_dir} not found")
    
    # Get all json files in the directory
    json_files = [f for f in os.listdir(playlist_dir) if f.endswith('.json')]
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {playlist_dir}")
    
    # Get the most recent file
    latest_file = max([os.path.join(playlist_dir, f) for f in json_files], key=os.path.getmtime)
    return latest_file

def extract_video_urls_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    video_urls = []
    for playlist in data:
        for video in playlist['videos']:
            video_urls.append(video['url'])
    
    return video_urls

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variable
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables")

    try:
        # Get latest playlist file and extract URLs
        latest_file = get_latest_playlist_file()
        video_urls = extract_video_urls_from_json(latest_file)
        print(f"Found {len(video_urls)} videos to process from {latest_file}")

        # Generate a timestamped output file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"exports/transcripts/{timestamp}_transcripts_metadata.json"
        
        # Ensure directory exists
        os.makedirs("exports/transcripts", exist_ok=True)

        # Fetch transcripts and save data
        download_transcripts(video_urls, output_file, API_KEY)
    except Exception as e:
        print(f"Error: {str(e)}")
