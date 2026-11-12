# LLM Brand Visibility & Competitive Benchmark Platform (V2)

An end-to-end Python pipeline for measuring and benchmarking brand visibility, recommendation rate, sentiment, and share of voice (SoV) across Large Language Model completions.

---

## 🏗️ Architecture & Pipeline Flow

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Ingestion (Brand, Competitors, Products, Services)       │
 └──────────────────────────────┬──────────────────────────────┘
                                │
 ┌──────────────────────────────▼──────────────────────────────┐
 │ 2. Prompt Generation (Branded, Unbranded, Competitor)       │
 └──────────────────────────────┬──────────────────────────────┘
                                │
 ┌──────────────────────────────▼──────────────────────────────┐
 │ 3. LLM Execution & Adapters (Gemini / OpenAI / Custom)      │
 └──────────────────────────────┬──────────────────────────────┘
                                │
 ┌──────────────────────────────▼──────────────────────────────┐
 │ 4. Raw Response Alignment & Preprocessing                   │
 └──────────────────────────────┬──────────────────────────────┘
                                │
 ┌──────────────────────────────▼──────────────────────────────┐
 │ 5. NLP Analysis (Spacy PhraseMatcher, NER, Stance, Citations)│
 └──────────────────────────────┬──────────────────────────────┘
                                │
 ┌──────────────────────────────▼──────────────────────────────┐
 │ 6. Metrics Engine (SoV, Mention Rate, MRR, Rec. Rate)        │
 └──────────────────────────────┬──────────────────────────────┘
                                │
 ┌──────────────────────────────▼──────────────────────────────┐
 │ 7. Reports (Rich Console Tables, JSON, Interactive HTML)    │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart & Setup

### 1. Prerequisites
- **Python >= 3.11**
- [**uv**](https://docs.astral.sh/uv/) (recommended package manager) or standard `pip`

### 2. Environment Variables
Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY="your-google-gemini-api-key"
# Optional override (default is gemini-2.5-flash):
GEMINI_MODEL="gemini-2.5-flash"
```

### 3. Dependencies
All dependencies are locked in `pyproject.toml`. With `uv`, you don't need to manually create or activate `.venv`:
```bash
# Verify environment and dependencies
uv sync
```

---

## 💻 How to Run

### Run the Complete Pipeline
Execute the main entrypoint:
```bash
uv run python src/llm_brand_visiblity_v2/main.py
```

You will be interactively prompted for:
1. **Brand Name**: (e.g. `Acme Corp`)
2. **Website URL**: (e.g. `https://acme.com`)
3. **Competitors** (comma-separated): (e.g. `Globex, Initech`)
4. **Products** (comma-separated, optional): (e.g. `Widget Pro, Widget Mini`)
5. **Services** (comma-separated, optional): (e.g. `Cloud Hosting`)
6. **Niche**: (e.g. `Cloud SaaS`)

---

## 📊 Outputs & Reports

Once execution completes, three formats are generated:

### 1. Terminal Report (Rich Tables)
* **Visibility Summary Table**: Entity name, role (brand/competitor), mentions count, mention rate (%), Share of Voice (%), Recommendation Rate (%), Average Rank, and MRR.
* **Sentiment Breakdown**: Positive, Neutral, Negative mention counts.
* **Citation Attribution**: Target vs. competitor URLs cited by the model.

### 2. Statistical JSON Export
* Saved to `reports/brand_visibility_report.json`.
* Contains complete aggregated metrics per entity, total prompts, citation lists, and machine-readable data for historical tracking.

### 3. Interactive Visual Dashboard
* Saved to `reports/brand_visibility_dashboard.html`.
* Standalone dashboard with **Tailwind CSS** styling and **Chart.js**:
  * Real-time **Share of Voice** Donut Chart.
  * **Sentiment Distribution** Stacked Bar Chart.
  * KPI summary cards and competitive comparison table.
  * Open directly in any browser:
    ```bash
    # Windows
    start reports/brand_visibility_dashboard.html
    # Mac
    open reports/brand_visibility_dashboard.html
    ```

---

## 🧩 Key Pipeline Modules

| Module Path | Purpose |
| :--- | :--- |
| `ingestion/` | CLI input prompts and strict Pydantic validation (`BrandInput`) |
| `core/prompt_gen/` | Generates prompt combinations across Intent (Buying, Informational, Comparison) and Context (Brand, Product, Service) |
| `core/llm_exec/` | Retry handling, token tracking, latency recording, and adapter execution |
| `results/raw/` | Pairwise mapping between prompts and successful completions |
| `results/nlp/` | Text normalization, SpaCy dictionary + NER extraction, entity resolution, ranking, and stance detection |
| `results/metrics/` | Aggregates Mention Rate, SoV, Reciprocal Rank (MRR), and Net Sentiment |
| `results/report/` | Terminal tables, JSON serialization, and interactive Chart.js HTML generation |

---

## 🧪 Testing

To run the automated end-to-end integration test (with mock data):
```bash
uv run python src/llm_brand_visiblity_v2/tests/test.py
```

