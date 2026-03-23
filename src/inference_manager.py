import os
import random
import time
import logging
from typing import List, Type, TypeVar, Optional, Any
from pydantic import BaseModel
from openai import OpenAI

from .data_models import Config, ModelDef

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class InferenceManager:
    """
    Manages communication with Groq APIs, implementing a dynamic model pool,
    weighted random sampling, structured output routing, and cooldown logic 
    for rate-limiting or errors.
    """
    def __init__(self, config: Config):
        self.config = config
        
        env_val = config.provider.llm_api_key_env
        # Si no se encuentra en las variables de entorno, asume que se pegó la llave directamente en el YAML
        api_key = os.environ.get(env_val, env_val)
        
        # Imprime la llave (enmascarada parcialmente por seguridad) para debugear
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else api_key
        logger.info(f"[DEBUG] Inicializando cliente OpenAI con API Key: {masked_key}")
        
        if api_key == env_val and not api_key.startswith("gsk_") and api_key != "GROQ_API_KEY":
            logger.warning(f"Cuidado: '{env_val}' no se encontró en 'os.environ' y no parece ser una llave válida de Groq.")
            
        self.client = OpenAI(
            api_key=api_key or "dummy_key",
            base_url=config.provider.llm_api_base_url,
            timeout=config.api.request_timeout_seconds
        )
        
        self.cooldowns: dict[str, int] = {}
        self.current_round = 0

    def get_available_models(self, requires_structured: bool = False) -> List[ModelDef]:
        pool = self.config.model_pool
        sel_cfg = self.config.model_selection
        
        candidates = [m for m in pool if m.enabled]
        
        if requires_structured and sel_cfg.require_structured_outputs_for_evaluation:
            candidates = [m for m in candidates if m.supports_structured_outputs]
        elif not requires_structured and sel_cfg.require_general_text_for_generation:
            candidates = [m for m in candidates if m.supports_general_text]
            
        if sel_cfg.cooldown_on_failure:
            available = []
            for m in candidates:
                if m.id in self.cooldowns:
                    if self.current_round < self.cooldowns[m.id]:
                        continue
                    else:
                        del self.cooldowns[m.id]
                available.append(m)
            candidates = available

        return candidates

    def _select_model(self, requires_structured: bool = False) -> ModelDef:
        candidates = self.get_available_models(requires_structured)
        
        if not candidates:
            raise RuntimeError(f"No available models in pool for requires_structured={requires_structured}")

        if self.config.model_selection.strategy == "weighted_random":
            weights = [m.weight for m in candidates]
            selected = random.choices(candidates, weights=weights, k=1)[0]
        else:
            # Fallback to pure uniform random
            selected = random.choice(candidates)
            
        logger.info(f"Selected model: {selected.id}")
        return selected

    def _apply_cooldown(self, model_id: str):
        if self.config.model_selection.cooldown_on_failure:
            duration = self.config.model_selection.cooldown_rounds
            self.cooldowns[model_id] = self.current_round + duration
            logger.warning(f"Applied cooldown to {model_id} until round {self.cooldowns[model_id]}")

    def call_llm(self, prompt: str, system_prompt: str = "You are a helpful assistant.", 
                 requires_structured: bool = False, response_format: Optional[Type[T]] = None) -> Any:
        
        self.current_round += 1
        retries = self.config.api.max_retries
        backoff = self.config.api.retry_backoff_seconds

        for attempt in range(retries):
            model = self._select_model(requires_structured=requires_structured)
            
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                kwargs = {
                    "model": model.id,
                    "messages": messages,
                }
                
                if requires_structured and response_format:
                    # Using OpenAI Beta parse for structured json schema
                    completion = self.client.beta.chat.completions.parse(
                        **kwargs,
                        response_format=response_format
                    )
                    return completion.choices[0].message.parsed
                else:
                    completion = self.client.chat.completions.create(**kwargs)
                    return completion.choices[0].message.content
                    
            except Exception as e:
                logger.error(f"Attempt {attempt+1}/{retries} failed on model {model.id}: {e}")
                
                if "429" in str(e) and self.config.scheduler.throttle_on_429:
                    self._apply_cooldown(model.id)
                else:
                    # On other errors, also cool it down to avoid hammering a broken endpoint
                    self._apply_cooldown(model.id)
                
                if attempt < retries - 1:
                    sleep_time = backoff * (attempt + 1)
                    if self.config.scheduler.retry_jitter:
                        sleep_time += random.uniform(0, 1)
                    logger.info(f"Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                else:
                    logger.error("Max retries exceeded.")
                    raise

    def generate_text(self, system_prompt: str, prompt: str) -> str:
        return self.call_llm(prompt=prompt, system_prompt=system_prompt, requires_structured=False)
        
    def generate_structured(self, system_prompt: str, prompt: str, response_format: Type[T]) -> T:
        return self.call_llm(prompt=prompt, system_prompt=system_prompt, requires_structured=True, response_format=response_format)

    def generate_json(self, system_prompt: str, prompt: str) -> dict:
        """Shorthand for generating arbitrary JSON using the json_object mode instead of a strict Pydantic class."""
        self.current_round += 1
        retries = self.config.api.max_retries
        backoff = self.config.api.retry_backoff_seconds

        for attempt in range(retries):
            model = self._select_model(requires_structured=True)
            
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                kwargs = {
                    "model": model.id,
                    "messages": messages,
                    "response_format": {"type": "json_object"}
                }
                completion = self.client.chat.completions.create(**kwargs)
                import json
                return json.loads(completion.choices[0].message.content)
            except Exception as e:
                logger.error(f"Attempt {attempt+1}/{retries} failed on model {model.id} (JSON Mode): {e}")
                if "429" in str(e) and self.config.scheduler.throttle_on_429:
                    self._apply_cooldown(model.id)
                else:
                    self._apply_cooldown(model.id)
                
                if attempt < retries - 1:
                    sleep_time = backoff * (attempt + 1)
                    if self.config.scheduler.retry_jitter:
                        sleep_time += random.uniform(0, 1)
                    time.sleep(sleep_time)
                else:
                    raise
