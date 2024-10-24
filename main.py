from fastapi import FastAPI
from api_functions import *
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Team(BaseModel):
    name: str

class Matchday(BaseModel):
    matchday: int

# TODO it works but has to be tested when YT update the videos 
# * GET VIEWS BY MATCHDAY (including announcements, statistics, and matches)
@app.post("/api/matchday-views/")
def matchday_views(request: Matchday):
    matchday_num = request.matchday
    videos = get_all_videos()

    total_views = 0
    matchday_videos = []

    # ? Filter videos related to the specified matchday
    for video in videos:
        title = video['titulo'].lower()
        if f"jornada {matchday_num}" in title:
            views = get_views(video['id'])
            total_views += views
            matchday_videos.append({"title": video['titulo'], "views": views})

    return {
        "matchday": matchday_num,
        "total_views": total_views,
        "videos": matchday_videos
    }

# TODO it works but has to be tested when YT update the videos
# * GET MOST VIEWED matchday
@app.get("/api/most-viewed-matchday/")
def most_viewed_matchday():
    videos = get_all_videos()

    matchdays_views = {}

    # ? Group videos by matchday and sum their views
    for video in videos:
        title = video['titulo'].lower()
        if "jornada" in title:
            for i in range(1, 9):  # Assuming max 8 matchdays
                if f"jornada {i}" in title:
                    views = get_views(video['id'])
                    matchdays_views[i] = matchdays_views.get(i, 0) + views

    # ? Find the matchday with the highest total views
    most_viewed_matchday = max(matchdays_views, key=matchdays_views.get)

    return {
        "matchday": most_viewed_matchday,
        "total_views": matchdays_views[most_viewed_matchday]
    }

# TODO it works but has to be tested when YT update the videos
# * GET MOST VIEWED MATCH
@app.get("/api/most-viewed-match/")
def most_viewed_match():
    videos = get_all_videos()
    max_views = 0
    most_viewed_match = {}

    # ? Find the match with the most views
    for video in videos:
        title = video['titulo'].lower()
        if "resumen | " in title:
            views = get_views(video['id'])
            if views > max_views:
                max_views = views
                most_viewed_match = {"title": video['titulo'], "views": views}

    return most_viewed_match

# * GET SINGLE TEAM VIEWS
@app.post("/api/single-team-views/")
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
@app.post("/api/teams-views/")
def teams_views(teams: List[Team]):
    teams_views_list = []
    for team in teams:
        team_name = team.name
        views = get_team_views(team_name)
        teams_views_list.append({"team": team_name, "total_views": views}) 
    return teams_views_list

# * GET FUTCREW 1st Edition TEAMS
@app.get("/api/first-edition-teams/")
def get_first_edition_teams():

    teams = [
        {"name": "Imperial crew"},
        {"name": "San Francisco Academia"},
        {"name": "Invu FC"},
        {"name": "Cedros Crew"},
        {"name": "Aston Rios PC"},
        {"name": "Barcola"},
        {"name": "Wolf"},
        {"name": "Vodka Juniors"},
        {"name": "CD Monte S"},
        {"name": "La Union FC"}
    ]


    return teams


# TODO Implements the GET TEAMS FOR EDITION in future editions
'''
# * GET FUTCREW 1st Edition TEAMS
@app.get("/teams-per-edition/")
def get_first_ediction_teams(edition: int):
    videos = get_all_videos()

    teams = []

    # ? Search the introduction video and get the teams
    for video in videos:
        title = video['titulo'].lower()
        description = video['description']
        if f"video introductorio de torneo futcrew {edition}" in title:
            for line in description.split('\n'):
                print(f"Desc line: {line}")
                if line.startswith('-'):
                    teams.append({"name": line.strip().replace('- ', '')})

    return teams
'''