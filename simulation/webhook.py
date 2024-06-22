from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_urls: dict[str, str] = {
    "new_players": "https://discord.com/api/webhooks/1254052927073685595/g6RGeNm7uEDmSRr771PAEwAGqPM09xJfvgGqSOcN5BLFqqgSUjlddxEMP54CUhFjp7vv",
}


def send_webhook(url, title="", body=""):
    webhook = DiscordWebhook(url=webhook_urls[url])
    webhookEmbed = DiscordEmbed(title=title, description=body, color="03b2f8")
    webhookEmbed.set_timestamp()
    webhookEmbed.set_footer(
        text="TRC Simulation",
        icon_url="https://cdn-icons-png.freepik.com/512/180/180658.png",
    )
    webhook.add_embed(webhookEmbed)
    webhook.execute()
