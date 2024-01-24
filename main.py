from generate import Generate
import os
from tkinter import Tk, filedialog
import pandas as pd

def combine_sheets():

    file_type = check_file_type()
    input_file = check_input_file()

     # Validate the file
    is_valid, validation_message = validate(input_file, file_type)

    if not is_valid:
        print('index: ', validation_message)

    # Save the uploaded Excel file
    uploaded_file_path = os.path.join("uploads", input_file)

    # create the desired files
    generate_files(uploaded_file_path,file_type)

    # Clear the contents of the "uploads" folder
    #clear_uploads_folder()

def generate_files(uploaded_file_path, file_type):

    generation_functions = {
        "yemk": Generate.generate_files_phl_bl1_yemk_vl1,
        "flip700": Generate.generatefiles_phl_bl1_Flip700,
    }

    generation_function = generation_functions.get(file_type)

    if generation_function:
        generation_function(uploaded_file_path)
    else:
        print("generation failed")

def clear_uploads_folder():
    # Define the path to the "uploads" folder
    uploads_folder_path = "uploads"

    # Check if the folder exists
    if os.path.exists(uploads_folder_path):
        # Iterate over the files in the folder and remove them
        for file_name in os.listdir(uploads_folder_path):
            file_path = os.path.join(uploads_folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print("The 'uploads' folder does not exist.")

def is_excel_file(file_storage):
    # Check if the file has a '.xlsx' extension
    return file_storage.lower().endswith('.xlsx')

def has_required_sheets(file_path):
    # Check if the Excel file has sheets named 'Samples' and 'High Controls'
    try:
        sheets = pd.read_excel(file_path, sheet_name=None).keys()
        return 'Samples' in sheets and 'High Controls' in sheets
    except Exception as e:
        # Handle exceptions (e.g., file not found, not a valid Excel file)
        return False

def has_valid_column_order(file_path, sheet_name, expected_columns):
    # Check if the columns in the specified sheet match the expected order
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        columns = list(df.columns)
        return columns == expected_columns
    except Exception as e:
        # Handle exceptions (e.g., file not found, not a valid Excel file, sheet not found)
        return False

def yemk_validation(input_file):
    # Define expected columns for Samples and High Controls sheets
    expected_samples_columns = [
        'X1',
        'Count',
        'Live/Cells/Singlet.Cells/pHL.|.Count',
        'Live/Cells/Singlet.Cells/YEMK.|.Count',
        'Live.|.Freq..of.Total.(%)',
        'Dead.|.Freq..of.Total.(%)',
        'Live/Cells/Singlet.Cells/pHL.|.Median.(VL2-H.::.VL2-H)',
        'Live/Cells/Singlet.Cells/pHL.|.Median.(BL1-H.::.BL1-H)',
        'Live/Cells/Singlet.Cells/YEMK.|.Median.(VL2-H.::.VL2-H)',
        'Live/Cells/Singlet.Cells/YEMK.|.Median.(BL1-H.::.BL1-H)'
    ]

    expected_high_controls_columns = [
        'X1',
        'Count',
        'Live/Cells/Singlet.Cells/pHL.|.Count',
        'Live/Cells/Singlet.Cells/YEMK.|.Count',
        'Live.|.Freq..of.Total.(%)',
        'Dead.|.Freq..of.Total.(%)',
        'Live/Cells/Singlet.Cells/pHL.|.Median.(VL2-H.::.VL2-H)',
        'Live/Cells/Singlet.Cells/pHL.|.Median.(BL1-H.::.BL1-H)',
        'Live/Cells/Singlet.Cells/YEMK.|.Median.(VL2-H.::.VL2-H)',
        'Live/Cells/Singlet.Cells/YEMK.|.Median.(BL1-H.::.BL1-H)'
    ]

    if not has_valid_column_order(input_file, 'Samples', expected_samples_columns):
        return False, "Invalid column order in the 'Samples' sheet. Please check the contents."
    
    if not has_valid_column_order(input_file, 'High Controls', expected_high_controls_columns):
        return False, "Invalid column order in the 'High Controls' sheet. Please check the contents."

def Flip700_validation(input_file):
    # Define expected columns for Samples and High Controls sheets
    expected_samples_columns = [
        '',
        'Count',
        'Live/Cells/Singlet Cells/FLIP700 | Count',
        'Live/Cells/Singlet Cells/pHL | Count',
        'Live | Freq. of Total (%)',
        'Dead | Freq. of Total (%)',
        'Live | Freq. of Parent (%)',
        'Dead | Freq. of Parent (%)',
        'Live/Cells/Singlet Cells/FLIP700 | Median (VL2-H :: VL2-H)',
        'Live/Cells/Singlet Cells/FLIP700 | Median (BL1-H :: BL1-H)',
        'Live/Cells/Singlet Cells/pHL | Median (VL2-H :: VL2-H)',
        'Live/Cells/Singlet Cells/pHL | Median (BL1-H :: BL1-H)'
    ]

    expected_high_controls_columns = [
        '',
        'Count',
        'Live/Cells/Singlet Cells/FLIP700 | Count',
        'Live/Cells/Singlet Cells/pHL | Count',
        'Live | Freq. of Total (%)',
        'Dead | Freq. of Total (%)',
        'Live | Freq. of Parent (%)',
        'Dead | Freq. of Parent (%)',
        'Live/Cells/Singlet Cells/FLIP700 | Median (VL2-H :: VL2-H)',
        'Live/Cells/Singlet Cells/FLIP700 | Median (BL1-H :: BL1-H)',
        'Live/Cells/Singlet Cells/pHL | Median (VL2-H :: VL2-H)',
        'Live/Cells/Singlet Cells/pHL | Median (BL1-H :: BL1-H)'
    ]    

    # Check column order for High Controls sheet
    if not has_valid_column_order(input_file, 'High Controls', expected_high_controls_columns):
        return False, "Invalid column order in the 'High Controls' sheet. Please check the contents."
    
    if not has_valid_column_order(input_file, 'High Controls', expected_high_controls_columns):
        return False, "Invalid column order in the 'High Controls' sheet. Please check the contents."

def default_validation(input_file):
    #expected sheets
    required_sheets = ['Samples','High Controls']
    
    # Check if it's an Excel file
    if not is_excel_file(input_file):
        return False, "Invalid file type. Please upload an Excel file."
    
    # Check if the file has required sheets
    if not has_required_sheets(input_file):
        return False, "The Excel file is missing required sheets. Please check the contents."

def validate(input_file, file_type):
    
    # Define a dictionary to map file types to corresponding validation functions
    validation_functions = {
        "yemk": yemk_validation,
        "flip700": Flip700_validation,
    }

    #perform default validations
    default_validation(input_file)

    # Get the validation function based on the file type or use the default_validation function
    validation_function = validation_functions.get(file_type.lower())
    
    # Check if the validation_function is not None before calling it
    if validation_function is not None:
        # Call the selected validation function
        validation_function(input_file)
    else:
        # Handle the case where file_type is not recognized
        return False, f"Unsupported file type: {file_type}"
    
    # All checks passed
    return True, None

def check_file_type():
    while True:
        # Prompt the user for file type and convert to lowercase for case-insensitive comparison
        file_type = input("Enter the file type (flip700 or yemk): ").lower()

        # Check if the file type is valid
        if file_type in ["flip700", "yemk"]:
            break  # Exit the loop if the input is valid
        else:
            print("Invalid file type. Please enter either 'flip700' or 'yemk'.")

    return file_type

def check_input_file():
    root = Tk()
    root.withdraw()  # Hide the main window

    # Open a file dialog to select the input file
    #input_file = "LC2-032_KCP1 pHL-YEMK DC 20231030.xlsx"
    input_file = filedialog.askopenfilename(
        title="Select Excel File", 
        filetypes=[("Excel Files", "*.xlsx")],
        parent=root
    )

    # extract file from extension
    input_file = os.path.basename(input_file)
    input_file, _ = os.path.splitext(input_file)

    # Check if the input file contains either 'yemk' or 'flip700'
    if any(keyword in input_file.lower() for keyword in ["yemk", "flip700"]):
        return input_file  # Return the selected file
    else:
        print("Invalid input file. It must contain either 'yemk' or 'flip700'. Please try again.")
        return check_input_file()  # Recursively prompt until a valid file is selected

if __name__ == "__main__":
    combine_sheets()