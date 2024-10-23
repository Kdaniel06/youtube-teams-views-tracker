from fastapi import FastAPI
from api_functions import *
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Team(BaseModel):
    name: str

# * GET SINGLE TEAM VIEWS
@app.post("/single-team-views/")
def single_team_views(request: Team):
    team_name = request.name
    videos = get_team_views_and_videos(team_name)
    
    # ? Get the total views sum
    total_views = sum(video['views'] for video in videos)
    
    return {
        "team": team_name,
        "total_views": total_views,
        "videos": videos
    }

# * GET MANY TEAMS VIEWS
@app.post("/teams-views/")
def teams_views(teams: List[Team]):
    teams_views_list = []
    for team in teams:
        team_name = team.name
        views = get_team_views(team_name)
        teams_views_list.append({"team": team_name, "total_views": views}) 
    return teams_views_list
