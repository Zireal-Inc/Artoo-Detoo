from typing import Optional
from ..core import GitFlow

class BaseCommand:
    def __init__(self, gitflow: GitFlow):
        self.gitflow = gitflow

    def start(self, name: str, base: Optional[str] = None) -> None:
        raise NotImplementedError

    def finish(self, name: str) -> None:
        raise NotImplementedError

    def list(self) -> None:
        raise NotImplementedError

    def publish(self, name: str) -> None:
        raise NotImplementedError
