import ollama
import json


class LLMClient:

    def __init__(self, model: str = "qwen2.5:3b"):
        self.model = model


    def generate(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.2,
                    "num_predict": 300     # This increases output length
                    }
            )

            return response["message"]["content"]

        except Exception as e:
            print(f"LLM error: {e}")
            return ""


    def generate_json(self, prompt: str):
        text = self.generate(prompt)

        try:
            return json.loads(text)
        except:
            return {"error": "Invalid JSON", "raw": text}