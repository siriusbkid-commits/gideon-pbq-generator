import json
import urllib.request
import urllib.error
from config import SIMULATOR_MODE, LOCAL_MODEL


class LocalOllamaLLM:
    """
    Offline LLM wrapper for Ollama using the REST API.
    Uses http://localhost:11434/api/generate instead of subprocess
    to avoid terminal line-wrapping artifacts.
    """

    def __init__(self, model: str):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def call(self, prompt: str) -> str:
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }).encode("utf-8")

        req = urllib.request.Request(
            self.api_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=600) as response:
                body = response.read().decode("utf-8")
                data = json.loads(body)
                return data.get("response", "")
        except urllib.error.URLError as e:
            return f"ERROR: Ollama API call failed: {e}"
        except Exception as e:
            return f"ERROR: Unexpected error calling Ollama API: {e}"


def get_llm():
    """
    Always return the local offline LLM.
    Cloud mode removed permanently.
    """
    return LocalOllamaLLM(model=LOCAL_MODEL)
