from discord_webhook import DiscordEmbed, DiscordWebhook

webhook_urls = {
    "new_players": "https://discord.com/api/webhooks/1355379450992398437/sW2jfPi24doIirzYvkzQA2teqYEPRBcefuoVnvJmWTSuGwmPKJfa5vkfZLspj4_nzzOl",
    "marked_upgrades": "https://discord.com/api/webhooks/1356639814182502591/TD0NeNQyWjF7Ds2wUf70m-vvxYW9B4Hii9Cg26E1iBj9IcoEUpN3p9BUsqihsf0rToAF",
    "specialty_rolls": "https://discord.com/api/webhooks/1356639719315865712/8D5KfRIzwlUzJfnNfq52Lki4T9j9QmoLmaSB5uvjiTaKVTAK8S3utuNBQqkhhV13YCiK",
    "stat_updates": "https://discord.com/api/webhooks/1282346787486699641/hrbc-Wv6V9NkCKHxJmQ6S_LKLWWvTArMW1c5vDbWuoELBJCVEcMoaInxmm6jXi_YtvgB",
    "alt_identifier": "https://discord.com/api/webhooks/1356639605927186475/_0QbjS8Rb9Jxi3ZLXwe_9b3HzO4sfK_Wb76q9-sPn5Qg84fB6Sm3JA__X7wh5v90x9BP",
    "payment_requests": "https://discord.com/api/webhooks/1326005936288043069/a47WxnumgPhna3DwFvzmKqvMQFwO2r--59HSC1W6t3A8LcOcFzt-6hD4NOOP9ZU5oQ6s",
    "breaking_news": "https://discord.com/api/webhooks/1356639948933173359/14wfoaOLRFl4S_ux31Vs3MteIi5ztSKa_vF3LFl1JInqhcFW6FdPF0M1i5-qs3rZxRSQ",
    "player_upgrades": "https://discord.com/api/webhooks/1356639655893667851/jkPt6CmfMgeI5C6paDcVF80FqCswVe998nVEcxNwSXWo717a_vvYg4OtNwW_VEDJt7ZA",
    "tinder": "https://canary.discord.com/api/webhooks/1371673902870167603/o_qUpeCS35Bw529j-p_FW3WGpgUL0__dhpcfE8YGCNhN55f_6XCeGGVgcWRNGSjPTKBd",
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
