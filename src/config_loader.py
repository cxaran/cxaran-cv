import yaml
from pathlib import Path
from typing import Union
from .data_models import Config, TargetJobsData, SeedCVData, SourceProfileData

def load_yaml(filepath: Union[str, Path]) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_config(filepath: Union[str, Path]) -> Config:
    data = load_yaml(filepath)
    return Config(**data)

def load_target_jobs(filepath: Union[str, Path]) -> TargetJobsData:
    data = load_yaml(filepath)
    return TargetJobsData(**data)

def load_seed_cv(filepath: Union[str, Path]) -> SeedCVData:
    data = load_yaml(filepath)
    return SeedCVData(**data)

def load_source_profile(filepath: Union[str, Path]) -> SourceProfileData:
    data = load_yaml(filepath)
    return SourceProfileData(**data)
