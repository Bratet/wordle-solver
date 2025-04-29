#!/usr/bin/env python3
"""
Wordle Solver Performance Analysis
----------------------------------
This script evaluates the performance of an entropy-based strategy for solving Wordle
puzzles and generates a comprehensive performance report.
"""

import contextlib
import io
import os
from typing import List, Dict, Any
import json
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from wordle import Wordle
from strategies import EntropyBasedStrategy, MinimaxBasedStrategy


def load_word_list(filepath: str) -> List[str]:
    """Load and return a list of words from a file."""
    with open(filepath, "r") as file:
        return [line.strip() for line in file]


def evaluate_strategy(game: Wordle, strategy: Any, target_words: List[str]) -> Dict[str, Any]:
    """
    Evaluate the strategy's performance against all target words.
    
    Args:
        game: Wordle game instance
        strategy: Strategy instance used to solve the game
        target_words: List of target words to test against
        
    Returns:
        Dictionary containing performance metrics
    """
    results = {
        "attempts": [],
        "failures": 0,
        "success_rate": 0.0,
        "word_results": {}
    }
    
    print(f"Evaluating strategy against {len(target_words)} target words...")
    
    for word in tqdm(target_words):
        game.reset_game(word)
        
        # Suppress output from the strategy
        with contextlib.redirect_stdout(io.StringIO()):
            strategy.solve(game)
        
        results["attempts"].append(game.attempts)
        
        # Store individual word results
        results["word_results"][word] = {
            "attempts": game.attempts,
            "success": game.attempts <= 6  # Standard Wordle allows 6 attempts
        }
        
        if game.attempts > 6:
            results["failures"] += 1
    
    total_words = len(target_words)
    results["success_rate"] = (total_words - results["failures"]) / total_words * 100
    results["average_attempts"] = sum(results["attempts"]) / total_words
    results["median_attempts"] = np.median(results["attempts"])
    
    # Count frequency of each number of attempts
    attempt_counts = {}
    for i in range(1, max(results["attempts"]) + 1):
        attempt_counts[i] = results["attempts"].count(i)
    results["attempt_distribution"] = attempt_counts
    
    return results


def generate_plots(results: Dict[str, Any], output_dir: str = "results") -> None:
    """
    Generate and save performance visualization plots.
    
    Args:
        results: Dictionary containing performance metrics
        output_dir: Directory to save the plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot 1: Attempts distribution
    plt.figure(figsize=(10, 6))
    
    attempts_dist = results["attempt_distribution"]
    attempts = list(attempts_dist.keys())
    counts = list(attempts_dist.values())
    
    plt.bar(attempts, counts)
    plt.axvline(x=6.5, color='r', linestyle='--', label='Wordle Limit (6)')
    plt.xlabel('Number of Attempts')
    plt.ylabel('Count')
    plt.title('Distribution of Attempts to Solve')
    plt.grid(axis='y', alpha=0.3)
    plt.legend()
    plt.savefig(f"{output_dir}/attempts_distribution.png")
    
    # Plot 2: Cumulative success rate
    plt.figure(figsize=(10, 6))
    
    cumulative_success = []
    total = len(results["attempts"])
    running_sum = 0
    
    for i in sorted(attempts_dist.keys()):
        running_sum += attempts_dist[i]
        if i <= 6:  # Standard Wordle limit
            cumulative_success.append(running_sum / total * 100)
    
    plt.plot(range(1, len(cumulative_success) + 1), cumulative_success, marker='o')
    plt.xlabel('Maximum Attempts')
    plt.ylabel('Success Rate (%)')
    plt.title('Cumulative Success Rate by Maximum Attempts Allowed')
    plt.grid(alpha=0.3)
    plt.xticks(range(1, len(cumulative_success) + 1))
    plt.savefig(f"{output_dir}/cumulative_success.png")
    
    plt.close('all')


def save_report(results: Dict[str, Any], output_dir: str = "results") -> str:
    """
    Save performance results as a markdown report and raw JSON data.
    
    Args:
        results: Dictionary containing performance metrics
        output_dir: Directory to save the report and data
        
    Returns:
        Path to the saved report file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save raw results as JSON
    with open(f"{output_dir}/strategy_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Create markdown report
    report_path = f"{output_dir}/performance_report.md"
    with open(report_path, "w") as f:
        f.write("# Wordle Solver Performance Report\n\n")
        
        f.write("## Summary\n")
        f.write(f"- **Success Rate**: {results['success_rate']:.2f}%\n")
        f.write(f"- **Average Attempts**: {results['average_attempts']:.2f}\n")
        f.write(f"- **Median Attempts**: {results['median_attempts']}\n")
        f.write(f"- **Total Words Tested**: {len(results['attempts'])}\n")
        f.write(f"- **Failures** (words not solved in 6 attempts): {results['failures']}\n\n")
        
        f.write("## Attempt Distribution\n")
        f.write("| Attempts | Count | Percentage |\n")
        f.write("|----------|-------|------------|\n")
        
        total = len(results["attempts"])
        for attempts, count in sorted(results["attempt_distribution"].items()):
            percentage = (count / total) * 100
            f.write(f"| {attempts} | {count} | {percentage:.2f}% |\n")
        
        f.write("\n")
        f.write("## Visualization\n")
        f.write("Two plots have been generated and saved:\n")
        f.write("1. `attempts_distribution.png`: Shows the distribution of attempts needed to solve puzzles\n")
        f.write("2. `cumulative_success.png`: Shows the cumulative success rate by maximum attempts allowed\n\n")
        
        f.write("## Hardest Words\n")
        f.write("These words required the most attempts to solve:\n\n")
        
        # Get the 10 words that required the most attempts
        hardest_words = sorted(
            results["word_results"].items(), 
            key=lambda x: x[1]["attempts"], 
            reverse=True
        )[:10]
        
        f.write("| Word | Attempts |\n")
        f.write("|------|----------|\n")
        for word, data in hardest_words:
            f.write(f"| {word} | {data['attempts']} |\n")
    
    print(f"Performance report saved to {report_path}")
    return report_path


def main():
    """Main function to run the evaluation and generate the report."""
    # Define paths
    allowed_words_path = "data/allowed_words.txt"
    possible_words_path = "data/possible_words.txt"
    base_output_dir = "results"
    
    # Initialize the game
    game = Wordle(allowed_words=allowed_words_path, possible_words=possible_words_path)
    
    # Load target words
    target_words = load_word_list(possible_words_path)
    
    # Define strategies to evaluate
    strategies = {
        "minimax_strategy": MinimaxBasedStrategy(),
    }
    
    # Evaluate each strategy
    for strategy_name, strategy in strategies.items():
        print(f"\nEvaluating {strategy_name}...")
        
        # Create strategy-specific output directory
        strategy_output_dir = os.path.join(base_output_dir, strategy_name)
        
        # Evaluate strategy performance
        results = evaluate_strategy(game, strategy, target_words)
        
        # Generate plots and save report
        generate_plots(results, strategy_output_dir)
        report_path = save_report(results, strategy_output_dir)
        
        print(f"Evaluation of {strategy_name} completed successfully.")
        print(f"Performance report saved to {report_path}")
        print(f"Raw data saved to {strategy_output_dir}/strategy_results.json")


if __name__ == "__main__":
    main()