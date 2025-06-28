from dotenv import load_dotenv

from app.generate_plot import PlotAgent
from app.fetch_score import LeetCodeClient
from app.send_webhook import DiscordWebhookSender

from config.load_config import Config
from config.prompt_loader import PromptManager


load_dotenv()

config = Config()
plot_agent = PlotAgent()
prompts = PromptManager()
leetcode_client = LeetCodeClient()

users = config.get_users()
sys_prmpt = prompts.get_prompt("battle")
all_scores = leetcode_client.get_scores(users)

print("Fetching response from AI.")

res = plot_agent.run(
    all_scores,
    sys_prmpt,
)

print("Generating discor webhook")

discord_client = DiscordWebhookSender()
discord_client.send_embed("HAHAHAHAHAHA", all_scores, res)

print("Done")
