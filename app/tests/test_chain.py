from app.chain.steps import PromptBuilder
from app.chain.steps import PromptBuilderInput

def test_prompt_builder():
    step = PromptBuilder()

    input_data = PromptBuilderInput(
        question="What is this dataset?",
        dataset_summary="mean=10 std=2"
    )

    output = step.invoke(input_data)

    assert "What is this dataset?" in output.prompt
    assert "mean=10 std=2" in output.prompt
    

