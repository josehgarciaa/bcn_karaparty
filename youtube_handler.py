import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import re
from googleapiclient.errors import HttpError


class YouTubeManager:
    """A class for handling YouTube URLs, validating them, and extracting video IDs."""

    
    def __init__(self, client_secrets_file):
        """Initialize the YouTubeHandler class with YouTube URL patterns."""    
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = client_secrets_file
        self.youtube = self.initialize_youtube_client()

        #Patterns to decided whereas links are valid or not
        self.patterns = [
            r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^\s&?]{11})',
            r'(?:https?:\/\/)?(?:m\.)?(youtube\.com\/watch\?v=)([^\s&?]{11})'
        ]        


    def initialize_youtube_client(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials)
        
        return youtube

    def is_valid_youtube_link(self, url):
        """Check if the URL is a valid YouTube video link.
        
        Args:
            url (str): The URL to check.
        
        Returns:
            bool: True if the URL is a valid YouTube link, False otherwise.
        """
        for pattern in self.patterns:
            if re.search(pattern, url):
                return True
        return False

    def extract_video_id(self, url):
        """Extract and return the YouTube video ID from the URL.
        
        Args:
            url (str): The YouTube URL from which to extract the video ID.
        
        Returns:
            str or None: The extracted video ID if the URL is valid, otherwise None.
        """
        for pattern in self.patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def add_video_to_playlist(self, video_url, playlist_id):
       
        if self.is_valid_youtube_link(video_url):
            request_body = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': self.extract_video_id(video_url)
                    },
                    'position': 0  # Optional, specifies the position in the playlist.
                    }
                }

            request = self.youtube.playlistItems().insert(
                part="snippet",
                body=request_body
            )
            response = request.execute()
            print(f"Added video to playlist: {response}")
            return response


    def remove_all_videos_from_playlist(self, playlist_id):
        try:
            # Retrieve playlist items
            next_page_token = ''
            while next_page_token is not None:
                playlist_items_response = self.youtube.playlistItems().list(
                    part='id',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                # Delete each item
                for item in playlist_items_response['items']:
                    self.youtube.playlistItems().delete(id=item['id']).execute()

                next_page_token = playlist_items_response.get('nextPageToken')
            
            print("All videos have been removed from the playlist.")
        
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
