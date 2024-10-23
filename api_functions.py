import requests
from api_settings import *

# ? YOUTUBE API
api_key = YT_API_KEY

# ? ID ICT
channel_id = YT_CHANEL_ID

# * GET ALL VIDEOS 
def get_all_videos():
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    videos = []
    
    # ? Request params
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'maxResults': 50,
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    for item in data['items']:
        if item['id']['kind'] == 'youtube#video':
            video = {
                'id': item['id']['videoId'],
                'titulo': item['snippet']['title']
            }
            videos.append(video)
    
    return videos

# * Get video views
def get_views(video_id):
    base_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'statistics',
        'id': video_id,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        return int(data['items'][0]['statistics']['viewCount'])
    return 0

# * Get videos and the views sum for a specific team
def get_team_views_and_videos(team):
    videos = get_all_videos()
    team_videos = []
    
    for video in videos:
        # ? Verify team in titles
        if team.lower() in video['titulo'].lower():
            views = get_views(video['id'])
            team_videos.append({
                'title': video['titulo'],
                'views': views
            })
    
    return team_videos

# * Get only the views sum for a specific team
def get_team_views(team):
    videos = get_all_videos()
    team_views = 0
    
    for video in videos:
        # ? Verify team in titles
        if team.lower() in video['titulo'].lower():
            team_views += get_views(video['id'])
            
    return team_views

