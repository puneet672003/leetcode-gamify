import os
from discord_webhook import DiscordWebhook, DiscordEmbed


class DiscordWebhookSender:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL")

    def send_embed(self, title, description, username="Test", avatar_url=None):
        webhook = DiscordWebhook(url=self.webhook_url)

        embed = DiscordEmbed(title=title, description=description, color="7289DA")

        webhook.add_embed(embed)
        response = webhook.execute()
        return response.status_code == 200
