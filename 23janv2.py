import streamlit as st
import pandas as pd
import plotly.express as px
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

    # Interactive Histogram: Distribution of SGPA
    st.subheader("Distribution of SGPA")
    fig_hist = px.histogram(
        results_df, x="SGPA", nbins=10, title="Distribution of SGPA",
        labels={"SGPA": "SGPA"}, color_discrete_sequence=["purple"]
    )
    fig_hist.update_layout(xaxis_title="SGPA", yaxis_title="Frequency")
    st.plotly_chart(fig_hist)

    # Interactive Grade Distribution (Example: Categorizing grades based on SGPA)
    st.subheader("Grade Distribution")
    results_df["Grade"] = pd.cut(
        results_df["SGPA"],
        bins=[0, 7, 8, 9, 10],
        labels=["C", "B", "A", "O"]
    )
    grade_counts = results_df["Grade"].value_counts().sort_index()

    fig_grade = px.bar(
        x=grade_counts.index, y=grade_counts.values, 
        labels={"x": "Grade", "y": "Number of Students"},
        title="Grade Distribution", color_discrete_sequence=["orange"]
    )
    fig_grade.update_layout(xaxis_title="Grade", yaxis_title="Number of Students")
    st.plotly_chart(fig_grade)

    # Interactive Scatter Plot: SGPA Distribution
    st.subheader("SGPA Distribution")
    fig_scatter = px.scatter(
        results_df, x=results_df.index, y="SGPA", hover_data={"Seat Number": True, "SGPA": True},
        title="Scatter Plot: SGPA Distribution",
        labels={"x": "Student Index", "SGPA": "SGPA"},
        color_discrete_sequence=["blue"]
    )
    fig_scatter.update_layout(xaxis_title="Student Index", yaxis_title="SGPA")
    st.plotly_chart(fig_scatter)

    st.success("Analysis completed! You can upload another file to analyze more results.")
