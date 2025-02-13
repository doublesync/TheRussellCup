from django.core.management.base import BaseCommand
from logs.models import ContractOfferLog, ContractLog
from django.utils.timezone import now
from simulation.webhook import send_webhook
from simulation.artificial import prompt_signing_tweet

class Command(BaseCommand):
    help = 'Finalize contracts that have passed their confirmation time'

    def handle(self, *args, **kwargs):
        
        contracts_finalized = []

        # Find all contract offers that are verbally agreed and have a confirmation time less than or equal to the current time
        offers_to_finalize = ContractOfferLog.objects.filter(
            confirmation_time__lte=now(), verbally_agreed=True
        )
        
        # Finalize each contract offer
        for offer in offers_to_finalize:
            # Create the contract from the offer
            new_contract = ContractLog.objects.create(
                player=offer.player,
                season=offer.season.season,
                length=offer.length,
                year_1_payment=offer.year_1_payment,
                year_2_payment=offer.year_2_payment,
                year_3_payment=offer.year_3_payment,
                year_2_option=offer.year_2_option,
                year_3_option=offer.year_3_option
            )

            # Set the player's current contract to the new contract, and team to the offer's team
            offer.player.contract = new_contract
            offer.player.team = offer.team
            offer.officially_signed = True
            offer.player.save()
            offer.save()

            # Delete all other offers for the player (excluding the signed one)
            ContractOfferLog.objects.filter(season=offer.season, player=offer.player).exclude(id=offer.id).delete()

            # Append to the finalized contracts list
            contracts_finalized.append(offer)

            # Send a discord webhook notification
            signing_tweet = prompt_signing_tweet(offer, official=True)
            send_webhook(
                url="breaking_news",
                title="",
                body=signing_tweet,
            )

        # Print the finalized contracts
        if contracts_finalized:
            self.stdout.write(self.style.SUCCESS('Finalized contracts:'))
            for contract in contracts_finalized:
                self.stdout.write(f' - {contract.player} signed with {contract.team} for {contract.length} years.')
        else:
            self.stdout.write(self.style.WARNING('No contracts to finalize.'))