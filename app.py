import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Complaints Dashboard", layout="wide")

@st.cache_data
def load_data(path=r"C:\Users\DELL\OneDrive\Documents\OneDrive\Desktop\deepanshu project\complaints_app\data.csv"):
    return pd.read_csv(path)

df = load_data(r"C:\Users\DELL\OneDrive\Documents\OneDrive\Desktop\deepanshu project\complaints_app\data.csv")

st.title("📊 Customer Complaints Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌍 Country Analysis", 
    "💳 Product Analysis", 
    "🏢 Company Analysis", 
    "📅 Time Trends", 
    "📊 Comparisons", 
    "🌀 Advanced Views"
])

#  Country 

with tab1:
    st.header("Complaints by Country")
    if "Country" in df.columns:
        top_countries = df["Country"].value_counts().head(10)

        fig = px.bar(top_countries, x=top_countries.index, y=top_countries.values,
                     title="Top  Countries with Complaints",
                     text=top_countries.values,
                     color=top_countries.values, color_continuous_scale="Tealgrn")
        st.plotly_chart(fig, use_container_width=True)

        country_counts = df["Country"].value_counts().reset_index()
        country_counts.columns = ["Country", "Complaints"]
        fig_map = px.choropleth(country_counts, locations="Country", locationmode="country names",
                                color="Complaints", hover_name="Country",
                                title="🌍 Geographical Distribution of Complaints",
                                color_continuous_scale="Plasma")
        st.plotly_chart(fig_map, use_container_width=True)

#  Product 

with tab2:
    st.header("Complaints by Product")
    if "Product" in df.columns:
        product_counts = df["Product"].value_counts()

        fig_pie = px.pie(product_counts, names=product_counts.index,
                         values=product_counts.values, hole=0.4,
                         title="Product-wise Complaints", 
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

       
        if "Country" in df.columns:
            treemap = px.treemap(df, path=["Country", "Product"], 
                                 title="Treemap: Country → Product → Complaints",
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(treemap, use_container_width=True)

#  Company

with tab3:
    st.header("Complaints by Company")
    if "Company" in df.columns:
        top_companies = df["Company"].value_counts().head(15)

        fig_barh = px.bar(top_companies, x=top_companies.values, y=top_companies.index,
                          orientation="h", title="Top Companies with Complaints",
                          text=top_companies.values,
                          color=top_companies.values, color_continuous_scale="Cividis")
        st.plotly_chart(fig_barh, use_container_width=True)

       
        company_counts = df["Company"].value_counts()
        fig_hist = px.histogram(company_counts, nbins=20,
                                title="Histogram: Complaints Distribution Across Companies",
                                color_discrete_sequence=["#E45756"])
        st.plotly_chart(fig_hist, use_container_width=True)


#  Comparisons

with tab5:
    st.header("Comparisons")
    if "Product" in df.columns and "Company response to consumer" in df.columns:
        comp = df.groupby(["Product", "Company response to consumer"]).size().reset_index(name="Count")
        fig_stacked = px.bar(comp, x="Product", y="Count", color="Company response to consumer",
                             title="Stacked Bar: Product vs Company Response",
                             color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_stacked, use_container_width=True)

    if "Country" in df.columns and "Product" in df.columns:
        heatmap_data = df.groupby(["Country", "Product"]).size().reset_index(name="Complaints")
        fig_heatmap = px.density_heatmap(heatmap_data, x="Product", y="Country", z="Complaints",
                                         color_continuous_scale="Viridis",
                                         title="Heatmap: Product vs Country Complaints")
        st.plotly_chart(fig_heatmap, use_container_width=True)

#  Advanced Views

with tab6:
    st.header("Bubble, Scatter & Extra Views")
    if "Company" in df.columns and "Product" in df.columns:
        bubble = df.groupby(["Company", "Product"]).size().reset_index(name="Complaints")
        fig_bubble = px.scatter(bubble, x="Company", y="Product", size="Complaints", color="Product",
                                hover_name="Company", 
                                title="Bubble Chart: Company vs Product Complaints",
                                color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_bubble, use_container_width=True)

    if "Product" in df.columns and "Country" in df.columns:
        fig_strip = px.strip(df, x="Product", y="Country", 
                             title="Strip Plot: Distribution of Complaints by Product & Country",
                             color="Product")
        st.plotly_chart(fig_strip, use_container_width=True)
