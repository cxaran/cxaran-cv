import os
import json
import yaml
import logging
from pathlib import Path

from src.config_loader import load_config, load_seed_cv, load_source_profile, load_target_jobs
from src.inference_manager import InferenceManager
from src.evaluator import Evaluator
from src.generator import Generator
from src.engine import EvolutionEngine
from src.sanitizer import sanitize_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger(__name__)

def ensure_dir(d: Path):
    d.mkdir(parents=True, exist_ok=True)

def main():
    root_dir = Path(__file__).parent.parent
    input_dir = root_dir / "input"
    output_dir = root_dir / "output"
    
    config = load_config(input_dir / "config.yaml")
    seed_cv = load_seed_cv(input_dir / "seed_cv.yaml")
    source_profile = load_source_profile(input_dir / "source_profile.yaml")
    target_jobs = load_target_jobs(input_dir / "target_jobs.yaml")
    
    logger.info("Sanitizing inputs before running evolution...")
    safe_seed = sanitize_data(seed_cv.model_dump())
    safe_profile = sanitize_data(source_profile.model_dump())
    
    im = InferenceManager(config)
    evaluator = Evaluator(im, config)
    generator = Generator(im, config, safe_profile)
    
    engine = EvolutionEngine(config, evaluator, generator, target_jobs.jobs)
    
    logger.info("Starting CV Evolution Loop...")
    final_population = engine.run(safe_seed["cv"])
    
    logger.info("Evolution complete. Exporting results to output folder...")
    
    gen_dir = output_dir / "final"
    ensure_dir(gen_dir)
    
    best_variant = final_population[0]
    best_cv_path = gen_dir / "best_cv.yaml"
    with open(best_cv_path, "w", encoding="utf-8") as f:
        out_yaml = {"cv": best_variant.cv_data, "design": safe_seed.get("design")}
        yaml.dump(out_yaml, f, allow_unicode=True, sort_keys=False)
        
    logger.info(f"Saved best CV to {best_cv_path}")
    
    report = {
        "best_fitness": best_variant.fitness,
        "best_scores": best_variant.scores,
        "best_lineage": best_variant.lineage,
        "top_5_fitness": [p.fitness for p in final_population[:5]]
    }
    
    report_path = gen_dir / "final_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    logger.info(f"Saved evolution report to {report_path}")

if __name__ == "__main__":
    main()
