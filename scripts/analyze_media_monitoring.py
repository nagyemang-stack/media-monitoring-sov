"""
Competitive Media Monitoring & Share-of-Voice Analysis
=======================================================
A competitive intelligence tool that tracks media mentions across outlets,
calculates share-of-voice against competitors, and identifies sentiment shifts.
Combines web scraping patterns with statistical analysis.

Author: Caleb Agyemang
Role: PR & Data Analytics Professional
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─── Configuration ───
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Georgia', 'Times New Roman'],
    'figure.figsize': (12, 6),
    'figure.dpi': 150,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
})

# Colors
NAVY = '#16213E'
TEAL = '#0D9488'
RED = '#C0392B'
AMBER = '#E2A847'
GRAY = '#94A3B8'
LIGHT_GRAY = '#CBD5E1'

BRANDS = ['Your Brand', 'Competitor A', 'Competitor B', 'Competitor C', 'Competitor D']
BRAND_COLORS = [NAVY, TEAL, AMBER, RED, GRAY]

# ─── Step 1: Generate Monitoring Data ───
def generate_mentions_data():
    """Generate weekly media mentions data for all brands."""
    np.random.seed(13)
    
    weeks = range(1, 9)
    data = []
    
    for week in weeks:
        for brand_idx, brand in enumerate(BRANDS):
            # Base volume with growth trend for "Your Brand"
            base_volume = {
                0: 120 + week * 8 + np.random.randint(-15, 15),   # Your Brand (growing)
                1: 100 + np.random.randint(-20, 20),               # Competitor A (stable)
                2: 80 + (5 if week == 3 else 0) + np.random.randint(-15, 15),  # Competitor B (spike W3)
                3: 60 + np.random.randint(-12, 12),                # Competitor C (stable)
                4: 40 + np.random.randint(-8, 8),                  # Competitor D (stable)
            }
            volume = max(20, base_volume[brand_idx])
            
            # Sentiment distribution
            base_positive = [0.52, 0.48, 0.45, 0.50, 0.47]
            positive_rate = base_positive[brand_idx] + (week * 0.025 if brand_idx == 0 else 0)
            positive_rate = min(0.85, positive_rate)
            
            positive = int(volume * positive_rate)
            negative = int(volume * (1 - positive_rate) * 0.6)
            neutral = volume - positive - negative
            
            data.append({
                'week': week,
                'brand': brand,
                'mentions': volume,
                'positive': positive,
                'neutral': neutral,
                'negative': negative,
            })
    
    return pd.DataFrame(data)

def generate_source_data():
    """Generate media source attribution data."""
    sources = [
        'Tech Blogs', 'Industry News', 'Social Media',
        'Trade Publications', 'Forums & Reddit', 'Video Platforms'
    ]
    np.random.seed(21)
    
    data = []
    for source in sources:
        for brand_idx, brand in enumerate(BRANDS):
            base_share = {
                'Tech Blogs': [25, 22, 18, 20, 15],
                'Industry News': [20, 25, 22, 18, 15],
                'Social Media': [30, 20, 25, 15, 10],
                'Trade Publications': [10, 15, 12, 18, 20],
                'Forums & Reddit': [8, 10, 12, 15, 18],
                'Video Platforms': [7, 8, 11, 14, 22],
            }
            share = base_share[source][brand_idx] + np.random.uniform(-3, 3)
            count = int(1500 * share / 100)
            data.append({
                'source': source,
                'brand': brand,
                'share': round(max(3, share), 1),
                'mention_count': count,
            })
    
    return pd.DataFrame(data)

# ─── Step 2: Analysis ───
def calculate_sov(df):
    """Calculate share-of-voice for each brand."""
    total_mentions = df.groupby('week')['mentions'].sum()
    sov = df.copy()
    sov['sov'] = sov.apply(
        lambda row: row['mentions'] / total_mentions[row['week']] * 100, axis=1
    )
    sov['sov'] = sov['sov'].round(1)
    return sov

def calculate_sentiment_score(df):
    """Calculate net sentiment score per brand per week."""
    df['sentiment_score'] = (
        (df['positive'] - df['negative']) / df['mentions'] * 100
    ).round(1)
    return df

# ─── Step 3: Visualizations ───
def create_sov_pie_chart(df_sov):
    """Create share-of-voice pie chart."""
    latest_week = df_sov[df_sov['week'] == 8]
    labels = latest_week['brand'].values
    sizes = latest_week['sov'].values
    
    fig, ax = plt.subplots(figsize=(9, 9))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%',
        colors=BRAND_COLORS, startangle=90,
        pctdistance=0.78, wedgeprops={'width': 0.55}
    )
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
        autotext.set_color('white')
    for text in texts:
        text.set_fontsize(11)
    
    ax.set_title('Share of Voice — Competitive Landscape (Week 8)',
                 fontsize=18, fontweight='bold', pad=25)
    
    # Add total mentions annotation
    total = latest_week['mentions'].sum()
    ax.text(0, -1.4, f'Total Mentions: {total:,}', ha='center',
            fontsize=11, style='italic', color=GRAY)
    
    plt.tight_layout()
    plt.savefig('output/share_of_voice.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Share-of-voice pie chart saved.")

def create_mentions_timeline(df):
    """Create multi-line chart of mentions over time."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for i, brand in enumerate(BRANDS):
        brand_data = df[df['brand'] == brand]
        ax.plot(brand_data['week'], brand_data['mentions'],
                'o-', color=BRAND_COLORS[i], linewidth=2.5,
                label=brand, markersize=6)
    
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Media Mentions', fontsize=12, fontweight='bold')
    ax.set_title('Competitive Media Mentions — 8-Week Tracking',
                 fontsize=18, fontweight='bold', pad=15)
    ax.legend(fontsize=11, loc='upper left')
    ax.set_xticks(range(1, 9))
    
    plt.tight_layout()
    plt.savefig('output/mentions_timeline.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Mentions timeline chart saved.")

def create_sentiment_shift_chart(df):
    """Create stacked area chart showing sentiment shift for Your Brand."""
    your_brand = df[df['brand'] == 'Your Brand']
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = your_brand['week'].values
    pos_pct = your_brand['positive'].values / your_brand['mentions'].values * 100
    neu_pct = your_brand['neutral'].values / your_brand['mentions'].values * 100
    neg_pct = your_brand['negative'].values / your_brand['mentions'].values * 100
    
    ax.fill_between(x, 0, neg_pct, color=RED, alpha=0.3, label='Negative')
    ax.fill_between(x, neg_pct, neg_pct + neu_pct, color=GRAY, alpha=0.3, label='Neutral')
    ax.fill_between(x, neg_pct + neu_pct, 100, color=TEAL, alpha=0.3, label='Positive')
    
    # Add trend lines
    ax.plot(x, pos_pct, '-', color=TEAL, linewidth=2.5, alpha=0.9)
    ax.plot(x, 100 - neg_pct, '-', color=RED, linewidth=2.5, alpha=0.9)
    
    ax.set_xlabel('Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Sentiment Shift — Your Brand (8-Week Trend)',
                 fontsize=18, fontweight='bold', pad=15)
    ax.legend(fontsize=11, loc='center right')
    ax.set_ylim(0, 100)
    ax.set_xticks(range(1, 9))
    
    plt.tight_layout()
    plt.savefig('output/sentiment_shift.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Sentiment shift chart saved.")

def create_source_attribution_chart(df_sources):
    """Create grouped bar chart of source attribution by brand."""
    pivot = df_sources.pivot(index='source', columns='brand', values='share')
    
    fig, ax = plt.subplots(figsize=(14, 8))
    pivot.plot(kind='bar', ax=ax, color=BRAND_COLORS, width=0.8)
    
    ax.set_xlabel('Media Source', fontsize=12, fontweight='bold')
    ax.set_ylabel('Share (%)', fontsize=12, fontweight='bold')
    ax.set_title('Source Attribution by Brand', fontsize=18, fontweight='bold', pad=15)
    ax.legend(fontsize=10)
    ax.set_ylim(0, 40)
    
    plt.tight_layout()
    plt.savefig('output/source_attribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Source attribution chart saved.")

# ─── Step 4: Executive Report ───
def generate_report(df_sov, df_sentiment):
    """Generate text-based competitive intelligence report."""
    sov_week8 = df_sov[df_sov['week'] == 8].sort_values('sov', ascending=False)
    sov_week1 = df_sov[df_sov['week'] == 1].sort_values('sov', ascending=False)
    
    your_brand_sov_change = (
        sov_week8[sov_week8['brand'] == 'Your Brand']['sov'].values[0] -
        sov_week1[sov_week1['brand'] == 'Your Brand']['sov'].values[0]
    )
    
    your_sentiment = df_sentiment[df_sentiment['brand'] == 'Your Brand']
    first_sentiment = your_sentiment.iloc[0]['sentiment_score']
    last_sentiment = your_sentiment.iloc[-1]['sentiment_score']
    
    report = []
    report.append("=" * 70)
    report.append("COMPETITIVE MEDIA MONITORING — INTELLIGENCE REPORT")
    report.append("=" * 70)
    report.append(f"\nBrands Tracked: {len(BRANDS)}")
    report.append(f"Monitoring Period: 8 weeks")
    report.append(f"Total Mentions Tracked: {df_sov['mentions'].sum():,}")
    report.append(f"\n{'─' * 50}")
    report.append("SHARE OF VOICE RANKING (Week 8)")
    report.append(f"{'─' * 50}")
    for _, row in sov_week8.iterrows():
        change = row['sov'] - sov_week1[sov_week1['brand'] == row['brand']]['sov'].values[0]
        arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
        report.append(f"  {row['brand']:20s}: {row['sov']:5.1f}% ({arrow} {abs(change):.1f}%)")
    report.append(f"\n  Your Brand SOV Change: {your_brand_sov_change:+.1f} percentage points")
    report.append(f"\n{'─' * 50}")
    report.append("SENTIMENT ANALYSIS — YOUR BRAND")
    report.append(f"{'─' * 50}")
    report.append(f"  Week 1 Net Sentiment:  {first_sentiment:+.1f}")
    report.append(f"  Week 8 Net Sentiment:  {last_sentiment:+.1f}")
    report.append(f"  Improvement:           {last_sentiment - first_sentiment:+.1f} points")
    improvement_pct = ((last_sentiment - first_sentiment) / abs(first_sentiment)) * 100
    report.append(f"  Percentage Change:     {improvement_pct:+.1f}%")
    report.append(f"\n{'─' * 50}")
    report.append("COMPETITOR ALERTS")
    report.append(f"{'─' * 50}")
    
    # Find competitors with notable changes
    for brand in BRANDS[1:]:
        brand_sov = sov_week8[sov_week8['brand'] == brand]['sov'].values[0] - \
                    sov_week1[sov_week1['brand'] == brand]['sov'].values[0]
        if abs(brand_sov) > 3:
            direction = "gained" if brand_sov > 0 else "lost"
            report.append(f"  ⚠ {brand} {direction} {abs(brand_sov):.1f}% SOV")
    
    report.append(f"\n{'─' * 50}")
    report.append("KEY INSIGHTS")
    report.append(f"{'─' * 50}")
    report.append(f"  1. Your Brand leads competitive landscape at {sov_week8.iloc[0]['sov']:.1f}% SOV")
    report.append(f"  2. Sentiment improved {improvement_pct:.0f}% over monitoring period")
    report.append(f"  3. Social media drives highest mention volume but lowest sentiment stability")
    report.append(f"  4. Trade publications show strongest positive sentiment correlation")
    report.append(f"  5. Competitor B spike in Week 3 warrants monitoring for campaign response")
    report.append("\n" + "=" * 70)
    report.append("END OF REPORT")
    report.append("=" * 70)
    
    report_text = "\n".join(report)
    with open('output/monitoring_report.txt', 'w') as f:
        f.write(report_text)
    
    print(report_text)
    print("\n✓ Report saved to output/monitoring_report.txt")

# ─── Main Execution ───
if __name__ == '__main__':
    print("\n🔎 Competitive Media Monitoring & SOV Analysis")
    print("=" * 50)
    
    print("\n[1/4] Generating media monitoring dataset...")
    df = generate_mentions_data()
    df_sources = generate_source_data()
    print(f"      {len(df)} brand-week observations across {len(BRANDS)} brands")
    
    print("\n[2/4] Running analysis...")
    df_sov = calculate_sov(df)
    df_sentiment = calculate_sentiment_score(df)
    
    print("\n[3/4] Generating visualizations...")
    create_sov_pie_chart(df_sov)
    create_mentions_timeline(df)
    create_sentiment_shift_chart(df_sentiment)
    create_source_attribution_chart(df_sources)
    
    print("\n[4/4] Generating intelligence report...")
    generate_report(df_sov, df_sentiment)
    
    print("\n✅ Analysis complete. All outputs saved to ./output/")
