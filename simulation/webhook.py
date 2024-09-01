from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_urls: dict[str, str] = {
    "new_players": "https://discord.com/api/webhooks/1254052927073685595/g6RGeNm7uEDmSRr771PAEwAGqPM09xJfvgGqSOcN5BLFqqgSUjlddxEMP54CUhFjp7vv",
    "marked_upgrades": "https://discord.com/api/webhooks/1268653807789670561/53mrONM9fgS84cFrDhHXxyiXSV-gdvYiDpUwUOjpdXf0DoqFPObKd-qbIBbA1BRVc9nx",
    "specialty_rolls": "https://discord.com/api/webhooks/1270538828049813595/BSTrO04VRJGs2HKz6shLnDaPotAU6IVduXR0YhNYhVRSTiV3-uajHeW92OR8Fpu9HtYy",
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
