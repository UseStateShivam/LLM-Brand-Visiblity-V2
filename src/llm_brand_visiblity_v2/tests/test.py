from llm_brand_visiblity_v2.schemas import (
    BrandInput,
    RawResult,
    PromptExec,
)
from llm_brand_visiblity_v2.core.prompt_gen.builder import BuildPrompts
from llm_brand_visiblity_v2.results.raw.response_preprocessor import ResponsePreprocessor
from llm_brand_visiblity_v2.results.nlp.text_preprocessing import PreprocessText
from llm_brand_visiblity_v2.results.nlp.entity_extraction import EntityExtraction
from llm_brand_visiblity_v2.results.nlp.entity_resolution import EntityResolution
from llm_brand_visiblity_v2.results.nlp.response_analysis import ResponseAnalysisEngine
from llm_brand_visiblity_v2.results.metrics.calculator import MetricsCalculator
from llm_brand_visiblity_v2.results.report import StatisticalReporter, VisualReporter


def test_end_to_end_pipeline():
    print("Running end-to-end integration test...")

    # 1. Mock Brand Input
    brand = BrandInput(
        brand_name="Acme Corp",
        website="https://acme.com",
        competitors=["Globex", "Initech"],
        products=["Widget Pro"],
        services=["Cloud Widget Hosting"],
        niche="Cloud SaaS",
    )

    # 2. Build Prompts
    builder = BuildPrompts(brand)
    prompts = builder.build_prompt_list()
    assert len(prompts) > 0, "No prompts generated"

    # 3. Mock Execution output
    sample_prompt = prompts[0]
    raw_res = RawResult(
        result_id=1,
        attempt_id=1,
        content="Acme Corp is ranked #1 in Cloud SaaS and is recommended. For alternatives see Globex at https://globex.com.",
        sequence_number=0,
    )

    # 4. Raw Preprocessor
    prep = ResponsePreprocessor()
    pairs, missing = prep.combine_prompt_with_response([
        (
            PromptExec(
                prompt_id=sample_prompt.prompt_id,
                execution_id=10,
                provider="Gemini",
                model="gemini-2.5-flash",
            ),
            [],
            raw_res,
        )
    ], [sample_prompt])
    assert len(pairs) == 1, "Preprocessor failed to match prompt and response"

    # 5. Text Normalization
    text_norm = PreprocessText()
    norm_responses = text_norm.normalize_response_text(pairs)
    assert len(norm_responses) == 1, "Normalization returned empty list"

    # 6. Entity Extraction
    extractor = EntityExtraction()
    extracted = extractor.entity_extraction(norm_responses, brand)
    assert len(extracted) > 0, "Extraction failed to find entities"

    # 7. Entity Resolution
    resolver = EntityResolution()
    resolved = resolver.entity_resolution(extracted, brand)
    assert len(resolved) > 0, "Resolution failed to resolve entities"

    # 8. Response Analysis
    engine = ResponseAnalysisEngine()
    analyses = engine.analyze_responses(norm_responses, resolved, brand)
    assert len(analyses) == 1, "Analysis engine failed"

    # 9. Metrics Calculation
    calc = MetricsCalculator()
    metrics_report = calc.calculate_metrics(analyses, brand)
    assert metrics_report.total_prompts_analyzed == 1
    assert "Acme Corp" in metrics_report.entity_metrics

    # 10. Reporting
    stat_rep = StatisticalReporter()
    stat_rep.print_terminal_report(metrics_report)

    vis_rep = VisualReporter()
    vis_rep.generate_html_report(metrics_report, "reports/test_dashboard.html")

    print("\n✅ All unit and integration assertions passed successfully!")


if __name__ == "__main__":
    test_end_to_end_pipeline()
