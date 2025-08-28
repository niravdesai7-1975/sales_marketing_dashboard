import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sales & Marketing AI Use Case Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .priority-high { color: #d62728; font-weight: bold; }
    .priority-medium { color: #ff7f0e; font-weight: bold; }
    .priority-low { color: #2ca02c; font-weight: bold; }
    .sector-common { color: #1f77b4; font-weight: bold; }
    .sector-industrial { color: #2ca02c; font-weight: bold; }
    .value-chain { color: #ff7f0e; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sales_marketing_data():
    """Load and prepare the sales and marketing AI use case data"""
    
    use_cases = [
        'Sales Planning', 'Lead Management', 'Product Planning', 'Personalized Selling',
        'Personalized Quote', 'Providing alternate options for complex / configurable products',
        'Sell products that leverage excess raw material inventory', 'Product availability',
        'Service Contracts', 'Update on product request', '3d model generator',
        'Recommend for upgrade', 'Recommend for upgrade', 'Product recommendation',
        'Proposal analyser', 'Pricing guide', 'Deviations request', 'Customer acquisition',
        'Contact validation', 'Content Generation for marketing', 'Market research assistant',
        'Market research assistant', 'Email Assistant', 'Content Generation',
        'opportunity prioritisation for better lead scoring', 'Customer data insights',
        'CRM data entry assistant', 'Customer segmentation for better lead scoring',
        'Pricing assistant', 'CRM Analytics', 'Sales Forecasting', 'Competitive Benchmarking',
        'Prescriptive modelling', 'Customer Segmentation', 'Sales Product Assistant',
        'Sales Process Assistant', 'Sales Delivery Assistant', 'Generative Product Design',
        'Vision AI for Bearing wear', 'ML to predict customer churn',
        'Sales Eanblement: customer research'
    ]
    
    sectors = [
        'Common', 'Common', 'Common', 'Industrial', 'Industrial', 'Industrial',
        'Industrial', 'Industrial', 'Industrial', 'Industrial', 'Industrial',
        'Industrial', 'Industrial', 'Industrial', 'Industrial', 'Industrial',
        'Industrial', 'Industrial', 'Industrial', 'Industrial', 'Industrial',
        'Industrial', 'Industrial', 'Industrial', 'Industrial', 'Industrial',
        'Industrial', 'Industrial', 'Industrial', 'Common', 'Common', 'Common',
        'Common', 'Common', 'Common', 'Common', 'Common', 'Common', 'Common',
        'Common', 'Common'
    ]
    
    value_chains = [
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing', 'Sales and Marketing',
        'Sales and Marketing'
    ]
    
    personas = [
        'Sales Manager', 'Sales Manager', 'Product Manager', 'Sales Engineer',
        'Sales Engineer', 'Sales Engineer', 'Sales Engineer', 'Sales Engineer',
        'Sales Engineer', 'Sales Rep', 'Sales Rep', 'Sales Rep', 'Sales Rep',
        'Sales Rep', 'Sales Rep', 'Sales Rep', 'Sales Rep', 'Sales Rep',
        'Support', 'Marketing', 'Marketing', 'Marketing', 'Sales Rep',
        'Sales Rep', 'Sales Rep', 'Sales Rep', 'Sales Rep', 'Sales Rep',
        'Sales Rep', 'Sales Rep', 'Sales Engineer', 'Sales Engineer', 'Sales Engineer',
        'Marketing Manager', 'Marketing Department', 'Sales Engineer', 'Sales Engineer',
        'Sales Engineer', 'Product Manager', 'Service reprentative', 'Sales Manager'
    ]
    
    descriptions = [
        '1) Generate region wise sales plan. 2) Generate region wise foot fall expectation per showroom',
        'Tracking, follow up, and other lead generation activities.',
        'Generate various product launch and model line up. Generate Sales projections for models',
        'Customer specific pre-defined product models, dynamic pricing, promotions / special offers',
        'Customized quotes in customer specific formats, terms',
        'Quickly provide alternate quotes that provide better price and delivery terms based on available raw materials if the customer specific requirements are more challenging to comply with. Identify a standard product that is closest to the customer requirement and offer competitive terms.',
        'Promote sales of configurable products based on what can be built with available excess raw material stock (what can you build with available slow moving inventory?)',
        'Throughout the quote cycle as the customer requirements change, provide accurate estimates of product availability and provide inputs to production for early procurement and production activities.',
        'Generate optimized service contracts based on product features, installed base BOM',
        'Auto Generate product description, track request. Provide update on product request',
        'Creation of 3D Elevator Model based on customer requirements, at customer site.',
        'Recommendations for Modernization and upgrades, proposals to the customers based on historic data (service events, IoT, Supply chain, etc.)',
        'Recommendations for a product to be upgraded to next generation. Example " Analyse all Gen2 units so that customer can be contacted to create opportunities to upgrade it to Gen 360".',
        'Recommendations of the product to the customer based on the historical success rate depending on the market segment /competitor and other criteria.',
        'Help Sales Rep to understand factors contributing towards Proposal loss to help Sales Rep make better decision on future proposals',
        'Help Sales Rep with pricing guidance for Service Contract in CRM',
        'Suggest deviations request based on Customer , Product and its configuration , Country',
        'Customer acquisition through historical market data',
        'Periodically validate email Ids and contact numbers of customer POC',
        'Generate high-quality blog posts, articles, product descriptions, and social media content to maintain an active online presence and engage with your audience.',
        'Analyse and summarize market research reports, customer reviews, and social media conversations to identify trends, sentiment, and customer preferences.',
        'Automatically gather and summarize information about competitors\' products, features, pricing, and market positioning.',
        'Sales Emails: Generative AI will assist sales representatives in crafting personalized and persuasive email messages to engage with prospects and customers.',
        'Product Descriptions: AI will generate compelling product descriptions and marketing content, making it easier to create content for online sales channels',
        'Generative AI will analyse and score incoming leads based on various criteria, helping sales teams prioritize and focus on the most promising opportunities.',
        'AI-driven analytics can generate insights from customer data, helping sales teams understand customer preferences, behaviour, and buying patterns to tailor their approach.',
        'Enhance CRM application by automating routine data entry and administrative tasks',
        'Use Gen AI to provide predictive analytics for improved lead scoring and customer segmentation within CRM',
        'Service Sales Dynamic Pricing - assist in dynamically adjusting pricing based on historical data, and other factors.',
        'AI assigns scores to leads based on their likelihood to convert into customers.',
        'AI predicts future sales trends by analyzing historical and real-time data.',
        'AI analyzes market dynamics, competitor pricing, and customer behavior to optimize product pricing',
        'The capability to connect to or build upon the broader OEM\'s telematics and marketing data lakes, harnessing the power of machine learning and next best action to enhance service offerings and customer experience.',
        'AI groups customers based on behavior and preferences, allowing targeted marketing efforts. AI tailors marketing messages to individual customers, enhancing engagement. AI identifies patterns in customer purchasing behavior, suggesting cross-selling or upselling opportunities. Analyse sales calls and meetings, and provides insights to improve communication',
        'Chatbot assisting in providing real-time on the go information on specific product, give product demo suggestions based on live customer data and preferences fed, ideas for better customer engagement',
        'Chatbot assisting with the sales process, contracts, risk compliance, key terms to highlight during negotiations, overall sales deal',
        'Improve lead time calculation accuracy, backorder inventory management, customer prioritization',
        'suggest product innovation ideas based on relevant market intelligence data, analyse current product trends, customer preferences, industry trends. AI monitors social media conversations to gauge customer sentiment and adjust marketing strategies',
        'Leverage Vision AI to identify bearing wear category and use AI to suggest repair based on past data',
        'solution can be used to analyze historical data and use machine learning/deep learning techniques to identify customers likely to churn due to elevator maintenance services.',
        'Create a signle view portal where all the data for the particular customer can be displayed (news, annual reports etc). Leverage gen AI to fetch necessary'
    ]
    
    # Generate synthetic metrics for analysis
    business_impacts = [
        5, 5, 4, 4, 4, 4, 3, 4, 4, 3, 4, 4, 4, 4, 4, 3, 3, 4, 2, 4, 4, 4, 3, 3, 5, 4, 3, 4, 4, 5, 5, 4, 4, 5, 4, 4, 4, 4, 3, 4, 4
    ]
    
    implementation_complexities = [
        4, 3, 4, 3, 3, 4, 3, 4, 4, 2, 4, 4, 4, 3, 4, 3, 3, 4, 2, 3, 3, 3, 2, 2, 4, 3, 2, 4, 3, 4, 4, 3, 4, 4, 3, 3, 4, 4, 4, 4, 3
    ]
    
    estimated_rois = [
        35.0, 40.0, 30.0, 25.0, 25.0, 30.0, 20.0, 30.0, 25.0, 20.0, 35.0, 30.0, 30.0, 25.0, 20.0, 20.0, 20.0, 30.0, 15.0, 30.0, 25.0, 25.0, 20.0, 20.0, 40.0, 30.0, 20.0, 35.0, 25.0, 40.0, 35.0, 30.0, 35.0, 40.0, 30.0, 30.0, 35.0, 35.0, 25.0, 30.0, 30.0
    ]
    
    implementation_timelines = [
        8, 6, 8, 5, 5, 6, 4, 6, 6, 3, 8, 6, 6, 5, 6, 4, 4, 6, 2, 5, 5, 5, 3, 3, 8, 6, 3, 6, 5, 8, 8, 6, 8, 8, 6, 6, 8, 8, 6, 6, 6
    ]
    
    risk_levels = [
        'Medium', 'Low', 'Medium', 'Low', 'Low', 'Medium', 'Low', 'Medium', 'Medium', 'Low', 'High', 'Medium', 'Medium', 'Low', 'Medium', 'Low', 'Low', 'Medium', 'Low', 'Low', 'Low', 'Low', 'Low', 'Low', 'Medium', 'Medium', 'Low', 'Medium', 'Low', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium'
    ]
    
    # Create DataFrame
    df = pd.DataFrame({
        'use_case_name': use_cases,
        'sector': sectors,
        'value_chain': value_chains,
        'persona': personas,
        'description': descriptions,
        'business_impact': business_impacts,
        'implementation_complexity': implementation_complexities,
        'estimated_roi': estimated_rois,
        'implementation_timeline': implementation_timelines,
        'risk_level': risk_levels
    })
    
    # Calculate priority scores
    def calculate_score(row):
        impact_factor = row['business_impact'] * 0.4
        roi_factor = (row['estimated_roi'] / 40.0) * 5 * 0.3
        timeline_factor = ((12 - row['implementation_timeline']) / 12) * 5 * 0.2
        risk_scores = {'Low': 5, 'Medium': 3, 'High': 1}
        risk_factor = risk_scores[row['risk_level']] * 0.1
        return round(impact_factor + roi_factor + timeline_factor + risk_factor, 2)
    
    df['priority_score'] = df.apply(calculate_score, axis=1)
    
    # Add priority category
    def get_priority_category(score):
        if score >= 4.5:
            return 'High Priority'
        elif score >= 4.0:
            return 'Medium Priority'
        else:
            return 'Lower Priority'
    
    df['priority_category'] = df['priority_score'].apply(get_priority_category)
    
    return df

def main():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">📈 Sales & Marketing AI Use Case Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_sales_marketing_data()
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # Sector filter
    selected_sectors = st.sidebar.multiselect(
        "Select Sectors",
        options=df['sector'].unique(),
        default=df['sector'].unique()
    )
    
    # Priority filter
    selected_priorities = st.sidebar.multiselect(
        "Select Priority Levels",
        options=df['priority_category'].unique(),
        default=df['priority_category'].unique()
    )
    
    # Risk level filter
    selected_risks = st.sidebar.multiselect(
        "Select Risk Levels",
        options=df['risk_level'].unique(),
        default=df['risk_level'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['sector'].isin(selected_sectors)) &
        (df['priority_category'].isin(selected_priorities)) &
        (df['risk_level'].isin(selected_risks))
    ]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Use Cases", len(filtered_df))
    
    with col2:
        avg_roi = filtered_df['estimated_roi'].mean()
        st.metric("Average ROI", f"{avg_roi:.1f}%")
    
    with col3:
        avg_priority = filtered_df['priority_score'].mean()
        st.metric("Average Priority Score", f"{avg_priority:.2f}")
    
    with col4:
        high_priority_count = len(filtered_df[filtered_df['priority_category'] == 'High Priority'])
        st.metric("High Priority Cases", high_priority_count)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Priority distribution
        priority_counts = filtered_df['priority_category'].value_counts()
        fig_priority = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            title="Priority Distribution",
            color_discrete_map={
                'High Priority': '#d62728',
                'Medium Priority': '#ff7f0e',
                'Lower Priority': '#2ca02c'
            }
        )
        fig_priority.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_priority, use_container_width=True)
        
        # ROI vs Implementation Timeline
        fig_scatter = px.scatter(
            filtered_df,
            x='implementation_timeline',
            y='estimated_roi',
            color='priority_category',
            size='business_impact',
            hover_data=['use_case_name'],
            title="ROI vs Implementation Timeline",
            labels={'implementation_timeline': 'Implementation Timeline (months)', 'estimated_roi': 'Estimated ROI (%)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Sector distribution
        sector_counts = filtered_df['sector'].value_counts()
        fig_sector = px.bar(
            x=sector_counts.index,
            y=sector_counts.values,
            title="Use Cases by Sector",
            labels={'x': 'Sector', 'y': 'Number of Use Cases'},
            color=sector_counts.index,
            color_discrete_map={
                'Common': '#1f77b4',
                'Industrial': '#2ca02c'
            }
        )
        st.plotly_chart(fig_sector, use_container_width=True)
        
        # Risk level distribution
        risk_counts = filtered_df['risk_level'].value_counts()
        fig_risk = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Level Distribution",
            color_discrete_map={
                'Low': '#2ca02c',
                'Medium': '#ff7f0e',
                'High': '#d62728'
            }
        )
        fig_risk.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Persona analysis
    st.subheader("👥 Persona Analysis")
    persona_counts = filtered_df['persona'].value_counts().head(10)
    fig_persona = px.bar(
        x=persona_counts.values,
        y=persona_counts.index,
        orientation='h',
        title="Top 10 Personas by Use Case Count",
        labels={'x': 'Number of Use Cases', 'y': 'Persona'}
    )
    st.plotly_chart(fig_persona, use_container_width=True)
    
    # Detailed use case table
    st.subheader("📋 Detailed Use Case Analysis")
    
    # Sort by priority score
    sorted_df = filtered_df.sort_values('priority_score', ascending=False)
    
    # Display table with better formatting
    for idx, row in sorted_df.iterrows():
        with st.expander(f"📈 {row['use_case_name']} - Priority Score: {row['priority_score']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {row['description']}")
                st.write(f"**Sector:** {row['sector']}")
                st.write(f"**Persona:** {row['persona']}")
                st.write(f"**Value Chain:** {row['value_chain']}")
            
            with col2:
                st.metric("Business Impact", row['business_impact'])
                st.metric("Implementation Complexity", row['implementation_complexity'])
                st.metric("Estimated ROI", f"{row['estimated_roi']}%")
                st.metric("Timeline", f"{row['implementation_timeline']} months")
                
                # Color-coded priority and risk
                priority_color = "priority-high" if row['priority_category'] == 'High Priority' else \
                               "priority-medium" if row['priority_category'] == 'Medium Priority' else "priority-low"
                
                st.markdown(f'<p class="{priority_color}">Priority: {row["priority_category"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p>Risk Level: {row["risk_level"]}</p>', unsafe_allow_html=True)
    
    # Recommendations section
    st.subheader("💡 Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🚀 Quick Wins (High ROI, Low Complexity):**
        - Lead Management & CRM Analytics
        - Content Generation & Email Assistant
        - Contact Validation & CRM Data Entry
        - Pricing Guide & Deviations Request
        """)
        
        st.markdown("""
        **⚡ High Impact Projects:**
        - Sales Planning & Forecasting
        - Customer Segmentation & Analytics
        - Lead Scoring & Opportunity Prioritization
        - Competitive Benchmarking
        """)
    
    with col2:
        st.markdown("""
        **🔧 Strategic Initiatives:**
        - Generative Product Design
        - 3D Model Generator
        - Vision AI for Bearing Wear
        - Customer Churn Prediction
        """)
        
        st.markdown("""
        **📊 Focus Areas:**
        - Sales Enablement & CRM enhancement
        - Marketing automation & content generation
        - Customer insights & predictive analytics
        - Product innovation & design
        """)
    
    # Value chain insights
    st.subheader("🔗 Value Chain Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Sales Focus:**
        - Lead management and scoring
        - Sales planning and forecasting
        - Customer acquisition and retention
        - Pricing optimization
        """)
    
    with col2:
        st.markdown("""
        **📢 Marketing Focus:**
        - Content generation and automation
        - Market research and competitive analysis
        - Customer segmentation and targeting
        - Social media monitoring and sentiment analysis
        """)

if __name__ == "__main__":
    main()
