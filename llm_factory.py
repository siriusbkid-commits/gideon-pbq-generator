import subprocess
import json
from config import SIMULATOR_MODE, LOCAL_MODEL


class LocalOllamaLLM:
    """
    Minimal offline LLM wrapper for Ollama.
    Calls: ollama run <model> "<prompt>"
    """

    def __init__(self, model: str):
        self.model = model

    def call(self, prompt: str) -> str:
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            return result.stdout.decode("utf-8")

        except Exception as e:
            return f"ERROR: Local Ollama call failed: {e}"


def get_llm():
    """
    Always return the local offline LLM.
    Cloud mode removed permanently.
    """

    return LocalOllamaLLM(model=LOCAL_MODEL)

