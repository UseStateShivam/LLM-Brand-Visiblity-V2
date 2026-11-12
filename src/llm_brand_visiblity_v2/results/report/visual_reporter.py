from pathlib import Path
import json
from jinja2 import Template

from llm_brand_visiblity_v2.results.metrics.calculator import MetricsReport


HTML_DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Brand Visibility Report - {{ report.target_brand }}</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen p-6 md:p-10">

    <div class="max-w-7xl mx-auto space-y-8">
        
        <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-700 pb-6 gap-4">
            <div>
                <span class="inline-block px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-full text-xs font-semibold uppercase tracking-wider mb-2">
                    LLM Brand Visibility Analysis
                </span>
                <h1 class="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
                    {{ report.target_brand }}
                    <span class="text-xs bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full font-medium">Target Brand</span>
                </h1>
                <p class="text-slate-400 text-sm mt-1">Benchmark against competitors across AI completions</p>
            </div>
            <div class="flex gap-4">
                <div class="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-center">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Total Prompts</p>
                    <p class="text-2xl font-bold text-white">{{ report.total_prompts_analyzed }}</p>
                </div>
                <div class="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-center">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Citations Extracted</p>
                    <p class="text-2xl font-bold text-indigo-400">{{ report.all_citations|length }}</p>
                </div>
            </div>
        </header>

        <!-- KPI Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            {% set target = report.entity_metrics[report.target_brand] %}
            
            <div class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 shadow-lg">
                <span class="text-xs text-slate-400 uppercase font-semibold">Share of Voice</span>
                <div class="text-3xl font-extrabold text-indigo-400 mt-2">{{ target.share_of_voice if target else 0 }}%</div>
                <p class="text-xs text-slate-400 mt-1">Percentage of all brand mentions</p>
            </div>

            <div class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 shadow-lg">
                <span class="text-xs text-slate-400 uppercase font-semibold">Mention Rate</span>
                <div class="text-3xl font-extrabold text-emerald-400 mt-2">{{ target.mention_rate if target else 0 }}%</div>
                <p class="text-xs text-slate-400 mt-1">Presence across all evaluated prompts</p>
            </div>

            <div class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 shadow-lg">
                <span class="text-xs text-slate-400 uppercase font-semibold">Recommendation Rate</span>
                <div class="text-3xl font-extrabold text-purple-400 mt-2">{{ target.recommendation_rate if target else 0 }}%</div>
                <p class="text-xs text-slate-400 mt-1">Explicitly endorsed / recommended</p>
            </div>

            <div class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 shadow-lg">
                <span class="text-xs text-slate-400 uppercase font-semibold">MRR (Mean Reciprocal Rank)</span>
                <div class="text-3xl font-extrabold text-amber-400 mt-2">{{ target.mrr if target else 0.0 }}</div>
                <p class="text-xs text-slate-400 mt-1">Rank prominence in structured outputs</p>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Share of Voice Chart -->
            <div class="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 shadow-md">
                <h3 class="text-base font-semibold text-slate-200 mb-4">Share of Voice Distribution</h3>
                <div class="relative h-64 flex justify-center">
                    <canvas id="sovChart"></canvas>
                </div>
            </div>

            <!-- Sentiment Breakdown Chart -->
            <div class="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 shadow-md">
                <h3 class="text-base font-semibold text-slate-200 mb-4">Sentiment Breakdown by Entity</h3>
                <div class="relative h-64">
                    <canvas id="sentimentChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Detailed Statistical Table -->
        <div class="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 shadow-md overflow-hidden">
            <h3 class="text-base font-semibold text-slate-200 mb-4">Competitive Benchmark Metrics</h3>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-slate-300">
                    <thead class="bg-slate-700/50 text-slate-400 uppercase text-xs">
                        <tr>
                            <th class="py-3 px-4 rounded-l-lg">Entity</th>
                            <th class="py-3 px-4">Role</th>
                            <th class="py-3 px-4 text-right">Total Mentions</th>
                            <th class="py-3 px-4 text-right">Mention Rate</th>
                            <th class="py-3 px-4 text-right">Share of Voice</th>
                            <th class="py-3 px-4 text-right">Recommendation Rate</th>
                            <th class="py-3 px-4 text-right">Avg Rank</th>
                            <th class="py-3 px-4 text-right">MRR</th>
                            <th class="py-3 px-4 text-right rounded-r-lg">Net Sentiment</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-700/50">
                        {% for name, m in report.entity_metrics.items() %}
                        <tr class="hover:bg-slate-700/30 transition-colors {{ 'bg-indigo-950/20' if name == report.target_brand else '' }}">
                            <td class="py-3.5 px-4 font-semibold {{ 'text-indigo-400' if name == report.target_brand else 'text-white' }}">
                                {{ "★ " if name == report.target_brand else "" }}{{ name }}
                            </td>
                            <td class="py-3.5 px-4 text-xs">
                                <span class="px-2 py-0.5 rounded-full {{ 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' if name == report.target_brand else 'bg-slate-700 text-slate-400' }}">
                                    {{ m.entity_type.value if m.entity_type.value is defined else m.entity_type }}
                                </span>
                            </td>
                            <td class="py-3.5 px-4 text-right font-medium">{{ m.total_mentions }}</td>
                            <td class="py-3.5 px-4 text-right">{{ m.mention_rate }}%</td>
                            <td class="py-3.5 px-4 text-right font-semibold">{{ m.share_of_voice }}%</td>
                            <td class="py-3.5 px-4 text-right">{{ m.recommendation_rate }}%</td>
                            <td class="py-3.5 px-4 text-right">{{ m.average_rank if m.average_rank is not none else "—" }}</td>
                            <td class="py-3.5 px-4 text-right font-mono text-xs">{{ m.mrr }}</td>
                            <td class="py-3.5 px-4 text-right font-semibold {{ 'text-emerald-400' if m.net_sentiment_score > 0 else ('text-rose-400' if m.net_sentiment_score < 0 else 'text-slate-400') }}">
                                {{ "+" if m.net_sentiment_score > 0 else "" }}{{ m.net_sentiment_score }}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Citation Intelligence -->
        <div class="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-6 shadow-md">
            <h3 class="text-base font-semibold text-slate-200 mb-2">Citation & Source Attribution</h3>
            <p class="text-xs text-slate-400 mb-4">Domains and URLs referenced by LLMs during generation</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-4 bg-slate-900/50 rounded-xl border border-slate-700/40">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Target Brand URLs Cited</p>
                    <p class="text-2xl font-bold text-emerald-400 mt-1">{{ report.brand_citations_count }}</p>
                </div>
                <div class="p-4 bg-slate-900/50 rounded-xl border border-slate-700/40">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Third-Party & Competitor URLs Cited</p>
                    <p class="text-2xl font-bold text-amber-400 mt-1">{{ report.competitor_citations_count }}</p>
                </div>
            </div>
            {% if report.all_citations %}
            <div class="mt-4 pt-4 border-t border-slate-700/50">
                <span class="text-xs text-slate-400 uppercase font-semibold block mb-2">Sample Extracted URLs</span>
                <ul class="text-xs space-y-1 text-indigo-400 font-mono break-all">
                    {% for url in report.all_citations[:8] %}
                    <li>• <a href="{{ url }}" target="_blank" class="hover:underline">{{ url }}</a></li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>

    </div>

    <!-- Chart Configuration Script -->
    <script>
        const entities = {{ chart_labels | tojson }};
        const sovData = {{ chart_sov | tojson }};
        const positiveData = {{ chart_positive | tojson }};
        const neutralData = {{ chart_neutral | tojson }};
        const negativeData = {{ chart_negative | tojson }};

        // Share of Voice Doughnut Chart
        new Chart(document.getElementById('sovChart'), {
            type: 'doughnut',
            data: {
                labels: entities,
                datasets: [{
                    data: sovData,
                    backgroundColor: [
                        '#6366f1', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#3b82f6'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#cbd5e1', boxWidth: 12 } }
                }
            }
        });

        // Sentiment Stacked Bar Chart
        new Chart(document.getElementById('sentimentChart'), {
            type: 'bar',
            data: {
                labels: entities,
                datasets: [
                    { label: 'Positive', data: positiveData, backgroundColor: '#10b981' },
                    { label: 'Neutral', data: neutralData, backgroundColor: '#64748b' },
                    { label: 'Negative', data: negativeData, backgroundColor: '#ef4444' }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { stacked: true, ticks: { color: '#94a3b8' }, grid: { display: false } },
                    y: { stacked: true, ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
                },
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#cbd5e1', boxWidth: 12 } }
                }
            }
        });
    </script>
</body>
</html>
"""


class VisualReporter:
    """Generates an interactive, standalone HTML visual report with charts and KPIs."""

    def generate_html_report(self, report: MetricsReport, output_file: str | Path) -> Path:
        """Renders an interactive HTML dashboard and saves it to the specified path."""
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)

        chart_labels = list(report.entity_metrics.keys())
        chart_sov = [m.share_of_voice for m in report.entity_metrics.values()]
        chart_positive = [m.positive_sentiment_count for m in report.entity_metrics.values()]
        chart_neutral = [m.neutral_sentiment_count for m in report.entity_metrics.values()]
        chart_negative = [m.negative_sentiment_count for m in report.entity_metrics.values()]

        template = Template(HTML_DASHBOARD_TEMPLATE)
        html_content = template.render(
            report=report,
            chart_labels=chart_labels,
            chart_sov=chart_sov,
            chart_positive=chart_positive,
            chart_neutral=chart_neutral,
            chart_negative=chart_negative,
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return path

