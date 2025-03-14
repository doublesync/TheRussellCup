# Python imports
import os
import random

# Django imports
from django.core.cache import cache

# Local imports
import simulation.config as config
from stats.models import Season, Game, TeamGameStats, PlayerGameStats
from logs.models import ContractOfferLog, UpgradeLog

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

def prompt_upgrade_tweet(upgrade):
    # Extract player details
    player_name = f"{upgrade.player.first_name} {upgrade.player.last_name}"
    upgrades = upgrade.upgrades["attributes"]

    # Build the narrative around the upgrades
    upgrade_statements = [
        f"{player_name} has upgraded {attribute}." 
        for attribute, details in upgrades.items() if details["start"] < details["new"]
    ]

    # Ensure there's a tweet-worthy statement
    if not upgrade_statements:
        upgrade_statements.append(f"{player_name} has been putting in extra work on their game.")

    # Construct the prompt
    prompt = (
        "You are a webhook for our Discord server, we call you Coach Smithers. "
        "You're going to make an update message about a player's upgrade.\n"
        f"Player: {player_name}\n"
        "Recent upgrades:\n"
    )

    for statement in upgrade_statements:
        prompt += f"- {statement}\n"

    prompt += (
        "Please format your response as an update with each particular upgrade in a bullet point format. "
        "Be sure to accurately list these, you should only list what has actually been upgraded.\n"
        "Make sure to keep the message concise and to the point, as it will be sent to a Discord channel.\n"
        "Make the title simple and avoid referencing specific time periods like the offseason or playoffs, "
        "as the phase may change over time, and we want the title to remain relevant regardless of the current phase.\n"
    )

    # Randomly decide whether to add a joke
    if random.random() < 0.60:  # 60% probability
        joke_targets = [
            ("Klub Bobert", "manages his team like it’s 1950 and is a known racist"),
            ("AC Abass", "is short and fat despite spending thousands on himself"),
            ("Archie Hermann", "stat-chases but somehow still has a mid career"),
            ("Billy King Jr.", "is Australian and Leo Gagnon’s son"),
            ("DC Kelly Jr.", "is bad at basketball despite spending so much money"),
            ("Leo Gagnon", "is crippled by his insecurity and low self-esteem"),
            ("Jauvy Campbell", "is chronically online"),
            ("Mikael Goldman", "would be a Wendy's employee if he wasn't 7'1"),
            ("Zaire Cape", "has less rings than Forrest Quinton and Alvin Melo"),
            ("Zachary James", "is a Walmart version of PJ Irving"),
            ("Adam Max-max", "doesn't shower and is incredibly smelly")
        ]
        event_references = [
            "Archie Hermann left the Raptors and they immediately won a championship",
            "Klub Bobert drafted Jafari Junior with the first overall pick",
            "How bad of a manager Deion Johnson was",
            "The seven-team trade where the Houston Rockets betrayed LaMarw Jackson",
            "How short AC Abass III is",
            "How ugly Deion Johnson is in real life",
            "How America is much better than Australia",
            "How Canada is much better than America",
            "How DC Kelly Jr. is horrible at basketball despite spending so much money",
            "How Zaire Cape ring chased the first half of his career without winning a ring",
            "How Raito Kanashimi keeps getting demoted back to second option every season",
            "How Vonte keeps retiring his players within two seasons"
        ]

        # Select a joke and an event randomly
        player_joke = random.choice(joke_targets)
        event_joke = random.choice(event_references)

        prompt += f"At the bottom of the message, as a joke, make a raunchy and extremely inappropriate comment about {player_joke[0]}: {player_joke[1]}. Insult them in the most inappropriate way you can\n"
        prompt += f"Reference this event with the joke: {event_joke} or feel free to fabricate your own raunchy event.\n"

    # Get the completion from the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )
    response = completion.choices[0].message.content
    return response
