class LiveUtilities:    
    @staticmethod
    def calculate_live_mean(analysis_df):
        
        live_mean = analysis_df['live_percentage'].mean()

        return live_mean

    @staticmethod
    def calculate_live_sd(analysis_df):

        live_sd = analysis_df['live_percentage'].std()

        return live_sd
    
    @staticmethod
    def populate_live_z_score(analysis_df, live_mean, live_sd):
        analysis_df['live_z_score'] = (analysis_df['live_percentage'] - live_mean) / live_sd
        
        # Add a check for 'total_count' to prevent populating if less than 5,000
        condition = analysis_df['total_count'] >= 5000
        
        # Populate 'live_z_score' based on the condition
        analysis_df.loc[condition, 'live_z_score'] = (analysis_df.loc[condition, 'live_percentage'] - live_mean) / live_sd

        return analysis_df
    
    @staticmethod
    def populate_hits_live_z_score(analysis_df):
        # Use boolean indexing to filter rows based on conditions
        condition = analysis_df['live_z_score'] < -5

        # Populate 'hits_live_z_score' based on the condition
        analysis_df.loc[condition, 'hits_live_z_score'] = analysis_df.loc[condition, 'live_z_score']

        return analysis_df