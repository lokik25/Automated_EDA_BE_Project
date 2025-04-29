import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="ML Data Explorer", layout="wide")

# Custom CSS for a cool, modern UI
st.markdown("""
    <style>
        /* Background and Font */
        .stApp {
            background: linear-gradient(135deg, #1E3C72, #2A5298);
            font-family: 'Arial', sans-serif;
            color: white;
        }
        
        /* Header */
        .header {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            padding: 15px;
            background: #1B262C;
            color: white;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }

        /* Navbar */
        .navbar {
            display: flex;
            justify-content: center;
            background: #0F4C75;
            padding: 12px;
            border-radius: 10px;
            margin-top: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }

        .navbar a {
            text-decoration: none;
            color: white;
            font-size: 18px;
            margin: 0 15px;
            padding: 10px 15px;
            border-radius: 5px;
            transition: 0.3s;
        }

        .navbar a:hover {
            background: #BBE1FA;
            color: black;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 10px;
            position: fixed;
            bottom: 0;
            width: 100%;
            background: #1B262C;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'>🔍 ML Data Explorer</div>", unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
    <div class="navbar">
        <a href="#eda">📊 EDA</a>
        <a href="#visuals">📈 Visualizations</a>
        <a href="#about">ℹ️ About</a>
    </div>
""", unsafe_allow_html=True)

# Upload dataset
st.markdown("### 📂 Upload Your Dataset (CSV)")
data = st.file_uploader("", type=["csv", "txt"])

if data is not None:
    df = pd.read_csv(data)
    st.write("### 📊 Data Preview")
    st.dataframe(df.head())

    # EDA Section
    st.markdown("<h3 id='eda' style='color:#BBE1FA;'>📊 Exploratory Data Analysis (EDA)</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.checkbox("🔢 Show Shape"):
            st.write(df.shape)

        if st.checkbox("📌 Show Columns"):
            st.write(df.columns.to_list())

    with col2:
        if st.checkbox("📊 Summary Statistics"):
            st.write(df.describe())

        if st.checkbox("🔄 Value Counts"):
            st.write(df.iloc[:, -1].value_counts())

    with col3:
        if st.checkbox("🛠 Select Columns"):
            selected_columns = st.multiselect("Select Columns", df.columns)
            st.dataframe(df[selected_columns])

    # Visualizations Section
    st.markdown("<h3 id='visuals' style='color:#BBE1FA;'>📈 Data Visualizations</h3>", unsafe_allow_html=True)

    plot_type = st.selectbox("Select Plot Type", ["Bar", "Line", "Area", "Histogram", "Box", "KDE"])
    selected_columns = st.multiselect("Select Columns for Plot", df.columns)

    if st.button("Generate Plot"):
        st.success(f"Generating {plot_type} plot for {selected_columns}")

        if plot_type == "Bar":
            st.bar_chart(df[selected_columns])
        elif plot_type == "Line":
            st.line_chart(df[selected_columns])
        elif plot_type == "Area":
            st.area_chart(df[selected_columns])
        else:
            fig, ax = plt.subplots()
            df[selected_columns].plot(kind=plot_type.lower(), ax=ax)
            st.pyplot(fig)

# Footer
st.markdown("<div class='footer'>Made with ❤️ by Moshi</div>", unsafe_allow_html=True)
