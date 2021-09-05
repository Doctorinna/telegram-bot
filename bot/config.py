from environs import Env


class Config:
    def __init__(self, bot_token: str, admin_ids: tuple[int]):
        self.bot_token = bot_token
        self.admin_ids = admin_ids


def load_config(dotenv_file_path: str = None):
    env = Env()
    env.read_env(dotenv_file_path)

    return Config(
        bot_token=env.str("BOT_TOKEN"),
        admin_ids=tuple(map(int, env.list("ADMIN_IDS")))
    )
