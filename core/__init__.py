# core/__init__.py

from .functions import (
    get_installed_models,
    load_model_attributes,
    save_model_attributes,
    check_ollama_available,
    OLLAMA_BIN,
    start_model_background,
    query_model_api
    # run_prompt_interactive
)

# On module load, try to start default model if present
DEFAULT_MODEL = "mistral"
INSTALLED_MODELS = get_installed_models()

if DEFAULT_MODEL in INSTALLED_MODELS:
    start_model_background(DEFAULT_MODEL)
