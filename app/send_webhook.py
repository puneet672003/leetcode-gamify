import os
from typing import Dict, List
from discord_webhook import DiscordWebhook, DiscordEmbed


class DiscordWebhookSender:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL")

    def _parse_data(self, scores: List[Dict]):
        sorted_scores = sorted(scores, key=lambda x: x["total"], reverse=True)
        winner = sorted_scores[0]["user"]
        leaderboard = "\n".join(
            f"**{i}. {user['user']}** - {user['total']}"
            for i, user in enumerate(sorted_scores, start=1)
        )

        return winner, leaderboard

    def send_embed(self, title: str, scores: List[Dict], plot: str):
        webhook = DiscordWebhook(url=self.webhook_url)
        winner, leaderboard = self._parse_data(scores)

        embed = DiscordEmbed(title=title, description=plot, color="ff0055")
        embed.add_embed_field(name="🏆 Winner", value=f"**{winner}**", inline=True)
        embed.add_embed_field(name="📊 Leaderboard", value=leaderboard, inline=True)

        webhook.add_embed(embed)
        response = webhook.execute()
        return response.status_code == 200
