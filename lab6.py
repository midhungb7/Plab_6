
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Karnataka Agriculture Crop Yield Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Built-in Domain Dataset (Karnataka Crop Yield Records)
@st.cache_data
def load_data():
    data = {
        "Record_ID": [f"KA{i:03d}" for i in range(1, 37)],
        "District": [
            "Mandya", "Belagavi", "Tumakuru", "Dharwad", "Shivamogga", "Kalaburagi",
            "Mandya", "Belagavi", "Tumakuru", "Dharwad", "Shivamogga", "Kalaburagi",
            "Mandya", "Belagavi", "Tumakuru", "Dharwad", "Shivamogga", "Kalaburagi",
            "Mandya", "Belagavi", "Tumakuru", "Dharwad", "Shivamogga", "Kalaburagi",
            "Mandya", "Belagavi", "Tumakuru", "Dharwad", "Shivamogga", "Kalaburagi",
            "Mandya", "Belagavi", "Tumakuru", "Dharwad", "Shivamogga", "Kalaburagi"
        ],
        "Crop": [
            "Sugarcane", "Sugarcane", "Ragi", "Maize", "Paddy", "Tur",
            "Paddy", "Cotton", "Groundnut", "Paddy", "Sugarcane", "Maize",
            "Ragi", "Maize", "Paddy", "Cotton", "Sugarcane", "Groundnut",
            "Sugarcane", "Sugarcane", "Ragi", "Maize", "Paddy", "Tur",
            "Paddy", "Cotton", "Groundnut", "Paddy", "Sugarcane", "Maize",
            "Ragi", "Maize", "Paddy", "Cotton", "Sugarcane", "Groundnut"
        ],
        "Crop_Type": [
            "Cash Crop", "Cash Crop", "Food Grain", "Food Grain", "Food Grain", "Pulse",
            "Food Grain", "Cash Crop", "Oilseed", "Food Grain", "Cash Crop", "Food Grain",
            "Food Grain", "Food Grain", "Food Grain", "Cash Crop", "Cash Crop", "Oilseed",
            "Cash Crop", "Cash Crop", "Food Grain", "Food Grain", "Food Grain", "Pulse",
            "Food Grain", "Cash Crop", "Oilseed", "Food Grain", "Cash Crop", "Food Grain",
            "Food Grain", "Food Grain", "Food Grain", "Cash Crop", "Cash Crop", "Oilseed"
        ],
        "Season": [
            "Kharif", "Kharif", "Kharif", "Rabi", "Kharif", "Kharif",
            "Rabi", "Kharif", "Summer", "Kharif", "Kharif", "Rabi",
            "Summer", "Kharif", "Rabi", "Rabi", "Kharif", "Summer",
            "Kharif", "Kharif", "Kharif", "Rabi", "Kharif", "Kharif",
            "Rabi", "Kharif", "Summer", "Kharif", "Kharif", "Rabi",
            "Summer", "Kharif", "Rabi", "Rabi", "Kharif", "Summer"
        ],
        "Year": [
            2021, 2021, 2021, 2021, 2021, 2021,
            2022, 2022, 2022, 2022, 2022, 2022,
            2023, 2023, 2023, 2023, 2023, 2023,
            2024, 2024, 2024, 2024, 2024, 2024,
            2025, 2025, 2025, 2025, 2025, 2025,
            2026, 2026, 2026, 2026, 2026, 2026
        ],
        "Area_Hectares": [
            1500, 3200, 4100, 2200, 3100, 5000,
            1600, 2800, 1800, 2500, 3300, 4800,
            2100, 2400, 3900, 1900, 3400, 2000,
            1550, 3250, 4150, 2250, 3150, 5050,
            1650, 2850, 1850, 2550, 3350, 4850,
            2150, 2450, 3950, 1950, 3450, 2050
        ],
        "Production_Tonnes": [
            142500, 288000, 7790, 8800, 10850, 4200,
            152000, 11200, 3240, 9750, 313500, 19200,
            4410, 9600, 13650, 7600, 323000, 3600,
            147250, 292500, 7885, 9000, 11025, 4242,
            156750, 11400, 3330, 9945, 318250, 19400,
            4515, 9800, 13825, 7800, 327750, 3690
        ]
    }
    df = pd.DataFrame(data)
    df["Yield_Tonnes_Per_Ha"] = (df["Production_Tonnes"] / df["Area_Hectares"]).round(2)
    return df

df_raw = load_data()

# Sidebar Filters
st.sidebar.title("Crop Yield Analytics")
st.sidebar.markdown("---")
st.sidebar.header("Data Filters")

crop_type_options = ["All"] + sorted(df_raw["Crop_Type"].unique().tolist())
selected_crop_type = st.sidebar.selectbox("Crop Type", crop_type_options)

district_options = sorted(df_raw["District"].unique().tolist())
selected_districts = st.sidebar.multiselect("District", district_options, default=district_options)

season_options = sorted(df_raw["Season"].unique().tolist())
selected_seasons = st.sidebar.multiselect("Season", season_options, default=season_options)

min_year, max_year = int(df_raw["Year"].min()), int(df_raw["Year"].max())
selected_year = st.sidebar.slider("Harvest Year Range", min_year, max_year, (min_year, max_year))

min_area, max_area = int(df_raw["Area_Hectares"].min()), int(df_raw["Area_Hectares"].max())
selected_area = st.sidebar.slider("Cultivated Area (Hectares)", min_area, max_area, (min_area, max_area), step=100)

st.sidebar.markdown("---")
st.sidebar.header("Plot Settings")
sample_size = st.sidebar.slider("Sample Size for Dense Plots", 10, 36, 36, step=1)

st.sidebar.markdown("---")
st.sidebar.text("Dataset: Karnataka Agricultural Yield\nTotal Records: 36\nDomain: Agriculture Analytics")

# Filter Data
df = df_raw.copy()
if selected_crop_type != "All":
    df = df[df["Crop_Type"] == selected_crop_type]
if selected_districts:
    df = df[df["District"].isin(selected_districts)]
if selected_seasons:
    df = df[df["Season"].isin(selected_seasons)]
df = df[(df["Year"] >= selected_year[0]) & (df["Year"] <= selected_year[1])]
df = df[(df["Area_Hectares"] >= selected_area[0]) & (df["Area_Hectares"] <= selected_area[1])]

df_sample = df.sample(n=min(sample_size, len(df)), random_state=42) if len(df) > 0 else df

# Header
st.title("🌾 Karnataka Agricultural Crop Yield Analytics")

# Navigation Tabs
tab_overview, tab_line, tab_scatter, tab_hist, tab_heat, tab_box, tab_multi, tab_insights = st.tabs([
    "Dataset Overview",
    "Line Plot",
    "Scatter Plot",
    "Histogram",
    "Heatmap",
    "Box Plot",
    "Multiple Variable Plot",
    "Insights and Conclusion"
])

PLOT_TEMPLATE = "simple_white"

# ----------------------------------------------------
# TAB 1: DATASET OVERVIEW
# ----------------------------------------------------
with tab_overview:
    st.header("Key Performance Indicators (KPIs)")

    total_records = len(df)
    total_production = df["Production_Tonnes"].sum()
    avg_production = df["Production_Tonnes"].mean() if total_records > 0 else 0
    total_area = df["Area_Hectares"].sum()
    avg_yield = (total_production / total_area) if total_area > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Records", f"{total_records:,}")
    col2.metric("Total Production", f"{total_production/1e5:.2f} Lakh t")
    col3.metric("Avg Production / Record", f"{avg_production:,.0f} t")
    col4.metric("Total Area", f"{total_area:,} ha")
    col5.metric("Weighted Mean Yield", f"{avg_yield:.2f} t/ha")

    st.markdown("---")
    st.header("Category-wise Summary")

    c_a, c_b, c_c = st.columns(3)
    with c_a:
        st.subheader("By Crop Type")
        type_summary = (
            df.groupby("Crop_Type")
            .agg(Count=("Record_ID", "count"), Total_Production=("Production_Tonnes", "sum"), Avg_Yield=("Yield_Tonnes_Per_Ha", "mean"))
            .reset_index()
            .sort_values("Count", ascending=False)
        )
        type_summary["Total_Production"] = type_summary["Total_Production"].map("{:,.0f} t".format)
        type_summary["Avg_Yield"] = type_summary["Avg_Yield"].map("{:.2f} t/ha".format)
        st.dataframe(type_summary, use_container_width=True, hide_index=True)

    with c_b:
        st.subheader("By District")
        district_summary = (
            df.groupby("District")
            .agg(Count=("Record_ID", "count"), Total_Production=("Production_Tonnes", "sum"), Avg_Area=("Area_Hectares", "mean"))
            .reset_index()
            .sort_values("Total_Production", ascending=False)
        )
        district_summary["Total_Production"] = district_summary["Total_Production"].map("{:,.0f} t".format)
        district_summary["Avg_Area"] = district_summary["Avg_Area"].map("{:,.0f} ha".format)
        st.dataframe(district_summary, use_container_width=True, hide_index=True)

    with c_c:
        st.subheader("By Season")
        season_summary = (
            df.groupby("Season")
            .agg(Count=("Record_ID", "count"), Avg_Production=("Production_Tonnes", "mean"))
            .reset_index()
            .sort_values("Count", ascending=False)
        )
        season_summary["Avg_Production"] = season_summary["Avg_Production"].map("{:,.0f} t".format)
        st.dataframe(season_summary, use_container_width=True, hide_index=True)

    st.markdown("---")
    with st.expander("View Filtered Data Table", expanded=False):
        st.dataframe(df, use_container_width=True)
        st.caption(f"Displaying {total_records:,} filtered observations.")

    with st.expander("Statistical Summary of Numerical Attributes", expanded=False):
        st.dataframe(
            df[["Year", "Area_Hectares", "Production_Tonnes", "Yield_Tonnes_Per_Ha"]].describe().round(2),
            use_container_width=True
        )

# ----------------------------------------------------
# TAB 2: LINE PLOT
# ----------------------------------------------------
with tab_line:
    st.header("Line Plot: Temporal Trends")
    st.write("Line plots represent changes and variations in crop metrics over harvest years.")

    yearly_metrics = (
        df.groupby("Year")
        .agg(
            Total_Production=("Production_Tonnes", "sum"),
            Avg_Yield=("Yield_Tonnes_Per_Ha", "mean"),
            Total_Area=("Area_Hectares", "sum")
        )
        .reset_index()
        .sort_values("Year")
    )

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        fig_line1 = px.line(
            yearly_metrics,
            x="Year",
            y="Total_Production",
            markers=True,
            title="Yearly Total Crop Production Trend",
            labels={"Year": "Harvest Year", "Total_Production": "Production (Tonnes)"},
            template=PLOT_TEMPLATE
        )
        st.plotly_chart(fig_line1, use_container_width=True)
        st.caption("Figure: Line plot tracing total agricultural output across consecutive harvest years.")

    with col_l2:
        fig_line2 = px.line(
            yearly_metrics,
            x="Year",
            y="Avg_Yield",
            markers=True,
            title="Yearly Average Yield Trend",
            labels={"Year": "Harvest Year", "Avg_Yield": "Average Yield (Tonnes/Ha)"},
            template=PLOT_TEMPLATE
        )
        st.plotly_chart(fig_line2, use_container_width=True)
        st.caption("Figure: Line plot illustrating variations in mean yield density over harvest years.")

    # Cumulative Production Line Chart
    yearly_metrics["Cumulative_Production"] = yearly_metrics["Total_Production"].cumsum()
    fig_line3 = px.line(
        yearly_metrics,
        x="Year",
        y="Cumulative_Production",
        markers=True,
        title="Cumulative Production Growth Over Time",
        labels={"Year": "Harvest Year", "Cumulative_Production": "Cumulative Production (Tonnes)"},
        template=PLOT_TEMPLATE
    )
    st.plotly_chart(fig_line3, use_container_width=True)
    st.caption("Figure: Line plot tracking cumulative crop production generated across successive harvest seasons.")

# ----------------------------------------------------
# TAB 3: SCATTER PLOT
# ----------------------------------------------------
with tab_scatter:
    st.header("Scatter Plot: Bivariate Numerical Relationships")
    st.write("Scatter plots display relationships, clusters, and outliers between area and production.")

    c_s1, c_s2 = st.columns([3, 1])
    with c_s2:
        scatter_color_var = st.selectbox("Group by Variable", ["Crop_Type", "Season", "District"], key="scatter_col")
        scatter_x = st.selectbox("X-axis Variable", ["Area_Hectares", "Year"], index=0)
        scatter_y = st.selectbox("Y-axis Variable", ["Production_Tonnes", "Yield_Tonnes_Per_Ha"], index=0)

    with c_s1:
        fig_scatter = px.scatter(
            df_sample,
            x=scatter_x,
            y=scatter_y,
            color=scatter_color_var,
            hover_data=["Crop", "District", "Season", "Year"],
            title=f"Scatter Plot: {scatter_y} vs {scatter_x} (Categorized by {scatter_color_var})",
            labels={scatter_x: scatter_x.replace("_", " "), scatter_y: scatter_y.replace("_", " ")},
            template=PLOT_TEMPLATE,
            opacity=0.8
        )
        fig_scatter.update_layout(height=480)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption(f"Figure: Scatter plot depicting correlation between {scatter_x} and {scatter_y}.")

    # Secondary Bubble Style Scatter Plot
    fig_scatter2 = px.scatter(
        df_sample,
        x="Area_Hectares",
        y="Production_Tonnes",
        size="Yield_Tonnes_Per_Ha",
        color="Crop_Type",
        hover_data=["Crop", "District"],
        title="Scatter Plot: Production vs Area (Point Size Proportional to Yield per Ha)",
        labels={"Area_Hectares": "Cultivated Area (ha)", "Production_Tonnes": "Production (Tonnes)"},
        template=PLOT_TEMPLATE,
        opacity=0.8
    )
    fig_scatter2.update_layout(height=460)
    st.plotly_chart(fig_scatter2, use_container_width=True)
    st.caption("Figure: Multivariate scatter plot mapping Area, Production, and Yield density across Crop Types.")

# ----------------------------------------------------
# TAB 4: HISTOGRAM
# ----------------------------------------------------
with tab_hist:
    st.header("Histogram: Univariate and Bivariate Distributions")
    st.write("Histograms show the frequency distribution and spread of continuous numerical crop variables.")

    col_h1, col_h2 = st.columns(2)

    with col_h1:
        fig_hist1 = px.histogram(
            df,
            x="Area_Hectares",
            nbins=15,
            color="Season",
            barmode="overlay",
            opacity=0.7,
            title="Histogram: Area Distribution by Season",
            labels={"Area_Hectares": "Cultivated Area (Hectares)", "count": "Frequency"},
            template=PLOT_TEMPLATE
        )
        st.plotly_chart(fig_hist1, use_container_width=True)
        st.caption("Figure: Overlaid histogram displaying frequency distribution of cultivated area by season.")

    with col_h2:
        fig_hist2 = px.histogram(
            df,
            x="Production_Tonnes",
            nbins=15,
            color="Crop_Type",
            barmode="overlay",
            opacity=0.7,
            title="Histogram: Production Volume Distribution by Crop Type",
            labels={"Production_Tonnes": "Production (Tonnes)", "count": "Frequency"},
            template=PLOT_TEMPLATE
        )
        st.plotly_chart(fig_hist2, use_container_width=True)
        st.caption("Figure: Histogram of crop production volume partitioned across crop categories.")

    # Yield histogram
    fig_hist3 = px.histogram(
        df,
        x="Yield_Tonnes_Per_Ha",
        nbins=12,
        title="Histogram: Distribution of Crop Yield Density (t/ha)",
        labels={"Yield_Tonnes_Per_Ha": "Yield Density (Tonnes per Hectare)", "count": "Record Count"},
        template=PLOT_TEMPLATE
    )
    st.plotly_chart(fig_hist3, use_container_width=True)
    st.caption("Figure: Discrete histogram illustrating crop yield efficiency values.")

# ----------------------------------------------------
# TAB 5: HEATMAP
# ----------------------------------------------------
with tab_heat:
    st.header("Heatmap: Correlation Matrix and Cross-Tabulation")
    st.write("Heatmaps reveal pattern density, association strength, and correlation across multi-dimensional crop features.")

    col_ht1, col_ht2 = st.columns(2)

    with col_ht1:
        # Correlation Heatmap
        corr_matrix = df[["Year", "Area_Hectares", "Production_Tonnes", "Yield_Tonnes_Per_Ha"]].corr().round(3)
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues",
            title="Correlation Heatmap: Numerical Attributes",
            template=PLOT_TEMPLATE
        )
        fig_corr.update_layout(height=420)
        st.plotly_chart(fig_corr, use_container_width=True)
        st.caption("Figure: Heatmap showing pairwise Pearson correlation coefficients between numerical metrics.")

    with col_ht2:
        # Cross-tabulation Heatmap (District vs Crop Type)
        pivot_dist_type = (
            df.groupby(["District", "Crop_Type"])["Record_ID"]
            .count()
            .reset_index()
            .pivot(index="District", columns="Crop_Type", values="Record_ID")
            .fillna(0)
        )
        fig_pivot = px.imshow(
            pivot_dist_type,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Purples",
            title="Cross-Tabulation Heatmap: Record Count by District and Crop Type",
            template=PLOT_TEMPLATE
        )
        fig_pivot.update_layout(height=420)
        st.plotly_chart(fig_pivot, use_container_width=True)
        st.caption("Figure: Two-way heatmap showing crop record distribution across District and Crop Type.")

    # 2D Density Heatmap
    fig_density = px.density_heatmap(
        df_sample,
        x="Area_Hectares",
        y="Production_Tonnes",
        nbinsx=15,
        nbinsy=15,
        color_continuous_scale="Viridis",
        title="2D Density Heatmap: Data Concentration by Area and Production",
        labels={"Area_Hectares": "Area (ha)", "Production_Tonnes": "Production (Tonnes)"},
        template=PLOT_TEMPLATE
    )
    fig_density.update_layout(height=440)
    st.plotly_chart(fig_density, use_container_width=True)
    st.caption("Figure: 2D histogram density heatmap illustrating bivariate density of Area vs Production.")

# ----------------------------------------------------
# TAB 6: BOX PLOT
# ----------------------------------------------------
with tab_box:
    st.header("Box Plot: Spread, Quartiles, and Outliers")
    st.write("Box plots illustrate median, interquartile ranges (IQR), and outliers across agricultural cohorts.")

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        fig_box1 = px.box(
            df,
            x="Crop_Type",
            y="Production_Tonnes",
            color="Crop_Type",
            notched=True,
            title="Box Plot: Production Volume by Crop Type",
            labels={"Production_Tonnes": "Production (Tonnes)", "Crop_Type": "Crop Type"},
            template=PLOT_TEMPLATE
        )
        fig_box1.update_layout(showlegend=False)
        st.plotly_chart(fig_box1, use_container_width=True)
        st.caption("Figure: Notched box plot showing production distribution, medians, and outliers by crop type.")

    with col_b2:
        fig_box2 = px.box(
            df,
            x="District",
            y="Yield_Tonnes_Per_Ha",
            color="District",
            notched=True,
            title="Box Plot: Crop Yield Density by District",
            labels={"Yield_Tonnes_Per_Ha": "Yield (Tonnes/Ha)", "District": "District"},
            template=PLOT_TEMPLATE
        )
        fig_box2.update_layout(showlegend=False)
        st.plotly_chart(fig_box2, use_container_width=True)
        st.caption("Figure: Box plot comparing crop yield variation and IQR across Karnataka districts.")

    col_b3, col_b4 = st.columns(2)

    with col_b3:
        fig_box3 = px.box(
            df,
            x="Season",
            y="Area_Hectares",
            color="Season",
            title="Box Plot: Cultivated Area by Season",
            labels={"Area_Hectares": "Area (Hectares)", "Season": "Season"},
            template=PLOT_TEMPLATE
        )
        fig_box3.update_layout(showlegend=False)
        st.plotly_chart(fig_box3, use_container_width=True)
        st.caption("Figure: Box plot showing area variation across seasons.")

    with col_b4:
        fig_box4 = px.box(
            df,
            x="Crop_Type",
            y="Yield_Tonnes_Per_Ha",
            color="Crop_Type",
            title="Box Plot: Yield Density by Crop Type",
            labels={"Yield_Tonnes_Per_Ha": "Yield (Tonnes/Ha)", "Crop_Type": "Crop Type"},
            template=PLOT_TEMPLATE
        )
        fig_box4.update_layout(showlegend=False)
        st.plotly_chart(fig_box4, use_container_width=True)
        st.caption("Figure: Box plot illustrating average yield per hectare per crop category.")

# ----------------------------------------------------
# TAB 7: MULTIPLE VARIABLE PLOT
# ----------------------------------------------------
with tab_multi:
    st.header("Multiple Variable Plot: High-Dimensional Analytics")
    st.write("Multiple variable plots display relationships and multidimensional variations across several numerical features concurrently.")

    # 1. Scatter Matrix (Pair Plot)
    st.subheader("1. Scatter Matrix (Pair Plot)")
    fig_matrix = px.scatter_matrix(
        df_sample,
        dimensions=["Year", "Area_Hectares", "Production_Tonnes", "Yield_Tonnes_Per_Ha"],
        color="Crop_Type",
        title="Scatter Matrix of Multiple Numerical Variables by Crop Type",
        labels={
            "Year": "Year",
            "Area_Hectares": "Area",
            "Production_Tonnes": "Production",
            "Yield_Tonnes_Per_Ha": "Yield"
        },
        template=PLOT_TEMPLATE,
        opacity=0.7
    )
    fig_matrix.update_traces(diagonal_visible=False, marker=dict(size=5))
    fig_matrix.update_layout(height=600)
    st.plotly_chart(fig_matrix, use_container_width=True)
    st.caption("Figure: Pairwise scatter matrix comparing 4 numerical attributes simultaneously colored by crop type.")

    st.markdown("---")

    # 2. Parallel Coordinates Plot
    st.subheader("2. Parallel Coordinates Plot")
    type_numerical_map = {"Food Grain": 0, "Cash Crop": 1, "Pulse": 2, "Oilseed": 3}
    df_parallel = df_sample.copy()
    df_parallel["Type_Code"] = df_parallel["Crop_Type"].map(type_numerical_map)

    fig_parallel = px.parallel_coordinates(
        df_parallel,
        dimensions=["Year", "Area_Hectares", "Production_Tonnes", "Yield_Tonnes_Per_Ha", "Type_Code"],
        color="Type_Code",
        color_continuous_scale=px.colors.diverging.Tealrose,
        title="Parallel Coordinates Plot: High-Dimensional Attribute Paths by Crop Type",
        labels={
            "Year": "Year",
            "Area_Hectares": "Area (ha)",
            "Production_Tonnes": "Prod (t)",
            "Yield_Tonnes_Per_Ha": "Yield (t/ha)",
            "Type_Code": "Type (0:FG, 1:CC, 2:Pul, 3:Oil)"
        },
        template=PLOT_TEMPLATE
    )
    fig_parallel.update_layout(height=480)
    st.plotly_chart(fig_parallel, use_container_width=True)
    st.caption("Figure: Parallel coordinates plot depicting individual crop record trajectories across all continuous variables.")

# ----------------------------------------------------
# TAB 8: INSIGHTS AND CONCLUSION
# ----------------------------------------------------
with tab_insights:
    st.header("Key Analytical Observations and Insights")

    top_district = df_raw.groupby("District")["Production_Tonnes"].sum().idxmax()
    top_district_prod = df_raw.groupby("District")["Production_Tonnes"].sum().max()
    cash_pct = round(df_raw[df_raw["Crop_Type"] == "Cash Crop"].shape[0] / len(df_raw) * 100, 1)
    top_season = df_raw["Season"].value_counts().idxmax()
    area_prod_corr = round(df_raw["Area_Hectares"].corr(df_raw["Production_Tonnes"]), 3)

    st.subheader("1. Geographic Concentration")
    st.info(f"{top_district} leads all districts with total crop production of {top_district_prod:,.0f} tonnes, representing the highest agricultural volume.")

    st.subheader("2. Crop Type Breakdown")
    st.info(f"{cash_pct}% of recorded crops belong to the Cash Crop category (e.g., Sugarcane), contributing heavily to gross tonnage.")

    st.subheader("3. Core Season Segment")
    st.info(f"The {top_season} season constitutes the largest harvesting window, making it critical for state yield modeling.")

    st.subheader("4. Area-to-Production Correlation")
    st.info(f"The correlation between Cultivated Area and Total Production is {area_prod_corr}, demonstrating a direct relationship between field area and output volume.")

    st.subheader("5. Yield Density Variation")
    st.warning("Cash crops like Sugarcane yield over 90 tonnes per hectare, whereas food grains and pulses range between 1.0 to 4.5 t/ha.")

    st.markdown("---")
    st.header("District-wise Aggregate Metrics")
    district_table = (
        df_raw.groupby("District")
        .agg(
            Record_Count=("Record_ID", "count"),
            Total_Production=("Production_Tonnes", "sum"),
            Average_Area=("Area_Hectares", "mean"),
            Average_Yield=("Yield_Tonnes_Per_Ha", "mean")
        )
        .reset_index()
        .sort_values("Total_Production", ascending=False)
    )
    district_table["Total_Production"] = district_table["Total_Production"].map("{:,.0f} t".format)
    district_table["Average_Area"] = district_table["Average_Area"].map("{:,.0f} ha".format)
    district_table["Average_Yield"] = district_table["Average_Yield"].map("{:.2f} t/ha".format)
    st.dataframe(district_table, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.header("Conclusion")
    st.markdown("""
This web analytics application provides an interactive, structured platform to explore and evaluate crop yield data for Karnataka.
By implementing the requested visualization types:

- **Line Plot**: Effectively tracks yearly total production, average yield trends, and cumulative production growth.
- **Scatter Plot**: Explores numerical relationships between cultivated area and total production across crop categories.
- **Histogram**: Assesses univariate frequency distributions and spreads for area, production volume, and yield density.
- **Heatmap**: Quantifies correlation coefficients and visualizes crop record distribution across district and crop type dimensions.
- **Box Plot**: Identifies medians, interquartile ranges, and outliers across crop categories and geographic districts.
- **Multiple Variable Plot**: Evaluates multivariate interactions simultaneously via Scatter Matrix and Parallel Coordinates.

The application adheres to clean interface guidelines, dynamic filter responsiveness, and comprehensive layout components.
    """)

