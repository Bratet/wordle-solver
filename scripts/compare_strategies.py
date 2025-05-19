#!/usr/bin/env python3
"""
Wordle Solver Strategy Comparison
--------------------------------
This script performs comparative analysis of different Wordle solving strategies
and generates comprehensive comparison reports and visualizations.
"""

import os
import json
import matplotlib.pyplot as plt
from typing import Dict, Any

def generate_comparative_plots(all_results: Dict[str, Dict[str, Any]], output_dir: str = "output") -> None:
    """
    Generate comparative plots for all strategies.
    
    Args:
        all_results: Dictionary containing results for all strategies
        output_dir: Directory to save the plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot 1: Comparative attempts distribution
    plt.figure(figsize=(12, 8))
    
    # Define colors for each strategy
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6']
    strategies = list(all_results.keys())
    
    # Plot each strategy's distribution
    for i, (strategy, results) in enumerate(all_results.items()):
        attempts_dist = results["attempt_distribution"]
        attempts = [int(k) for k in attempts_dist.keys()]
        counts = list(attempts_dist.values())
        total = sum(counts)
        percentages = [count/total * 100 for count in counts]
        
        plt.bar([x + i*0.2 for x in attempts], percentages, width=0.2, 
                label=strategy.replace('_', ' ').title(), color=colors[i])
    
    plt.axvline(x=6.5, color='black', linestyle='--', label='Wordle Limit (6)')
    plt.xlabel('Number of Attempts')
    plt.ylabel('Percentage of Words (%)')
    plt.title('Comparative Distribution of Attempts to Solve')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(range(1, 7))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/comparative_attempts_distribution.png", bbox_inches='tight', dpi=300)
    
    # Plot 2: Comparative cumulative success rate
    plt.figure(figsize=(12, 8))
    
    for i, (strategy, results) in enumerate(all_results.items()):
        attempts_dist = results["attempt_distribution"]
        total = sum(attempts_dist.values())
        running_sum = 0
        cumulative_success = []
        
        for attempts in range(1, 7):
            if str(attempts) in attempts_dist:
                running_sum += attempts_dist[str(attempts)]
            cumulative_success.append(running_sum / total * 100)
        
        plt.plot(range(1, 7), cumulative_success, marker='o', linewidth=2,
                label=strategy.replace('_', ' ').title(), color=colors[i])
    
    plt.xlabel('Maximum Attempts')
    plt.ylabel('Cumulative Success Rate (%)')
    plt.title('Comparative Cumulative Success Rate')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(alpha=0.3)
    plt.xticks(range(1, 7))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/comparative_cumulative_success.png", bbox_inches='tight', dpi=300)
    
    # Plot 3: Performance Ranking
    plt.figure(figsize=(10, 6))
    
    # Calculate performance score (weighted combination of success rate and average attempts)
    performance_scores = {}
    for strategy, results in all_results.items():
        # Higher success rate and lower average attempts is better
        score = results['success_rate'] - (results['average_attempts'] * 10)
        performance_scores[strategy] = score
    
    # Sort strategies by performance score
    sorted_strategies = sorted(performance_scores.items(), key=lambda x: x[1], reverse=True)
    strategies = [s[0].replace('_', ' ').title() for s in sorted_strategies]
    scores = [s[1] for s in sorted_strategies]
    
    # Create horizontal bar chart
    bars = plt.barh(strategies, scores, color=colors[:len(strategies)])
    
    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}', ha='left', va='center', fontweight='bold')
    
    plt.xlabel('Performance Score')
    plt.title('Strategy Performance Ranking')
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/performance_ranking.png", bbox_inches='tight', dpi=300)
    
    # Plot 4: Success Rate vs Average Attempts
    plt.figure(figsize=(10, 8))
    
    for i, (strategy, results) in enumerate(all_results.items()):
        plt.scatter(results['average_attempts'], results['success_rate'], 
                   s=200, color=colors[i], label=strategy.replace('_', ' ').title())
        plt.annotate(strategy.replace('_', ' ').title(),
                    (results['average_attempts'], results['success_rate']),
                    xytext=(10, 10), textcoords='offset points')
    
    plt.xlabel('Average Attempts')
    plt.ylabel('Success Rate (%)')
    plt.title('Success Rate vs Average Attempts')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/success_vs_attempts.png", bbox_inches='tight', dpi=300)
    
    plt.close('all')


def save_comparative_report(all_results: Dict[str, Dict[str, Any]], output_dir: str = "output") -> str:
    """
    Save comparative performance results as a markdown report.
    
    Args:
        all_results: Dictionary containing results for all strategies
        output_dir: Directory to save the report
        
    Returns:
        Path to the saved report file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save raw results as JSON
    with open(f"{output_dir}/all_strategies_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    # Calculate performance scores
    performance_scores = {}
    for strategy, results in all_results.items():
        score = results['success_rate'] - (results['average_attempts'] * 10)
        performance_scores[strategy] = score
    
    # Sort strategies by performance score
    sorted_strategies = sorted(performance_scores.items(), key=lambda x: x[1], reverse=True)
    best_strategy = sorted_strategies[0][0]
    
    # Create markdown report
    report_path = f"{output_dir}/comparative_performance_report.md"
    with open(report_path, "w") as f:
        f.write("# Wordle Solver Comparative Performance Report\n\n")
        
        # Highlight best performer
        f.write("## 🏆 Best Performing Strategy\n\n")
        best_results = all_results[best_strategy]
        f.write(f"**{best_strategy.replace('_', ' ').title()}** achieved the best overall performance:\n\n")
        f.write(f"- Success Rate: {best_results['success_rate']:.2f}%\n")
        f.write(f"- Average Attempts: {best_results['average_attempts']:.2f}\n")
        f.write(f"- Median Attempts: {best_results['median_attempts']}\n")
        f.write(f"- Failures: {best_results['failures']}\n\n")
        
        f.write("## 📊 Performance Summary\n")
        f.write("| Strategy | Success Rate | Avg Attempts | Median | Failures | Performance Score |\n")
        f.write("|----------|--------------|--------------|--------|----------|------------------|\n")
        
        for strategy, score in sorted_strategies:
            f.write(f"| {strategy.replace('_', ' ').title()} | {all_results[strategy]['success_rate']:.2f}% | {all_results[strategy]['average_attempts']:.2f} | {all_results[strategy]['median_attempts']} | {all_results[strategy]['failures']} | {performance_scores[strategy]:.1f} |\n")
        
        f.write("\n## 📈 Attempt Distribution\n")
        f.write("| Strategy | 1 | 2 | 3 | 4 | 5 | 6 | >6 |\n")
        f.write("|----------|---|---|---|---|---|---|----|\n")
        
        for strategy, score in sorted_strategies:
            dist = all_results[strategy]["attempt_distribution"]
            total = sum(dist.values())
            row = [strategy.replace('_', ' ').title()]
            for i in range(1, 7):
                count = dist.get(str(i), 0)
                percentage = (count / total) * 100
                row.append(f"{count} ({percentage:.1f}%)")
            failures = all_results[strategy]["failures"]
            row.append(str(failures))
            f.write("|" + "|".join(row) + "|\n")
        
        f.write("\n## 📊 Visualization\n")
        f.write("Four comparative plots have been generated and saved:\n")
        f.write("1. `comparative_attempts_distribution.png`: Distribution of attempts needed to solve puzzles\n")
        f.write("2. `comparative_cumulative_success.png`: Cumulative success rate by maximum attempts\n")
        f.write("3. `performance_ranking.png`: Overall performance ranking of strategies\n")
        f.write("4. `success_vs_attempts.png`: Success rate vs average attempts scatter plot\n\n")
        
        f.write("## 🎯 Strategy Analysis\n")
        for strategy, score in sorted_strategies:
            f.write(f"\n### {strategy.replace('_', ' ').title()}\n")
            
            # Calculate key metrics
            success_rate = all_results[strategy]['success_rate']
            avg_attempts = all_results[strategy]['average_attempts']
            failures = all_results[strategy]['failures']
            
            # Write analysis
            f.write(f"- **Success Rate**: {success_rate:.2f}%\n")
            f.write(f"- **Average Attempts**: {avg_attempts:.2f}\n")
            f.write(f"- **Failures**: {failures}\n")
            
            # Add performance insights
            if strategy == best_strategy:
                f.write("\n**Key Strengths**:\n")
                if success_rate > 95:
                    f.write("- Exceptional success rate\n")
                if avg_attempts < 4:
                    f.write("- Very efficient solving (low average attempts)\n")
                if failures < 10:
                    f.write("- Rarely fails to solve puzzles\n")
            
            f.write("\n**Hardest Words**:\n")
            hardest_words = sorted(
                all_results[strategy]["word_results"].items(), 
                key=lambda x: x[1]["attempts"], 
                reverse=True
            )[:5]
            
            f.write("| Word | Attempts |\n")
            f.write("|------|----------|\n")
            for word, data in hardest_words:
                f.write(f"| {word} | {data['attempts']} |\n")
    
    return report_path


def main():
    """Main function to run the comparative analysis."""
    base_output_dir = "output"
    
    # Load results for all strategies
    all_results = {}
    strategy_dirs = ["entropy_strategy", "minimax_strategy", "frequency_strategy"]
    
    for strategy in strategy_dirs:
        results_path = os.path.join(base_output_dir, strategy, "strategy_results.json")
        with open(results_path, "r") as f:
            all_results[strategy] = json.load(f)
    
    # Generate comparative plots and report
    generate_comparative_plots(all_results, base_output_dir)
    comparative_report_path = save_comparative_report(all_results, base_output_dir)
    print(f"Comparative performance report saved to {comparative_report_path}")


if __name__ == "__main__":
    main() 