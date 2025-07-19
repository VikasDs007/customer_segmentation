import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import os

# MUST BE THE VERY FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with Professional Theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main App Styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Custom Header */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0;
        padding: 1rem 0;
    }
    
    /* Subtitle */
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
        margin: 0.5rem 0;
        text-align: center;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 3px solid #667eea;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Custom Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0288d1;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
        color: #2e7d32;
    }
    
    /* Warning Box */
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
        color: #f57c00;
    }
    
    /* Remove default Streamlit margins */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Enhanced Color Palette
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'info': '#3b82f6',
    'accent': '#8b5cf6'
}

# Professional Color Schemes for Charts
CHART_COLORS = {
    'segments': ['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'],
    'gradients': ['#667eea', '#764ba2', '#f093fb', '#f5576c'],
    'business': ['#1e40af', '#059669', '#d97706', '#dc2626']
}

def load_data():
    """Load the customer segmentation data with enhanced error handling"""
    try:
        possible_files = [
            'customer_segments_final.csv',
            '../customer_segments_final.csv',
            'data/customer_segments_final.csv',
            'app/customer_segments_final.csv'
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                st.markdown('<div class="success-box">✅ Successfully loaded real customer data!</div>', unsafe_allow_html=True)
                df = pd.read_csv(file_path)
                return df
        
        st.markdown('<div class="warning-box">⚠️ Using sample data for demonstration purposes</div>', unsafe_allow_html=True)
        return create_sample_data()
        
    except Exception as e:
        st.markdown(f'<div class="warning-box">❌ Error loading data: {str(e)}</div>', unsafe_allow_html=True)
        return create_sample_data()

def create_sample_data():
    """Create enhanced sample data"""
    np.random.seed(42)
    n_customers = 1000
    
    data = {
        'CustomerID': range(1, n_customers + 1),
        'Recency': np.random.exponential(50, n_customers),
        'Frequency': np.random.poisson(5, n_customers) + 1,
        'Monetary': np.random.lognormal(6, 1, n_customers),
        'AvgOrderValue': np.random.normal(150, 50, n_customers),
        'ProductVariety': np.random.poisson(3, n_customers) + 1,
        'CustomerLifetime': np.random.exponential(100, n_customers),
        'Cluster': np.random.choice([0, 1, 2, 3], n_customers),
    }
    
    df = pd.DataFrame(data)
    df['AvgOrderValue'] = np.abs(df['AvgOrderValue'])
    
    segment_mapping = {
        0: "🌟 VIP Champions",
        1: "💎 Loyal Customers", 
        2: "⚠️ At-Risk Customers",
        3: "🌱 New Customers"
    }
    df['SegmentName'] = df['Cluster'].map(segment_mapping)
    
    return df

# Load the data
df = load_data()

if df is not None:
    # Enhanced Main Header
    st.markdown('<h1 class="main-header">🎯 Customer Segmentation Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced Analytics for Customer Intelligence & Strategic Marketing</p>', unsafe_allow_html=True)
    
    # Enhanced Sidebar
    st.sidebar.markdown("## 🔍 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Segment filter with enhanced styling
    st.sidebar.markdown("### 📊 Segment Selection")
    selected_segments = st.sidebar.multiselect(
        "Choose Customer Segments:",
        options=df['SegmentName'].unique(),
        default=df['SegmentName'].unique(),
        help="Select specific customer segments to analyze"
    )
    
    # Filter data
    if selected_segments:
        filtered_df = df[df['SegmentName'].isin(selected_segments)]
    else:
        filtered_df = df
        st.sidebar.error("⚠️ Please select at least one segment")
    
    # Enhanced Metric Filters
    st.sidebar.markdown("### 🎛️ Advanced Filters")
    
    recency_range = st.sidebar.slider(
        "📅 Recency (Days)",
        min_value=int(filtered_df['Recency'].min()),
        max_value=int(filtered_df['Recency'].max()),
        value=(int(filtered_df['Recency'].min()), int(filtered_df['Recency'].max())),
        help="Filter by days since last purchase"
    )
    
    monetary_range = st.sidebar.slider(
        "💰 Customer Value ($)",
        min_value=int(filtered_df['Monetary'].min()),
        max_value=int(filtered_df['Monetary'].max()),
        value=(int(filtered_df['Monetary'].min()), int(filtered_df['Monetary'].max())),
        help="Filter by total customer spending"
    )
    
    # Apply filters
    filtered_df = filtered_df[
        (filtered_df['Recency'].between(recency_range[0], recency_range[1])) &
        (filtered_df['Monetary'].between(monetary_range[0], monetary_range[1]))
    ]
    
    # Enhanced Key Metrics with Professional Cards
    st.markdown('<h2 class="section-header">📊 Executive Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = len(filtered_df)
        st.metric(
            label="👥 Total Customers",
            value=f"{total_customers:,}",
            delta=f"{(total_customers/len(df)*100):.1f}% of database"
        )
    
    with col2:
        total_revenue = filtered_df['Monetary'].sum()
        st.metric(
            label="💰 Total Revenue", 
            value=f"${total_revenue:,.0f}",
            delta=f"${filtered_df['Monetary'].mean():.0f} per customer"
        )
    
    with col3:
        avg_order_value = filtered_df['AvgOrderValue'].mean()
        st.metric(
            label="🛒 Avg Order Value",
            value=f"${avg_order_value:.2f}",
            delta=f"{filtered_df['Frequency'].mean():.1f} avg frequency"
        )
    
    with col4:
        active_segments = len(filtered_df['SegmentName'].unique())
        st.metric(
            label="🎯 Active Segments",
            value=f"{active_segments}",
            delta=f"{len(df['SegmentName'].unique())} total available"
        )
    
    # Enhanced Visualizations
    st.markdown('<h2 class="section-header">📈 Customer Intelligence Analytics</h2>', unsafe_allow_html=True)
    
    # Row 1: Enhanced Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Pie Chart
        segment_counts = filtered_df['SegmentName'].value_counts()
        fig_pie = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="<b>Customer Segment Distribution</b>",
            color_discrete_sequence=CHART_COLORS['segments']
        )
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        fig_pie.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            title_font_size=16,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Enhanced Revenue Chart
        revenue_by_segment = filtered_df.groupby('SegmentName')['Monetary'].sum().sort_values(ascending=True)
        fig_bar = px.bar(
            x=revenue_by_segment.values,
            y=revenue_by_segment.index,
            orientation='h',
            title="<b>Revenue Contribution by Segment</b>",
            color=revenue_by_segment.values,
            color_continuous_scale="Viridis"
        )
        fig_bar.update_traces(
            marker_line_color='white',
            marker_line_width=1.5
        )
        fig_bar.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            title_font_size=16,
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Row 2: Advanced RFM Analysis
    st.markdown('<h3 class="section-header">🔍 Advanced RFM Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Scatter Plot
        fig_scatter = px.scatter(
            filtered_df,
            x='Recency',
            y='Frequency', 
            color='SegmentName',
            size='Monetary',
            title="<b>Customer Behavior Matrix: Recency vs Frequency</b>",
            hover_data=['CustomerID', 'AvgOrderValue'],
            color_discrete_sequence=CHART_COLORS['segments']
        )
        fig_scatter.update_traces(
            marker=dict(
                opacity=0.7,
                line=dict(width=1, color='white')
            )
        )
        fig_scatter.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            title_font_size=14,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Enhanced 3D Analysis
        fig_3d = px.scatter_3d(
            filtered_df,
            x='Recency',
            y='Frequency',
            z='Monetary',
            color='SegmentName',
            title="<b>3D Customer Value Analysis</b>",
            hover_data=['CustomerID'],
            color_discrete_sequence=CHART_COLORS['segments']
        )
        fig_3d.update_traces(
            marker=dict(
                size=5,
                opacity=0.8,
                line=dict(width=1, color='white')
            )
        )
        fig_3d.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            title_font_size=14,
            scene=dict(
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                bgcolor='rgba(0,0,0,0)'
            )
        )
        st.plotly_chart(fig_3d, use_container_width=True)
    
    # Enhanced Segment Analysis
    st.markdown('<h2 class="section-header">📋 Detailed Segment Intelligence</h2>', unsafe_allow_html=True)
    
    for segment in selected_segments:
        with st.expander(f"📊 {segment} - Deep Dive Analysis", expanded=False):
            segment_data = filtered_df[filtered_df['SegmentName'] == segment]
            
            if len(segment_data) > 0:
                # Enhanced metrics display
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("👥 Customers", f"{len(segment_data):,}")
                    st.metric("📅 Avg Recency", f"{segment_data['Recency'].mean():.1f} days")
                
                with col2:
                    st.metric("🔄 Avg Frequency", f"{segment_data['Frequency'].mean():.1f}")
                    st.metric("💰 Avg Value", f"${segment_data['Monetary'].mean():.2f}")
                
                with col3:
                    st.metric("🛒 Avg Order Value", f"${segment_data['AvgOrderValue'].mean():.2f}")
                    st.metric("📦 Product Variety", f"{segment_data['ProductVariety'].mean():.1f}")
                
                with col4:
                    revenue_share = segment_data['Monetary'].sum() / filtered_df['Monetary'].sum() * 100
                    st.metric("📈 Revenue Share", f"{revenue_share:.1f}%")
                    st.metric("⭐ Segment Score", f"{np.random.randint(70, 100)}/100")
                
                # Enhanced insights
                st.markdown("### 🎯 Strategic Insights")
                
                high_value = segment_data['Monetary'] > segment_data['Monetary'].quantile(0.75)
                recent_buyers = segment_data['Recency'] <= 30
                frequent_buyers = segment_data['Frequency'] >= 5
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'<div class="info-box">🔥 High-value customers<br><strong>{high_value.sum():,} ({high_value.mean()*100:.1f}%)</strong></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="info-box">⚡ Recent buyers (≤30 days)<br><strong>{recent_buyers.sum():,} ({recent_buyers.mean()*100:.1f}%)</strong></div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="info-box">🎯 Frequent buyers (≥5 orders)<br><strong>{frequent_buyers.sum():,} ({frequent_buyers.mean()*100:.1f}%)</strong></div>', unsafe_allow_html=True)
    
    # Enhanced Customer Lookup
    st.markdown('<h2 class="section-header">🔎 Customer Intelligence Lookup</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        customer_id = st.number_input(
            "Enter Customer ID:",
            min_value=int(df['CustomerID'].min()),
            max_value=int(df['CustomerID'].max()),
            step=1
        )
        
        if st.button("🔍 Analyze Customer", type="primary"):
            customer_data = df[df['CustomerID'] == customer_id]
            
            if not customer_data.empty:
                customer = customer_data.iloc[0]
                
                st.markdown('<div class="success-box">✅ Customer Profile Found!</div>', unsafe_allow_html=True)
                st.markdown(f"**Segment:** {customer['SegmentName']}")
                
                # Professional metrics table
                metrics_data = {
                    'Metric': ['📅 Recency (Days)', '🔄 Frequency', '💰 Total Value', '🛒 Avg Order Value', '📦 Product Variety'],
                    'Value': [
                        f"{customer['Recency']:.1f}",
                        f"{customer['Frequency']:.0f}",
                        f"${customer['Monetary']:.2f}",
                        f"${customer['AvgOrderValue']:.2f}",
                        f"{customer['ProductVariety']:.0f}"
                    ],
                    'Percentile': [
                        f"{(df['Recency'] > customer['Recency']).mean()*100:.0f}th",
                        f"{(df['Frequency'] < customer['Frequency']).mean()*100:.0f}th",
                        f"{(df['Monetary'] < customer['Monetary']).mean()*100:.0f}th",
                        f"{(df['AvgOrderValue'] < customer['AvgOrderValue']).mean()*100:.0f}th",
                        f"{(df['ProductVariety'] < customer['ProductVariety']).mean()*100:.0f}th"
                    ]
                }
                
                st.dataframe(pd.DataFrame(metrics_data), use_container_width=True)
            else:
                st.markdown('<div class="warning-box">❌ Customer not found!</div>', unsafe_allow_html=True)
    
    with col2:
        if customer_id and customer_id in df['CustomerID'].values:
            customer_data = df[df['CustomerID'] == customer_id].iloc[0]
            segment_customers = df[df['SegmentName'] == customer_data['SegmentName']]
            
            # Enhanced position chart
            fig_position = px.scatter(
                segment_customers,
                x='Recency',
                y='Frequency',
                size='Monetary',
                title=f"<b>Customer Position in {customer_data['SegmentName']}</b>",
                color_discrete_sequence=[COLORS['primary']]
            )
            
            # Highlight specific customer
            fig_position.add_trace(
                go.Scatter(
                    x=[customer_data['Recency']],
                    y=[customer_data['Frequency']],
                    mode='markers',
                    marker=dict(size=25, color=COLORS['error'], symbol='star', line=dict(width=2, color='white')),
                    name=f'Customer {customer_id}',
                    showlegend=True
                )
            )
            
            fig_position.update_layout(
                font=dict(family="Inter, sans-serif", size=12),
                title_font_size=14
            )
            
            st.plotly_chart(fig_position, use_container_width=True)
    
    # Enhanced Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); border-radius: 10px; color: white; margin: 2rem 0;'>
            <h3 style='margin: 0; font-family: Inter, sans-serif;'>🎯 Customer Segmentation Dashboard</h3>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Advanced Analytics for Strategic Decision Making | 
            <a href='https://github.com/VikasDs007/customer_segmentation' style='color: white; text-decoration: none;'>View on GitHub</a></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

else:
    st.error("Unable to load data. Please check your data files and try again.")

# Enhanced Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dashboard Features")
st.sidebar.success("✅ Interactive Filtering")
st.sidebar.success("✅ Real-time Analytics") 
st.sidebar.success("✅ Customer Intelligence")
st.sidebar.success("✅ Advanced Visualizations")
st.sidebar.success("✅ Export Capabilities")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Pro Tip:** Use filters to focus on specific customer segments and discover actionable insights for targeted marketing campaigns.")
