import secrets
from dataclasses import dataclass, fields
from datetime import datetime, timedelta
from typing import Any, Literal, Optional, Protocol

States = dict[type[Any], object]


@dataclass(kw_only=True)
class StateConfig:
  secret_key: Optional[str] = None
  backend: Literal["memory", "null"] = "memory"

  def init(self, config: "StateConfig"):
    for field in fields(StateConfig):
      setattr(self, field.name, getattr(config, field.name))


class StateSessionBackend(Protocol):
  def restore(self, state_hash: str, states: States) -> bool:
    raise NotImplementedError()

  def save(self, states: States) -> str:
    raise NotImplementedError()

  def clear_stale_sessions(self):
    raise NotImplementedError()


class NullStateSessionBackend(StateSessionBackend):
  def restore(self, state_hash: str, states: States) -> bool:
    return False

  def save(self, states: States) -> str:
    return ""

  def clear_stale_sessions(self):
    pass


class MemoryStateSessionBackend(StateSessionBackend):
  def __init__(self):
    self.cache = {}

  def restore(self, state_hash: str, states: States) -> bool:
    if state_hash not in self.cache:
      return False
    _, states = self.cache[state_hash]
    for key, state in states.items():
      states[key] = state
    del self.cache[state_hash]
    return True

  def save(self, states: States) -> str:
    state_hash = secrets.token_urlsafe(16)
    self.cache[state_hash] = (datetime.now(), states)
    return state_hash

  def clear_stale_sessions(self):
    stale_keys = set()

    current_time = datetime.now()
    for key, (timestamp, _) in self.cache.items():
      if timestamp + timedelta(minutes=10) < current_time:
        stale_keys.add(key)

    for key in stale_keys:
      del self.cache[key]


class StateSession:
  def __init__(self, config: Optional[StateConfig] = None):
    self.backend = NullStateSessionBackend()
    if config:
      self.init(config)

  def init(self, config: StateConfig):
    if config.backend == "null":
      self.backend = NullStateSessionBackend()
    elif config.backend == "memory":
      self.backend = MemoryStateSessionBackend()

  def restore(self, state_hash: str, states: States):
    self.backend.restore(state_hash, states)

  def save(self, states: States) -> str:
    return self.backend.save(states)

  def clear_stale_sessions(self):
    self.backend.clear_stale_sessions()


state_session = StateSession()
config = StateConfig()
