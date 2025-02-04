import os
import re
import pandas as pd
from PIL import Image
from dateutil import parser
import pytesseract
from entities import Patient

art = r"""
 ______   _______  _       _________ _______  _______  _______ _________
(  __  \ (  ____ \( (    /|\__   __/(  ____ )(  ___  )(  ____ \\__   __/
| (  \  )| (    \/|  \  ( |   ) (   | (    )|| (   ) || (    \/   ) (
| |   ) || (__    |   \ | |   | |   | (____)|| (___) || |         | |
| |   | ||  __)   | (\ \) |   | |   |     __)|  ___  || |         | |
| |   ) || (      | | \   |   | |   | (\ (   | (   ) || |         | |
| (__/  )| (____/\| )  \  |   | |   | ) \ \__| )   ( || (____/\   | |
(______/ (_______/|/    )_)   )_(   |/   \__/|/     \|(_______/   )_(
"""
# Print the ASCII art and a brief intro
print(art)
print("Add the name of the of the image you want to extract the patient's info from.")


def main():
    """
    This is the main function that interacts with the user, performs image text extraction,
    parses patient information from the extracted text, and saves the information to a CSV file.
    """

    # Loop to get a valid file name
    while True:
        file_name = input("Enter image file name: ")
        if not file_name:
            print("File name cannot be empty. Please enter a valid name.")
            continue
        if not os.path.isfile(file_name):
            print("Error: File not found. Please enter a valid file name.")
            continue
        # Extract the text from the file
        text = extract(file_name)
        if not text.strip():
            print("No text found in the image. Please try another file.")
            continue
        # Print the extracted text from the file
        print("\nExtracted text:\n\n" + text + "\n")
        break

    while True:
        try:
            answer = input("Would you like to parse patient's info from this text?(Yes/No) ").strip().lower()
            if answer in ["yes", "y"]:
                parsed_text = parse(text)
                print("\nHere is the parsed info:\n")
                print(parsed_text.to_dict())
                print("\n")
                while True:
                    answer_2 = input("Would you like to add the info to the CSV file?(Yes/No) ").strip().lower()
                    if answer_2 in ["yes", "y"]:
                        save_to_csv(parsed_text)
                        # Ask if user wants to process another image or exit
                        while True:
                            answer_3 = input("Do you want to process another image? (Yes/No) ").strip().lower()
                            if answer_3 in ["yes", "y"]:
                                return main()
                            elif answer_3 in ["no", "n"]:
                                print("Exiting program. Goodbye!")
                                exit()
                            else:
                                print("Invalid response. Please answer Yes or No.")
                    elif answer_2 in ["no", "n"]:
                        print("Let's start over!")
                        return main()
                    else:
                        print("Invalid response. Please answer with Yes or No.")
                        continue
            elif answer in ["no", "n"]:
                print("Let's try again!")
                return main()
            else:
                print("Invalid response. Please answer with Yes or No.")
        except Exception as e:
            print(f"An error occurred: {e}")


def extract(image):
    """
    This function extracts text from an image file using pytesseract OCR and PIL.

    Args:
        image (str): The image file name or path from which text will be extracted.

    Returns:
        str: The extracted text from the image.

    Raises:
        Exception: If there's an error during the extraction process.
    """

    try:
        text = pytesseract.image_to_string(Image.open(image))
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from the file: {e}")
        raise e


def parse(text):
    """
    This function parses the extracted text to extract relevant patient information and stores it in a Patient object.
    It uses robust regular expressions to allow it work with many different formats and data orderings.
    It also uses the dateutil library to parse the dates and save them in a consistent format.

    Args:
        text (str): The text extracted from the image containing the patient's details.

    Returns:
        Patient: A Patient object containing the parsed information.
    """

    # Creating a Patient instance
    patient = Patient()

    # Replacing extra spaces with a single space for cleaning up
    text = re.sub(r'\s+', ' ', text)

    if name_matches := re.search(r'[Nn]ame:\s*([A-Za-z]+(?:\s+[A-Za-z]+){0,3})(?:\s+Medical)?(?=\s*[A-Z][a-z]*(?::|-)|\s*$)', text):
        patient.name = name_matches.group(1).strip()

    if age_matches := re.search(r'[Aa]ge:\s*(\d{1,3})(?:\s+Medical)?(?=\s*[A-Z][a-z]*(?::|-)|\s*)', text):
        patient.age = int(age_matches.group(1))

    if address_matches := re.search(r'[Aa]ddress:\s*([A-Za-z0-9 ,]+?)(?:\s+Medical)?(?=\s*[A-Z][a-z]*(?::|-)|\s*$)', text):
        patient.address = address_matches.group(1).strip()

    if history_matches := re.search(r'[Hh]istory[:|-]\s*(.*?)(?:\s+Medical)?(?=\s*(?:[A-Z][a-z]*[:|-]|\n|$))', text):
        patient.history = history_matches.group(1).strip()

    if complaint_matches := re.search(r'[Cc]omplaint[:|-]\s*(.*?)(?:\s+Medical)?(?=\s*(?:[A-Z][a-z]*[:|-]|\n|$))', text):
        patient.complaint = complaint_matches.group(1).strip()

    if insurance_matches := re.search(r'[Ii]nsurance[:|-]\s*(.*?)(?:\s+Medical)?(?=\s*(?:[A-Z][a-z]*[:|-]|\n|$))', text):
        patient.insurance = insurance_matches.group(1).strip()

    if diagnosis_matches := re.search(r'(?:[Dd]iagnosis)[:|-]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*(?:(?:,|\s*-|\s*\(and\))\s*[A-Za-z]+(?:\s+[A-Za-z]+)*){0,3})(?:\s+Medical)?(?=\s*[A-Z][a-z]*(?::|-)|\s*$)', text):
        patient.diagnosis = diagnosis_matches.group(1).strip()

    if procedure_matches := re.search(r'(?:(?:[Mm]edical\s*)?[Pp]rocedure)[:|-]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*(?:(?:,|\s*-|\s*\(and\))\s*[A-Za-z]+(?:\s+[A-Za-z]+)*){0,3})(?:\s+Medical)?(?=\s*[A-Z][a-z]*(?::|-)|\s*$)', text):
        patient.procedure = procedure_matches.group(1).strip()

    if medications_matches := re.search(r'(?:[Mm]edications)[:|-]\s*([A-Za-z]+(?:\s+[A-Za-z]+)*(?:(?:,|\s*-|\s*\(and\))\s*[A-Za-z]+(?:\s+[A-Za-z]+)*){0,3})(?:\s+Medical)?(?=\s*[A-Z][a-z]*(?::|-)|\s*$)', text):
        patient.medications = medications_matches.group(1).strip()

    if email_matches := re.search(r'(((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W]))', text):
        patient.email = email_matches.group(1).strip()

    if phone_matches := re.search(r'(\+?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4})', text):
        patient.phone = phone_matches.group(0).strip()

    if visit_date_matches := re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})', text):
        visit_date = parser.parse(visit_date_matches.group(1))
        patient.visit_date = visit_date.strftime("%Y-%m-%d")

    return patient


def save_to_csv(patient, file_name="patients.csv"):
    """
    Saves the patient's parsed data to a CSV file using pandas library.

    Args:
        patient (Patient): The Patient object containing the parsed information.
        file_name (str, optional): The name of the CSV file. Default is "patients.csv".

    Raises:
        Exception: If there's an error during the saving process.
    """
    # Create a DataFrame from the patient's information
    patient_df = pd.DataFrame([patient.to_dict()])
    try:
        # Append to CSV if it exists, otherwise create a new one
        patient_df.to_csv(file_name, mode="a", index=False,
                          header=not pd.io.common.file_exists(file_name))
        print("Patient data saved to CSV Successfully.\n")
    except Exception as e:
        print(f"Error saving patient data to CSV: {e}")
        raise e


if __name__ == "__main__":
    main()
