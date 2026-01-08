import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# Налаштування сторінки
st.set_page_config(page_title="Real Estate Analysis & Prediction", layout="wide", page_icon="🏠")

# 1. Словник координат центрів районів міста Ames
neighborhood_coords = {
    'CollgCr': [42.020, -93.685], 'Veenker': [42.040, -93.650], 'Crawfor': [42.015, -93.645],
    'NoRidge': [42.050, -93.655], 'Mitchel': [41.990, -93.600], 'Somerst': [42.050, -93.640],
    'NWAmes': [42.045, -93.635], 'OldTown': [42.030, -93.615], 'BrkSide': [42.032, -93.625],
    'Sawyer': [42.033, -93.670], 'NridgHt': [42.060, -93.655], 'NAmes': [42.045, -93.620],
    'SawyerW': [42.035, -93.685], 'IDOTRR': [42.020, -93.622], 'MeadowV': [41.995, -93.610],
    'Edwards': [42.020, -93.665], 'Timber': [41.995, -93.645], 'Gilbert': [42.060, -93.630],
    'StoneBr': [42.060, -93.640], 'ClearCr': [42.030, -93.675], 'NPkVill': [42.050, -93.625],
    'Blmngtn': [42.060, -93.620], 'BrDale': [42.052, -93.620], 'SWISU': [42.020, -93.650],
    'Blueste': [42.010, -93.650]
}

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_real-estate-market-analysis.csv")
    df['lat'] = df['Neighborhood'].map(lambda x: neighborhood_coords.get(x, [42.034, -93.642])[0])
    df['lon'] = df['Neighborhood'].map(lambda x: neighborhood_coords.get(x, [42.034, -93.642])[1])
    return df

try:
    df = load_data()

    st.title("🏠 Real Estate Market Analysis & Prediction")

    # --- БІЧНА ПАНЕЛЬ (Фільтри + ML) ---
    st.sidebar.header("🔍 Фільтри даних")
    
    # Вибір районів
    selected_neighborhoods = st.sidebar.multiselect(
        "Виберіть райони:",
        options=sorted(df["Neighborhood"].unique()),
        default=sorted(df["Neighborhood"].unique())[:5]
    )

    # Вибір року побудови
    year_range = st.sidebar.slider(
        "Рік побудови:",
        int(df["YearBuilt"].min()),
        int(df["YearBuilt"].max()),
        (int(df["YearBuilt"].min()), int(df["YearBuilt"].max()))
    )

    # Фільтрація основного датасету
    filtered_df = df[
        (df["Neighborhood"].isin(selected_neighborhoods)) & 
        (df["YearBuilt"].between(year_range[0], year_range[1]))
    ]

    st.sidebar.markdown("---")
    st.sidebar.header("🔮 Прогноз вартості")
    input_area = st.sidebar.number_input("Площа вашого будинку (кв.фт):", min_value=500, max_value=5000, value=1500)
    input_qual = st.sidebar.slider("Якість обробки (1-10):", 1, 10, 5)

    # Модель ML (навчається на повному датасеті для точності)
    X = df[['GrLivArea', 'OverallQual']]
    y = df['SalePrice']
    model = LinearRegression().fit(X, y)
    prediction = model.predict([[input_area, input_qual]])[0]

    st.sidebar.success(f"Орієнтовна вартість: ${prediction:,.0f}")

    # --- ОСНОВНА ЧАСТИНА (Метрики та Графіки) ---
    
    # Метрики
    col1, col2, col3 = st.columns(3)
    col1.metric("Об'єктів знайдено", len(filtered_df))
    col2.metric("Сер. ціна у вибірці", f"${filtered_df['SalePrice'].mean():,.0f}")
    col3.metric("Ваш прогноз", f"${prediction:,.0f}")

    # Карта (використовує filtered_df)
    st.subheader("📍 Теплова карта цін за районами")
    map_data = filtered_df.groupby('Neighborhood').agg({
        'SalePrice': 'mean', 'lat': 'first', 'lon': 'first'
    }).reset_index()

    fig_map = px.density_mapbox(
        map_data, lat='lat', lon='lon', z='SalePrice', radius=30,
        center=dict(lat=42.034, lon=-93.642), zoom=11,
        mapbox_style="carto-positron", height=400
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Box Plot (використовує filtered_df)
    st.subheader("📦 Розкид цін у вибраних районах")
    fig_box = px.box(filtered_df, x="Neighborhood", y="SalePrice", color="Neighborhood")
    st.plotly_chart(fig_box, use_container_width=True)

    # Scatter Plot (використовує filtered_df)
    st.subheader("📊 Залежність: Площа vs Ціна")
    fig_scatter = px.scatter(
        filtered_df, x="GrLivArea", y="SalePrice", color="OverallQual", 
        hover_name="Neighborhood", trendline="ols"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

except Exception as e:
    st.error(f"Виникла помилка: {e}")
