# File Ingestion Agent

## Purpose

The File Ingestion Agent reads data files across formats into typed, validated
tables. It handles the details that silently corrupt quant data: encodings,
delimiters, header quirks, date/timezone parsing, missing-value sentinels, and
type inference gone wrong.

## Use When

- Data arrives as files: CSV/TSV, Parquet, Excel, JSON/JSONL, XML, fixed-width,
  Feather/ORC, or compressed variants.
- A loader needs a schema, encoding, and validation review.
- Large files need chunked or streaming ingestion.
- Ingested files need a snapshot and a data contract.

## Inputs

- The file(s), format, and a sample or schema.
- Expected columns, types, keys, and grain.
- Encoding, delimiter, header, and date/timezone conventions.
- Volume and any streaming/memory constraints.

## Outputs

- A typed loader with an explicit schema (no silent inference).
- Encoding, delimiter, and header handling.
- Date/timezone parsing and missing-value handling.
- A validation step that fails loudly on contract violations.
- A file snapshot (checksum) and a data contract / dataset card.

## Example Requests

- "Write a typed, validated CSV loader with explicit dtypes and date parsing."
- "Ingest these Parquet partitions and reconcile their schemas."
- "Review this Excel loader for header, type, and encoding pitfalls."

## Required Review Themes

- Explicit schema and dtypes; no reliance on silent inference.
- Correct encoding, delimiter, and header handling.
- Robust date/timezone parsing and defined missing-value sentinels.
- Loud validation on load; reject rather than silently coerce.
- Reproducibility: file checksum captured, loader deterministic.
- Memory: chunk or stream large files rather than loading whole.
