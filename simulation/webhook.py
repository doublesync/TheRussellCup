from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_urls: dict[str, str] = {
    "new_players": "https://discord.com/api/webhooks/1254052927073685595/g6RGeNm7uEDmSRr771PAEwAGqPM09xJfvgGqSOcN5BLFqqgSUjlddxEMP54CUhFjp7vv",
    "marked_upgrades": "https://discord.com/api/webhooks/1268653807789670561/53mrONM9fgS84cFrDhHXxyiXSV-gdvYiDpUwUOjpdXf0DoqFPObKd-qbIBbA1BRVc9nx",
    "specialty_rolls": "https://discord.com/api/webhooks/1270538828049813595/BSTrO04VRJGs2HKz6shLnDaPotAU6IVduXR0YhNYhVRSTiV3-uajHeW92OR8Fpu9HtYy",
    "stat_updates": "https://discord.com/api/webhooks/1282346787486699641/hrbc-Wv6V9NkCKHxJmQ6S_LKLWWvTArMW1c5vDbWuoELBJCVEcMoaInxmm6jXi_YtvgB",
    "alt_identifier": "https://discord.com/api/webhooks/1288881934025363588/BqWgNfhFX2KjpTyqpO7bEtx8uIqwALdWq64sc68Lwl-pCgGjsN8Yi1T2f9cqrKy4EL95",
    "payment_requests": "https://canary.discord.com/api/webhooks/1298810551480090704/AeM_2ushAiUJn_PvVMGFrjT5jVh3InNaDcHbz_IWZCrRJkLpHGIlJwZDHwIqQyQ6gImq",
}


def send_webhook(url, title="", body="", fields=None):
    webhook = DiscordWebhook(url=webhook_urls[url])
    webhookEmbed = DiscordEmbed(title=title, description=body, color="03b2f8")
    webhookEmbed.set_timestamp()
    webhookEmbed.set_footer(
        text="rcup.live",
        icon_url="https://cdn-icons-png.freepik.com/512/180/180658.png",
    )
    if fields:
        for field in fields:
            webhookEmbed.add_embed_field(name=field[0], value=field[1], inline=False)
    webhook.add_embed(webhookEmbed)
    webhook.execute()
