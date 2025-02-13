from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_urls: dict[str, str] = {
    "new_players": "https://discord.com/api/webhooks/1326005929824489532/OCyiOK98HPJcKYxSavkTnuCGuj1RQSpwpT2QMxHd1WohkloYafPx49Xo-hhCGtMot-_X",
    "marked_upgrades": "https://discord.com/api/webhooks/1326005781144932393/tmvLbqcnEKZH90K5MHG1SvIT7ttrM52Pzd8J8zXYA8VG9XtMXt7Upt4HoWwLjLMh1EQY",
    "specialty_rolls": "https://discord.com/api/webhooks/1326005794012921897/hT8KfgxGkCJUvvku5GEkz7WQFg8fo3sycqgUqVsSgfXCfCj5KOMgax01o2MUz9KhvuP9",
    "stat_updates": "https://discord.com/api/webhooks/1282346787486699641/hrbc-Wv6V9NkCKHxJmQ6S_LKLWWvTArMW1c5vDbWuoELBJCVEcMoaInxmm6jXi_YtvgB",
    "alt_identifier": "https://discord.com/api/webhooks/1326005937949118475/umkaVz-vGOiKq1DsEr2UpfPsF_Dj5YZycsVuD-qa5JM0nqrDPz_1jH-VrszgAz_A-NQo",
    "payment_requests": "https://discord.com/api/webhooks/1326005936288043069/a47WxnumgPhna3DwFvzmKqvMQFwO2r--59HSC1W6t3A8LcOcFzt-6hD4NOOP9ZU5oQ6s",
    "breaking_news": "https://canary.discord.com/api/webhooks/1339340914778439752/56wK6XnDHQ6lk5HRj3GkwPahW2VrY9-Jg-I84uU3HoWEFQyrNhGTpJRfbQxdYsGCxelm"
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
