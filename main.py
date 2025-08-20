from dotenv import load_dotenv

from app.fetch_score import LeetCodeAPI
from app.generate_plot import PlotAgent
from app.send_webhook import DiscordWebhookSender

from config.load_config import Config
from config.prompt_loader import PromptManager


load_dotenv()

config = Config()
plot_agent = PlotAgent()
prompts = PromptManager()
discord_client = DiscordWebhookSender()

users = config.get_users()
sys_prmpt = prompts.get_prompt("battle")

all_scores = []
print("Fetching leetcode progress")
for user in users:
    progress_dict = {}
    progress_dict["user"] = user

    leetcode_client = LeetCodeAPI(user)
    question_progress = leetcode_client.get_question_progress()
    progress_dict["detail"] = question_progress
    progress_dict["total"] = sum(it.get("count", 0) for it in question_progress)

    all_scores.append(progress_dict)

print("Fetching response from AI.")
res = plot_agent.run(
    all_scores,
    sys_prmpt,
)

print("Generating discor webhook")
discord_client.send_embed("HAHAHAHAHAHA", all_scores, res)
print("Done!")
