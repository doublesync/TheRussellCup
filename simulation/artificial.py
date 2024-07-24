# Python imports
import os

# Django imports
from django.core.cache import cache

# Local imports
import simulation.config as config
from stats.models import Season, Game, TeamGameStats, PlayerGameStats

# Third party imports
from openai import OpenAI
from dotenv import load_dotenv

# Load secrets from .env file or production environment
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def prompt_storylines():

    # Initialize the prompts list & other data points
    prompts = []
    week = config.CONFIG_SEASON["GAME_WEEK"]
    season = Season.objects.get(season=config.CONFIG_SEASON["CURRENT_SEASON"])
    games = Game.objects.filter(season=season, week=week)

    # Check if the season & week are in the cache already
    if cache.get(f"storylines_{season}_{week}"):
        return cache.get(f"storylines_{season}_{week}")
    else:
        # Go through each game, get the team stats and player stats from 'sets' and make a prompt
        for game in games:

            # Get team & player stats
            player_stats = game.playergamestats_set.all()
            # Make the prompt
            prompt = f"Write a short (75 words), espn-like, storyline for the game between {game.home_team.name} and {game.away_team.name}, the game ended {game.home_team_score}-{game.away_team_score}.\n"
            # Add the player stats
            prompt += f"Players stats:\n"
            for player_stat in player_stats:
                player_team = player_stat.player.team.name if player_stat.player.team else "Free Agent"
                player_name = f"{player_stat.player.first_name} {player_stat.player.last_name}"
                prompt += f"{player_team} {player_name}: {player_stat.points} PTS, {player_stat.rebounds} REB, {player_stat.assists} AST, {player_stat.steals} STL, {player_stat.blocks} BLK, {player_stat.turnovers} TOV\n, {player_stat.personal_fouls} PF\n (FG: {player_stat.field_goals_made}/{player_stat.field_goals_attempted}, 3P: {player_stat.three_pointers_made}/{player_stat.three_pointers_attempted}, FT: {player_stat.free_throws_made}/{player_stat.free_throws_attempted})\n"
            # Add the prompt to the list
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )
            prompts.append(completion.choices[0].message)

        # Set in cache & return the prompts
        cache.set(f"storylines_{season}_{week}", prompts, 60*60*24)
        return prompts