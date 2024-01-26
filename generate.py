from utilities import AnalysisUtilities
from Flip700utilities import Flip700Utilities
from ph1utilities import PhlUtilities
from liveutilities import LiveUtilities
from yemkutilities import YemkUtilities
import os
import pandas as pd
import matplotlib.pyplot as plt

class Generate:

    @staticmethod
    def generate_phl(analysis_df):

        # Calculate 'pHL_VL2_BL1' column
        analysis_df = PhlUtilities.calculate_pHL_VL2_BL1(analysis_df)

        # calculate the slopes
        slope_phl_vl2_phl_bl1 = PhlUtilities.calculate_slope_phl_vl2_phl_bl1(analysis_df)

        # Calculate and populate the corrected slope for phl_vl2_bl1
        analysis_df = PhlUtilities.calculate_slope_corrected_phl_vl2_bl1(analysis_df, slope_phl_vl2_phl_bl1)

        # calculate the means
        mean_phl_vl2_phl_bl1 = PhlUtilities.calculate_mean_phl_vl2_phl_bl1(analysis_df)

        # calculate the standard deviations
        sd_phl_vl2_phl_bl1 = PhlUtilities.calculate_sd_phl_vl2_phl_bl1(analysis_df)

        # calculate the cuttoffs
        cuttoff_phl_vl2_phl_bl1 = PhlUtilities.calculate_cuttoff_phl_vl2_phl_bl1(mean_phl_vl2_phl_bl1, sd_phl_vl2_phl_bl1)

        # populate the cutoff_PHL_VL2_BL1_below_cuttoff if above the cutoff don't include
        analysis_df = PhlUtilities.populate_cutoff_PHL_VL2_BL1_below_cuttoff(analysis_df, cuttoff_phl_vl2_phl_bl1)

        #calculate correct mean or phl_vl2_phl_bl1 and Flip700_vl2_Flip700_bl1
        corrected_mean_phl_vl2_phl_bl1 = PhlUtilities.calculate_corrected_mean_phl_vl2_phl_bl1(analysis_df)

        # calculate correct standard deviation for phl and Flip700
        corrected_sd_phl_vl2_phl_bl1 = PhlUtilities.calculate_corrected_sd_phl_vl2_phl_bl1(analysis_df)

        #populate phl z score
        analysis_df = PhlUtilities.populate_phl_z_score(analysis_df, corrected_mean_phl_vl2_phl_bl1, corrected_sd_phl_vl2_phl_bl1)

        #populate the hits
        analysis_df = PhlUtilities.populate_hits_phl_z_score(analysis_df)

                # Create a DataFrame named analysis_indicators
        phl_indicators = pd.DataFrame({
            'slope_ph': [slope_phl_vl2_phl_bl1],
            'mean_ph':[mean_phl_vl2_phl_bl1],
            'corrected_mean_ph' : [corrected_mean_phl_vl2_phl_bl1],
            'sd_ph':[sd_phl_vl2_phl_bl1],
            'corrected_sd_ph':[corrected_sd_phl_vl2_phl_bl1],
            'cuttoff_ph':[cuttoff_phl_vl2_phl_bl1],
        })

        return analysis_df, phl_indicators

    @staticmethod
    def generate_yemk(analysis_df):
        # Calculate 'yemk_vl2_bl1' column
        analysis_df = YemkUtilities.calculate_yemk_vl2_bl1(analysis_df)

        # calculate the slopes
        slope_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_slope_yemk_vl2_bl1(analysis_df)

        # Calculate and populate the corrected slope for phl_vl2_bl1
        analysis_df = YemkUtilities.calculate_slope_corrected_yemk_vl2_bl1(analysis_df, slope_yemk_vl2_yemk_bl1)

        # calculate the means
        mean_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_mean_yemk_vl2_yemk_bl1(analysis_df)

        # calculate the standard deviations
        sd_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_sd_yemk_vl2_yemk_bl1(analysis_df)

        # calculate the cuttoffs
        cuttoff_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_cuttoff_yemk_vl2_yemk_bl1(mean_yemk_vl2_yemk_bl1, sd_yemk_vl2_yemk_bl1)

        # populate the cutoff_PHL_VL2_BL1_below_cuttoff if above the cutoff don't include
        analysis_df = YemkUtilities.populate_cutoff_yemk_vl2_bl1_below_cuttoff(analysis_df, cuttoff_yemk_vl2_yemk_bl1)

        #calculate correct mean or phl_vl2_phl_bl1 and yemk_vl2_yemk_bl1
        corrected_mean_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_corrected_mean_yemk_vl2_yemk_bl1(analysis_df)

        # calculate correct standard deviation for phl and yemk
        corrected_sd_yemk_vl2_yemk_bl1 = YemkUtilities.calculate_corrected_sd_yemk_vl2_yemk_bl1(analysis_df)

        #populate phl and yemk z score
        analysis_df = YemkUtilities.populate_yemk_z_score(analysis_df, corrected_mean_yemk_vl2_yemk_bl1, corrected_sd_yemk_vl2_yemk_bl1)

        #populate the hits
        analysis_df = YemkUtilities.populate_hits_yemk_z_score(analysis_df)

        yemk_indicators = pd.DataFrame({
            'slope_yemk': [slope_yemk_vl2_yemk_bl1],
            'mean_yemk': [mean_yemk_vl2_yemk_bl1],
            'corrected_mean_yemk': [corrected_mean_yemk_vl2_yemk_bl1],
            'sd_yemk': [sd_yemk_vl2_yemk_bl1],
            'corrected_sd_yemk': [corrected_sd_yemk_vl2_yemk_bl1],
            'cuttoff_yemk': [cuttoff_yemk_vl2_yemk_bl1],
        })

        return analysis_df, yemk_indicators

    @staticmethod
    def generate_flip700(analysis_df):
        
        # Calculate 'Flip700_vl2_bl1' column
        analysis_df = Flip700Utilities.calculate_Flip700_vl2_bl1(analysis_df)

        # calculate the slopes
        slope_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_slope_Flip700_vl2_bl1(analysis_df)

        # Calculate and populate the corrected slope for phl_vl2_bl1
        analysis_df = Flip700Utilities.calculate_slope_corrected_flip700_vl2_bl1(analysis_df, slope_Flip700_vl2_Flip700_bl1)

        # Calculate and populate the corrected slope for phl_vl2_bl1
        analysis_df = Flip700Utilities.calculate_slope_corrected_flip700_vl2_bl1(analysis_df, slope_Flip700_vl2_Flip700_bl1)

        # calculate the means
        mean_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_mean_flip700_vl2_flip700_bl1(analysis_df)   

        # calculate the standard deviations
        sd_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_sd_flip700_vl2_flip700_bl1(analysis_df)

        # calculate the cuttoffs
        cuttoff_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_cuttoff_flip700_vl2_flip700_bl1(mean_Flip700_vl2_Flip700_bl1, sd_Flip700_vl2_Flip700_bl1)

        # populate the cutoff_PHL_VL2_BL1_below_cuttoff if above the cutoff don't include
        analysis_df = Flip700Utilities.populate_cutoff_flip700_vl2_bl1_below_cuttoff(analysis_df, cuttoff_Flip700_vl2_Flip700_bl1)

        #calculate correct mean or phl_vl2_phl_bl1 and Flip700_vl2_Flip700_bl1
        corrected_mean_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_corrected_mean_flip700_vl2_flip700_bl1(analysis_df)

        # calculate correct standard deviation for phl and Flip700
        corrected_sd_Flip700_vl2_Flip700_bl1 = Flip700Utilities.calculate_corrected_sd_flip700_vl2_flip700_bl1(analysis_df)

        #populate phl and Flip700 z score
        analysis_df = Flip700Utilities.populate_flip700_z_score(analysis_df, corrected_mean_Flip700_vl2_Flip700_bl1, corrected_sd_Flip700_vl2_Flip700_bl1)

        #populate the hits
        analysis_df = Flip700Utilities.populate_hits_flip700_z_score(analysis_df)

                # Create a DataFrame named analysis_indicators
        flip700_indicators = pd.DataFrame({
            'slope_Flip700': [slope_Flip700_vl2_Flip700_bl1],
            'mean_Flip700': [mean_Flip700_vl2_Flip700_bl1],
            'corrected_mean_Flip700': [corrected_mean_Flip700_vl2_Flip700_bl1],
            'sd_Flip700': [sd_Flip700_vl2_Flip700_bl1],
            'corrected_sd_Flip700': [corrected_sd_Flip700_vl2_Flip700_bl1],
            'cuttoff_Flip700':[cuttoff_Flip700_vl2_Flip700_bl1]
        })

        return analysis_df, flip700_indicators

    @staticmethod
    def generate_live(analysis_df):

        #calculate live mean and standard deviation
        live_mean = LiveUtilities.calculate_live_mean(analysis_df)
        live_sd = LiveUtilities.calculate_live_sd(analysis_df)

        #populate live z score
        analysis_df = LiveUtilities.populate_live_z_score(analysis_df, live_mean, live_sd)

        #populate the hits
        analysis_df = LiveUtilities.populate_hits_live_z_score(analysis_df)

                # Create a DataFrame named analysis_indicators
        live_indicators = pd.DataFrame({
            'live_mean':[live_mean],
            'live_sd':[live_sd]
        })

        return analysis_df, live_indicators

    @staticmethod
    def generateGraphs(analysis_df, y_axes_list):

        # Create the 'images' directory if it doesn't exist
        output_folder = os.path.join("downloads", "images")
        os.makedirs(output_folder, exist_ok=True)

        # Loop through each y-axis and generate/save the corresponding graph
        for y_axis in y_axes_list:
            # Create a new figure and axis
            fig, ax = plt.subplots()

            # Plot the data
            ax.scatter(analysis_df['relative_well_number'], analysis_df[y_axis])

            # Set labels and title
            ax.set_xlabel('Relative Well Number')
            ax.set_ylabel(y_axis.replace('_', ' ').title())  # Replace underscores with spaces for better labels
            ax.set_title(f'relative_well_number vs {y_axis}')

            # Set y-axis limit to start at 0 and add a buffer to the upper limit
            max_value = analysis_df[y_axis].max()
            buffer_factor = 1.1  # Adjust as needed
            ax.set_ylim(0, max_value * buffer_factor)

            # Save the figure
            output_path = os.path.join(output_folder, f'{y_axis}_scatterplot.png')
            plt.savefig(output_path)

            # Close the figure to free up resources
            plt.close()

    @staticmethod
    def generatefiles_phl_bl1_Flip700(uploaded_file_path):
        
        sheet1 = "Samples"
        sheet2 = "High Controls"
        final_sheet = "Analysis"

        # Specify the path to your Excel file
        file_name = AnalysisUtilities.getfile_name(uploaded_file_path)
        file_path = "uploads/" + file_name + ".xlsx"
        
        #get functions to retreave the desired data
        renamed_column_names_list = Flip700Utilities.get_renamed_column_names()
        new_column_names_list = Flip700Utilities.get_new_column_names()
        sheet1_name = AnalysisUtilities.getsheet1_name(sheet1)
        sheet2_name = AnalysisUtilities.getsheet2_name(sheet2)
        new_sheet_name = AnalysisUtilities.get_new_sheet_name(final_sheet)
        removed_rows_names_list = AnalysisUtilities.remove_rows_names_list()    
        
        # Prepare analysis DataFrame by combining data from Samples and High Controls and removing mean and SD rows
        combined_df = AnalysisUtilities.prepare_analysis_df(file_path, sheet1_name, sheet2_name, removed_rows_names_list)

        # Assuming 'Live | Freq. of Parent (%)' and 'Dead | Freq. of Parent (%)' are the column names to be removed
        columns_to_remove = ['Live | Freq. of Parent (%)', 'Dead | Freq. of Parent (%)']

        # Check if columns exist before attempting to drop them
        existing_columns = set(combined_df.columns)
        columns_to_drop = [col for col in columns_to_remove if col in existing_columns]

        if columns_to_drop:
            # Remove columns if they exist
            combined_df = combined_df.drop(columns=columns_to_drop, axis=1)

        # get current combined_df column names
        old_column_name_list = AnalysisUtilities.get_old_column_names(combined_df)

        # rewrite columns and add new columns
        analysis_df = AnalysisUtilities.rewrite_column_names(combined_df, old_column_name_list,  renamed_column_names_list, new_column_names_list)

        # Calculate 'relative_well_number' column
        analysis_df = AnalysisUtilities.calculate_relative_well_number(analysis_df)

        # generate phl
        analysis_df, phl_indicators = Generate.generate_phl(analysis_df)
        
        # generate flip700
        analysis_df, flip700_indicators = Generate.generate_flip700(analysis_df)

        # generate live
        analysis_df, live_indicators = Generate.generate_live(analysis_df)

        analysis_indicators = pd.concat([flip700_indicators, phl_indicators, live_indicators], axis=1)
        
        #write the All_Plates_Flip700_pHL_Live Excel file
        Flip700Utilities.export_All_Plates_flip700_pHL_Live(analysis_df, 'All_P_Flip700_pHL_Live_' + file_name + '.xlsx','All_P_Flip700_pHL_Live')

        #write All hits excel file exclude all rows that don't have a hit in at least 1 of the three z numbers
        Flip700Utilities.export_All_hits(analysis_df,'All_hits_' + file_name + '.xlsx','All_hits')

        # Write analysis sheet
        YemkUtilities.write_analysis_sheet(analysis_df, "uploads/" + file_name + ".xlsx", new_sheet_name, analysis_indicators)

        # Define the y-axes for each graph
        y_axes_list = ["total_count", "phl_count", "flip700_count", "live_percentage", "pHL_VL2_BL1", "flip700_vl2_bl1"]

        Generate.generateGraphs(analysis_df, y_axes_list)
        
    @staticmethod
    def generate_files_phl_bl1_yemk_vl1(uploaded_file_path):
        
        sheet1 = "Samples"
        sheet2 = "High Controls"
        final_sheet = "Analysis"

        # Specify the path to your Excel file
        file_name = AnalysisUtilities.getfile_name(uploaded_file_path)
        file_path = "uploads/" + file_name + ".xlsx"
        
        #get functions to retreave the desired data
        renamed_column_names_list = YemkUtilities.get_renamed_column_names()
        new_column_names_list = YemkUtilities.get_new_column_names()
        sheet1_name = AnalysisUtilities.getsheet1_name(sheet1)
        sheet2_name = AnalysisUtilities.getsheet2_name(sheet2)
        new_sheet_name = AnalysisUtilities.get_new_sheet_name(final_sheet)
        removed_rows_names_list = AnalysisUtilities.remove_rows_names_list()
        
        # Prepare analysis DataFrame by combining data from Samples and High Controls and removing mean and SD rows
        combined_df = AnalysisUtilities.prepare_analysis_df(file_path, sheet1_name, sheet2_name, removed_rows_names_list)

        # get current combined_df column names
        old_column_name_list = AnalysisUtilities.get_old_column_names(combined_df)

        # rewrite columns and add new columns
        analysis_df = AnalysisUtilities.rewrite_column_names(combined_df, old_column_name_list,  renamed_column_names_list, new_column_names_list)

        # Calculate 'relative_well_number' column
        analysis_df = AnalysisUtilities.calculate_relative_well_number(analysis_df)
        
        # generate phl
        analysis_df, phl_indicators = Generate.generate_phl(analysis_df)

        # generate yemk
        analysis_df, yemk_indicators = Generate.generate_yemk(analysis_df)

        # generate live
        analysis_df, live_indicators = Generate.generate_live(analysis_df)

        analysis_indicators = pd.concat([yemk_indicators, phl_indicators, live_indicators], axis=1)

        #write the All_Plates_YEMK_pHL_Live Excel file
        YemkUtilities.export_All_Plates_YEMK_pHL_Live(analysis_df, 'All_P_YEMK_pHL_Live_' + file_name + '.xlsx','All_P_YEMK_pHL_Live')

        #write All hits excel file exclude all rows that don't have a hit in at least 1 of the three z numbers
        YemkUtilities.export_All_hits(analysis_df, 'All_hits_' + file_name + '.xlsx','All_hits')
 
        # Write analysis sheet
        YemkUtilities.write_analysis_sheet(analysis_df, "uploads/" + file_name + ".xlsx", new_sheet_name, analysis_indicators)

        # Define the y-axes for each graph
        y_axes_list = ["total_count", "phl_count", "yemk_count", "live_percentage", "pHL_VL2_BL1", "yemk_vl2_bl1"]

        Generate.generateGraphs(analysis_df, y_axes_list)