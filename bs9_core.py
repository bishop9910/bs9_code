from typing import Any

class bishop9910_lib:
  def __init__(self) -> None:
    self.version: tuple[int, int, int] = (0, 0, 1)
    self.author: str = "bishop9910"
  def __call__(self) -> dict[str, Any]:
    return {
      "version": self.version, 
      "author": self.author
      }