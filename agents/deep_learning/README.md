# Deep Learning Agents

Grouped in `deep_learning/`, these agents translate deep-learning research into reviewable quant workflows. The first set is grounded in *Deep Learning for Portfolio Optimization* by Zhang, Zohren, and Roberts, which directly optimizes portfolio Sharpe ratio with neural networks, softmax long-only weights, volatility scaling, transaction-cost analysis, crisis review, and feature sensitivity.

## Group Workflow

1. `dl_portfolio_orchestrator/` scopes the request and routes it through architecture, objective, cost, risk, and explainability roles.
2. `sequence_architecture_agent/` chooses FCN, CNN, LSTM, or successor architectures for financial sequences and documents why.
3. `differentiable_objective_agent/` turns portfolio objectives such as Sharpe, Sortino, diversification, and drawdown-aware variants into trainable losses.
4. `allocation_constraint_agent/` owns the portfolio-weight layer, including long-only softmax, leverage, turnover, exposure, and desk constraints.
5. `volatility_cost_agent/` handles volatility scaling, transaction costs, turnover diagnostics, and capacity implications.
6. `crisis_explainability_agent/` stress-tests regimes and explains feature/weight behavior with sensitivity and attribution diagnostics.

## Design Philosophy

These are design-and-review agents, not a promise that a neural net is better. The default posture is adversarial: prove that direct objective optimization survives leakage checks, cost realism, turnover drag, regime breaks, and baseline comparison.

## Paper-Derived Anchors

- Bypass return forecasting when the target decision is allocation; optimize portfolio weights directly.
- Treat Sharpe or another differentiable portfolio objective as the training signal.
- Preserve portfolio constraints explicitly in the output layer.
- Compare against fixed allocation, mean-variance, maximum diversification, and stochastic portfolio baselines.
- Include volatility scaling and transaction costs in evaluation, not as an afterthought.
- Explain crisis behavior and feature sensitivity before claiming robustness.
