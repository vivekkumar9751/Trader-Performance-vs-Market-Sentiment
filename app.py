import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")

st.title("Trader Performance vs Market Sentiment")

@st.cache_data
def load_and_preprocess_data():
    hist_df = pd.read_csv("historical_data.csv")
    fg_df = pd.read_csv("fear_greed_index.csv")

    hist_df['datetime'] = pd.to_datetime(hist_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
    hist_df['date'] = hist_df['datetime'].dt.strftime('%Y-%m-%d')
    fg_df['date'] = pd.to_datetime(fg_df['date']).dt.strftime('%Y-%m-%d')
    
    df = hist_df.merge(fg_df[['date', 'value', 'classification']], on='date', how='inner')
    
    def map_sentiment(c):
        if pd.isna(c): return 'Neutral'
        c = c.lower()
        if 'fear' in c: return 'Fear'
        elif 'greed' in c: return 'Greed'
        else: return 'Neutral'

    df['Sentiment'] = df['classification'].apply(map_sentiment)
    
    daily_trader = df.groupby(['Account', 'date', 'Sentiment']).agg(
        daily_PnL=('Closed PnL', 'sum'),
        trades_count=('Order ID', 'count'),
        total_volume_usd=('Size USD', 'sum'),
        winning_trades=('Closed PnL', lambda x: (x > 0).sum()),
        losing_trades=('Closed PnL', lambda x: (x < 0).sum()),
        long_trades=('Direction', lambda x: (x.str.lower().isin(['buy', 'long', 'open long'])).sum()),
        short_trades=('Direction', lambda x: (x.str.lower().isin(['sell', 'short', 'open short'])).sum())
    ).reset_index()

    daily_trader['win_rate'] = (daily_trader['winning_trades'] / daily_trader['trades_count']).fillna(0)
    daily_trader['avg_trade_size_usd'] = (daily_trader['total_volume_usd'] / daily_trader['trades_count']).fillna(0)
    daily_trader['long_ratio'] = daily_trader['long_trades'] / daily_trader['trades_count']

    # Segmentation
    trader_stats = daily_trader.groupby('Account').agg(
        avg_daily_volume=('total_volume_usd', 'mean'),
        avg_trades_per_day=('trades_count', 'mean')
    )
    vol_median = trader_stats['avg_daily_volume'].median()
    freq_median = trader_stats['avg_trades_per_day'].median()
    trader_stats['Volume_Segment'] = np.where(trader_stats['avg_daily_volume'] > vol_median, 'High Volume', 'Low Volume')
    trader_stats['Freq_Segment'] = np.where(trader_stats['avg_trades_per_day'] > freq_median, 'Frequent', 'Infrequent')
    
    daily_trader = daily_trader.merge(trader_stats[['Volume_Segment', 'Freq_Segment']], on='Account', how='left')
    
    return daily_trader

with st.spinner("Loading and processing data..."):
    df = load_and_preprocess_data()

st.sidebar.markdown('## Filters')
sentiment_filter = st.sidebar.multiselect("Select Sentiment", df['Sentiment'].unique(), default=df['Sentiment'].unique())
filtered_df = df[df['Sentiment'].isin(sentiment_filter)]

st.markdown("### High-Level Metrics (Filtered by Sentiment)")
col1, col2, col3 = st.columns(3)
col1.metric("Average Daily PnL", f"${filtered_df['daily_PnL'].mean():.2f}")
col2.metric("Average Win Rate", f"{filtered_df['win_rate'].mean():.2%}")
col3.metric("Average Trade Size", f"${filtered_df['avg_trade_size_usd'].mean():.2f}")

st.markdown("---")
st.markdown("### Performance Differentials: Fear vs Greed")

col4, col5 = st.columns(2)

with col4:
    st.markdown("**Average Daily PnL vs Sentiment**")
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(data=filtered_df, x='Sentiment', y='daily_PnL', estimator=np.mean, ax=ax)
    st.pyplot(fig)

with col5:
    st.markdown("**Long vs Short Bias by Sentiment**")
    sentiment_behavior = filtered_df.groupby('Sentiment')[['long_trades', 'short_trades']].mean()
    fig2, ax2 = plt.subplots(figsize=(6,4))
    sentiment_behavior.plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

st.markdown("---")
st.markdown("### Trader Segments Analysis")

col6, col7 = st.columns(2)

with col6:
    st.markdown("**Frequent vs Infrequent Traders (Avg PnL)**")
    df_freq = filtered_df.groupby(['Freq_Segment', 'Sentiment'])['daily_PnL'].mean().unstack()
    fig3, ax3 = plt.subplots(figsize=(6,4))
    df_freq.plot(kind='bar', ax=ax3)
    st.pyplot(fig3)

with col7:
    st.markdown("**Volume Segments (Avg PnL)**")
    df_vol = filtered_df.groupby(['Volume_Segment', 'Sentiment'])['daily_PnL'].mean().unstack()
    fig4, ax4 = plt.subplots(figsize=(6,4))
    df_vol.plot(kind='bar', ax=ax4)
    st.pyplot(fig4)

st.markdown("---")
st.markdown("""
### Summary of Insights:
1. **Fear drives higher profitability**: On average, the Daily PnL is higher during Fear days, driven by High Volume traders capitalizing on volatility.
2. **Greed induces Overtrading**: Traders execute more trades on Greed days, often attempting to short rallies, ending in lower average PnL.
3. **Consistency vs Infrequency**: Frequent traders significantly outperform infrequent traders across all market sentiments.
""")
