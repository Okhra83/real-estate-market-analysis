# Real Estate Market Analysis 🏠

## 📋 Мета проекту
Цей проект присвячений аналізу факторів, що впливають на вартість житла. Мета — надати інструмент для швидкої візуалізації зв'язку між ціною, площею та якістю будинків у різних районах міста Еймс, штату Айова, США.

## 🛠 Проведена робота
В ході виконання проекту було реалізовано наступне:

Збір даних (Collect Data):

Дані для цього проекту були отримані з репозиторію **OpenML**

Назва датасету: House Prices (Ames, Iowa)

Платформа: OpenML.org

ID датасету: 42165 (або назва house_prices)

Опис датасету: Набір даних включає 79 ознак, що описують майже кожен аспект житлових будинків в Еймсі, Айова

Використано бібліотеку `scikit-learn` для програмного завантаження Ames Housing Dataset безпосередньо в середовищі DataLab: 🔗 https://www.datacamp.com/datalab/w/5660a3b9-6444-45cc-920c-ada99f79d31b/edit

Очищення даних (Clean Data):

Відібрано 5 найбільш релевантних ознак: (SalePrice (Вартість), GrLivArea (Площа), Neighborhood (Район забудови), OverallQual (Якість оздоблення), YearBuilt (Рік будівництва)).

![Dashboard Screenshot](newplot4.png)

Видалено пропущені значення та відкориговано типи даних.

Дані збережено у компактний формат CSV для оптимізації швидкості роботи додатка.

Розробка дашборду (Present Findings): 

Створено інтерактивний інтерфейс на Streamlit з фільтрацією за районами та роком забудови.

Реалізовано статистичну теплову карту для виявлення найбільш значущих факторів впливу на вартість об'єктів.

Здійснено адаптацію даних під європейський ринок: автоматична конвертація площі з квадратних футів у квадратні метри.

## 📊 Математична модель
Для прогнозування використовується модель **багатофакторної лінійної регресії**. 
Формула прогнозу:
$$Price = (w_1 \cdot Area) + (w_2 \cdot Quality) + b$$

Модель враховує житлову площу та загальні бали якості забудови (Overall Quality за шкалою 1-10).

## 📊 Основні висновки (Insights)
Кореляція ціни та площі: Спостерігається чітка лінійна залежність — чим більша житлова площа (GrLivArea), тим вища ціна продажу.

Вплив якості: Будинки з високим показником OverallQual (загальна якість) мають значно вищу ціну навіть при аналогічній площі.

Територіальний фактор: Найвищі ціни на нерухомість зафіксовані в районах, побудованих після 2000-х років.

Додатково: Район Northridge має найбільший розкид цін, що свідчить про різноманітність типів забудови в цій локації.

Проект доводить, що поєднання візуалізації та машинного навчання дозволяє робити ринок нерухомості прозорим та прогнозованим.

## 🚀 Функціонал
- **Інтерактивна аналітика:** Фільтрація об'єктів за районами та роком побудови.
- **Гео-візуалізація:** Теплова карта цін за районами міста.
- **Статистичний аналіз:** Порівняння розподілу цін (Box Plots) та виявлення залежностей (Scatter Plots).
- **ML Прогноз:** Моментальне оцінювання вартості будинку на основі його площі та якості обробки.

![Dashboard Screenshot](newplot.png)

![Dashboard Screenshot](newplot2.png)

![Dashboard Screenshot](newplot3.png)

Запуск локально:

Клонуйте репозиторій: git clone https://github.com/Okhra83/real-estate-market-analysis.git

Встановіть необхідні бібліотеки: pip install -r requirements.txt

Запустіть сервер Streamlit: streamlit run app.py

Хмарні сервіси:

Демо-версія проекту на Streamlit: 🔗 https://real-estate-market-analysis-49dub7safnm3eraopw9zuu.streamlit.app/

Або:

<div align="center">
  <img src=qr.png width="200" alt="QR Code">
  <p><i>Відскануйте, щоб відкрити додаток</i></p>
</div>

## 🧪 Викоритсані інструменти
* **Python 3.9+**
* **Streamlit:** Створення веб-інтерфейсу.
* **Pandas & NumPy:** Обробка та очищення даних.
* **Plotly:** Створення інтерактивних графіків та карт.
* **Scikit-Learn:** Модель машинного навчання (Linear Regression).
* **Statsmodels:** Розрахунок ліній тренду.

## 📂 Структура проекту
* `app.py` — головний файл додатку Streamlit.
* `notebooks/` — Jupyter Notebook з процесом отримання та очищення даних (DataLab).
* `data/` — очищений набір даних у форматі CSV.
* `requirements.txt` — список необхідних бібліотек.
```text
real-estate-market-analysis/                      # Репозиторій проекту
├── data/
│   └── cleaned_real-estate-market-analysis.csv   # Очищені та підготовлені дані
├── notebooks/
│   └── data_preprocessing.ipynb                  # Jupyter Notebook з процесом отримання та очищення даних (DataLab)
├── app.py                                        # Код додатка Streamlit
├── requirements.txt                              # Залежності проекту
└── README.md                                     # Документація проекту
```

---
## 👨‍💻 Автор

**Kostiantyn Okhrimchuk** *Data Science Student*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kostiantyn-okhrimchuk-3842a3384/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Okhra83)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:konstantin.okhrimchuk@gmail.com)
