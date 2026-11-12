from dataclasses import asdict
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from llm_brand_visiblity_v2.results.metrics.calculator import MetricsReport


class StatisticalReporter:
    """Generates detailed console tables and JSON export for metrics and statistical reporting."""

    def __init__(self):
        self.console = Console()

    def print_terminal_report(self, report: MetricsReport) -> None:
        """Prints a rich, formatted statistical terminal report."""
        self.console.print()
        self.console.print(
            Panel.fit(
                f"[bold cyan]LLM Brand Visibility & Competitive Benchmark Report[/bold cyan]\n"
                f"[yellow]Target Brand:[/yellow] [bold]{report.target_brand}[/bold] | "
                f"[yellow]Prompts Evaluated:[/yellow] [bold]{report.total_prompts_analyzed}[/bold]",
                border_style="cyan"
            )
        )

        table = Table(title="Entity Visibility & Share of Voice Summary", show_header=True, header_style="bold magenta")
        table.add_column("Entity", style="bold")
        table.add_column("Type", justify="center")
        table.add_column("Mentions", justify="right")
        table.add_column("Mention Rate (%)", justify="right")
        table.add_column("Share of Voice (%)", justify="right")
        table.add_column("Rec. Rate (%)", justify="right")
        table.add_column("Avg Rank", justify="right")
        table.add_column("MRR", justify="right")
        table.add_column("Net Sentiment", justify="right")

        for name, metrics in report.entity_metrics.items():
            is_target = (name == report.target_brand)
            color = "green" if is_target else "white"
            row_prefix = "[bold green]★ [/bold green]" if is_target else "  "

            table.add_row(
                f"[{color}]{row_prefix}{name}[/{color}]",
                metrics.entity_type.value if hasattr(metrics.entity_type, "value") else str(metrics.entity_type),
                str(metrics.total_mentions),
                f"{metrics.mention_rate}%",
                f"{metrics.share_of_voice}%",
                f"{metrics.recommendation_rate}%",
                str(metrics.average_rank) if metrics.average_rank is not None else "N/A",
                f"{metrics.mrr:.4f}",
                f"{metrics.net_sentiment_score:+.2f}",
            )

        self.console.print(table)

        # Sentiment breakdown table
        sentiment_table = Table(title="Sentiment Breakdown", show_header=True, header_style="bold blue")
        sentiment_table.add_column("Entity", style="bold")
        sentiment_table.add_column("Positive", style="green", justify="right")
        sentiment_table.add_column("Neutral", style="yellow", justify="right")
        sentiment_table.add_column("Negative", style="red", justify="right")

        for name, metrics in report.entity_metrics.items():
            sentiment_table.add_row(
                name,
                str(metrics.positive_sentiment_count),
                str(metrics.neutral_sentiment_count),
                str(metrics.negative_sentiment_count),
            )

        self.console.print(sentiment_table)

        # Citations summary
        self.console.print(
            Panel(
                f"[bold]Total Citations Extracted:[/bold] {len(report.all_citations)}\n"
                f"• Target Brand Mentions in URLs: [bold green]{report.brand_citations_count}[/bold green]\n"
                f"• Competitor / Third-Party URLs: [bold yellow]{report.competitor_citations_count}[/bold yellow]",
                title="Citation Attribution",
                border_style="blue"
            )
        )
        self.console.print()

    def export_json(self, report: MetricsReport, file_path: str | Path) -> None:
        """Serializes statistical report into a structured JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = asdict(report)
        # Convert enums to strings
        for entity_data in data.get("entity_metrics", {}).values():
            if isinstance(entity_data.get("entity_type"), dict) and "_value_" in entity_data["entity_type"]:
                entity_data["entity_type"] = entity_data["entity_type"]["_value_"]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

