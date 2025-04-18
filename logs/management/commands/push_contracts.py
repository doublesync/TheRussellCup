from django.core.management.base import BaseCommand
from django.utils.timezone import now

from logs.models import ContractLog, ContractOfferLog
from simulation.artificial import prompt_signing_tweet
from simulation.webhook import send_webhook


class Command(BaseCommand):
    """
    Command to finalize contracts that have passed their confirmation time.
    """

    help = "Finalize contracts that have passed their confirmation time"

    def handle(self, *args, **kwargs):
        """
        Handle the command to finalize contracts.
        """

        contracts_finalized = []

        offers_to_finalize = ContractOfferLog.objects.filter(
            confirmation_time__lte=now(), verbally_agreed=True
        )

        for offer in offers_to_finalize:
            new_contract = ContractLog.objects.create(
                player=offer.player,
                season=offer.season.season,
                length=offer.length,
                year_1_payment=offer.year_1_payment,
                year_2_payment=offer.year_2_payment,
                year_3_payment=offer.year_3_payment,
                year_2_option=offer.year_2_option,
                year_3_option=offer.year_3_option,
            )

            offer.player.contract = new_contract
            offer.player.team = offer.team
            offer.officially_signed = True
            offer.player.save()
            offer.save()

            ContractOfferLog.objects.filter(
                season=offer.season, player=offer.player
            ).exclude(id=offer.id).delete()

            contracts_finalized.append(offer)

            signing_tweet = prompt_signing_tweet(offer, official=True)
            send_webhook(
                url="breaking_news",
                title="",
                body=signing_tweet,
            )

        if contracts_finalized:
            self.stdout.write(self.style.SUCCESS("Finalized contracts:"))
            for contract in contracts_finalized:
                self.stdout.write(
                    f" - {contract.player} signed with {contract.team} for {contract.length} years."
                )
        else:
            self.stdout.write(self.style.WARNING("No contracts to finalize."))
