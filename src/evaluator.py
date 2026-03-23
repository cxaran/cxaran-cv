import json
import logging
from pydantic import BaseModel, Field
from typing import Dict, Any

from .data_models import JobPosting, Config
from .inference_manager import InferenceManager

logger = logging.getLogger(__name__)

class EvaluationScores(BaseModel):
    job_coverage_score: int = Field(ge=1, le=5, description="Adjusted fit against the Target Job requirements.")
    ats_match_score: int = Field(ge=1, le=5, description="How well this CV passes ATS keyword parsing.")
    evidence_density_score: int = Field(ge=1, le=5, description="Density of verifiable facts, metrics, and achievements.")
    reasoning: str = Field(description="Brief justification of the scores provided.")

class Evaluator:
    def __init__(self, inference_manager: InferenceManager, config: Config):
        self.im = inference_manager
        self.config = config

    def evaluate_variant(self, cv_variant: Dict[str, Any], job: JobPosting) -> EvaluationScores:
        logger.debug(f"Evaluating CV against job {job.job_id}")
        system_prompt = (
            "You are an expert technical recruiter and ATS software simulator. "
            "You must evaluate the provided Candidate CV against the Target Job Description. "
            f"Score dimensions on a scale of {self.config.evaluation.score_scale_min} to {self.config.evaluation.score_scale_max}."
        )
        
        prompt = f"""
TARGET JOB:
Title: {job.title}
Company: {job.company}
Requirements: {json.dumps(job.requirements, ensure_ascii=False)}
Must Have Skills: {json.dumps(job.must_have_skills, ensure_ascii=False)}

CANDIDATE CV:
{json.dumps(cv_variant, ensure_ascii=False, indent=2)}

Please evaluate this CV and provide the structured scores alongside a brief reasoning.
"""
        return self.im.generate_structured(
            system_prompt=system_prompt,
            prompt=prompt,
            response_format=EvaluationScores
        )
