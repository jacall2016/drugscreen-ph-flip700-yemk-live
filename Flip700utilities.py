import pandas as pd
from scipy.stats import linregress
from datetime import datetime
import os
import shutil

class Flip700Utilities:    
    
    @staticmethod
    def get_new_column_names():

        new_column_names_list = ["pHL_VL2_BL1","flip700_vl2_bl1","relative_well_number","slope_corrected_phl_vl2_bl1","slope_corrected_flip700_vl2_bl1","cutoff_PHL_VL2_BL1_below_cuttoff","cutoff_flip700_vl2_bl1_below_cuttoff","phl_z_score","flip700_z_score","live_z_score","hits_phl_z_score","hits_flip700_z_score","hits_live_z_score"]

        return new_column_names_list 

    @staticmethod
    def get_renamed_column_names():
        
        renamed_column_names_list = ["well_number","total_count","phl_count","flip700_count","live_percentage","dead_percentage","phl_vl2","phl_bl1","flip700_vl2","flip700_bl1"]

        return renamed_column_names_list
    
    
    @staticmethod
    def calculate_Flip700_vl2_bl1(analysis_df):

        """
        Calculate the values for the 'flip700_vl2_bl1' column in the analysis DataFrame.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - pd.DataFrame: The analysis DataFrame with the 'flip700_vl2_bl1' column calculated.
        """
        analysis_df['flip700_vl2_bl1'] = analysis_df['flip700_vl2'] / analysis_df['flip700_bl1']
        return analysis_df
    
    @staticmethod
    def calculate_slope_Flip700_vl2_bl1(analysis_df):
        """
        Calculate the slope of 'flip700_vl2_bl1' vs 'relative_well_number' columns.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - float: The slope of the linear regression.
        """
        # Perform linear regression
        slope, _, _, _, _ = linregress(analysis_df['relative_well_number'], analysis_df['flip700_vl2_bl1'])

        return slope
    
    @staticmethod
    def calculate_mean_flip700_vl2_flip700_bl1(analysis_df):
        """
        Calculate the mean of the 'flip700_vl2_bl1' column.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - float: The mean of the 'flip700_vl2_bl1' column.
        """
        # Calculate the mean
        mean_flip700_vl2_flip700_bl1 = analysis_df['slope_corrected_flip700_vl2_bl1'].mean()

        return mean_flip700_vl2_flip700_bl1
    
    @staticmethod
    def calculate_sd_flip700_vl2_flip700_bl1(analysis_df):
        """
        Calculate the standard deviation of the 'flip700_vl2_bl1' column.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - float: The standard deviation of the 'flip700_vl2_bl1' column.
        """
        # Calculate the standard deviation
        sd_flip700_vl2_flip700_bl1 = analysis_df['slope_corrected_flip700_vl2_bl1'].std()

        return sd_flip700_vl2_flip700_bl1
    
    @staticmethod
    def calculate_cuttoff_flip700_vl2_flip700_bl1(mean_flip700_vl2_flip700_bl1, sd_flip700_vl2_flip700_bl1):
        
        cutoff = mean_flip700_vl2_flip700_bl1 + (1.5 * sd_flip700_vl2_flip700_bl1)

        return cutoff
    
    @staticmethod
    def calculate_slope_corrected_flip700_vl2_bl1(analysis_df, slope_flip700_vl2_flip700_bl1):
        """
        Calculate the values for the 'slope_corrected_flip700_vl2_bl1' column.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.
        - slope_flip700_vl2_flip700_bl1 (float): The calculated slope.

        Returns:
        - pd.DataFrame: The analysis DataFrame with the 'slope_corrected_flip700_vl2_bl1' column calculated.
        """
        analysis_df['slope_corrected_flip700_vl2_bl1'] = analysis_df['flip700_vl2_bl1'] - (analysis_df['relative_well_number'] * slope_flip700_vl2_flip700_bl1)
        return analysis_df
    
    @staticmethod
    def populate_cutoff_flip700_vl2_bl1_below_cuttoff(analysis_df, cuttoff_flip700_vl2_flip700_bl1):
        """
        Populate the 'cutoff_flip700_vl2_bl1_below_cuttoff' column based on the cutoff value.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.
        - cuttoff_flip700_vl2_flip700_bl1 (float): The cutoff value.

        Returns:
        - pd.DataFrame: The analysis DataFrame with the 'cutoff_flip700_vl2_bl1_below_cuttoff' column populated.
        """
        # Create a copy of the 'flip700_vl2_bl1' column
        analysis_df['cutoff_flip700_vl2_bl1_below_cuttoff'] = analysis_df['slope_corrected_flip700_vl2_bl1']

        # Replace values with None where the condition is not met
        analysis_df.loc[analysis_df['slope_corrected_flip700_vl2_bl1'] > cuttoff_flip700_vl2_flip700_bl1, 'cutoff_flip700_vl2_bl1_below_cuttoff'] = None

        return analysis_df
    
    @staticmethod
    def calculate_corrected_mean_flip700_vl2_flip700_bl1(analysis_df):
        
        # calculate the corrected_mean_flip700_vl2_flip700_bl1 by the cutoff_flip700_vl2_bl1_below_cuttoff 
        corrected_mean_flip700_vl2_flip700_bl1 = analysis_df['cutoff_flip700_vl2_bl1_below_cuttoff'].mean()

        return corrected_mean_flip700_vl2_flip700_bl1
    
    @staticmethod
    def calculate_corrected_sd_flip700_vl2_flip700_bl1(analysis_df):
        
        # calculate the corrected_mean_flip700_vl2_flip700_bl1 by the cutoff_flip700_vl2_bl1_below_cuttoff 
        corrected_sd_flip700_vl2_flip700_bl1 = analysis_df['cutoff_flip700_vl2_bl1_below_cuttoff'].std()

        return corrected_sd_flip700_vl2_flip700_bl1
    
    @staticmethod
    def populate_flip700_z_score(analysis_df, corrected_mean_flip700_vl2_flip700_bl1, corrected_sd_flip700_vl2_flip700_bl1):

        if not analysis_df['cutoff_flip700_vl2_bl1_below_cuttoff'].isna().all():
            analysis_df['flip700_z_score'] = (analysis_df['cutoff_flip700_vl2_bl1_below_cuttoff'] - corrected_mean_flip700_vl2_flip700_bl1)/corrected_sd_flip700_vl2_flip700_bl1

        return analysis_df
    
    @staticmethod
    def populate_hits_flip700_z_score(analysis_df):
        # Use boolean indexing to filter rows based on conditions
        condition = (analysis_df['cutoff_flip700_vl2_bl1_below_cuttoff'].notna()) & (analysis_df['flip700_z_score'] < -5)

        # Populate 'hits_flip700_z_score' based on the condition
        analysis_df.loc[condition, 'hits_flip700_z_score'] = analysis_df.loc[condition, 'flip700_z_score']

        return analysis_df
    
    @staticmethod
    def export_All_Plates_flip700_pHL_Live(analysis_df, excel_file_path, base_sheet_name):
        # Select relevant columns from analysis_df
        selected_columns = ['well_number', 'phl_z_score', 'flip700_z_score', 'live_z_score']
        export_df = analysis_df[selected_columns]

        # Format datetime for readability
        formatted_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Append formatted datetime to the base sheet name
        sheet_name = f"{base_sheet_name}_{formatted_datetime}"

        # Create the file if it doesn't exist
        if not os.path.isfile(excel_file_path):
            export_df.to_excel('downloads/'+ excel_file_path, sheet_name, index=False, engine='openpyxl')
        else:
            # Export the selected columns to a new sheet if the file exists
            with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a') as writer:
                export_df.to_excel(writer, sheet_name=sheet_name, index=False)
        return export_df
    
    @staticmethod
    def export_All_hits(analysis_df, excel_file_path, sheet_name):
        
        # Select relevant columns from analysis_df
        selected_columns = ['well_number', 'hits_phl_z_score', 'hits_flip700_z_score', 'hits_live_z_score']

        # Filter out rows where all specified columns don't have any numeric values
        export_df = analysis_df[analysis_df[selected_columns].map(lambda x: isinstance(x, (int, float))).any(axis=1)]

        # Include only the selected columns in export_df
        export_df = export_df[selected_columns]

        # Check if the file exists
        file_exists = os.path.isfile(excel_file_path)

        # Create the file if it doesn't exist
        if not file_exists:
            export_df.to_excel('downloads/' + excel_file_path, sheet_name, index=False, engine='openpyxl')
        else:
            # Export the selected columns to a new sheet if the file exists
            with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a') as writer:
                export_df.to_excel(writer, sheet_name=sheet_name, index=False)

        return export_df

    @staticmethod
    def write_analysis_sheet(analysis_df, file_path, new_sheet_name, analysis_indicators):
       
        # Melt the DataFrame to reshape it
        analysis_indicators = pd.melt(analysis_indicators, var_name='indicators', value_name='value')

        # Extract the file name from the original file path
        original_file_name = os.path.basename(file_path)

        # Add "analysis_" prefix to the original file name
        new_file_name = f"analysis_{original_file_name}"

        # Construct the new file path in the "downloads" folder
        new_file_path = os.path.join("downloads", new_file_name)

        # Read the original Excel file into a DataFrame
        original_df = pd.read_excel(file_path, sheet_name=None)

        # Delete the existing "Analysis" sheet if it exists
        if new_sheet_name in original_df:
            del original_df[new_sheet_name]

        # Copy the original file to the "downloads" folder with the new file name
        shutil.copy(file_path, new_file_path)

        # Read the copied Excel file into a DataFrame
        copied_df = pd.read_excel(new_file_path, sheet_name=None)

        # Check if the new sheet already exists and delete it in the copied file
        with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
            # Write the original sheets to the copied file
            for sheet_name, sheet_df in original_df.items():
                sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Write the "Analysis" DataFrame to a new sheet named "Analysis" in the copied file
            analysis_df.to_excel(writer, sheet_name=new_sheet_name, index=False)

            # Write the analysis_indicators dataframe to the Analysis_indicators sheet in the coppied file
            analysis_indicators.to_excel(writer, "Analysis_indicators", index=False)

        return new_file_path