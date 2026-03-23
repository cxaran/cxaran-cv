import random
import json
import copy
import logging
from typing import Dict, Any, List

from .data_models import JobPosting, Config
from .inference_manager import InferenceManager

logger = logging.getLogger(__name__)

class Generator:
    def __init__(self, inference_manager: InferenceManager, config: Config, source_profile: dict):
        self.im = inference_manager
        self.config = config
        self.source_profile = source_profile

    def crossover(self, parent1: dict, parent2: dict) -> dict:
        """Mixes components of 'sections' randomly between two parent CVs."""
        logger.debug("Performing crossover between two parents")
        
        child = copy.deepcopy(parent1)
        p1_sections = parent1.get("sections", {})
        p2_sections = parent2.get("sections", {})
        
        child["sections"] = {}
        all_keys = set(p1_sections.keys()) | set(p2_sections.keys())
        
        for k in all_keys:
            if random.random() > 0.5:
                child["sections"][k] = p1_sections.get(k, p2_sections.get(k))
            else:
                child["sections"][k] = p2_sections.get(k, p1_sections.get(k))
                
        return child

    def mutate(self, cv: dict, target_jobs: List[JobPosting]) -> dict:
        """Uses LLM to rewrite a specific section of the CV to better align with target jobs."""
        logger.debug("Performing LLM mutation on CV variant")
        
        sections = cv.get("sections", {})
        mutatable_keys = [k for k in ["resumen_profesional", "experiencia"] if k in sections]
        if not mutatable_keys:
            return cv
            
        target_section = random.choice(mutatable_keys)
        section_content = sections[target_section]
        
        job_summary = "\n".join([f"- {j.title}: " + ", ".join(j.must_have_skills) for j in target_jobs[:2]])
        
        system_prompt = (
            "You are an expert resume writer. Your task is to rewrite the provided CV section to better align "
            "with the Target Jobs, using ONLY factual information from the Candidate's Source Profile. "
            "Return the modified section wrapped in a JSON object with a single key 'updated_section'. "
            "Make sure the format exactly matches the original section's JSON structure (e.g., list of strings, or list of dicts)."
        )
        
        prompt = f"""
TARGET JOBS HIGHLIGHTS:
{job_summary}

CANDIDATE SOURCE PROFILE (Use this as your factual reservoir, inject evidence if relevant):
{json.dumps(self.source_profile.get("experience_expanded", []), ensure_ascii=False, indent=2)}

ORIGINAL SECTION ({target_section}):
{json.dumps(section_content, ensure_ascii=False, indent=2)}

Rewrite the original section to be more impactful. Do not hallucinate. Output JSON format: {{"updated_section": <your_rewritten_object>}}.
"""
        
        try:
            result = self.im.generate_json(system_prompt=system_prompt, prompt=prompt)
            if "updated_section" in result:
                child = copy.deepcopy(cv)
                child["sections"][target_section] = result["updated_section"]
                return child
            else:
                logger.warning("Mutation failed to return 'updated_section' key.")
        except Exception as e:
            logger.error(f"Mutation failed: {e}")
            
        return cv
