from app.chain.runnable import Runnable
from transformers import pipeline

from app.schemas import (
    PromptBuilderInput,
    PromptBuilderOutput,
    LLMRunnerOutput,
    AskResponse
)

generator = pipeline(
    "text-generation",
    model="HuggingFaceTB/smolLM2-135M-Instruct"
)

class PromptBuilder(
    Runnable[PromptBuilderInput, PromptBuilderOutput]
):
    def invoke(
        self,
        input: PromptBuilderInput
    ) -> PromptBuilderOutput:
        
        prompt = f"""
You are a helpful data analyst AI.
Use the dataset statistics below to answer the question.

Dataset statistics:
{input.dataset_summary}

Question:
{input.question}

Answer clearly and briefly.
"""
        return PromptBuilderOutput(
            prompt=prompt
        )
    
class LLMRunner(
    Runnable[PromptBuilderOutput, LLMRunnerOutput]
):
    def invoke(
        self, 
        input: PromptBuilderOutput
    ) -> LLMRunnerOutput:
        
        result = generator(
            input.prompt,
            max_new_tokens=100
        )

        raw_text = result[0]["generated_text"]

        return LLMRunnerOutput(
            raw_response=raw_text
        )
    
class ResponseParser(
    Runnable[LLMRunnerOutput, AskResponse]
):
    def invoke(
        self,
        inout: LLMRunnerOutput
    ) -> AskResponse:
        
        answer = input.raw_response

        return AskResponse(
            question="unknown",
            answer=answer,
            model="HuggingFaceTB/smolLM2-135M-Instruct"
        )