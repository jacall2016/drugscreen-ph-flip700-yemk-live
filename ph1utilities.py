from scipy.stats import linregress

class PhlUtilities:
    
    @staticmethod
    def calculate_pHL_VL2_BL1(analysis_df):
        """
        Calculate the values for the 'pHL_VL2_BL1' column in the analysis DataFrame.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - pd.DataFrame: The analysis DataFrame with the 'pHL_VL2_BL1' column calculated.
        """
        analysis_df['pHL_VL2_BL1'] = analysis_df['phl_vl2'] / analysis_df['phl_bl1']
        
        return analysis_df
    
    @staticmethod
    def calculate_slope_phl_vl2_phl_bl1(analysis_df):
        """
        Calculate the slope of 'pHL_VL2_BL1' vs 'relative_well_number' columns.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - float: The slope of the linear regression.
        """
        # Perform linear regression
        slope, _, _, _, _ = linregress(analysis_df['relative_well_number'], analysis_df['pHL_VL2_BL1'])

        return slope
    
    @staticmethod
    def calculate_mean_phl_vl2_phl_bl1(analysis_df):
        """
        Calculate the mean of the 'pHL_VL2_BL1' column.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - float: The mean of the 'pHL_VL2_BL1' column.
        """
        # Calculate the mean
        mean_phl_vl2_phl_bl1 = analysis_df['slope_corrected_phl_vl2_bl1'].mean()

        return mean_phl_vl2_phl_bl1
    
    @staticmethod
    def calculate_sd_phl_vl2_phl_bl1(analysis_df):
        """
        Calculate the standard deviation of the 'pHL_VL2_BL1' column.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.

        Returns:
        - float: The standard deviation of the 'pHL_VL2_BL1' column.
        """
        # Calculate the standard deviation
        sd_phl_vl2_phl_bl1 = analysis_df['slope_corrected_phl_vl2_bl1'].std()

        return sd_phl_vl2_phl_bl1
    
    @staticmethod
    def calculate_cuttoff_phl_vl2_phl_bl1(mean_phl_vl2_phl_bl1, sd_phl_vl2_phl_bl1):

        cutoff = mean_phl_vl2_phl_bl1 + (1.5 * sd_phl_vl2_phl_bl1)

        return cutoff
    
    @staticmethod
    def calculate_slope_corrected_phl_vl2_bl1(analysis_df, slope_phl_vl2_phl_bl1):
        """
        Calculate the values for the 'slope_corrected_phl_vl2_bl1' column.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.
        - slope_phl_vl2_phl_bl1 (float): The calculated slope.

        Returns:
        - pd.DataFrame: The analysis DataFrame with the 'slope_corrected_phl_vl2_bl1' column calculated.
        """
        analysis_df['slope_corrected_phl_vl2_bl1'] = analysis_df['pHL_VL2_BL1'] - (analysis_df['relative_well_number'] * slope_phl_vl2_phl_bl1)
        return analysis_df
    
    @staticmethod
    def populate_cutoff_PHL_VL2_BL1_below_cuttoff(analysis_df, cuttoff_phl_vl2_phl_bl1):
        """
        Populate the 'cutoff_PHL_VL2_BL1_below_cuttoff' column based on the cutoff value.

        Parameters:
        - analysis_df (pd.DataFrame): The analysis DataFrame.
        - cuttoff_phl_vl2_phl_bl1 (float): The cutoff value.

        Returns:
        - pd.DataFrame: The analysis DataFrame with the 'cutoff_PHL_VL2_BL1_below_cuttoff' column populated.
        """
        # Create a copy of the 'pHL_VL2_BL1' column
        analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'] = analysis_df['slope_corrected_phl_vl2_bl1']

        # Replace values with None where the condition is not met
        analysis_df.loc[analysis_df['slope_corrected_phl_vl2_bl1'] > cuttoff_phl_vl2_phl_bl1, 'cutoff_PHL_VL2_BL1_below_cuttoff'] = None

        return analysis_df
    
    @staticmethod
    def calculate_corrected_mean_phl_vl2_phl_bl1(analysis_df):
        
        # calculate the corrected_mean_phl_vl2_phl_bl1 by the cutoff_PHL_VL2_BL1_below_cuttoff 
        corrected_mean_phl_vl2_phl_bl1 = analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].mean()

        return corrected_mean_phl_vl2_phl_bl1
    
    @staticmethod
    def calculate_corrected_sd_phl_vl2_phl_bl1(analysis_df):
        
        # calculate the corrected_mean_phl_vl2_phl_bl1 by the cutoff_PHL_VL2_BL1_below_cuttoff 
        corrected_sd_phl_vl2_phl_bl1 = analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].std()

        return corrected_sd_phl_vl2_phl_bl1
    
    @staticmethod
    def populate_phl_z_score(analysis_df, corrected_mean_phl_vl2_phl_bl1, corrected_sd_phl_vl2_phl_bl1):

        if not analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].isna().all():
            analysis_df['phl_z_score'] = (analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'] - corrected_mean_phl_vl2_phl_bl1)/corrected_sd_phl_vl2_phl_bl1

        return analysis_df
    
    @staticmethod
    def populate_hits_phl_z_score(analysis_df):
        # Use boolean indexing to filter rows based on conditions
        condition = (analysis_df['cutoff_PHL_VL2_BL1_below_cuttoff'].notna()) & (analysis_df['phl_z_score'] < -5)

        # Populate 'hits_phl_z_score' based on the condition
        analysis_df.loc[condition, 'hits_phl_z_score'] = analysis_df.loc[condition, 'phl_z_score']

        return analysis_df