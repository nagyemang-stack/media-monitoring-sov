# Methodology — Competitive Media Monitoring & SOV

## Share of Voice (SOV)

Share-of-voice is the standard PR metric for measuring brand visibility relative to competitors.

```
SOV = (Brand Mentions / Total Industry Mentions) × 100
```

A SOV above 30% typically indicates market leadership in media presence.

## Net Sentiment Score

```
Net Score = (Positive − Negative) / Total Mentions × 100
```

Range: -100 to +100. Positive scores above +30 indicate strong brand health.

## Monitoring Architecture

The monitoring system follows a continuous loop:

1. **Collection** — Web scraping (BeautifulSoup) or API feeds gather mentions
2. **Deduplication** — Duplicate mentions across sources are removed
3. **Classification** — Each mention is tagged with brand, source, sentiment
4. **Aggregation** — Metrics are calculated weekly
5. **Alerting** — Anomalies (SOV changes >3%, sentiment drops >10%) trigger alerts
6. **Reporting** — Executive summaries are generated automatically

## Competitor Selection Criteria

Competitors should be selected based on:
- Direct competitors in the same market segment
- Similar audience size and media footprint
- Active media presence (minimum 5 mentions/week)
- Mix of market leaders and emerging challengers
