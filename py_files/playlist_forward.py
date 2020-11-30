from googleapiclient.discovery import build
import json
import os

playlistarr = []

filepath = "C:/Users/xstom/OneDrive/Desktop/Python Challenge/videoListBen.txt"

api_key = os.getenv('YOUTUBE_API_KEY')
oauth_id = os.getenv('OAUTH_ID')

api_service = "youtube"
api_version = 'v3'

youtube = build(api_service, api_version, developerKey=api_key)

request = youtube.playlistItems().list(
    playlistId="PLTl3hocai-cpn7fcgUPFnvAMaLFKoYAc2",
    part="snippet",
    maxResults=50)

response = request.execute()

try:
    for i in range(len(response["items"])):
        playlistarr.append(json.dumps(
            response["items"][i]['snippet']['resourceId']['videoId'], indent=4, sort_keys=True))
except:
    print("failure")


txtfile = open(filepath, 'w')
for i in range(len(playlistarr)):
    playlistarr[i] = playlistarr[i].replace('"', "")
    txtfile.write(playlistarr[i] + ",\n")
txtfile.close()
