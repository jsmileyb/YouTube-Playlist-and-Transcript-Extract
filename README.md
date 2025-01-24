# YouTube Playlist & Transcript Extractor

This project provides tools to extract metadata and transcripts from YouTube playlists and videos using the YouTube Data API and the YouTube Transcript API. It saves the extracted data in JSON format for further use, such as analysis, reporting, or archiving.

---

## Features

- Extracts metadata for YouTube playlists and their videos, including:
  - Playlist title, description, and channel details
  - Video titles, descriptions, publication dates, and URLs
- Retrieves video transcripts (if available) in English.
- Saves extracted data as JSON files in organized folders.
- Handles multiple playlists through a `.env` configuration.

---

## Project Structure

```
/
├── exports/
│   ├── playlist-metadata/
│   │   ├── [timestamp]_all_playlists.json
│   └── transcripts/
│       ├── [timestamp]_transcripts_metadata.json
├── .env.example
├── get-urls-from-listId.py
├── get-youTube-transcripts.py
├── LICENSE
└── requirements.txt
```

---

## Prerequisites

1. **Python 3.8+**: Ensure Python is installed.
2. **YouTube API Key**: Create an API key from the [Google Developer Console](https://console.cloud.google.com/).
3. **Environment File (`.env`)**:
   - Copy `.env.example` to `.env` and populate it with your YouTube API key and playlist IDs:
     ```ini
     YOUTUBE_API_KEY=your_api_key_here
     YOUTUBE_PLAYLIST_IDS=playlist_id1,playlist_id2
     ```

---

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `exports/playlist-metadata` and `exports/transcripts` directories exist:
   ```bash
   mkdir -p exports/playlist-metadata exports/transcripts
   ```

---

## Usage

### 1. Extract Playlist Data

Run `get-urls-from-listId.py` to extract metadata and video URLs from YouTube playlists:

```bash
python get-urls-from-listId.py
```

### 2. Fetch Video Transcripts

Use `get-youTube-transcripts.py` to download transcripts and additional metadata for videos in the playlists:

```bash
python get-youTube-transcripts.py
```

### Output

- **Playlist Metadata**: Saved in `exports/playlist-metadata/`.
- **Video Transcripts**: Saved in `exports/transcripts/`.

---

## Error Handling

- If a playlist is private or invalid, it will be skipped, and an error message will be displayed.
- Videos without transcripts will still have metadata saved.

---

## Requirements

- **Python Libraries**:
  - `defusedxml`
  - `google-api-python-client`
  - `python-dotenv`
  - `pytube`
  - `requests`
  - `youtube_transcript_api`

Install them using:

```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Future Enhancements

- Support for multiple transcript languages.
- Improved error handling for API rate limits.
- Integration with cloud storage for storing large datasets.

---

## Contributing

Feel free to fork the repository and submit pull requests for improvements or new features.

---

## Author

Developed by Josh S. Baltz. For inquiries, please contact jsbaltz@outlook.com.
