# Python imports

# Third party imports

# Local imports
from players.models import Player
from simulation.scripts import badge
from simulation.scripts import default

def yellow(message):
    print("\033[93m[*]\033[0m", message)

def red(message):
    print("\033[91m[*]\033[0m", message)

# Create your tests here.
def run():
    # players = [Player.objects.get(pk=12)]
    players = Player.objects.all()
    d_attributes = default.default_attributes()
    d_badges = default.default_badges()
    badge_prices = badge.badge_prices
    convert_badges = badge.convertable_badges
    refund_badges = badge.refundable_badges

    for p in players:
        badge_refund = 0
        badges_refunded = set()
        groups_merged = set()

        attributes = p.attributes
        badges = p.badges
        badges_copy = badges.copy()

        # Remove old attributes
        for a in list(attributes):  # Create a list to avoid modifying during iteration
            if a not in d_attributes:
                del attributes[a]

        # Add new badges
        for new_badge in d_badges:
            if new_badge not in badges:
                badges_copy[new_badge] = 0 

        # Refund & merge badges
        for b in badges:
            badge_level = badges[b]

            # Refund removed badges
            if b in refund_badges and badge_level in badge_prices and b not in badges_refunded:
                refund_amount = badge.check_badge_price(0, badge_level)
                badge_refund += refund_amount
                badges_refunded.add(b)
                # red(f"[B] Refunded | Badge Removed | {b}: {refund_amount} SP")

            # Convert merged badges
            if b in convert_badges:
                merges_into = convert_badges[b]
                if merges_into in groups_merged:
                    continue  # Skip past this one

                badge_group = {key: value for key, value in badges.items() if convert_badges.get(key) == merges_into}
                if b not in badge_group:
                    continue  # Skip past this one

                owns_all_group_badges = all(value > 0 for value in badge_group.values())

                if not owns_all_group_badges:
                    if badge_level in badge_prices and b not in badges_refunded:
                        refund_amount = badge.check_badge_price(0, badge_level)
                        badge_refund += refund_amount
                        badges_refunded.add(b)
                        # red(f"[B] Refunded | {b} | Does Not Own All | {badge_group} : {refund_amount} SP")
                else:
                    # Set merge badge to lowest value between badges in badge group
                    min_badge = min(badge_group, key=badge_group.get)
                    badges_copy[merges_into] = badge_group[min_badge]
                    # yellow(f"[B] Merged | {merges_into} | Level {badges_copy[merges_into]} | {badge_group}")
                    # Refund other badges in badge group
                    del badge_group[min_badge]
                    for m_badge in badge_group:
                        if m_badge not in badges_refunded:
                            # If the badge is the same as the one used to set the merge badge value, don't refund
                            # if badge_group[m_badge] == badges_copy[merges_into]:
                            #     continue
                            # If it's different, refund
                            # m_refund_amount = badge_prices[badge_group[m_badge]] # Use only if you want just the current tier's price, and don't want to use stacked prices
                            m_refund_amount = badge.check_badge_price(0, badge_group[m_badge])
                            badge_refund += m_refund_amount
                            badges_refunded.add(b)
                            # red(f"[B] Refunded | {m_badge} | BG Leftover | {badge_group} : {m_refund_amount} SP")

                groups_merged.add(merges_into)

        # Display badge refund amount
        yellow(f"[B-REF] Refunded {p.first_name} {p.last_name} {badge_refund} SP for badges!")
        red(f"Updated {p.first_name} {p.last_name}'s badges!")

        # Remove old badges
        for b in p.badges:
            if b not in d_badges:
                del badges_copy[b]
    
        # Set 'player.badges' to 'badge_copy'
        p.badges = badges_copy
        p.save()
        if p.user:
            p.user.sp += badge_refund
            p.user.save()