import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
from PyPDF2 import PdfReader

# Streamlit app title
st.title("Student Result Analysis")

# File uploader for the result PDF
uploaded_file = st.file_uploader("Upload the Students' Result PDF", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    reader = PdfReader(uploaded_file)
    pdf_text = "".join(page.extract_text() for page in reader.pages)

    # Extract seat numbers, SGPA, and credits earned using regex
    student_data = re.findall(r"SEAT NO\.: (T\d+).*?SGPA\s+:\s+([\d.]+),\s+TOTAL CREDITS EARNED\s+:\s+(\d+)", pdf_text, re.DOTALL)

    # Convert extracted data into a DataFrame
    results_df = pd.DataFrame(student_data, columns=["Seat Number", "SGPA", "Total Credits Earned"])
    results_df["SGPA"] = pd.to_numeric(results_df["SGPA"], errors="coerce")
    results_df["Total Credits Earned"] = pd.to_numeric(results_df["Total Credits Earned"], errors="coerce")

    # Display the extracted data
    st.subheader("Extracted Results Data")
    st.dataframe(results_df)

    # Class-wide SGPA and Credit Analysis
    st.subheader("Class-Wide SGPA and Credit Analysis")
    sgpa_summary = pd.DataFrame({
        "Metric": ["Class Average SGPA", "Highest SGPA", "Lowest SGPA", "Average Total Credits Earned"],
        "Value": [
            results_df["SGPA"].mean().round(2),
            results_df["SGPA"].max(),
            results_df["SGPA"].min(),
            results_df["Total Credits Earned"].mean().round(2)
        ]
    })
    st.table(sgpa_summary)

    # Histogram: Distribution of Total Marks
    st.subheader("Distribution of SGPA")
    plt.figure(figsize=(10, 6))
    plt.hist(results_df["SGPA"], bins=10, color="purple", edgecolor="black", alpha=0.7)
    plt.title("Histogram: Distribution of SGPA")
    plt.xlabel("SGPA")
    plt.ylabel("Frequency")
    st.pyplot(plt)

    # Grade Distribution (Example: Categorizing grades based on SGPA)
    st.subheader("Grade Distribution")
    grades = pd.cut(
        results_df["SGPA"],
        bins=[0, 7, 8, 9, 10],
        labels=["C", "B", "A", "O"]
    ).value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    grades.plot(kind="bar", color="orange")
    plt.title("Bar Chart: Grade Distribution")
    plt.xlabel("Grades")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=0)
    st.pyplot(plt)

    # Scatter Plot: SGPA Distribution vs. Seat Number
    st.subheader("SGPA Distribution")
    plt.figure(figsize=(10, 6))
    plt.scatter(results_df.index, results_df["SGPA"], alpha=0.6, color="blue")
    plt.title("Scatter Plot: SGPA Distribution")
    plt.xlabel("Student Index")
    plt.ylabel("SGPA")
    st.pyplot(plt)

    st.success("Analysis completed! You can upload another file to analyze more results.")
