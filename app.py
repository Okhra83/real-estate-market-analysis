import streamlit as st
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(page_title="Аналіз нерухомості Ames", layout="wide")

st.title("🏠 Аналіз ринку нерухомості (Ames, Iowa)")
st.markdown("""
Цей додаток дозволяє аналізувати ціни на будинки залежно від їхньої площі, району та якості побудови.
""")

# 1. Завантаження даних
@st.cache_data
def load_data():
    # На GitHub файл завантажений в папці data/
    df = pd.read_csv("data/cleaned_real-estate-market-analysis.csv")
    return df

df = load_data()

# 2. Бічна панель (Sidebar) для фільтрів
st.sidebar.header("Фільтри")

# Вибір району
neighborhoods = st.sidebar.multiselect(
    "Виберіть район:",
    options=df["Neighborhood"].unique(),
    default=df["Neighborhood"].unique()[:5] # за замовчуванням виберемо перші 5
)

# Вибір діапазону років побудови
year_range = st.sidebar.slider(
    "Рік побудови:",
    int(df["YearBuilt"].min()),
    int(df["YearBuilt"].max()),
    (1950, 2010)
)

# Фільтрація даних
filtered_df = df[
    (df["Neighborhood"].isin(neighborhoods)) & 
    (df["YearBuilt"].between(year_range[0], year_range[1]))
]

# 3. Основні метрики
col1, col2, col3 = st.columns(3)
col1.metric("Кількість будинків", len(filtered_df))
col2.metric("Сер. ціна ($)", f"{filtered_df['SalePrice'].mean():,.0f}")
col3.metric("Сер. площа (кв.фт)", f"{filtered_df['GrLivArea'].mean():,.0f}")

# 4. Візуалізація
st.subheader("Зв'язок ціни та площі")
fig = px.scatter(
    filtered_df, 
    x="GrLivArea", 
    y="SalePrice", 
    color="OverallQual",
    hover_name="Neighborhood",
    labels={"GrLivArea": "Площа (кв. фути)", "SalePrice": "Ціна ($)", "OverallQual": "Якість"},
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Розподіл цін за районами")
fig_box = px.box(
    filtered_df, 
    x="Neighborhood", 
    y="SalePrice", 
    color="Neighborhood",
    title="Розкид цін у вибраних районах"
)
st.plotly_chart(fig_box, use_container_width=True)

# 5. Перегляд сирих даних
if st.checkbox("Показати таблицю даних"):
    st.write(filtered_df)
