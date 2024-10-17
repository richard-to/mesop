from mesop.configuration.app_settings import AppSettings
from mesop.runtime import runtime


def configure_app(settings: AppSettings):
  runtime().configure_app(settings)
