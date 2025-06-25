# core/functions.py

import threading
import subprocess
import json
import os
import queue
import ollama

import time
# import tkinter as tk


output_queue = queue.Queue()
ATTRIB_FILE = "model_types.json"

# Globals

# Just the directory path
OLLAMA_DIR = r"C:\Users\Louis\AppData\Local\Programs\Ollama"
# OLLAMA_DIR = r"C:\Users\Louis"

# When you need to run a command:
OLLAMA_BIN = os.path.join(OLLAMA_DIR, "ollama.exe")
# send_prompt_async(prompt, selected_model, handle_response_line, OLLAMA_PATH)


def query_model_api(model_name: str, prompt: str) -> str:
    try:
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            stream=False  # stream=False makes it easy for GUI integration
        )
        return response['response']
    except Exception as e:
        return f"[Error calling model '{model_name}']: {str(e)}"


def check_ollama_available():
    try:
        print(f"[DEBUG] OLLAMA_BIN = {OLLAMA_BIN}")
        result = subprocess.run(
            [OLLAMA_BIN, "--version"],
            capture_output=True,
            text=True,
            timeout=5  # seconds
        )
        print(f"[DEBUG] return code = {result.returncode}")
        print(f"[DEBUG] stdout = {result.stdout.strip()}")
        print(f"[DEBUG] stderr = {result.stderr.strip()}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("[ERROR] Timeout: ollama.exe took too long.")
        return False
    except FileNotFoundError:
        print("[ERROR] ollama.exe not found at path.")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def start_model_background(model="mistral"):
    """Launch model in background so it's warmed up for use."""
    try:
        subprocess.Popen(
            [OLLAMA_BIN, "run", model],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        return True
    except Exception as e:
        print(f"[ERROR] Failed to start model '{model}': {e}")
        return False


def load_model_attributes():
    if not os.path.exists(ATTRIB_FILE):
        return {}
    with open(ATTRIB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_model_attributes(attr_dict):
    with open(ATTRIB_FILE, "w", encoding="utf-8") as f:
        json.dump(attr_dict, f, indent=2)


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



