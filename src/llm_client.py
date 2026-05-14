import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "https://ollama.com")
        self.model = os.getenv("MODEL", "gpt-oss:120b")
        self.api_key = os.getenv("OLLAMA_API_KEY", "")

    def chat(self, prompt, system=None, temp=0.7, max_tokens=512):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": temp,
                "num_predict": max_tokens
            },
            "stream": False
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        for tentativa in range(3):
            try:
                inicio = time.time()
                resp = requests.post(
                    f"{self.host}/api/chat",
                    json=payload,
                    headers=headers,
                    timeout=120
                )
                resp.raise_for_status()
                data = resp.json()
                tempo_ms = int((time.time() - inicio) * 1000)

                resposta = data.get("message", {}).get("content", "")
                tokens_prompt = data.get("prompt_eval_count", 0)
                tokens_resposta = data.get("eval_count", 0)

                return {
                    "resposta": resposta,
                    "tokens_prompt": tokens_prompt,
                    "tokens_resposta": tokens_resposta,
                    "tempo_ms": tempo_ms
                }

            except requests.exceptions.Timeout:
                print(f"Timeout na tentativa {tentativa + 1}/3")
                time.sleep(2)
            except requests.exceptions.ConnectionError as e:
                print(f"Erro de conexão: {e}")
                time.sleep(2)
            except requests.exceptions.HTTPError as e:
                print(f"Erro HTTP {resp.status_code}: {e}")
                break

        return {
            "resposta": "[ERRO: LLM indisponível]",
            "tokens_prompt": 0,
            "tokens_resposta": 0,
            "tempo_ms": 0
        }
