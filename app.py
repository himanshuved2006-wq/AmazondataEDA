import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Amazon Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF9900;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #232F3E 0%, #FF9900 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .insight-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF9900;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Amazon Sales Analysis Dashboard</h1>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('amazon_sales_data.csv')
        # Convert date columns
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
        return df
    except FileNotFoundError:
        st.error("Please run generate_amazon_data.py first to create the dataset!")
        return None

df = load_data()

if df is not None:
    # Sidebar
    st.sidebar.header("🎯 Dashboard Controls")
    
    # Filters
    st.sidebar.subheader("Filters")
    
    # Category filter
    categories = ['All'] + list(df['Category'].unique())
    selected_category = st.sidebar.selectbox("Select Category", categories)
    
    # City filter
    cities = ['All'] + list(df['City'].unique())
    selected_city = st.sidebar.selectbox("Select City", cities)
    
    # Customer segment filter
    segments = ['All'] + list(df['Customer_Segment'].unique())
    selected_segment = st.sidebar.selectbox("Customer Segment", segments)
    
    # Date range filter
    st.sidebar.subheader("Date Range")
    min_date = df['Order_Date'].min().date()
    max_date = df['Order_Date'].max().date()
    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    
    if selected_segment != 'All':
        filtered_df = filtered_df[filtered_df['Customer_Segment'] == selected_segment]
    
    filtered_df = filtered_df[
        (filtered_df['Order_Date'].dt.date >= start_date) & 
        (filtered_df['Order_Date'].dt.date <= end_date)
    ]
    
    # Key Metrics
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_sales = filtered_df['Final_Price'].sum()
        st.metric("Total Sales", f"₹{total_sales:,.0f}")
    
    with col2:
        avg_order_value = filtered_df['Final_Price'].mean()
        st.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")
    
    with col3:
        total_orders = len(filtered_df)
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col4:
        avg_rating = filtered_df['Customer_Rating'].mean()
        st.metric("Avg Rating", f"{avg_rating:.2f} ⭐")
    
    with col5:
        return_rate = (filtered_df['Returned'] == 'Yes').mean() * 100
        st.metric("Return Rate", f"{return_rate:.1f}%")
    
    st.markdown("---")
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Sales Overview", 
        "📦 Product Analysis", 
        "👥 Customer Insights",
        "🚚 Delivery Analytics",
        "📈 Trends & Patterns"
    ])
    
    with tab1:
        st.header("Sales Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales by Category
            st.subheader("Sales by Category")
            category_sales = filtered_df.groupby('Category')['Final_Price'].sum().sort_values(ascending=True)
            fig = px.bar(
                x=category_sales.values, 
                y=category_sales.index,
                orientation='h',
                title="Total Sales by Category",
                labels={'x': 'Total Sales (₹)', 'y': 'Category'},
                color_discrete_sequence=['#FF9900']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Payment Method Distribution
            st.subheader("Payment Methods")
            payment_dist = filtered_df['Payment_Method'].value_counts()
            fig = px.pie(
                values=payment_dist.values,
                names=payment_dist.index,
                title="Payment Method Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Daily Sales Trend
        st.subheader("Daily Sales Trend")
        daily_sales = filtered_df.groupby('Order_Date')['Final_Price'].sum().reset_index()
        fig = px.line(
            daily_sales, 
            x='Order_Date', 
            y='Final_Price',
            title="Daily Sales Trend",
            labels={'Final_Price': 'Sales (₹)', 'Order_Date': 'Date'}
        )
        fig.update_traces(line_color='#FF9900', line_width=2)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Product Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top Products by Sales
            st.subheader("Top 10 Subcategories by Sales")
            top_products = filtered_df.groupby('Subcategory')['Final_Price'].sum().nlargest(10)
            fig = px.bar(
                x=top_products.values,
                y=top_products.index,
                orientation='h',
                title="Top 10 Subcategories",
                labels={'x': 'Sales (₹)', 'y': 'Subcategory'},
                color_discrete_sequence=['#2E86AB']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average Rating by Category
            st.subheader("Average Rating by Category")
            avg_rating_cat = filtered_df.groupby('Category')['Customer_Rating'].mean().sort_values()
            fig = px.bar(
                x=avg_rating_cat.values,
                y=avg_rating_cat.index,
                orientation='h',
                title="Average Customer Rating by Category",
                labels={'x': 'Average Rating', 'y': 'Category'},
                color=avg_rating_cat.values,
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Discount Analysis
        st.subheader("Discount Distribution by Category")
        fig = px.box(
            filtered_df,
            x='Category',
            y='Discount_Percent',
            title="Discount Percent Distribution by Category",
            color='Category',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("Customer Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer Segment Analysis
            st.subheader("Sales by Customer Segment")
            segment_sales = filtered_df.groupby('Customer_Segment')['Final_Price'].sum()
            fig = px.pie(
                values=segment_sales.values,
                names=segment_sales.index,
                title="Sales Distribution by Customer Segment",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # City-wise Analysis
            st.subheader("Top 10 Cities by Sales")
            city_sales = filtered_df.groupby('City')['Final_Price'].sum().nlargest(10)
            fig = px.bar(
                x=city_sales.index,
                y=city_sales.values,
                title="Sales by City",
                labels={'x': 'City', 'y': 'Sales (₹)'},
                color=city_sales.values,
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Rating Distribution
        st.subheader("Customer Rating Distribution")
        rating_dist = filtered_df['Customer_Rating'].value_counts().sort_index()
        fig = px.bar(
            x=rating_dist.index,
            y=rating_dist.values,
            title="Distribution of Customer Ratings",
            labels={'x': 'Rating', 'y': 'Count'},
            color=rating_dist.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("Delivery Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Delivery Status
            st.subheader("Delivery Status Distribution")
            delivery_status = filtered_df['Delivery_Status'].value_counts()
            fig = px.pie(
                values=delivery_status.values,
                names=delivery_status.index,
                title="Delivery Performance",
                color_discrete_sequence=['#2ECC71', '#E74C3C', '#F1C40F']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Average Delivery Days by Category
            st.subheader("Avg Delivery Days by Category")
            avg_delivery = filtered_df.groupby('Category')['Delivery_Days'].mean().sort_values()
            fig = px.bar(
                x=avg_delivery.values,
                y=avg_delivery.index,
                orientation='h',
                title="Average Delivery Time by Category",
                labels={'x': 'Average Days', 'y': 'Category'},
                color=avg_delivery.values,
                color_continuous_scale='blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Delivery Days Distribution
        st.subheader("Delivery Days Distribution")
        fig = px.histogram(
            filtered_df,
            x='Delivery_Days',
            nbins=20,
            title="Distribution of Delivery Days",
            labels={'Delivery_Days': 'Delivery Days', 'count': 'Number of Orders'},
            color_discrete_sequence=['#3498DB']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("Trends & Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly Sales Trend
            st.subheader("Monthly Sales Trend")
            monthly_sales = filtered_df.groupby('Order_Month')['Final_Price'].sum()
            fig = px.line(
                x=monthly_sales.index,
                y=monthly_sales.values,
                title="Sales by Month",
                labels={'x': 'Month', 'y': 'Sales (₹)'},
                markers=True
            )
            fig.update_traces(line_color='#FF9900', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Day of Week Analysis
            st.subheader("Sales by Day of Week")
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_sales = filtered_df.groupby('Order_DayName')['Final_Price'].sum().reindex(day_order)
            fig = px.bar(
                x=dow_sales.index,
                y=dow_sales.values,
                title="Sales by Day of Week",
                labels={'x': 'Day', 'y': 'Sales (₹)'},
                color=dow_sales.values,
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation Heatmap
        st.subheader("Correlation Heatmap")
        numeric_cols = ['Product_Price', 'Quantity', 'Discount_Percent', 'Final_Price', 
                       'Customer_Rating', 'Delivery_Days', 'Profit_Margin']
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix of Numerical Variables",
            color_continuous_scale='RdBu'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Data Preview Section
    st.markdown("---")
    st.header("📋 Data Preview")
    
    if st.checkbox("Show Raw Data"):
        st.subheader("Filtered Data")
        st.dataframe(filtered_df.head(100), use_container_width=True)
        
        # Download button for filtered data
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_amazon_data.csv",
            mime="text/csv"
        )
    
    # Key Insights
    st.markdown("---")
    st.header("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**📊 Sales Insights:**")
        st.markdown(f"- Highest selling category: **{filtered_df.groupby('Category')['Final_Price'].sum().idxmax()}**")
        st.markdown(f"- Most profitable category: **{filtered_df.groupby('Category')['Profit_Margin'].sum().idxmax()}**")
        st.markdown(f"- Best rated category: **{filtered_df.groupby('Category')['Customer_Rating'].mean().idxmax()}**")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**📦 Operational Insights:**")
        st.markdown(f"- Average delivery time: **{filtered_df['Delivery_Days'].mean():.1f} days**")
        st.markdown(f"- On-time delivery rate: **{(filtered_df['Delivery_Status'] == 'On Time').mean()*100:.1f}%**")
        st.markdown(f"- Most popular payment: **{filtered_df['Payment_Method'].mode()[0]}**")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Please run generate_amazon_data.py first to create the dataset!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 10px;'>
        Built with ❤️ using Streamlit | Amazon Sales Analysis Dashboard
    </div>
    """,
    unsafe_allow_html=True
)