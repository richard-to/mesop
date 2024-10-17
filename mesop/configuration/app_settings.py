from dataclasses import dataclass

from mesop.exceptions import MesopDeveloperException


@dataclass(kw_only=True)
class StaticFolder:
  dir_path: str
  url_path: str = "static/"

  def __post_init__(self):
    self.dir_path = self.dir_path.strip()
    if not self.dir_path.strip():
      raise MesopDeveloperException("A dir_path must be specified.")
    if self.dir_path.startswith("/"):
      raise MesopDeveloperException(
        "The dir_path must be a relative path from your application directory."
      )

    self.url_path = self.url_path.strip()
    if not self.url_path:
      raise MesopDeveloperException("A url_path must be specified.")
    if self.url_path.startswith("/"):
      raise MesopDeveloperException(
        "The url_path should not start with a forward slash, which is implicit."
      )
    if not self.url_path.endswith("/"):
      raise MesopDeveloperException(
        "The url_path must end with a forward slash."
      )


@dataclass(kw_only=True)
class AppSettings:
  static_folder: StaticFolder | None = None
