# Python imports
import random

# Third party imports
from faker import Faker

# Local imports
from simulation.create import CreatePlayer
from simulation.scripts.default import (
    position_choices,
    country_choices,
    college_choices,
)
from accounts.models import CustomUser


# Create your tests here.
def run():
    user = CustomUser.objects.get(pk=1)
    first_name, last_name = Faker().name().split()
    player = CreatePlayer(
        first_name=first_name,
        last_name=last_name,
        position=random.choice(position_choices),
        number=random.randint(0, 99),
        country=random.choice(country_choices),
        college=random.choice(college_choices),
        user=user,
    )
    player = player.create()
    for key, value in player.__dict__.items():
        print(f"{key}: {value}")
