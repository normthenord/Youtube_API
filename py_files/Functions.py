from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
import json

api_service = "youtube"
api_version = 'v3'
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def getAPI():
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

    return build(api_service, api_version, credentials=credentials)


def getPlaylistVideoIds(_api):

    request = _api.playlistItems().list(
        playlistId='PLPSSZSQLOk1ruB4Htohv1HMhhab-N2XfI', part='contentDetails', maxResults=100)
    response = request.execute()

    videoList = []

    for item in response['items']:
        videoList.append(item['contentDetails']['videoId'])

    return videoList


def getPlaylistLength(_api, _videoList):
    request = _api.videos().list(id=_videoList, part='contentDetails')

    response = request.execute()
    videoLengthList = []
    for item in response['items']:
        videoLengthList.append(item['contentDetails']['duration'])

    totalTime = {'hours': 0, 'minutes': 0, 'seconds': 0}

    for item in videoLengthList:
        item = item[2:]
        currentNumber = ''
        for c in item:
            if c.isnumeric():
                currentNumber += c
            else:
                if c == 'H':
                    totalTime['hours'] += int(currentNumber)
                    currentNumber = ''
                if c == 'M':
                    totalTime['minutes'] += int(currentNumber)
                    currentNumber = ''
                if c == 'S':
                    totalTime['seconds'] += int(currentNumber)
                    currentNumber = ''

    totalTime['minutes'] += int(totalTime['seconds'] / 60)
    totalTime['seconds'] = totalTime['seconds'] % 60
    totalTime['hours'] += int(totalTime['minutes'] / 60)
    totalTime['minutes'] = totalTime['minutes'] % 60
    print(totalTime)


api = getAPI()
videoList = getPlaylistVideoIds(api)
getPlaylistLength(api, videoList)
