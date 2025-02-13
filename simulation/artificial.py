# Python imports
import os

# Django imports
from django.core.cache import cache

# Local imports
import simulation.config as config
from stats.models import Season, Game, TeamGameStats, PlayerGameStats
from logs.models import ContractOfferLog

# Third party imports
from openai import OpenAI
from dotenv import load_dotenv

# Load secrets from .env file or production environment
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def prompt_upgrade_advice(player):
    
    # Check if the players user has this seasons care package
    if not player.user.has_care_package: 
        return """
        <h2>Upgrade Advice</h2>
        You need to buy this seasons care package to get upgrade advice.
        """

    # Prompts upgrade advice for players (based on vitals, attributes, badges, & tendencies)
    prompt = "You are an upgrade advisor for an NBA2K basketball player. Here are the player's vitals, attributes, badges, and tendencies:\n"
    prompt += f"Name: {player.first_name} {player.last_name}\n"
    prompt += f"Position: {player.position}\n"
    prompt += f"Height: {player.height_imperial}\n"
    prompt += f"Weight: {player.weight} lbs\n"
    prompt += f"Wingspan: {player.wingspan}/100\n"
    prompt += f"Attributes:{player.attributes}\n"
    prompt += f"Badges:{player.badges}\n"
    prompt += f"Tendencies:{player.tendencies}\n"
    prompt += "Based on the player's vitals, attributes, badges, and tendencies, what would you recommend for the player to upgrade? (for tendencies note whether they should increase or decrease the tendency)\n"
    prompt += "Please provide a short, 75charcter-ish simplified list of attributes, badges, and tendencies that the player should upgrade.\n"
    prompt += "At the top of the list, provide the 'plan' for the player (e.g. 'Focus on shooting, playmaking, and defense').\n"
    prompt += "Your response should be in HTML list format (titled 'Upgrade Advice' at the top) ready to be sent directly in a HttpResponse using Django (just the HTML, no need to notate with markdown).\n"

    # Get the completion from the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response

def prompt_signing_tweet(offer, official=False):
    # Prompts a tweet for a player signing a contract
    prompt = "You are a social media manager for the NBA (think Shams Charania or Woj). Here is the player's signing information:\n"
    prompt += f"Player: {offer.player.first_name} {offer.player.last_name}\n"
    prompt += f"Position: {offer.player.position}\n"
    prompt += f"Height: {offer.player.height_imperial}\n"
    prompt += f"Weight: {offer.player.weight} lbs\n"
    prompt += f"Projected Role: {offer.projected_role}\n"
    prompt += f"Team: {offer.team.name}\n"
    prompt += f"Contract Length: {offer.length} years\n"
    prompt += f"Contract Year 1 Payment: ${offer.year_1_payment}\n"
    prompt += f"Contract Year 2 Payment: ${offer.year_2_payment}\n"
    prompt += f"Contract Year 3 Payment: ${offer.year_3_payment}\n"
    prompt += f"Contract Year 2 Option: {offer.year_2_option}\n"
    prompt += f"Contract Year 3 Option: {offer.year_3_option}\n"
    prompt += "Please provide a tweet announcing the player's signing with the team.\n"
    prompt += "Feel free to add a sentence or two extra to spice up the lore.\n"
    if official:
        prompt += "This is an official signing announcement -- the grace period has passed.\n"
    else:
        prompt += "This is a verbal agreement -- the grace period has not passed yet; either party can back out of the agreement for eight hours.\n"
    prompt += "Your response should be formatted in the way Shams or Woj formats their tweets, make sure the salary amounts are formatted as they are (do not inflate them).\n"

    # Get the completion from the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response