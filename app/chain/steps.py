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
You are a strict data analysis assistant.

RULES: 
- Only use the dataset provided below.
- If the answer cannot be derived from the dataset, say: "Not enough data in dataset"
- Do NOT guess or use external knowledge.
- Be concise and factual.

Dataset statistics:
{input.dataset_summary}

Question:
{input.question}

ANSWER (1-3 sentences only):
"""
        return PromptBuilderOutput(
            prompt=prompt,
            question=input.question
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
            raw_response=raw_text,
            question= input.question
        )
    
class ResponseParser(
    Runnable[LLMRunnerOutput, AskResponse]
):
    def invoke(
        self,
        input: LLMRunnerOutput
    ) -> AskResponse:
        
        text = input.raw_response

        # ta bort originalprompten
        if "ANSWER (1-3 sentences only):" in text:
            text = text.split("ANSWER (1-3 sentences only):")[-1]

        text = text.strip()

        # ta första stycket bara
        text = text.split("\n\n")[0]

        # fallback om modellen svarar tomt
        if not text:
            text = "Model returned empty response."

        return AskResponse(
            question=input.question,
            answer=text,
            model="HuggingFaceTB/smolLM2-135M-Instruct"
        )