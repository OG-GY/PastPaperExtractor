import streamlit as st
import os

st.title("Search Past Paper")

col1,col2=st.columns(2)
start=int(os.getenv("YEAR_START",2015))
end=int(os.getenv("YEAR_END",2024))
folder_path="uploaded_papers"
file_names = os.listdir(folder_path)

years=[]
matched=[]
t_matched=[]
ty_matched=[]

for i in range(end-start+1):
    years.append(start+i)


with col1:
    teacher=st.text_input("Enter teacher name").lower()
with col2:
    session=st.selectbox("Session",years)
with col1:
    course=st.text_input("Course Name").lower()
with col2:
    sem=st.selectbox("Semester",["1","2","3","4","5","6","7","8"])
typ=st.selectbox("Type",["MidTerm Exam","Final Exam","Quiz"])



for name in file_names:
    if course:
        cou=name.split(" ")[0]
        cou=cou.split(".")[0]
        if cou==course:
            matched.append(name)
    if teacher:
        teac=name.split(" ")[1]
        teac=teac.split("-")[0]
        teac=teac.split(".")[0]
        if teacher==teac:
            t_matched.append(name)

if matched:
    st.subheader("Course Wise")
for img in matched:
    st.image("uploaded_papers/"+img)
if t_matched:
    st.subheader("Teacher Wise")
for img in t_matched:
    st.image("uploaded_papers/"+img)
