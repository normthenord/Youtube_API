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

playlist = "UU3LRlyWVfA3RTKDS_Ryf-4w"

filepath = "..\\txt_files\\BurningSkull.txt"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()

youtube = build(api_service, api_version, credentials=credentials)


arr = open("BurningSkull.txt", 'r')

txt = arr.read().split("\n")

for i in range(len(txt)):
    try:
        request = youtube.videos().rate(
            id=txt[i],
            rating="like"
        )
        request.execute()
    except:
        print("can't")


# request = youtube.playlistItems().list(
#     playlistId = playlist,
#     part="snippet",
#     maxResults = 50)
# response = request.execute()

# nextPageToken = response["nextPageToken"]

# txtfile = open(filepath, 'w')
# for i in range(len(response['items'])):
#         txtfile.write(json.dumps(response["items"][i]["snippet"]["resourceId"]['videoId']) + ",\n")


# for x in range (0,4):
#     request = youtube.playlistItems().list(
#         playlistId = playlist,
#         pageToken = nextPageToken,
#         part="snippet",
#         maxResults = 50)
#     response = request.execute()
#     nextPageToken = response["nextPageToken"]

#     for i in range(len(response['items'])):
#         txtfile.write(json.dumps(response["items"][i]["snippet"]["resourceId"]['videoId']) + ",\n")


# txtfile.close()
# try:
#     print (response['items'][0]['statistics']['subscriberCount'])
# except:
#     print("failure")
