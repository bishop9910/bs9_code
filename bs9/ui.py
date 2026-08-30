"""Shared console output helpers (rich-based) for the entry points."""

from __future__ import annotations

from rich import print as rprint

from .constants import AUTHOR, DATE, VERSION


def banner() -> None:
    """Print the standard version banner."""
    rprint(
        f"[bold blue]Bs9 Encoder/Decoder[/bold blue] "
        f"[white on red][[/white on red][white on blue]VERSION[/white on blue] "
        f"{VERSION} [green]{DATE}[/green][white on red]][/white on red] "
        f"[green]by[/green] [white on purple]{AUTHOR}[/white on purple]"
    )


def error(message: str) -> None:
    """Print an error line."""
    rprint(f"[red]Error:[/red] [bold red]{message}[/bold red]")


def info(message: str) -> None:
    """Print an informational line."""
    rprint(f"[blue]{message}[/blue]")


def menu_help() -> None:
    """Print the interactive-menu help (formerly ``bs9Help.printHelp``)."""
    rprint("[white on blue]1: encode files[/white on blue]")
    rprint("[white on blue]To make a bs9 file, you need to select a text file, html file , javascript file or more like this.\n[/white on blue]")
    rprint("[white on blue]2: decode files[/white on blue]")
    rprint("[white on blue]To decode a bs9 file, you need to select a bs9 file, make sure it's a valid bs9 file and encoded by this program of this version.\n[/white on blue]")
    rprint("[white on blue]3: show data[/white on blue]")
    rprint("[white on blue]Display the character data table used to encode and decode.\n[/white on blue]")
    rprint("[white on blue]4: make bs9pack[/white on blue]")
    rprint("[white on blue]To make a bs9pack, you need to select a folder, make sure it's a valid folder with files in it and if it's a website folder, it should contain a index.html file.\n[/white on blue]")
    rprint("[white on blue]5: unpack bs9pack[/white on blue]")
    rprint("[white on blue]To unpack a bs9pack, you need to select a bs9pack file, make sure it's a valid bs9pack file and encoded by this program of this version.\n[/white on blue]")
    rprint("[white on blue]6: encode texts[/white on blue]")
    rprint("[white on blue]To encode the text you entered, also support chinese but won't convert to numbers.\n[/white on blue]")
    rprint("[white on blue]7: decode bs9 texts[/white on blue]")
    rprint("[white on blue]To decode the bs9 texts you entered, make sure the version of the encoded text is supported to this decoder.\n[/white on blue]")
    rprint("[white on blue]8: exit[/white on blue]")
    rprint("[white on blue]Exit the program with code 0 (normal).\n[/white on blue]")
