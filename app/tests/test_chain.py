from app.chain.steps import PromptBuilder,PromptBuilderInput, LLMRunner, PromptBuilderOutput

def test_prompt_builder():
    step = PromptBuilder()

    input_data = PromptBuilderInput(
        question="What is this dataset?",
        dataset_summary="mean=10 std=2"
    )

    output = step.invoke(input_data)

    assert "What is this dataset?" in output.prompt
    assert "mean=10 std=2" in output.prompt
    

def test_llm_runner(monkeypatch):
    def fake_pipeline(*args, **kwargs):
        return [{"generated_text": "ANSWER: test response"}]

    monkeypatch.setattr("app.chain.steps.generator", fake_pipeline)

    step = LLMRunner()

    input_data = PromptBuilderOutput(
        prompt="fake prompt",
        question="test?"
    )

    output = step.invoke(input_data)

    assert "test response" in output.raw_response
    assert output.question == "test?"