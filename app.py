import streamlit as st
import pandas as pd
from datetime import date

# Page configuration
st.set_page_config(page_title="Attendance Management System", layout="centered")

st.title("🏫 Attendance Management System")

# Initialize session state
if "students" not in st.session_state:
    st.session_state.students = []

if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(
        columns=["Name", "Date", "Status"]
    )

# Sidebar menu
menu = st.sidebar.radio(
    "Menu",
    ["Home", "Add Student", "Mark Attendance", "View Attendance"]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("📌 Project Overview")
    st.write("""
    This Attendance Management System helps teachers or students:
    - Maintain student records
    - Mark daily attendance
    - View attendance history
    - Calculate attendance percentage
    
    **Technology Used:** Python + Streamlit
    """)

# ---------------- ADD STUDENT ----------------
elif menu == "Add Student":
    st.subheader("➕ Add Student")

    student_name = st.text_input("Enter Student Name")

    if st.button("Add Student"):
        if student_name and student_name not in st.session_state.students:
            st.session_state.students.append(student_name)
            st.success("Student added successfully ✅")
        else:
            st.warning("Student already exists or name is empty")

# ---------------- MARK ATTENDANCE ----------------
elif menu == "Mark Attendance":
    st.subheader("📝 Mark Attendance")

    if not st.session_state.students:
        st.warning("No students available. Please add students first.")
    else:
        selected_student = st.selectbox(
            "Select Student",
            st.session_state.students
        )

        status = st.radio("Attendance Status", ["Present", "Absent"])
        today = date.today()

        if st.button("Submit Attendance"):
            new_record = {
                "Name": selected_student,
                "Date": today,
                "Status": status
            }

            st.session_state.attendance = pd.concat(
                [st.session_state.attendance, pd.DataFrame([new_record])],
                ignore_index=True
            )

            st.success("Attendance marked successfully ✅")

# ---------------- VIEW ATTENDANCE ----------------
elif menu == "View Attendance":
    st.subheader("📊 Attendance Records")

    if st.session_state.attendance.empty:
        st.warning("No attendance records found")
    else:
        st.dataframe(st.session_state.attendance)

        st.subheader("📈 Attendance Percentage")

        summary = (
            st.session_state.attendance
            .groupby("Name")["Status"]
            .apply(lambda x: (x == "Present").sum() / len(x) * 100)
            .reset_index(name="Attendance %")
        )

        st.dataframe(summary)
