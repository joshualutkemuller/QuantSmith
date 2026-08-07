# Local Model Runtime Adapter

## Use For

- Restricted data that cannot leave controlled infrastructure.
- Deterministic extraction or classification experiments.
- Offline or cost-controlled workflows.

## Delivery Rules

- Record model artifact, checksum, runtime, hardware, quantization, and prompt URI.
- Capture input/output artifacts and environment metadata.
- Validate that model weights and runtime are approved for the workflow.
- Use reproducible containers or environment manifests for production runs.

## Risks

- Local models may have weaker instruction following or evaluation coverage.
- Hardware and quantization choices can change outputs.
- Runtime artifacts must be versioned to preserve reproducibility.
