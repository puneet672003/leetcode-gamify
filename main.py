from dotenv import load_dotenv

from app.generate_plot import PlotAgent
from app.fetch_score import LeetCodeClient
from app.send_webhook import DiscordWebhookSender

from config.prompt_loader import PromptManager


load_dotenv()

leetcode_client = LeetCodeClient()
prompts = PromptManager()


def generate_score_string(scores: dict[str, int]):
    score_string = ""
    for user, score in scores.items():
        score_string += f"Warrior: {user} Power Level: {score}. \n"

    return score_string


users = ["puneet67", "rituraj_1234"]
scores = {}

for username in users:
    score = leetcode_client.get_total_solved(username)
    scores[username] = score

sys_prmpt = prompts.get_prompt("battle").invoke(
    {"score_string": generate_score_string(scores)}
)

print(sys_prmpt.to_string())

plot_agent = PlotAgent()
res = plot_agent.run(
    f"Write 100 words short anime-style battle story featuring today's warriors — and {max(scores, key=scores.get)} emerged victorious.",
    system_prompt=sys_prmpt.to_string(),
)

print(res)

discord_client = DiscordWebhookSender()
discord_client.send_embed("HAHAHAHAHAHA", res)
