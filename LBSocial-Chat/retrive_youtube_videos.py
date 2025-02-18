from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

# YouTube API setup
google_api_key = get_secret('google')['api_key']
youtube = build("youtube", "v3", developerKey=google_api_key)


def get_video_captions(video_id):
    try:
        captions = YouTubeTranscriptApi.get_transcript(video_id)
        return captions
    except Exception as e:
        print (e)
        return "No captions available"

def get_playlist_videos(playlist_id):
    videos = []
    next_page_token = None
    
    while True:
        playlist_items = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        for item in playlist_items["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            captions = get_video_captions(video_id)
            videos.append({
                "title": title,
                "url": url,
                "video_id": video_id,
                "captions": captions
            })
        
        next_page_token = playlist_items.get("nextPageToken")
        if not next_page_token:
            break
    
    return videos
