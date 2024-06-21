from typing import Literal

from mesop.state_session.state_session import StateConfig, config, state_session


def configure_state(*, backend: Literal["memory", "null"] = "memory"):
  print("CONFIG")
  config.init(StateConfig(backend=backend))
  state_session.init(config)
