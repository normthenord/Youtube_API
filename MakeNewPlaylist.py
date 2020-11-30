from googleapiclient.discovery import build
import os
import google_auth_oauthlib.flow
import json

api_key = os.getenv('YOUTUBE_API_KEY')
oauth_id = os.getenv('OAUTH_ID')

api_service = "youtube"
api_version = 'v3'
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

filepath = "DroneTricks.txt"
playlist = ""
channelid = "UC4phggZ8FpQIVJQflp2LEaQ"
playlistTitle = "Test"


def deletePlaylist():
    playlist_tmp = ""
    youtube = build(api_service, api_version, credentials=credentials)
    request = youtube.playlists().list(
        part="snippet",
        channelId=channelid,
        maxResults=25
    )
    response = request.execute()
    for i in range(len(response["items"])):
        if(json.dumps(response["items"][i]["snippet"]["title"]) == f'"{playlistTitle}"'):
            playlist_tmp = json.dumps(response["items"][i]["id"])
    playlist_tmp = playlist_tmp.replace('"', "")

    try:
        request = youtube.playlists().delete(id=playlist_tmp)
        request.execute()
    except:
        print("playlist doesn't exist")


def makePlaylist(title):
    youtube = build(api_service, api_version, credentials=credentials)

    request = youtube.playlists().insert(
        part="snippet, status",
        body={
            "snippet": {
                "title": title},
            "status": {
                "privacyStatus": "public"
            }
        }
    )

    response = request.execute()

    x = json.dumps(response["id"])
    x = x.replace('"', "")

    return x


def addVideosToPlaylist(playlistID, _videoArr):
    youtube = build(api_service, api_version, credentials=credentials)

    for video in _videoArr:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlistID,
                    "resourceId": {
                        "videoId": video,
                        "kind": "youtube#video"
                    }
                }
            }
        )
        request.execute()


flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()

youtube = build(api_service, api_version, credentials=credentials)


txt = open(filepath, 'r')
videosArr = txt.read().split(",\n")
videosArr.pop(-1)
txt.close()

deletePlaylist()
playlist = makePlaylist(playlistTitle)
addVideosToPlaylist(playlist, videosArr)
