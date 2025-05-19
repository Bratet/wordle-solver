# Wordle Solver Comparative Performance Report

## 🏆 Best Performing Strategy

**Entropy Strategy** achieved the best overall performance:

- Success Rate: 100.00%
- Average Attempts: 4.17
- Median Attempts: 4.0
- Failures: 0

## 📊 Performance Summary
| Strategy | Success Rate | Avg Attempts | Median | Failures | Performance Score |
|----------|--------------|--------------|--------|----------|------------------|
| Entropy Strategy | 100.00% | 4.17 | 4.0 | 0 | 58.3 |
| Frequency Strategy | 100.00% | 4.37 | 4.0 | 0 | 56.3 |
| Minimax Strategy | 100.00% | 4.44 | 4.0 | 0 | 55.6 |

## 📈 Attempt Distribution
| Strategy | 1 | 2 | 3 | 4 | 5 | 6 | >6 |
|----------|---|---|---|---|---|---|----|
|Entropy Strategy|0 (0.0%)|4 (0.2%)|302 (13.1%)|1361 (58.9%)|581 (25.2%)|61 (2.6%)|0|
|Frequency Strategy|0 (0.0%)|32 (1.4%)|439 (19.0%)|878 (38.0%)|566 (24.5%)|394 (17.1%)|0|
|Minimax Strategy|0 (0.0%)|1 (0.0%)|166 (7.2%)|1068 (46.3%)|968 (41.9%)|106 (4.6%)|0|

## 📊 Visualization
Four comparative plots have been generated and saved:
1. `comparative_attempts_distribution.png`: Distribution of attempts needed to solve puzzles
2. `comparative_cumulative_success.png`: Cumulative success rate by maximum attempts
3. `performance_ranking.png`: Overall performance ranking of strategies
4. `success_vs_attempts.png`: Success rate vs average attempts scatter plot

## 🎯 Strategy Analysis

### Entropy Strategy
- **Success Rate**: 100.00%
- **Average Attempts**: 4.17
- **Failures**: 0

**Key Strengths**:
- Exceptional success rate
- Rarely fails to solve puzzles

**Hardest Words**:
| Word | Attempts |
|------|----------|
| aging | 6 |
| aping | 6 |
| axial | 6 |
| belly | 6 |
| berry | 6 |

### Frequency Strategy
- **Success Rate**: 100.00%
- **Average Attempts**: 4.37
- **Failures**: 0

**Hardest Words**:
| Word | Attempts |
|------|----------|
| aging | 6 |
| alloy | 6 |
| aloof | 6 |
| alpha | 6 |
| amass | 6 |

### Minimax Strategy
- **Success Rate**: 100.00%
- **Average Attempts**: 4.44
- **Failures**: 0

**Hardest Words**:
| Word | Attempts |
|------|----------|
| arena | 6 |
| await | 6 |
| aware | 6 |
| baker | 6 |
| baler | 6 |
