import random
import logging
import copy
from typing import List, Dict, Any

from .data_models import Config, JobPosting
from .evaluator import Evaluator
from .generator import Generator

logger = logging.getLogger(__name__)

class Variant:
    def __init__(self, cv_data: dict):
        self.cv_data = cv_data
        self.fitness: float = 0.0
        self.scores: dict = {}
        self.lineage: List[str] = ["seed"]

class EvolutionEngine:
    def __init__(self, config: Config, evaluator: Evaluator, generator: Generator, target_jobs: List[JobPosting]):
        self.config = config
        self.evaluator = evaluator
        self.generator = generator
        self.target_jobs = target_jobs

    def _calculate_fitness(self, variant: Variant):
        evaluation_results = []
        for job in self.target_jobs:
            scores = self.evaluator.evaluate_variant(variant.cv_data, job)
            evaluation_results.append(scores)
        
        if not evaluation_results:
            return

        total_job = sum(e.job_coverage_score for e in evaluation_results) / len(evaluation_results)
        total_ats = sum(e.ats_match_score for e in evaluation_results) / len(evaluation_results)
        total_ev = sum(e.evidence_density_score for e in evaluation_results) / len(evaluation_results)
        
        variant.scores = {
            "job_coverage": total_job, 
            "ats_match": total_ats, 
            "evidence_density": total_ev
        }
        
        c = self.config.evaluation
        variant.fitness = (
            total_job * c.job_coverage_weight +
            total_ats * c.ats_weight +
            total_ev * c.evidence_density_weight
        )

    def run(self, seed_cv: dict) -> List[Variant]:
        population_size = self.config.evolution.population_size
        num_generations = self.config.evolution.num_generations
        
        logger.info(f"Initializing population of size {population_size}")
        population = [Variant(copy.deepcopy(seed_cv)) for _ in range(population_size)]
        
        for idx, variant in enumerate(population):
            logger.info(f"Evaluating initial seed variant {idx + 1}/{population_size}")
            self._calculate_fitness(variant)
            
        for generation in range(num_generations):
            logger.info(f"--- Generation {generation + 1}/{num_generations} ---")
            
            # Sort descending by fitness
            population.sort(key=lambda x: x.fitness, reverse=True)
            
            elite_count = int(population_size * self.config.evolution.elite_ratio)
            elites = population[:elite_count]
            new_population = list(elites)
            
            # Record elite retention
            for elite in elites:
                elite.lineage.append(f"gen_{generation}_elite")
            
            while len(new_population) < population_size:
                # Tournament Selection
                tournament1 = random.sample(population, self.config.evolution.tournament_size)
                parent1 = max(tournament1, key=lambda x: x.fitness)
                
                tournament2 = random.sample(population, self.config.evolution.tournament_size)
                parent2 = max(tournament2, key=lambda x: x.fitness)
                
                # Crossover
                if random.random() < self.config.evolution.crossover_rate:
                    child_cv = self.generator.crossover(parent1.cv_data, parent2.cv_data)
                    lineage_tag = f"gen_{generation}_crossover"
                else:
                    child_cv = copy.deepcopy(parent1.cv_data)
                    lineage_tag = f"gen_{generation}_clone"
                
                # Mutation
                if random.random() < self.config.evolution.mutation_rate:
                    child_cv = self.generator.mutate(child_cv, self.target_jobs)
                    lineage_tag += "+mutation"
                    
                child = Variant(child_cv)
                child.lineage = parent1.lineage.copy()
                child.lineage.append(lineage_tag)
                
                self._calculate_fitness(child)
                new_population.append(child)
                
            population = new_population
            best_fitness = max(p.fitness for p in population)
            avg_fitness = sum(p.fitness for p in population) / len(population)
            logger.info(f"Gen {generation + 1} complete. Best Fitness: {best_fitness:.2f}, Avg: {avg_fitness:.2f}")

        population.sort(key=lambda x: x.fitness, reverse=True)
        return population
