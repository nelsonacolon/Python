"""Project-local helper functions to provide print_llm_response for LLM.py

This file intentionally shadows the installed `helper_functions` package when
imported from the project folder so `from helper_functions import print_llm_response`
resolves to this local implementation.
"""
import json
from typing import Any

__all__ = ["print_llm_response"]


def print_llm_response(resp: Any) -> None:
    """Pretty-print an LLM-style response.

    - If resp is a mapping (dict-like), prints keys and pretty JSON for values.
    - If resp is a string, prints the string.
    - If resp is an object with `get("content")` or similar, attempts reasonable formatting.
    """
    # Mapping-like
    try:
        from collections.abc import Mapping
    except Exception:
        Mapping = dict

    if isinstance(resp, Mapping):
        for k, v in resp.items():
            try:
                print(f"{k}:")
                print(json.dumps(v, indent=2, ensure_ascii=False))
            except Exception:
                print(f"{k}: {v}")
    elif isinstance(resp, str):
        print(resp)
    else:
        # Try to serialize unknown objects
        try:
            print(json.dumps(resp, indent=2, ensure_ascii=False))
        except Exception:
            print(str(resp))
