#question 1 will be coded and answered here

import pandas as pd
import numpy as np

class ProcessGameState:
    """
    python class that will proccess game data using a parquet file

    parameters in __init__
        parquetFile: path to the parquet file

    attributes
        parquet_file_path
        gameData: game data loaded from a Parquet file
    """

    def __init__(self, parquetFile=None):
        if parquetFile is None:
            self.parquetFile = "game_state_frame_data.parquet"
        else:
            self.parquetFile = parquetFile
        self.gameData = None
    
    def ingestion(self): #a
        """
        handle file ingestions and ETL
        if deemed necessary
        load parquet file into pandas dataframe
        """
        try:
            self.gameData = pd.read_parquet(self.parquetFile)
        except FileNotFoundError: #if no file found. location incorrect
            print(f"Error: File '{self.parquetFile}' is not found. Please check file location.")
    