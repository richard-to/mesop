import json
from typing import Any, Optional, Protocol

import redis

from mesop.dataclass_utils import (
  serialize_dataclass,
  update_dataclass_from_json,
)
from mesop.server.config import Config

States = dict[type[Any], object]


class StateSessionBackend(Protocol):
  def restore(self, session_id: str, states: States):
    raise NotImplementedError()

  def save(self, session_id: str, states: States):
    raise NotImplementedError()


class NullStateSessionBackend(StateSessionBackend):
  def restore(self, session_id: str, states: States):
    pass

  def save(self, session_id: str, states: States):
    pass


class MemoryStateSessionBackend(StateSessionBackend):
  def __init__(self):
    self.cache = {}

  def restore(self, session_id: str, states: States):
    for key, state in self.cache[session_id].items():
      states[key] = state

  def save(self, session_id: str, states: States):
    self.cache[session_id] = states


class RedisStateSessionBackend(StateSessionBackend):
  def __init__(self, redis_uri: str):
    self.redis = redis.from_url(redis_uri)

  def restore(self, session_id: str, states: States):
    json_states = json.loads(self.redis.get(session_id))
    for state, json_state in zip(states.values(), json_states):
      update_dataclass_from_json(state, json_state)

  def save(self, session_id: str, states: States):
    self.redis.set(
      session_id,
      json.dumps([serialize_dataclass(state) for state in states.values()]),
      ex=600,  # Clear cache after 10 minutes of inactivity
    )


class StateSession:
  def __init__(self, config: Optional[Config]):
    self.backend = NullStateSessionBackend()
    if config:
      self.init(config)

  def init(self, config: Config):
    if config.state_session_backend == "memory":
      self.backend = MemoryStateSessionBackend()
    elif config.state_session_backend == "redis":
      self.backend = RedisStateSessionBackend(
        config.states_session_backend_redis_uri
      )

  def restore(self, session_id: str, states: States):
    self.backend.restore(session_id, states)

  def save(self, session_id: str, states: States):
    self.backend.save(session_id, states)
