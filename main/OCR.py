import pytesseract
from PIL import Image
import cv2
import re
import numpy as np

# Optional: Set path to tesseract if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

roman_to_int = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10
}

def extract_metadata_from_image(image_bytes):
    # Convert bytes to numpy array
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return None

    # Convert to grayscale and apply adaptive thresholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10
    )
    pil_img = Image.fromarray(thresh)

    # OCR with better config
    text = pytesseract.image_to_string(pil_img, config='--oem 3 --psm 6')

    metadata = {
        "Course Instructor": None,
        "Exam Type": None,
        "Course Name": None,
        "Session": None,
        "Semester": None,
        "Date": None
    }

    # Exam Type
    exam_match = re.search(
        r'\b(Final\s*Term|Mid\s*Term|Final\s*Exam|Midterm)\b', text, re.IGNORECASE)
    if exam_match:
        metadata["Exam Type"] = exam_match.group(1).strip()

    # Course Name
    course_name_match = re.search(
        r'Course\s*:\s*(.+)', text, re.IGNORECASE)
    if course_name_match:
        metadata["Course Name"] = course_name_match.group(1).strip()

    # Session
    session_match = re.search(r'Session\s*:\s*(\d{4})', text, re.IGNORECASE)
    if session_match:
        metadata["Session"] = session_match.group(1).strip()

    # Date
    date_match = re.search(r'Date\s*:\s*(\d{1,2}-\d{1,2}-\d{4})', text)
    if date_match:
        metadata["Date"] = date_match.group(1).strip()

    # Semester (Handle '2019 Spring Semester')
    sem_match = re.search(r'Year\s*:\s*(\d{4})\s*(Spring|Fall)?', text, re.IGNORECASE)
    if sem_match:
        year = sem_match.group(1).strip()
        season = sem_match.group(2).capitalize() if sem_match.group(2) else ""
        metadata["Semester"] = f"{season} {year}".strip()

    # Instructor - Try alternate patterns
    instructor_match = re.search(
        r'(Instructor|Teacher(?: Name)?|Course Instructor)\s*[:\-]?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
    if instructor_match:
        metadata["Course Instructor"] = instructor_match.group(2).strip()

    print("Extracted Metadata:\n", metadata)
    return metadata
