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
    attributes = upgrade.upgrades["attributes"]
    badges = upgrade.upgrades["badges"]
    badge_levels = {
        "0": "None",
        "1": "Bronze",
        "2": "Silver",
        "3": "Gold",
        "4": "Hall of Fame"
    }

    # Build the narrative around the upgrades
    attribute_statements = [
        f"{player_name} has upgraded {attribute} to {details["new"]}." 
        for attribute, details in attributes.items() if details["start"] < details["new"]
    ]

    badge_statements = [
        f"{player_name} has upgraded {badge} to {badge_levels[str(details["new"])]}." 
        for badge, details in badges.items() if details["start"] < details["new"]
    ]

    upgrade_statements = attribute_statements + badge_statements

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
        "Please format your response as an update with each particular upgrade in a bullet point format.\n" 
        "As an example, if the upgrade badge is 'Aerial Wizard' and the upgraded badge level is 'Bronze', then the bullet point should be formatted like: Aerial Wizard to Bronze\n"
        "Be sure to accurately list these, you should only list what has actually been upgraded.\n"
        "Make sure to keep the message concise and to the point, as it will be sent to a Discord channel.\n"
        "For the title, use the following example: "
        "If the player's name is John Smith, the title should be formatted like: Update: John Smith.\n"
        "The title should be in bold."
    )

    # Randomly decide whether to add extra text
    if random.random() < 1.00:  # 100% probability
        attribute_descriptions = [
            ("Ball Control", "determines a player’s ability to handle and control the basketball while dribbling, particularly in tight spaces or when attempting advanced dribble moves like crossovers, spins, or behind-the-back dribbles."),
            ("Block", "determines a player's ability to contest or block shots from opponents, especially near the basket."),
            ("Close Shot", "determines a player's effectiveness in making shots near the basket but outside the immediate layup and dunking range."),
            ("Defensive Consistency", "determines a player's ability to maintain effective defensive performance throughout the game."),
            ("Defensive Rebound", "determines a player's effectiveness in securing rebounds on the defensive end."),
            ("Draw Foul", "determines ability to attract fouls from defenders while shooting close to the basket or driving it."),
            ("Driving Dunk", "determines a player's ability to execute dunks while driving towards the basket."),
            ("Free Throw", "determines a player's ability to successfully convert free throw attempts. Generally, timing the shot is easier for players with a high Free Throw attribute."),
            ("Hands", "determines a player's ability to secure and control the basketball. This includes their effectiveness in catching passes and finishing plays."),
            ("Help Defense IQ", "determines a player's ability to provide effective help on defense, such as knowing when to execute double teams or assist teammates without compromising coverage on their primary assignment."),
            ("Hustle", "determines a player's effort and tenacity in making plays, particularly on defense and when going after loose balls."),
            ("Interior Defense", "determines a player's ability to defend against opponents in the paint effectively."),
            ("Driving Layup", "determines a player's ability to successfully make layup shots, which are typically taken close to the basket."),
            ("Midrange Shot", "determines a player's effectiveness in shooting from mid-range distances."),
            ("Offensive Consistency", "determines a player's ability to maintain a high level of offensive performance throughout the game."),
            ("Offensive Rebound", "determines a player's ability to grab rebounds after missed shots."),
            ("Pass Accuracy", "determines a player's likelihood of successfully completing passes to teammates, especially in high-pressure situations or when defenders are nearby."),
            ("Passing IQ", "determines a player's ability to make smart passing decisions during gameplay. It influences the effectiveness of a player's passing, particularly in identifying the best options and minimizing the risk of turnovers."),
            ("Pass Perception", "determines a player's ability to anticipate and react to passing lanes, leading to successful disruptions of the opponent's offensive plays."),
            ("Passing Vision", "determines a player's ability to quickly recognize and anticipate passing opportunities on the court."),
            ("Perimeter Defense", "determines a player's effectiveness in guarding opponents on the perimeter, particularly against outside shooters and drivers. It influences how well a player can stay in front of their assigned offensive player, contest shots, and prevent drives to the basket."),
            ("Post Moves", "determines a player's ability to perform moves while backing down an opponent, execute post shots, and successfully finish around the basket."),
            ("Post Fade", "determines a player's effectiveness in executing fadeaway shots while in the post."),
            ("Post Hook", "determines a player's ability to successfully execute hook shots while in the post position."),
            ("Shot IQ", "determines a player's understanding of shot selection and decision-making when taking shots. This attribute influences how well a player can read the game and make effective shooting choices based on the situation, such as recognizing when to shoot, pass, or drive."),
            ("Standing Dunk", "determines a player's ability to successfully execute dunks while standing still, which is especially important for big men and players who primarily rely on their vertical leap in close proximity to the basket."),
            ("Steal", "determines a player's ability to intercept passes and take the ball away from opponents."),
            ("3pt Shot", "determines a player's ability to make three-point shots. It's important to note that the ability to time shots precisely can significantly impact a player's success rate when attempting outside shots.")
        ]
        badge_descriptions = [
            ("Deadeye", "Jump shots taken with a defender closing out receive less of a penalty from a shot contest"),
            ("Limitless Range", "Extends the range from which a player can shoot three-pointers effectively from deep"),
            ("Mini Marksman", "Elevates the likelihood of making shots over taller defenders."),
            ("Set Shot Specialist", "Boosts chances of knocking down stand-still jump shots."),
            ("Shifty Shooter", "Improves a player's ability to successfully make off-the-dribble, high-difficulty jump shots."),
            ("Aerial Wizard", "Increases the ability to finish an alley-oop from a teammate, or putback a finish off an offensive rebound"),
            ("Float Game", "Improves a player's ability to make floaters"),
            ("Hook Specialist", "Improves a player's ability to make post hooks"),
            ("Layup Mixmaster", "improves a player's ability to finish fancy or acrobatic layups successfully."),
            ("Paint Prodigy", "Improves a player's ability to quickly and efficiently score while going to work in the paint."),
            ("Physical Finisher", "Improves a player's ability to battle through contact and convert contact layups."),
            ("Post Fade Phenomr", "Improves a player's ability to make post fades and hop shots"),
            ("Post Powerhouse", "Strengthens a player's ability at backing down defenders and moving them with dropsteps."),
            ("Post-Up Poet", "Raises the chances of faking or getting by the defender, as well as scoring, when performing moves in the post."),
            ("Posterizer", "Increases the chances of throwing down a dunk on your defender"),
            ("Ankle Assassin", "Increases the ability to break down the defender or cross them up."),
            ("Bail Out", "Passing out of a jump shot or layup yields fewer errant passes than normal. Additionally, helps passing out of double teams"),
            ("Break Starter", "After grabbing a defensive board, deep outlet passes made up the court are more accurate. Passes must be made quickly following the defensive rebound"),
            ("Dimer", "When in the half-court, passes by Dimers to open shooters yield a shot percentage boost"),
            ("Handles for Days", "A player takes less of an energy hit when performing consecutive dribble moves, allowing them to chain together combos quicker and for longer periods of time"),
            ("Lightning Launch", "Speeds up launches when attacking from the perimeter."),
            ("Strong Handle", "Reduces the likelihood of being bothered by defenders when dribbling."),
            ("Unpluckable", "Defenders have a tougher time poking the ball free with their steal attempts"),
            ("Versatile Visionary", "Improves a player's ability to thread and fit tight passes, including alley-oops, quickly and on time."),
            ("Challenger", "Improves the effectiveness of well-timed contests against perimeter shooters"),
            ("Glove", "Increases the ability to successfully steal from ball-handlers, or strip layup attempts"),
            ("Interceptor", "The frequency of successfully tipped or intercepted passes greatly increases"),
            ("High-Flying Denier", "Boosts the speed and leaping ability of a defensive player in anticipation of a block attempt."),
            ("Immovable Enforcer", "Improves a defensive player's strength when defending ball handlers and finishers"),
            ("Off-Ball Pest", "Makes players more difficult to get past when playing off-ball, as the can grab and hold their matchup and don't get their ankles broken as often"),
            ("On-Ball Menace", "Hounds and bodies up while defending on the perimeter."),
            ("Paint Patroller", "Increases a player's ability to block or contest shots at the rim."),
            ("Pick Dodger", "Improves a player's ability to navigate through and around screens while on defense. At the Hall of Fame level, can blow through screens in the park or blacktop"),
            ("Post Lockdown", "Strengthens a player's ability to effectively defend moves in the post, with an increased chance at stripping the opponent"),
            ("Boxout Beast", "Increases the likelihood of dunking or posterizing your opponent when standing in the painted area"),
            ("Rebound Chaser", "Increases the likelihood of dunking or posterizing your opponent when standing in the painted area"),
            ("Brick Wall", "Increases the effectiveness of screens and drains energy from opponents on physical contact"),
            ("Slippery Off-Ball", "When attempting to get open off screens, the player more effectively navigates through traffic"),
            ("Pogo Stick", "Allows players to quickly go back up for another jump upon landing. This could be after a rebound, block attempt, or even jumpshot")
        ]
        upgrade_descriptions = attribute_descriptions + badge_descriptions

        # If a badge been upgraded, select one randomly
        if upgrade_statements:
            attributes = [
                attribute
                for attribute, details in attributes.items() if details["start"] < details["new"]
            ]
            badges = [
                badge 
                for badge, details in badges.items() if details["start"] < details["new"]
            ]
            upgrades = attributes + badges
            random_upgrade = random.choice(upgrades)
            for description in upgrade_descriptions:
                if str(random_upgrade) == description[0]:
                    upgrade_description = description[1]
                                            
            prompt += (f"At the bottom of the message, make an analytical comment about how {random_upgrade} is going to have an impact on {player_name}'s game. The on-court impact of the upgrade is based off of this description: {upgrade_description}.\n"
                        "Use the player's last name instead of their first name when referring to them.\n"
                        "Keep the analysis to maximum one sentence and don't always use the exact same words that are in the upgrade descriptions.\n"
                        "The analysis should not make meta reference to the name of the upgrade or the upgrade level.\n"
                        "The analysis should be in the style of a sports reporter providing a scoop on a player's efforts to improve./n"
                        "If the player's name is John Smith and the upgrade is Pogo Stick, an example analysis might be: "
                        "Team sources say that John Smith has developed some extra bounce lately, and that his blocking game has improved as a result."
                      )

    # 1% probability
    if random.random() < 0.01:
        prompt += "Instead of writing any of the above, just write a message talking about how much either D.C. Kelly or Spiro Hermann sucks at basketball."

    # Get the completion from the API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )
    response = completion.choices[0].message.content
    return response
