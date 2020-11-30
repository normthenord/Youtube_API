from googleapiclient.discovery import build
import os

api_key = os.getenv('YOUTUBE_API_KEY')
oauth_id = os.getenv('OAUTH_ID')

api_service = "youtube"
api_version = 'v3'

youtube = build(api_service, api_version, developerKey=api_key)
request = youtube.channels().list(id="UCQ-W1KE9EYfdxhL6S4twUNw", part="statistics")
response = request.execute()
try:
    print(response['items'][0]['statistics']['subscriberCount'])
except:
    print("failure")
