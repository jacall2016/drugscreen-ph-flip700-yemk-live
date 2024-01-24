import pandas as pd
from scipy.stats import linregress
from datetime import datetime
import os

class AnalysisUtilities:
    
    @staticmethod
    def getfile_name(uploaded_file_path):
        # Extract the base name (file name with extension) from the full path
        file_name_with_extension = os.path.basename(uploaded_file_path)
        
        # Remove the extension to get only the file name
        file_name_without_extension = os.path.splitext(file_name_with_extension)[0]

        return file_name_without_extension

    @staticmethod
    def getsheet1_name(sheet1):
        return sheet1

    @staticmethod
    def getsheet2_name(sheet2):
        return sheet2
    
    @staticmethod
    def get_new_sheet_name(final_sheet):
        return final_sheet

    @staticmethod
    def remove_rows_names_list():
        return ['mean', 'sd']

    @staticmethod
    def get_old_column_names(combined_df):
        # Extract only the column names from the combined_df DataFrame
        old_column_name_list = combined_df.columns.tolist()
        
        return old_column_name_list

    @staticmethod
    def prepare_analysis_df(file_path, sheet1, sheet2, remove_columns_names):

        # Create DataFrames for "Samples" and "High Controls" sheets
        samples_df = pd.read_excel(file_path, sheet_name=sheet1)
        
        high_controls_df = pd.read_excel(file_path, sheet_name=sheet2)

        # Combine the DataFrames into one
        combined_df = pd.concat([samples_df, high_controls_df], ignore_index=True)

        # Remove empty rows
        combined_df = combined_df.dropna(how='all')

        # Convert values in "X1" column to lowercase and remove rows where the value is "mean" or "sd"
        combined_df = combined_df[~combined_df[combined_df.columns[0]].str.lower().isin(remove_columns_names)]

        # remove any duplicate rows
        combined_df = combined_df.drop_duplicates()

        return combined_df

    @staticmethod
    def rewrite_column_names(combined_df, old_column_name_list, renamed_column_names_list, new_column_names_list):
        analysis_df = combined_df.copy()  # Create a copy to avoid modifying the original DataFrame

        # Rename existing columns
        for old_name, new_name in zip(old_column_name_list, renamed_column_names_list):
            analysis_df.rename(columns={old_name: new_name}, inplace=True)

        # Add new empty columns
        for new_name in new_column_names_list:
            analysis_df[new_name] = ''

        return analysis_df
    
    @staticmethod
    def calculate_relative_well_number(analysis_df):
        """
        Calculate the values for the 'relative_well_number' column in the analysis DataFrame.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - pd.DataFrame: The analysis DataFrame with the 'relative_well_number' column calculated.
        """
        analysis_df['relative_well_number'] = range(1, len(analysis_df) + 1)
        return analysis_df