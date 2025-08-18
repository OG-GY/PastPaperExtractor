import streamlit as st
import os
from io import BytesIO
from dotenv import load_dotenv
from OCR import extract_metadata_from_image  # import the above function here

load_dotenv()
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 2*1024*1024))
DIR = str(os.getenv("SAVE_DIR", "uploaded_papers"))
start = int(os.getenv("YEAR_START", 2015))
end = int(os.getenv("YEAR_END", 2024))
os.makedirs(DIR, exist_ok=True)

years = [start + i for i in range(end - start + 1)]

st.title("Upload Past Paper")

uploaded_file = st.file_uploader("Upload a Past Paper", type=["png", "jpg", "jpeg"])

# Initialize form fields
teacher = ""
session = years[0]
course = ""
sem = "1"
typ = "MidTerm Exam"

if uploaded_file:
    metadata = extract_metadata_from_image(uploaded_file)
    if metadata:
        teacher = metadata.get("Course Instructor") or ""
        session = int(metadata.get("Session") or years[0])
        course = metadata.get("Course Name") or ""
        sem = str(metadata.get("Semester") or "1")
        typ = metadata.get("Exam Type") or "MidTerm Exam"
    # Reset file pointer to start after reading
    uploaded_file.seek(0)

col1, col2 = st.columns(2)

with col1:
    teacher = st.text_input("Enter teacher name", value=teacher).lower()

with col2:
    session = st.selectbox("Session", years, index=years.index(session) if session in years else 0)

with col1:
    course = st.text_input("Course Name", value=course).lower()

with col2:
    sem = st.selectbox("Semester", ["1", "2", "3", "4", "5", "6", "7", "8"], index=int(sem)-1 if sem.isdigit() and 1 <= int(sem) <= 8 else 0)

typ = st.selectbox("Type", ["MidTerm Exam", "Final Exam", "Quiz"], index=["MidTerm Exam", "Final Exam", "Quiz"].index(typ) if typ in ["MidTerm Exam", "Final Exam", "Quiz"] else 0)

if teacher and course and sem:
    File_Name = f"{course} {teacher.split(' ')[0]}-{sem} {typ[0]}-{session}"

if st.button("Submit"):
    if uploaded_file and File_Name:
        st.image(uploaded_file)
        save_path = os.path.join(DIR, File_Name + ".jpg")
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved as {File_Name}.jpg")
