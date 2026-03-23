from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any

# ================= Configuration Models =================

class ModelDef(BaseModel):
    id: str
    enabled: bool
    weight: float
    supports_structured_outputs: bool
    supports_general_text: bool

class ModelSelectionConfig(BaseModel):
    strategy: str
    with_replacement: bool
    min_models_per_round: int
    max_models_per_round: int
    require_structured_outputs_for_evaluation: bool
    require_general_text_for_generation: bool
    cooldown_on_failure: bool
    cooldown_rounds: int

class FilesConfig(BaseModel):
    seed_cv_file: str
    source_profile_file: str
    target_jobs_file: str

class ConstraintsConfig(BaseModel):
    max_pages: int
    max_bullets_per_role: int
    max_words_summary: int
    allow_hallucinated_content: bool
    require_source_traceability: bool
    allow_prompt_fields: bool
    allow_instructional_content: bool

class APIConfig(BaseModel):
    request_timeout_seconds: int
    max_retries: int
    retry_backoff_seconds: int
    parallel_requests: int

class ProviderConfig(BaseModel):
    llm_provider: str
    llm_api_base_url: str
    llm_api_key_env: str
    llm_api_mode: str

class EvolutionConfig(BaseModel):
    population_size: int
    num_generations: int
    elite_ratio: float
    selection_ratio: float
    exploration_ratio: float
    exploitation_ratio: float
    selection_method: str
    tournament_size: int
    mutation_rate: float
    strong_mutation_rate: float
    crossover_rate: float
    content_injection_rate: float

class EvaluationConfig(BaseModel):
    score_scale_min: int
    score_scale_max: int
    variance_penalty_weight: float
    job_coverage_weight: float
    ats_weight: float
    evidence_density_weight: float
    aggregation_method: str
    evaluator_sampling: str

class SchedulerConfig(BaseModel):
    throttle_on_429: bool
    retry_on_429: bool
    retry_jitter: bool

class Config(BaseModel):
    provider: ProviderConfig
    model_pool: List[ModelDef]
    model_selection: ModelSelectionConfig
    files: FilesConfig
    constraints: ConstraintsConfig
    evolution: EvolutionConfig
    evaluation: EvaluationConfig
    api: APIConfig
    scheduler: SchedulerConfig

# ================= Target Jobs Models =================

class JobPosting(BaseModel):
    job_id: str
    title: str
    company: str
    source_url: Optional[str] = None
    seniority: Optional[str] = None
    industry: Optional[str] = None
    description: str
    requirements: List[str]
    responsibilities: List[str]
    must_have_skills: List[str]
    nice_to_have_skills: List[str]
    keywords_ats: List[str]

class TargetJobsData(BaseModel):
    jobs: List[JobPosting]

# ================= CV & Profile Models =================
# Since YAML structures can be quite dynamic, we'll keep some sections flexible 
# but define the known schema blocks.

class SeedCVData(BaseModel):
    model_config = ConfigDict(extra="allow")
    cv: Dict[str, Any]
    design: Optional[Dict[str, Any]] = None

class SourceProfileData(BaseModel):
    model_config = ConfigDict(extra="allow")
    candidate: Dict[str, Any]
    positioning_profiles: List[Dict[str, Any]]
    core_summary: Optional[Dict[str, Any]] = None
    experience_expanded: List[Dict[str, Any]]
    projects_expanded: List[Dict[str, Any]]
    education_expanded: Optional[List[Dict[str, Any]]] = None
    publications: Optional[List[Dict[str, Any]]] = None
    academic_and_teaching_activity: Optional[List[Dict[str, Any]]] = None
    skills_catalog: Optional[Dict[str, List[str]]] = None
    languages: Optional[List[Dict[str, str]]] = None
    ats_evidence: List[str]
    cv_strategy_notes: Optional[Dict[str, Any]] = None
