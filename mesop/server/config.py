import os
from typing import Literal, Optional

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
  secret_key: str
  state_session_backend: Literal["memory", "redis"]
  states_session_backend_redis_uri: Optional[str]


def CreateConfigFromEnv() -> Config:
  return Config(
    secret_key=os.getenv("SECRET_KEY"),
    state_session_backend=os.getenv("STATE_SESSION_BACKEND"),
    states_session_backend_redis_uri=os.getenv(
      "STATE_SESSION_BACKEND_REDIS_URI"
    ),
  )


config = CreateConfigFromEnv()
