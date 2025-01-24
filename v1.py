# Core Pkgs
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import ast

def flatten_scores(df):
    """ Function to flatten the JSON-like column into multiple columns """
    try:
        st.write("Flattening Scores")  # Debug message
        scores = df.iloc[:, 2].apply(ast.literal_eval)  # Convert JSON-like strings to dictionaries
        expanded_scores = pd.json_normalize(scores)  # Flatten nested JSON structure into columns
        return pd.concat([df.iloc[:, :2], expanded_scores], axis=1)
    except Exception as e:
        st.error(f"Error in flattening scores: {e}")
        return df  # Return the original if it fails

def main():
    """Semi Automated ML App with Streamlit"""

    activities = ["EDA", "Plots"]
    choice = st.sidebar.selectbox("Select Activities", activities)

    st.write(f"User selected {choice}")  # Debug message

    if choice == 'EDA':
        st.subheader("Exploratory Data Analysis")

        data = st.file_uploader("Upload a Dataset", type=["csv", "txt", "xlsx"])

        if data is not None:
            st.write("File uploaded successfully")  # Debug message

            try:
                if data.name.endswith('.csv') or data.name.endswith('.txt'):
                    df = pd.read_csv(data)
                elif data.name.endswith('.xlsx'):
                    df = pd.read_excel(data)
                
                st.write(df.head())  # Display the dataframe head

                # Flatten the third column containing JSON-like data
                if st.checkbox("Flatten Scores"):
                    df = flatten_scores(df)
                    st.dataframe(df.head())

                if st.checkbox("Show Shape"):
                    st.write(df.shape)

                if st.checkbox("Show Columns"):
                    all_columns = df.columns.to_list()
                    st.write(all_columns)

                if st.checkbox("Summary"):
                    st.write(df.describe())

                if st.checkbox("Show Selected Columns"):
                    selected_columns = st.multiselect("Select Columns", df.columns.to_list())
                    if selected_columns:
                        new_df = df[selected_columns]
                        st.dataframe(new_df)

                if st.checkbox("Show Value Counts"):
                    st.write(df.iloc[:, -1].value_counts())

                if st.checkbox("Correlation Plot (Matplotlib)"):
                    plt.matshow(df.corr())
                    st.pyplot()

                if st.checkbox("Correlation Plot (Seaborn)"):
                    sns.heatmap(df.corr(), annot=True)
                    st.pyplot()

                if st.checkbox("Pie Plot"):
                    column_to_plot = st.selectbox("Select 1 Column", df.columns.to_list())
                    if column_to_plot:
                        pie_plot = df[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
                        st.write(pie_plot)
                        st.pyplot()

            except Exception as e:
                st.error(f"Error loading or processing file: {e}")

    elif choice == 'Plots':
        st.subheader("Data Visualization")
        data = st.file_uploader("Upload a Dataset", type=["csv", "txt", "xlsx"])

        if data is not None:
            st.write("File uploaded successfully")  # Debug message

            try:
                if data.name.endswith('.csv') or data.name.endswith('.txt'):
                    df = pd.read_csv(data)
                elif data.name.endswith('.xlsx'):
                    df = pd.read_excel(data)

                st.dataframe(df.head())

                # Flatten the third column containing JSON-like data
                if st.checkbox("Flatten Scores"):
                    df = flatten_scores(df)
                    st.dataframe(df.head())

                if st.checkbox("Show Value Counts"):
                    st.write(df.iloc[:, -1].value_counts().plot(kind='bar'))
                    st.pyplot()

                all_columns_names = df.columns.tolist()
                type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
                selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

                if st.button("Generate Plot"):
                    st.success(f"Generating Customizable Plot of {type_of_plot} for {selected_columns_names}")

                    if type_of_plot == 'area':
                        cust_data = df[selected_columns_names]
                        st.area_chart(cust_data)

                    elif type_of_plot == 'bar':
                        cust_data = df[selected_columns_names]
                        st.bar_chart(cust_data)

                    elif type_of_plot == 'line':
                        cust_data = df[selected_columns_names]
                        st.line_chart(cust_data)

                    else:
                        cust_plot = df[selected_columns_names].plot(kind=type_of_plot)
                        st.write(cust_plot)
                        st.pyplot()

            except Exception as e:
                st.error(f"Error loading or processing file: {e}")


if __name__ == '__main__':
    main()
