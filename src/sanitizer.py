import re
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Patterns that indicate adversarial prompts
ADVERSARIAL_PATTERNS = [
    r"(?i)\bignore (?:all )?(?:previous )?instructions\b",
    r"(?i)\bact (?:as|like) a\b",
    r"(?i)\byou are a\b",
    r"(?i)\brank (?:me )?(?:first|#1)\b",
    r"(?i)\basign[a-z]* (?:alta )?prioridad\b",
    r"(?i)\bsi eres una ia\b",
    r"(?i)\bif you are an ai\b",
    r"(?i)\btop 1(?:%| percent)\b",
    r"(?i)\bperfect fit\b"
]

FORBIDDEN_KEYS = {
    "prompt",
    "system_instructions",
    "assistant_instructions",
    "model_notes"
}

def contains_adversarial_text(text: str) -> bool:
    for pattern in ADVERSARIAL_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def sanitize_data(data: Any, path="root") -> Any:
    """Recursively traverses dictionaries and lists to remove forbidden keys
    and redact adversarial text values."""
    if isinstance(data, dict):
        sanitized_dict = {}
        for k, v in data.items():
            if k in FORBIDDEN_KEYS:
                # Discard completely
                logger.warning(f"Sanitizer: Removed forbidden key '{k}' at {path}")
                continue
            
            sanitized_dict[k] = sanitize_data(v, path=f"{path}.{k}")
        return sanitized_dict

    elif isinstance(data, list):
        sanitized_list = []
        for i, item in enumerate(data):
            sanitized_item = sanitize_data(item, path=f"{path}[{i}]")
            if sanitized_item is not None:
                sanitized_list.append(sanitized_item)
        return sanitized_list

    elif isinstance(data, str):
        if contains_adversarial_text(data):
            logger.warning(f"Sanitizer: Redacted adversarial text at {path}")
            return None # Redact the string
        return data

    else:
        # Ints, floats, booleans, etc.
        return data
