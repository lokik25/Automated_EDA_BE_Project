import streamlit as st
import pandas as pd
import plotly.express as px

def classify_marks(marks):
    if pd.isna(marks):  # Handle missing values
        return None
    elif marks >= 75:
        return "Distinction"
    elif marks >= 60:
        return "First Class"
    elif marks >= 50:
        return "Second Class"
    else:
        return "Fail"

def main():
    st.title("Automated Result Analysis")
    st.write("Upload a CSV file to analyze student results.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Data Preview")
        st.dataframe(df.head())
        
        if "SGPA" in df.columns:
            # Top 10 Students based on SGPA
            top_10_students = df.sort_values(by="SGPA", ascending=False).head(10)
            st.write("### Top 10 Students (Based on SGPA)")
            st.dataframe(top_10_students)
            
            # All Clear vs Fail classification
            df["Status"] = df["SGPA"].apply(lambda x: "All Clear" if x > 0 else "Fail")
            status_counts = df["Status"].value_counts()
            st.write("### All Clear vs Fail Analysis")
            st.dataframe(df[["Seat Number", "SGPA", "Status"]])
            
            # Visualization: All Clear vs Fail using Plotly
            fig = px.bar(status_counts, x=status_counts.index, y=status_counts.values, 
                         labels={'x': 'Status', 'y': 'Number of Students'},
                         title="All Clear vs Fail Count", color=status_counts.index, 
                         color_discrete_map={"All Clear": "green", "Fail": "red"})
            st.plotly_chart(fig)
            
            # Classification (Distinction, First, Second, Fail)
            subject_columns = [col for col in df.columns if col not in ["Seat Number", "SGPA", "Status"]]  
            grades_df = df[["Seat Number"]].copy()
            for subject in subject_columns:
                grades_df[subject] = df[subject].apply(classify_marks)
            
            st.write("### Marks Classification")
            st.dataframe(grades_df)
            
            # Visualization: Grade Distribution using Plotly
            grade_counts = grades_df.iloc[:, 1:].apply(pd.Series.value_counts).sum(axis=1)
            grade_counts = grade_counts.dropna()  # Remove NA counts
            fig = px.bar(grade_counts, x=grade_counts.index, y=grade_counts.values, 
                         labels={'x': 'Grade Category', 'y': 'Number of Instances'},
                         title="Overall Grade Distribution",
                         color=grade_counts.index)
            st.plotly_chart(fig)
            
            # User selection for subject-wise visualization
            selected_subject = st.selectbox("Select a subject for visualization", subject_columns)
            if selected_subject:
                subject_grade_counts = grades_df[selected_subject].value_counts().dropna()
                fig = px.bar(subject_grade_counts, x=subject_grade_counts.index, y=subject_grade_counts.values, 
                             labels={'x': 'Grade Category', 'y': 'Number of Students'},
                             title=f"Grade Distribution for {selected_subject}",
                             color=subject_grade_counts.index)
                st.plotly_chart(fig)
            
            # User selection for subject-wise topper analysis
            selected_subject_topper = st.selectbox("Select a subject to find toppers", subject_columns)
            if selected_subject_topper:
                topper_score = df[selected_subject_topper].max()
                toppers_df = df[df[selected_subject_topper] == topper_score][["Seat Number", selected_subject_topper]]
                st.write(f"### Toppers for {selected_subject_topper}")
                st.dataframe(toppers_df)
            
        else:
            st.error("CSV file must contain an 'SGPA' column for analysis.")

if __name__ == "__main__":
    main()
