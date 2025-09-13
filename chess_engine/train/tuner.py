"""
Weight Tuner - Genetic Algorithm for optimizing evaluation weights

This module implements:
- Genetic algorithm for weight optimization
- Hill climbing as alternative optimization
- Fitness evaluation using game results
- Population management and selection
"""

import random
import json
import copy
from typing import List, Dict, Tuple, Any, Optional
from ..eval.evaluation import EvaluationEngine
from ..board.board import ChessBoard, Color
from ..search.minimax import MinimaxEngine

class Individual:
    """Individual in genetic algorithm population"""
    
    def __init__(self, weights: Dict[str, float], fitness: float = 0.0):
        self.weights = weights
        self.fitness = fitness
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
    
    def get_win_rate(self) -> float:
        """Calculate win rate"""
        if self.games_played == 0:
            return 0.0
        return (self.wins + 0.5 * self.draws) / self.games_played
    
    def __str__(self):
        return f"Individual(fitness={self.fitness:.3f}, win_rate={self.get_win_rate():.3f})"

class WeightTuner:
    """Genetic algorithm tuner for evaluation weights"""
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1, 
                 crossover_rate: float = 0.8, elite_size: int = 5):
        """
        Initialize weight tuner
        
        Args:
            population_size: Size of population
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
            elite_size: Number of elite individuals to preserve
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        
        self.population = []
        self.generation = 0
        self.best_individual = None
        
        # Weight bounds for mutation
        self.weight_bounds = {
            "material": (0.5, 2.0),
            "position": (0.0, 2.0),
            "king_safety": (0.0, 3.0),
            "pawn_structure": (0.0, 2.0),
            "mobility": (0.0, 2.0),
            "center_control": (0.0, 2.0),
            "development": (0.0, 2.0),
            "tempo": (0.0, 2.0)
        }
    
    def initialize_population(self, base_weights: Optional[Dict[str, float]] = None):
        """Initialize population with random weights"""
        if base_weights is None:
            base_weights = {
                "material": 1.0,
                "position": 1.0,
                "king_safety": 1.0,
                "pawn_structure": 1.0,
                "mobility": 1.0,
                "center_control": 1.0,
                "development": 1.0,
                "tempo": 1.0
            }
        
        self.population = []
        
        # Add base individual
        self.population.append(Individual(copy.deepcopy(base_weights)))
        
        # Generate random individuals
        for _ in range(self.population_size - 1):
            weights = self._generate_random_weights()
            self.population.append(Individual(weights))
        
        self.generation = 0
    
    def _generate_random_weights(self) -> Dict[str, float]:
        """Generate random weights within bounds"""
        weights = {}
        for key, (min_val, max_val) in self.weight_bounds.items():
            weights[key] = random.uniform(min_val, max_val)
        return weights
    
    def evaluate_fitness(self, individual: Individual, opponent_weights: Optional[Dict[str, float]] = None, 
                        num_games: int = 10) -> float:
        """
        Evaluate fitness of individual by playing games
        
        Args:
            individual: Individual to evaluate
            opponent_weights: Weights for opponent (None for random)
            num_games: Number of games to play
            
        Returns:
            Fitness score
        """
        if opponent_weights is None:
            opponent_weights = self._generate_random_weights()
        
        wins = 0
        losses = 0
        draws = 0
        
        for _ in range(num_games):
            result = self._play_game(individual.weights, opponent_weights)
            
            if result == 1:
                wins += 1
            elif result == -1:
                losses += 1
            else:
                draws += 1
        
        # Update individual stats
        individual.games_played += num_games
        individual.wins += wins
        individual.losses += losses
        individual.draws += draws
        
        # Calculate fitness (win rate + bonus for draws)
        fitness = (wins + 0.5 * draws) / num_games
        individual.fitness = fitness
        
        return fitness
    
    def _play_game(self, weights1: Dict[str, float], weights2: Dict[str, float]) -> int:
        """
        Play a game between two weight sets
        
        Args:
            weights1: First player weights
            weights2: Second player weights
            
        Returns:
            1 if weights1 wins, -1 if weights2 wins, 0 if draw
        """
        # TODO: Implement actual game playing
        # - Create two engines with different weights
        # - Play game with time limit
        # - Return result
        
        # Placeholder: random result for now
        return random.choice([-1, 0, 1])
    
    def evolve(self, num_generations: int = 100, games_per_evaluation: int = 10):
        """
        Evolve population for specified number of generations
        
        Args:
            num_generations: Number of generations to evolve
            games_per_evaluation: Number of games per fitness evaluation
        """
        for gen in range(num_generations):
            self.generation = gen
            
            # Evaluate fitness for all individuals
            for individual in self.population:
                if individual.games_played == 0:  # Only evaluate if not already evaluated
                    self.evaluate_fitness(individual, num_games=games_per_evaluation)
            
            # Sort by fitness
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            
            # Update best individual
            if self.best_individual is None or self.population[0].fitness > self.best_individual.fitness:
                self.best_individual = copy.deepcopy(self.population[0])
            
            # Print generation statistics
            avg_fitness = sum(ind.fitness for ind in self.population) / len(self.population)
            print(f"Generation {gen}: Best={self.population[0].fitness:.3f}, "
                  f"Avg={avg_fitness:.3f}, Best Overall={self.best_individual.fitness:.3f}")
            
            # Create next generation
            self._create_next_generation()
    
    def _create_next_generation(self):
        """Create next generation using genetic operators"""
        new_population = []
        
        # Elitism: keep best individuals
        for i in range(self.elite_size):
            new_population.append(copy.deepcopy(self.population[i]))
        
        # Generate rest of population through crossover and mutation
        while len(new_population) < self.population_size:
            # Selection
            parent1 = self._tournament_selection()
            parent2 = self._tournament_selection()
            
            # Crossover
            if random.random() < self.crossover_rate:
                child1, child2 = self._crossover(parent1, parent2)
            else:
                child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
            
            # Mutation
            if random.random() < self.mutation_rate:
                self._mutate(child1)
            if random.random() < self.mutation_rate:
                self._mutate(child2)
            
            new_population.extend([child1, child2])
        
        # Trim to population size
        self.population = new_population[:self.population_size]
    
    def _tournament_selection(self, tournament_size: int = 3) -> Individual:
        """Tournament selection for parent selection"""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda x: x.fitness)
    
    def _crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Uniform crossover between two parents"""
        child1_weights = {}
        child2_weights = {}
        
        for key in parent1.weights:
            if random.random() < 0.5:
                child1_weights[key] = parent1.weights[key]
                child2_weights[key] = parent2.weights[key]
            else:
                child1_weights[key] = parent2.weights[key]
                child2_weights[key] = parent1.weights[key]
        
        return Individual(child1_weights), Individual(child2_weights)
    
    def _mutate(self, individual: Individual):
        """Mutate individual weights"""
        for key in individual.weights:
            if random.random() < 0.3:  # 30% chance to mutate each weight
                min_val, max_val = self.weight_bounds[key]
                # Gaussian mutation
                mutation = random.gauss(0, 0.1)
                individual.weights[key] = max(min_val, min(max_val, individual.weights[key] + mutation))
    
    def hill_climbing(self, initial_weights: Dict[str, float], max_iterations: int = 1000, 
                     step_size: float = 0.1) -> Dict[str, float]:
        """
        Hill climbing optimization as alternative to genetic algorithm
        
        Args:
            initial_weights: Starting weights
            max_iterations: Maximum iterations
            step_size: Step size for weight adjustments
            
        Returns:
            Optimized weights
        """
        current_weights = copy.deepcopy(initial_weights)
        current_fitness = self.evaluate_fitness(Individual(current_weights))
        
        for iteration in range(max_iterations):
            # Generate neighbor by adjusting one weight
            neighbor_weights = copy.deepcopy(current_weights)
            key = random.choice(list(neighbor_weights.keys()))
            
            # Adjust weight within bounds
            min_val, max_val = self.weight_bounds[key]
            adjustment = random.uniform(-step_size, step_size)
            neighbor_weights[key] = max(min_val, min(max_val, neighbor_weights[key] + adjustment))
            
            # Evaluate neighbor
            neighbor_fitness = self.evaluate_fitness(Individual(neighbor_weights))
            
            # Accept if better
            if neighbor_fitness > current_fitness:
                current_weights = neighbor_weights
                current_fitness = neighbor_fitness
                print(f"Iteration {iteration}: New best fitness = {current_fitness:.3f}")
        
        return current_weights
    
    def save_best_weights(self, filename: str = "best_weights.json"):
        """Save best weights to file"""
        if self.best_individual:
            with open(filename, 'w') as f:
                json.dump(self.best_individual.weights, f, indent=2)
            print(f"Best weights saved to {filename}")
    
    def load_weights(self, filename: str) -> Dict[str, float]:
        """Load weights from file"""
        with open(filename, 'r') as f:
            return json.load(f)
    
    def get_population_stats(self) -> Dict[str, Any]:
        """Get population statistics"""
        if not self.population:
            return {}
        
        fitnesses = [ind.fitness for ind in self.population]
        win_rates = [ind.get_win_rate() for ind in self.population]
        
        return {
            "generation": self.generation,
            "population_size": len(self.population),
            "best_fitness": max(fitnesses),
            "avg_fitness": sum(fitnesses) / len(fitnesses),
            "worst_fitness": min(fitnesses),
            "best_win_rate": max(win_rates),
            "avg_win_rate": sum(win_rates) / len(win_rates)
        }