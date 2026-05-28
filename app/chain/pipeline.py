# Motorn i hela uppgiften
from app.chain.steps import PromptBuilder, LLMRunner, ResponseParser

oraklet_pipeline = (
    PromptBuilder()
    | LLMRunner()
    | ResponseParser()
)