# Wordle Solver

A comprehensive Python toolkit for solving and analyzing Wordle puzzles using various solving strategies.

![Wordle Solver](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Wordle_196_example.svg/440px-Wordle_196_example.svg.png)

## Overview

This project implements and evaluates different algorithmic strategies for solving Wordle, the popular word-guessing game. The toolkit includes:

- A Wordle game simulator
- Multiple solving strategies (Entropy-based, Minimax, and Frequency-based)
- Performance analysis tools
- Visualization of solving patterns and success rates

## Features

- **Wordle Game Simulator**: Complete implementation of Wordle mechanics
- **Multiple Solving Strategies**:
  - **Entropy-based**: Chooses words that maximize information gain
  - **Minimax-based**: Minimizes the worst-case scenario
  - **Frequency-based**: Uses letter frequency analysis
- **Analysis Tools**: Scripts for comparative analysis of strategy performance
- **Visualizations**: Generates plots and reports of strategy effectiveness

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/wordle-solver.git
   cd wordle-solver
   ```

2. No additional dependencies are required for basic functionality, but for analysis tools and visualizations, install:
   ```
   pip install matplotlib numpy tqdm
   ```

## Usage

### Interactive Solver

To use the interactive solver (where you specify a target word):

```bash
python scripts/main.py
```

The solver will prompt you to enter a target word and then show how the chosen strategy attempts to solve it.

### Strategy Analysis

To analyze the performance of all solving strategies against the entire word list:

```bash
python scripts/analyze_strategy.py
```

This will generate detailed reports and visualizations in the `output` directory.

### Strategy Comparison

To compare the performance of different strategies:

```bash
python scripts/compare_strategies.py
```

This will create comparative visualizations and an overall performance report.

## Project Structure

- `src/`: Core implementation
  - `wordle.py`: Wordle game implementation
  - `strategies/`: Different solving strategies
    - `abstract_strategy.py`: Base class for all strategies
    - `entropy_strategy.py`: Information theory-based approach
    - `minimax_strategy.py`: Worst-case minimization approach
    - `frequency_strategy.py`: Letter frequency-based approach
- `scripts/`: Analysis and utility scripts
  - `main.py`: Interactive solver
  - `analyze_strategy.py`: Evaluates strategy performance
  - `compare_strategies.py`: Compares different strategies
- `data/`: Word lists
  - `allowed_words.txt`: List of all allowed guess words (~13,000 words)
  - `possible_words.txt`: List of possible target words (~2,300 words)
- `output/`: Generated reports and visualizations

## How the Strategies Work

### Entropy-Based Strategy
This strategy treats Wordle as an information theory problem. It chooses words that maximize the expected information gain (entropy) from the guess. The first guess is pre-computed as "tares".

### Minimax-Based Strategy
This strategy aims to minimize the worst-case scenario by choosing words that minimize the maximum possible remaining word list size after a guess. The first guess is pre-computed as "serai".

### Frequency-Based Strategy
This strategy uses letter frequency analysis at each position to make guesses. It scores words based on how frequently their letters appear in the remaining possible words. The first guess is pre-computed as "cares".

## Analysis & Reports

The analysis tools generate:

1. **Success Rates**: Percentage of words solved within 6 attempts
2. **Average Attempts**: Mean number of guesses required
3. **Attempt Distribution**: Visualization of how many attempts each word took
4. **Hardest Words**: Lists of words that required the most attempts
5. **Performance Comparison**: Direct comparison of all strategies

Sample visualizations include:
- Attempt distributions
- Cumulative success rates
- Performance rankings
- Success rate vs. average attempts scatter plots

## Contributing

Contributions are welcome! You could:
- Implement new solving strategies
- Improve existing strategies
- Enhance visualization and reporting
- Optimize performance

## License

[MIT License](LICENSE)

## Acknowledgments

- Wordle was created by Josh Wardle
- Word lists are based on common English 5-letter words