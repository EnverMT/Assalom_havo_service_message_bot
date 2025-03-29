from dataclasses import dataclass
from environs import Env


@dataclass
class EnvConfig:
    mode: str


@dataclass
class TgBot:
    token: str


@dataclass
class LogGroup:
    id: str
    thread_id: str


@dataclass
class ObsGroup:
    id: str


@dataclass
class Config:
    tg_bot: TgBot
    log_group: LogGroup
    obs_group: ObsGroup
    env_mode: EnvConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(token=env.str("BOT_TOKEN")),
        log_group=LogGroup(id=env.str("LOG_GROUP_ID"), thread_id=env.str("LOG_GROUP_THREAD_ID")),
        obs_group=ObsGroup(id=env.str("OBS_GROUP_ID")),
        env_mode=EnvConfig(mode=env.str("ENV_MODE")),
    )
