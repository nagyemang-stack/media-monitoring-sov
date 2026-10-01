# Methodology — Competitive Media Monitoring & SOV

## Evidence boundary
> Portfolio demonstration repository. The included monitoring series and outputs use generated demonstration data; they are not a client media-monitoring report or verified production performance.

## Core metrics

```text
SOV = (Brand Mentions / Total Industry Mentions) × 100
Net Sentiment = (Positive − Negative) / Total Mentions × 100
```

## Workflow
The script generates a monitoring series, assigns brands and sources, aggregates mentions, calculates share of voice and sentiment movement, and exports charts plus a text report. A real implementation would replace generated inputs with approved API feeds or documented public collections, then retain source URLs and collection dates.

## Reproduction
Run the repository’s documented requirements and `scripts/analyze_media_monitoring.py` to regenerate the files in `output/`.

## Limitations
SOV is relative visibility, not market share, quality, or business impact. Generated values cannot support claims about real brands. Competitor choice, source mix, deduplication, language coverage, and sentiment model performance can materially change the result.

## Attribution and AI-use note
AI tools may assist with research organisation, drafting, or prototyping. Caleb Agyemang reviews the method, checks outputs, edits the report, and owns the final interpretation.

**Author:** Caleb Agyemang  
**Status:** Public-safe methodology record prepared for review  
**License:** MIT
