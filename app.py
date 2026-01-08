import streamlit as st
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(page_title="Real Estate Market Analysis", layout="wide", page_icon="🏠")

# 1. Словник координат центрів районів міста Ames, Iowa
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

# 2. Завантаження даних
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_real-estate-market-analysis.csv")
    df['lat'] = df['Neighborhood'].map(lambda x: neighborhood_coords.get(x, [42.034, -93.642])[0])
    df['lon'] = df['Neighborhood'].map(lambda x: neighborhood_coords.get(x, [42.034, -93.642])[1])
    return df

try:
    df = load_data()

    st.title("🏠 Аналіз ринку нерухомості (Ames, Iowa)")

    # 3. Бічна панель
    st.sidebar.header("Фільтри пошуку")
    selected_neighborhoods = st.sidebar.multiselect(
        "Виберіть райони:",
        options=sorted(df["Neighborhood"].unique()),
        default=sorted(df["Neighborhood"].unique())[:5]
    )

    year_range = st.sidebar.slider(
        "Рік побудови:",
        int(df["YearBuilt"].min()),
        int(df["YearBuilt"].max()),
        (int(df["YearBuilt"].min()), int(df["YearBuilt"].max()))
    )

    filtered_df = df[
        (df["Neighborhood"].isin(selected_neighborhoods)) & 
        (df["YearBuilt"].between(year_range[0], year_range[1]))
    ]

    # 4. Метрики
    col1, col2, col3 = st.columns(3)
    col1.metric("Кількість об'єктів", len(filtered_df))
    col2.metric("Сер. ціна", f"${filtered_df['SalePrice'].mean():,.0f}")
    col3.metric("Сер. площа", f"{filtered_df['GrLivArea'].mean():,.0f} кв.фт")

    # 5. ГЕОГРАФІЧНА КАРТА
    st.subheader("📍 Теплова карта цін за районами")
    map_data = filtered_df.groupby('Neighborhood').agg({
        'SalePrice': 'mean', 'lat': 'first', 'lon': 'first'
    }).reset_index()

    fig_map = px.density_mapbox(
        map_data, lat='lat', lon='lon', z='SalePrice', radius=40,
        center=dict(lat=42.034, lon=-93.642), zoom=11,
        mapbox_style="carto-positron", height=450
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # 6. ВІЗУАЛІЗАЦІЯ РОЗКИДУ ЦІН (Box Plot)
    st.subheader("📦 Розкид цін у вибраних районах")
    fig_box = px.box(
        filtered_df, 
        x="Neighborhood", 
        y="SalePrice", 
        color="Neighborhood",
        points="all", # показує окремі будинки точками поверх боксів
        title="Розподіл вартості за локаціями",
        labels={'SalePrice': 'Ціна ($)', 'Neighborhood': 'Район'}
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    

    # 7. Зв'язок ціни та площі
    st.subheader("📊 Зв'язок ціни, площі та якості")
    fig_scatter = px.scatter(
        filtered_df, x="GrLivArea", y="SalePrice", color="OverallQual",
        hover_name="Neighborhood", template="plotly_white",
        labels={"GrLivArea": "Площа", "SalePrice": "Ціна"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

except Exception as e:
    st.error(f"Помилка: {e}")
