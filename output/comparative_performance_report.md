# Wordle Solver Comparative Performance Report

## Summary
| Strategy | Success Rate | Average Attempts | Median Attempts | Failures |
|----------|--------------|------------------|-----------------|----------|
| Entropy Strategy | 100.00% | 4.17 | 4.0 | 0 |
| Minimax Strategy | 100.00% | 4.44 | 4.0 | 0 |
| Frequency Strategy | 100.00% | 4.37 | 4.0 | 0 |
| Hybrid Strategy | 100.00% | 4.32 | 4.0 | 0 |

## Attempt Distribution
| Strategy | 1 | 2 | 3 | 4 | 5 | 6 | >6 |
|----------|---|---|---|---|---|---|----|
|Entropy Strategy|0 (0.0%)|4 (0.2%)|302 (13.1%)|1361 (58.9%)|581 (25.2%)|61 (2.6%)|0|
|Minimax Strategy|0 (0.0%)|1 (0.0%)|166 (7.2%)|1068 (46.3%)|968 (41.9%)|106 (4.6%)|0|
|Frequency Strategy|0 (0.0%)|32 (1.4%)|439 (19.0%)|878 (38.0%)|566 (24.5%)|394 (17.1%)|0|
|Hybrid Strategy|0 (0.0%)|32 (1.4%)|457 (19.8%)|907 (39.3%)|564 (24.4%)|349 (15.1%)|0|

## Visualization
Two comparative plots have been generated and saved:
1. `comparative_attempts_distribution.png`: Shows the distribution of attempts needed to solve puzzles for each strategy
2. `comparative_cumulative_success.png`: Shows the cumulative success rate by maximum attempts allowed for each strategy

## Hardest Words by Strategy

### Entropy Strategy
These words required the most attempts to solve:

| Word | Attempts |
|------|----------|
| aging | 6 |
| aping | 6 |
| axial | 6 |
| belly | 6 |
| berry | 6 |
| bless | 6 |
| boozy | 6 |
| boxer | 6 |
| charm | 6 |
| cheap | 6 |

### Minimax Strategy
These words required the most attempts to solve:

| Word | Attempts |
|------|----------|
| arena | 6 |
| await | 6 |
| aware | 6 |
| baker | 6 |
| baler | 6 |
| batty | 6 |
| bleed | 6 |
| bobby | 6 |
| booby | 6 |
| boozy | 6 |

### Frequency Strategy
These words required the most attempts to solve:

| Word | Attempts |
|------|----------|
| aging | 6 |
| alloy | 6 |
| aloof | 6 |
| alpha | 6 |
| amass | 6 |
| amiss | 6 |
| aorta | 6 |
| apple | 6 |
| arena | 6 |
| armor | 6 |

### Hybrid Strategy
These words required the most attempts to solve:

| Word | Attempts |
|------|----------|
| aging | 6 |
| allay | 6 |
| alpha | 6 |
| amass | 6 |
| amiss | 6 |
| apple | 6 |
| arena | 6 |
| armor | 6 |
| aroma | 6 |
| avert | 6 |
