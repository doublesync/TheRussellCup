# Python imports

# Third party imports

# Local imports
from accounts.models import CustomUser
from logs.models import ContractLog
from simulation.payment import pay_contracts

# Create your tests here.
def run():
    for user in CustomUser.objects.all():
        response = pay_contracts(user)
        print(f"{user.username} - {response}")
