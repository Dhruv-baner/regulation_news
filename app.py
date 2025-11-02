import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime
from collections import Counter
import matplotlib.colors as mcolors

# Page configuration
st.set_page_config(
    page_title="Norges Bank Regulatory Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color scheme
COLORS = {
    'primary': '#1A3A52',
    'accent': '#2C8C99',
    'highlight': '#F4A261',
    'alert': '#E76F51',
    'secondary': '#5D6D7E',
    'background': '#F8F9FA',
    'markets': {
        'United States': '#2C8C99',
        'Japan': '#E76F51',
        'United Kingdom': '#F4A261',
        'Germany': '#5D6D7E',
        'France': '#9B59B6'
    }
}

# Load data with caching
@st.cache_data
def load_data():
    processed_dir = Path('data/processed')
    latest_file = sorted(processed_dir.glob('analyzed_articles_*.json'))[-1]
    df = pd.read_json(latest_file)
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    return df, latest_file.stem.split('_')[-2] + '_' + latest_file.stem.split('_')[-1]

df, timestamp = load_data()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1A3A52;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #5D6D7E;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

print("Setup complete - paste this into app.py")

# Header
st.markdown('<p class="main-header">🏦 Norges Bank Regulatory Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Monitoring of Global Financial Regulations</p>', unsafe_allow_html=True)

st.markdown(f"**Last Updated:** {timestamp[:8]}-{timestamp[8:14]} | **Total Articles:** {len(df)}")

st.markdown("---")

# Sidebar filters
st.sidebar.header("Filters")

# Market filter
selected_markets = st.sidebar.multiselect(
    "Select Markets",
    options=df['market_name'].unique().tolist(),
    default=df['market_name'].unique().tolist()
)

# Relevance threshold
min_relevance = st.sidebar.slider(
    "Minimum Relevance Score",
    min_value=0,
    max_value=10,
    value=0,
    step=1
)

# Category filter
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['category'].unique().tolist(),
    default=df['category'].unique().tolist()
)

# Impact level filter
selected_impact = st.sidebar.multiselect(
    "Impact Level",
    options=['high', 'medium', 'low'],
    default=['high', 'medium', 'low']
)

# Apply filters
df_filtered = df[
    (df['market_name'].isin(selected_markets)) &
    (df['relevance_score'] >= min_relevance) &
    (df['category'].isin(selected_categories)) &
    (df['impact_level'].isin(selected_impact))
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered Articles:** {len(df_filtered)}")

print("Section 2 complete - add below Section 1")

# Key Metrics
st.subheader("Key Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Articles",
        value=len(df_filtered),
        delta=f"{len(df_filtered)/len(df)*100:.0f}% of total"
    )

with col2:
    avg_relevance = df_filtered['relevance_score'].mean()
    st.metric(
        label="Avg Relevance Score",
        value=f"{avg_relevance:.1f}/10"
    )

with col3:
    high_impact = len(df_filtered[df_filtered['impact_level'] == 'high'])
    st.metric(
        label="High Impact Articles",
        value=high_impact,
        delta=f"{high_impact/len(df_filtered)*100:.0f}% of filtered"
    )

with col4:
    markets_covered = df_filtered['market_name'].nunique()
    st.metric(
        label="Markets Covered",
        value=markets_covered,
        delta=f"out of 5"
    )

st.markdown("---")

print("Section 3 complete - add below Section 2")

# Visualizations in tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Overview", "📈 Category Analysis", "🗺️ Geographic View", "📰 Top Articles"])

with tab1:
    st.subheader("Market Coverage and Relevance")
    
    # Market overview chart
    market_overview = df_filtered.groupby('market_name').agg({
        'relevance_score': ['count', 'mean']
    }).reset_index()
    market_overview.columns = ['market', 'article_count', 'avg_relevance']
    market_overview = market_overview.sort_values('article_count', ascending=False)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=market_overview['market'],
            y=market_overview['article_count'],
            name='Article Count',
            marker_color=[COLORS['markets'][m] for m in market_overview['market']],
            text=market_overview['article_count'],
            textposition='outside',
            opacity=0.8
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=market_overview['market'],
            y=market_overview['avg_relevance'],
            name='Avg Relevance',
            mode='lines+markers',
            line=dict(color=COLORS['alert'], width=3),
            marker=dict(size=10, color=COLORS['alert'], line=dict(width=2, color='white')),
            yaxis='y2'
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        xaxis_title='Market',
        yaxis_title='Number of Articles',
        yaxis2_title='Average Relevance Score',
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified',
        font=dict(family='Arial, sans-serif', size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    fig.update_yaxes(range=[0, market_overview['article_count'].max() * 1.3], secondary_y=False)
    fig.update_yaxes(range=[0, 10], secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Relevance distribution
    st.subheader("Relevance Score Distribution by Market")
    
    market_order = df_filtered.groupby('market_name')['relevance_score'].median().sort_values(ascending=False).index
    
    fig2 = go.Figure()
    for market in market_order:
        market_data = df_filtered[df_filtered['market_name'] == market]['relevance_score']
        fig2.add_trace(go.Box(
            y=market_data,
            name=market,
            marker_color=COLORS['markets'][market],
            boxmean='sd',
            opacity=0.8
        ))
    
    fig2.update_layout(
        yaxis_title='Relevance Score (0-10)',
        xaxis_title='Market',
        height=500,
        showlegend=False,
        hovermode='closest',
        font=dict(family='Arial, sans-serif', size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(range=[0, 10])
    )
    
    st.plotly_chart(fig2, use_container_width=True)

print("Section 4 Tab 1 complete - add below Section 3")

with tab2:
    st.subheader("Regulatory Categories by Market")
    
    # Category distribution
    category_market = pd.crosstab(df_filtered['market_name'], df_filtered['category'])
    market_order_cat = category_market.sum(axis=1).sort_values(ascending=False).index
    category_market = category_market.loc[market_order_cat]
    
    # Combine cross_border with other
    if 'cross_border_investment' in category_market.columns:
        category_market['other'] = category_market['other'] + category_market['cross_border_investment']
        category_market = category_market.drop(columns=['cross_border_investment'])
    
    fig3 = go.Figure()
    
    category_colors = {
        'securities_regulation': '#2C8C99',
        'monetary_policy': '#F4A261', 
        'banking_regulation': '#E76F51',
        'central_banking': '#9B59B6',
        'market_infrastructure': '#5D6D7E',
        'other': '#BDC3C7'
    }
    
    for category in category_market.columns:
        fig3.add_trace(go.Bar(
            name=category.replace('_', ' ').title(),
            x=category_market.index,
            y=category_market[category],
            marker_color=category_colors.get(category, '#95A5A6'),
            opacity=0.85
        ))
    
    fig3.update_layout(
        xaxis_title='Market',
        yaxis_title='Number of Articles',
        barmode='group',
        height=500,
        legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=1.01),
        hovermode='x unified',
        font=dict(family='Arial, sans-serif', size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Geographic Regulatory Intelligence")
    
    # Map data
    country_iso = {
        'United States': 'USA',
        'United Kingdom': 'GBR',
        'Japan': 'JPN',
        'Germany': 'DEU',
        'France': 'FRA'
    }
    
    map_data = []
    for market in df_filtered['market_name'].unique():
        market_df = df_filtered[df_filtered['market_name'] == market]
        
        all_regs = []
        for regs in market_df['key_regulators']:
            if isinstance(regs, list):
                all_regs.extend(regs)
        
        if all_regs:
            top_reg = Counter(all_regs).most_common(1)[0]
            top_regulator = f"{top_reg[0]} ({top_reg[1]} mentions)"
        else:
            top_regulator = "N/A"
        
        top_category = market_df['category'].value_counts().index[0].replace('_', ' ').title()
        
        map_data.append({
            'market': market,
            'iso_code': country_iso[market],
            'article_count': len(market_df),
            'avg_relevance': round(market_df['relevance_score'].mean(), 1),
            'high_impact_count': (market_df['impact_level'] == 'high').sum(),
            'top_regulator': top_regulator,
            'primary_focus': top_category
        })
    
    map_df = pd.DataFrame(map_data)
    
    fig4 = px.choropleth(
        map_df,
        locations='iso_code',
        color='avg_relevance',
        hover_name='market',
        hover_data={
            'iso_code': False,
            'article_count': True,
            'avg_relevance': ':.1f',
            'high_impact_count': True,
            'top_regulator': True,
            'primary_focus': True
        },
        color_continuous_scale=[
            [0, '#EBF5FB'],
            [0.5, '#5DADE2'],
            [1, '#154360']
        ],
        labels={
            'avg_relevance': 'Avg Relevance',
            'article_count': 'Total Articles',
            'high_impact_count': 'High Impact Articles',
            'top_regulator': 'Most Mentioned Regulator',
            'primary_focus': 'Primary Regulatory Focus'
        }
    )
    
    fig4.update_geos(
        showcountries=True,
        countrycolor='#E0E0E0',
        showcoastlines=True,
        coastlinecolor='#CCCCCC',
        projection_type='natural earth',
        lataxis_range=[20, 70],
        lonaxis_range=[-130, 150],
        bgcolor='#F8F9FA'
    )
    
    fig4.update_layout(
        height=600,
        font=dict(family='Arial, sans-serif', size=12),
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    st.plotly_chart(fig4, use_container_width=True)

print("Section 5 complete - add below Section 4")

with tab4:
    st.subheader("Most Relevant Regulatory Articles")
    
    # Prepare filtered data
    df_clean = df_filtered.copy()
    df_clean['title_normalized'] = df_clean['title'].str.lower().str.replace('[^a-z0-9\s]', '', regex=True)
    df_unique = df_clean.drop_duplicates(subset='title_normalized', keep='first')
    
    # Exclude crypto sources
    excluded_sources = ['Economictimes.com', 'Bitcoinist', 'Cointelegraph']
    df_unique = df_unique[~df_unique['source_name'].isin(excluded_sources)]
    
    # Market order
    market_order = ['United States', 'United Kingdom', 'Germany', 'Japan', 'France']
    
    # Get top 5 per market
    top_articles_list = []
    for market in market_order:
        if market in df_unique['market_name'].values:
            market_top = df_unique[df_unique['market_name'] == market].nlargest(5, 'relevance_score')
            top_articles_list.append(market_top)
    
    if top_articles_list:
        top_articles = pd.concat(top_articles_list)
        table_data = top_articles[['title', 'market_name', 'relevance_score', 'impact_level', 'category', 'what_happened', 'source_name']].copy()
        
        # Color code by market
        market_colors = []
        for market in table_data['market_name']:
            hex_color = COLORS['markets'][market]
            rgb = mcolors.hex2color(hex_color)
            rgba = f'rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, 0.2)'
            market_colors.append(rgba)
        
        fig5 = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Title</b>', '<b>Market</b>', '<b>Score</b>', '<b>Impact</b>', '<b>Category</b>', '<b>What Happened</b>', '<b>Source</b>'],
                fill_color=COLORS['primary'],
                font=dict(color='white', size=12),
                align='left',
                height=40
            ),
            cells=dict(
                values=[
                    table_data['title'],
                    table_data['market_name'],
                    table_data['relevance_score'],
                    table_data['impact_level'],
                    table_data['category'].str.replace('_', ' ').str.title(),
                    table_data['what_happened'],
                    table_data['source_name']
                ],
                fill_color=[market_colors] + [['white']*len(table_data)]*6,
                align='left',
                font=dict(size=11),
                height=30
            )
        )])
        
        fig5.update_layout(
            height=900,
            font=dict(family='Arial, sans-serif'),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig5, use_container_width=True)
        st.caption(f"Showing {len(top_articles)} curated articles (crypto sources excluded)")
    else:
        st.info("No articles match the current filters.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #5D6D7E; padding: 20px;'>
    <p><b>Norges Bank Regulatory Intelligence Dashboard</b></p>
    <p>Powered by GPT-3.5-turbo | Data sources: NewsAPI, Google News</p>
</div>
""", unsafe_allow_html=True)

print("Section 6 complete - Dashboard finished! Save app.py and test with: streamlit run app.py")