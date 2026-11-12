from llm_brand_visiblity_v2.ingestion.input_pipeline import run_ingestion_pipeline
from llm_brand_visiblity_v2.core.prompt_gen.builder import BuildPrompts
from llm_brand_visiblity_v2.core.llm_exec.execution_manager import ExecutionManager
from llm_brand_visiblity_v2.results.raw.response_preprocessor import ResponsePreprocessor
from llm_brand_visiblity_v2.results.nlp.text_preprocessing import PreprocessText
from llm_brand_visiblity_v2.results.nlp.entity_extraction import EntityExtraction
from llm_brand_visiblity_v2.results.nlp.entity_resolution import EntityResolution
from llm_brand_visiblity_v2.results.nlp.response_analysis import ResponseAnalysisEngine
from llm_brand_visiblity_v2.results.metrics.calculator import MetricsCalculator
from llm_brand_visiblity_v2.results.report import StatisticalReporter, VisualReporter


def run_full_pipeline():
    """Runs the complete LLM Brand Visibility & Competitive Intelligence Pipeline."""
    print("=== Step 1: User & Brand Ingestion ===")
    brand_input = run_ingestion_pipeline()

    print("\n=== Step 2: Prompt Generation ===")
    prompt_builder = BuildPrompts(brand_input=brand_input)
    prompts = prompt_builder.build_prompt_list()
    print(f"Generated {len(prompts)} prompts across intent and context matrices.")

    print("\n=== Step 3: LLM Execution ===")
    execution_manager = ExecutionManager()
    execution_output = execution_manager.execute(prompts)

    print("\n=== Step 4: Raw Response Alignment ===")
    raw_preprocessor = ResponsePreprocessor()
    pairs, missing = raw_preprocessor.combine_prompt_with_response(execution_output, prompts)
    print(f"Successfully collected {len(pairs)} responses (Missing/Failed: {len(missing)}).")

    print("\n=== Step 5: Text Preprocessing & NLP Pipeline ===")
    text_preprocessor = PreprocessText()
    normalized_responses = text_preprocessor.normalize_response_text(pairs)

    entity_extractor = EntityExtraction()
    extracted_entities = entity_extractor.entity_extraction(normalized_responses, brand_input)

    entity_resolver = EntityResolution()
    resolved_entities = entity_resolver.entity_resolution(extracted_entities, brand_input)

    analysis_engine = ResponseAnalysisEngine()
    analyses = analysis_engine.analyze_responses(normalized_responses, resolved_entities, brand_input)

    print("\n=== Step 6: Metrics & Analysis ===")
    calculator = MetricsCalculator()
    report = calculator.calculate_metrics(analyses, brand_input)

    print("\n=== Step 7: Reporting ===")
    # Statistical Terminal & JSON Report
    stat_reporter = StatisticalReporter()
    stat_reporter.print_terminal_report(report)
    json_path = "reports/brand_visibility_report.json"
    stat_reporter.export_json(report, json_path)
    print(f"Statistical JSON saved to: {json_path}")

    # Visual HTML Dashboard Report
    visual_reporter = VisualReporter()
    html_path = "reports/brand_visibility_dashboard.html"
    visual_reporter.generate_html_report(report, html_path)
    print(f"Interactive HTML dashboard saved to: {html_path}")


def main():
    run_full_pipeline()


if __name__ == "__main__":
    main()

