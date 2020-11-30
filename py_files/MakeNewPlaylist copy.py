from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
import json

api_key = os.getenv('YOUTUBE_API_KEY')
oauth_id = os.getenv('OAUTH_ID')

api_service = "youtube"
api_version = 'v3'
CLIENT_SECRET_FILE = 'C:\\Users\\xstom\\OneDrive\\Desktop\\Python Challenge\\YoutubeAPI\\client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

filepath = "DroneTricks.txt"
playlist = ""
channelid = "UC4phggZ8FpQIVJQflp2LEaQ"
playlistTitle = "Testing"


def makePlaylist(_title):
    youtube = build(api_service, api_version, credentials=credentials)

    request = youtube.playlists().insert(
        part="snippet, status",
        body={
            "snippet": {
                "title": _title},
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    print(response)


credentials = None

if os.path.exists("token.pickle"):
    print("Loading Credentials From File...")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, scopes=SCOPES)

        flow.run_local_server(port=8080, prompt="consent",
                              authorization_prompt_message="")
        credentials = flow.credentials

        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

makePlaylist(playlistTitle)
