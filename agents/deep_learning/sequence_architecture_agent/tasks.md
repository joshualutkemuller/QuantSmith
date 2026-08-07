# Sequence Architecture Agent Tasks

## Standard Tasks

1. Define the input tensor from assets, features, and lookback window.
2. Compare FCN, CNN, LSTM, and any proposed successor architecture.
3. Estimate parameter count and overfitting risk.
4. Design lookback-window and architecture ablation tests.
5. Specify output shape and connection to allocation constraints.
6. Produce implementation notes for reproducible training.

## Evidence to Collect

- Tensor shape example.
- Architecture comparison table.
- Hyperparameter search boundary.
- Training/validation split design.
- Ablation results or required experiments.

## Red Flags

- Architecture selected because it is fashionable.
- Feature order or time axis left ambiguous.
- Too many parameters for the data size.
- No simpler model comparison.
- No robustness test across lookback windows.
