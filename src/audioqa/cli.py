from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from audioqa.loader import load_audio
from audioqa.models import Status
from audioqa.validators.clipping import validate_clipping
from audioqa.validators.levels import validate_peak_level
from audioqa.validators.metadata import validate_channels, validate_sample_rate
from audioqa.validators.silence import validate_end_silence, validate_start_silence

app = typer.Typer(
    help="Audio QA validation tool",
    invoke_without_command=False,
)
console = Console()

@app.command()
def version() -> None:
    """Show version information."""
    console.print("audioqa 0.1.0")

@app.command()
def validate(
    file_path: Path = typer.Argument(..., help="Path to the audio file to validate"),
    sample_rate: int = typer.Option(44100, help="Expected sample rate"),
    channels: int = typer.Option(2, help="Expected number of channels"),
    max_peak_dbfs: float = typer.Option(-1.0, help="Maximum allowed peak level in dBFS"),
) -> None:
    """Validate a single audio file."""

    if not file_path.exists():
        console.print(f"[red]File not found:[/red] {file_path}")
        raise typer.Exit(code=1)

    audio = load_audio(file_path)

    results = [
        validate_sample_rate(audio, allowed_sample_rates={sample_rate}),
        validate_channels(audio, allowed_channels={channels}),
        validate_peak_level(audio, max_peak_dbfs=max_peak_dbfs),
        validate_clipping(audio),
        validate_start_silence(audio),
        validate_end_silence(audio),
    ]

    overall_status = Status.PASS

    if any(result.status == Status.FAIL for result in results):
        overall_status = Status.FAIL
    elif any(result.status == Status.WARNING for result in results):
        overall_status = Status.WARNING

    console.print(f"\n[bold]Audio QA Report[/bold]")
    console.print(f"File: {file_path}")
    console.print(f"Overall status: [{_status_colour(overall_status)}]{overall_status.value}[/]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Message")
    table.add_column("Measured")
    table.add_column("Expected")

    for result in results:
        colour = _status_colour(result.status)
        table.add_row(
            result.check_name,
            f"[{colour}]{result.status.value}[/]",
            result.message,
            str(result.measured_value) if result.measured_value is not None else "",
            str(result.expected_value) if result.expected_value is not None else "",
        )

    console.print(table)

    if overall_status == Status.FAIL:
        raise typer.Exit(code=1)


def _status_colour(status: Status) -> str:
    match status:
        case Status.PASS:
            return "green"
        case Status.WARNING:
            return "yellow"
        case Status.FAIL:
            return "red"