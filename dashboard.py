import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Marketing Dashboard", layout="wide")
st.header("📊 Google Places Ranking - August 2025")
st.divider()

# ---------------------
# Load the local Excel file from the project folder
@st.cache_data
def load_data():
    file_path = "combined_ranks_202508.xlsx"  # make sure this file exists in your project directory
    return pd.read_excel(file_path)

df = load_data()

# Clean data types
df['Avg Rank'] = pd.to_numeric(df['Avg Rank'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df["Rating"] = df["Rating"].fillna(df.groupby("City")["Rating"].transform("mean"))
df["Reviews"] = df["Reviews"].fillna(df.groupby("City")["Reviews"].transform("mean"))

# ---------------------
# 1. OVERALL VIEW
st.header("🔍 Overall Summary")

col1, col2 = st.columns(2)

with col1:
    # Compute average rank per keyword across all cities
    keyword_avg = df.groupby("Keyword", as_index=False)["Avg Rank"].mean()
    keyword_avg['Color Rank'] = keyword_avg['Avg Rank'].apply(lambda x: min(x, 10))

    # Calculate mean across all keywords
    overall_mean = keyword_avg['Avg Rank'].mean()

    fig_overall = px.bar(
        keyword_avg,
        x="Keyword",
        y="Avg Rank",
        color="Color Rank",
        text="Avg Rank",
        title="Average Rank by Keyword (All Cities)",
        color_continuous_scale="OrRd",
        range_color=(1, 10),
        height=400
    )

    # Add horizontal mean line
    fig_overall.add_shape(
        type="line",
        x0=-0.5,
        x1=len(keyword_avg) - 0.5,
        y0=overall_mean,
        y1=overall_mean,
        line=dict(color="white", width=2, dash="dash")
    )

    # Add annotation for mean line
    fig_overall.add_annotation(
        x=4.5,  # or use x=4.5 depending on layout
        y=overall_mean,
        text=f"Overall Avg. Rank: {overall_mean:.2f}",
        showarrow=False,
        yshift=10,
        font=dict(color="white")
    )

    st.plotly_chart(fig_overall)

with col2:
    st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)
    m1, m2, m3, _ = st.columns(4)
    m2.metric("🔢 Avg. Rank", f"{df['Avg Rank'].mean():.2f}")
    m2.metric("⭐ Avg. Rating", f"{df['Rating'].mean():.2f}")
    m3.metric("🗣️ Total Reviews", f"{int(df['Reviews'].sum() / df['Keyword'].nunique())}")
    m3.metric("🗣️ Avg. Reviews", f"{int(df['Reviews'].mean())}")

st.divider()
# ---------------------
# 2. VIEW BY Location
st.header("🏙️ City View")
selected_city = st.selectbox("Select a City", sorted(df['City'].unique()), width=300)
city_data = df[df['City'] == selected_city]
col5, col6 = st.columns(2)

with col5:
    # Ensure values above 10 are capped visually for coloring
    city_data['Color Rank'] = city_data['Avg Rank'].apply(lambda x: min(x, 10))

    # Calculate mean
    mean_rank = city_data['Avg Rank'].mean()

    #st.subheader(f"Average Rank by Keyword in {selected_city}")
    fig2 = px.bar(
        city_data,
        x="Keyword",
        y="Avg Rank",
        color="Color Rank",
        text="Avg Rank",
        title=f"Average Rank by Keyword in {selected_city}",
        color_continuous_scale="OrRd",
        range_color=(1, 10),
        height=400
    )

    # Add horizontal line for mean
    fig2.add_shape(
        type="line",
        x0=-0.5, x1=len(city_data['Keyword']) - 0.5,  # full width of x-axis
        y0=mean_rank, y1=mean_rank,
        line=dict(color="white", width=2, dash="dash"),
    )

    # Optional: Add annotation for the line
    fig2.add_annotation(
        x=4.5,  # position on x-axis
        y=mean_rank,
        text=f"Avg. Rank: {mean_rank:.2f}",
        showarrow=False,
        yshift=10,
        font=dict(color="white")
    )

    st.plotly_chart(fig2)

with col6:
    st.markdown("<div style='height: 140px;'></div>", unsafe_allow_html=True)
    col7, col8, col9, _ = st.columns(4)
    col8.metric("🔢 Avg. Rank", f"{city_data['Avg Rank'].mean():.2f}")
    col8.metric("⭐ Avg. Rating", f"{city_data['Rating'].mean():.2f}")
    col9.metric("🗣️ Total Reviews", f"{int(city_data['Reviews'].sum() / city_data['Keyword'].nunique())}")

# ---------------------
# Optional: raw table
with st.expander("📄 Explore Data"):
    st.dataframe(df)
