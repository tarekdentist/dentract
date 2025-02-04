# DENTRACT

## Video Demo
[Video Demo Link](<https://youtu.be/VsUmkmWT0iI>)

## Description
Dentract is an application designed for dentists and medical professionals to extract patient information from images and save it to a CSV file in a structured format.

### How It Works
1. The application prompts the user for an image file name or file path.
2. It extracts the text from the image and displays it to the user.
3. The user is asked whether they want to parse the text to extract patient information.
4. If parsing is chosen, the extracted data is displayed in JSON format.
5. The user is given the option to save the information to a CSV file.
6. The user can then choose to process another image or exit the program.

---

## Main Functions

### `main()`
This is the core function that handles user interaction.
- Prompts the user to enter an image file name or path.
  - If empty, it returns an error: **"File name cannot be empty. Please enter a valid name."**
  - If invalid or nonexistent, it returns an error: **"Error: File not found. Please enter a valid file name."**
- Extracts and displays text from the image.
  - If the file is empty, it returns an error: **"No text found in the image. Please try another file."**
  - If an error occurs during extraction, it is displayed to the user.
- Asks the user: **"Would you like to parse patient’s info from this text? (Yes/No)"**
  - If **Yes**, the parsed patient information is displayed in JSON format.
  - If **No**, the program restarts.
  - If an invalid response is given, it keeps reprompting.
- If parsing was done, asks: **"Would you like to add the info to the CSV file?"**
  - If **Yes**, the data is saved to a CSV file.
  - If **No**, the program restarts.
  - If an invalid response is given, it keeps reprompting.
- Finally, asks: **"Do you want to process another image?"**
  - If **Yes**, the program restarts.
  - If **No**, the program exits.
  - If an invalid response is given, it keeps reprompting.

---

### `extract()`
This function extracts text from the provided image using **pytesseract OCR (Optical Character Recognition).**
- **Input:** Image file name or path.
- **Output:** Extracted text as a string (stripped of extra spaces).
- **Errors:** If an issue occurs during extraction, an exception is raised.

---

### `parse()`
This function extracts relevant patient details from the extracted text using **regular expressions** and **dateutil** for date parsing.
- **Input:** Extracted text.
- **Output:** A `Patient` object containing the parsed information.
- **Process:**
  - Removes extra spaces before parsing.
  - Uses regex to find relevant fields and assigns them to attributes in the `Patient` object.
  - Uses `dateutil.parser` to convert detected dates into a consistent `YYYY-MM-DD` format.
- **Missing Information:** If certain details are missing, their attributes remain as `None`.

---

### `save_to_csv()`
This function saves parsed patient data to a **CSV file** using `pandas`.
- **Input:** `Patient` object, optional file name (default: `patients.csv`).
- **Errors:** If an issue occurs during saving, an exception is raised.

---

## Patient Class
The `Patient` class represents a patient and stores extracted attributes.
- Attributes:
  - **name, age, address, email, phone, complaint, diagnosis, medical history, procedure, medications, insurance, visit date**
- Methods:
  - `to_dict()`: Converts the `Patient` object into a dictionary for easy storage in CSV or other formats.
  - **Output:** Dictionary with attribute names as keys and corresponding values.

---

## Technologies Used
- **Python**
- **pytesseract (OCR)**
- **Regular Expressions (Regex)**
- **dateutil (for date parsing)**
- **pandas (for CSV file handling)**

---

## Installation & Usage
1. Install required dependencies:
   ```bash
   pip install pytesseract pandas python-dateutil
   ```
2. Run the script:
   ```bash
   python dentract.py
   ```
3. Follow the on-screen prompts to extract, parse, and save patient data.

---

## Author
[Tarek Ismail](#)

