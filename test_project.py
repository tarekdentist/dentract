import os
from project import extract, parse, save_to_csv
import pytest

# Mock a simple patient object
class MockPatient:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {"name": self.name, "age": self.age}

# Sample text for testing
text = """Name: John Harvard Age: 45 Address: 123 Main Street, Springfield Medical History:
Hypertension, Type 2 Diabetes Medical Complaint: Pain in upper 7 tooth Diagnosis:
Tooth fracture Procedure: X-ray scan, splinting Medications: Paracetamol, Metoprolol
Email: johndoe@example.com Phone: +1-555-789-1234 Visit Date: 29-01-2025"""

# Parse the sample text into a patient object
patient = parse(text)

# testing the extract function
def test_extract():
    result = extract("patient1.png").strip()
    assert result == text
    assert result != ""
    assert result != " "

    # Raises exceptions when given invalid inputs
    with pytest.raises(Exception):
        extract("")
        extract(" ")
        extract("patient.pdf")

# Test for parsing the patient's name
def test_parse_name():
    assert patient.name == "John Harvard"
    assert patient.name != ""
    assert patient.name != " "
    assert patient.name != "John"
    assert patient.name != "Harvard"
    assert patient.name != None

# Test for parsing the patient's age
def test_parse_age():
    assert patient.age == 45
    assert patient.age != None
    assert patient.age != 4
    assert patient.age != 5
    assert patient.age != 25

# Test for parsing the patient's address
def test_parse_address():
    assert patient.address == "123 Main Street, Springfield"
    assert patient.address != "123 Main Street, Springfield Medical"
    assert patient.address != "123 Main Street"
    assert patient.address != "123 Main Street Springfield"
    assert patient.address != None
    assert patient.address != ""
    assert patient.address != " "

# Test for parsing the patient's medical history
def test_parse_history():
    assert patient.history == "Hypertension, Type 2 Diabetes"
    assert patient.history != None
    assert patient.history != ""
    assert patient.history != " "
    assert patient.history != "Hypertension"
    assert patient.history != "Type 2 Diabetes"
    assert patient.history != "Hypertension, Type 2 Diabetes Medical"

# Test for parsing the patient's medical complaint
def test_parse_complaint():
    assert patient.complaint == "Pain in upper 7 tooth"
    assert patient.complaint != None
    assert patient.complaint != ""
    assert patient.complaint != " "
    assert patient.complaint != "Pain"
    assert patient.complaint != "Pain in upper 7 tooth Diagnosis"

# Test for parsing the patient's insurance
def test_parse_insurance():
    assert patient.insurance == None
    assert patient.insurance != ""
    assert patient.insurance != " "
    assert patient.insurance != "insurance"

# Test for parsing the patient's diagnosis
def test_parese_diagnosis():
    assert patient.diagnosis == "Tooth fracture"
    assert patient.diagnosis != None
    assert patient.diagnosis != ""
    assert patient.diagnosis != " "
    assert patient.diagnosis != "Tooth fracture Procedure"
    assert patient.diagnosis != "Tooth"
    assert patient.diagnosis != "Fracture"

# Test for parsing the patient's procedure
def test_parse_procedure():
    assert patient.procedure == "X-ray scan, splinting"
    assert patient.procedure != None
    assert patient.procedure != ""
    assert patient.procedure != " "
    assert patient.procedure != "X-ray scan"
    assert patient.procedure != "splinting"
    assert patient.procedure != "X-ray scan, splinting Medications"

# Test for parsing the patient's medications
def test_parse_medications():
    assert patient.medications == "Paracetamol, Metoprolol"
    assert patient.medications != None
    assert patient.medications != ""
    assert patient.medications != " "
    assert patient.medications != "Paracetamol"
    assert patient.medications != "Metoprolol"
    assert patient.medications != "Paracetamol, Metoprolol Email"

# Test for parsing the patient's email
def test_parse_email():
    assert patient.email == "johndoe@example.com"
    assert patient.email != None
    assert patient.email != ""
    assert patient.email != " "
    assert patient.email != "johndoe@otherdomain.com"
    assert patient.email != "johndoe@example"

# Test for parsing the patient's phone
def test_parse_phone():
    assert patient.phone == "+1-555-789-1234"
    assert patient.phone != None
    assert patient.phone != ""
    assert patient.phone != " "
    assert patient.phone != "+1-555-123-4567"
    assert patient.phone != "555-789-1234"
    assert patient.phone != "+1-555-789-1234 X"
    assert patient.phone != "1-555-789-1234"

# Test for parsing the patient's visit date
def test_parse_visit_date():
    assert patient.visit_date == "2025-01-29"
    assert patient.phone != None
    assert patient.phone != ""
    assert patient.phone != " "
    assert patient.visit_date != "29-01-2025"
    assert patient.visit_date != "01-29-2025"

# Testing the save_to_csv function
def test_save_to_csv():
    # Create a mock patient object
    patient = MockPatient("John Harvard", 45)
    file_name = "test_patients.csv"

    # Call save_to_csv function
    save_to_csv(patient, file_name)

    # Check if file was created
    assert os.path.exists(file_name), "CSV file was not created"

    # Check if the data was written to the file (by reading the file and checking for patient name)
    with open(file_name, 'r') as f:
        content = f.read()
        assert "John Harvard" in content, "Patient name not found in CSV"

    # Remove the test CSV file after testing
    os.remove(file_name)

def test_save_to_csv_error_handling():
    # Create a mock patient object
    patient = MockPatient("John Harvard", 45)

    # Raises an error when given an invalid path
    with pytest.raises(Exception):
        save_to_csv(patient, "/invalid_path/test_patients.csv")

    # Raises an error with non-existent patient object
    with pytest.raises(Exception):
        save_to_csv(patient1, "/invalid_path/test_patients.csv")
