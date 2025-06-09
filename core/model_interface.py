# core/model_interface.py

import subprocess
import json
import os

ATTRIB_FILE = "model_types.json"

def load_model_attributes():
    if not os.path.exists(ATTRIB_FILE):
        return {}
    with open(ATTRIB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_model_attributes(attr_dict):
    with open(ATTRIB_FILE, "w", encoding="utf-8") as f:
        json.dump(attr_dict, f, indent=2)

def run_prompt_via_powershell(model_name: str, prompt: str) -> str:
    ps_command = f"echo \"{prompt}\" | ollama run {model_name}"

    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=120,
            encoding = 'utf-8',
            errors='replace'
        )
        if result.returncode != 0:
            return f"[PowerShell Error]\n{result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"[Exception] {str(e)}"

def get_installed_models() -> list:
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0:
            return ["starcoder2", "mistral", "qwen2.5-coder"]  # fallback

        lines = result.stdout.strip().split('\n')
        models = [line.split()[0] for line in lines[1:] if line.strip()]
        return models
    except Exception:
        return ["starcoder2", "mistral", "qwen2.5-coder"]
