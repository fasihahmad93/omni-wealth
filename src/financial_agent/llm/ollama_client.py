import logging
import requests

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url="http://127.0.0.1:11434", model="qwen3.5:4b", timeout=120):
        logger.info("Initializing OllamaClient model=%s base_url=%s", model, base_url)
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        logger.info("Sending prompt to Ollama model=%s prompt_length=%s", self.model, len(prompt))
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=self.timeout,
        )
        response.raise_for_status()
        result = response.json()["response"]
        logger.info("Received Ollama response length=%s", len(result))
        return result
