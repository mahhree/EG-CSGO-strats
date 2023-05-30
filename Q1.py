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





    
    def extract_Weapons(self):#c
        """
        Extract the weapon classes from the inventory JSON column,
        update inventory to have a list of weapons

        Updates the inventory in game_data and returns the weapon_classes dictionary.
        """
        weaponClasses = {}
        if self.gameData is None:
            self.ingestion()
        try:
            for index, inventory in enumerate(self.gameData['inventory']):
                if isinstance(inventory, np.ndarray):
                    weaponClasses_list = []
                    for item in inventory:
                        item_data = dict(item)
                        tempWeapons = item_data.get('weapon_class')
                        if tempWeapons:
                            weaponClasses_list.append(tempWeapons)
                    self.gameData.at[index, 'inventory'] = weaponClasses_list
                    weaponClasses[index] = weaponClasses_list
        except KeyError:
            print("Error: 'inventory' column not found in the loaded data.")
        #return weaponClasses
    
        """
        this is written based on the knowledge of there is no specific gun information given
        for example: the player has a rifle, but we do not know what type of rifle

        if each weapon has an attribute telling us what type of rifle, pistol, etc 
        this code can easily be modified to hold that information
        but i assume we do not care what type of rifle, smg, pistol, etc they have. just that they have one. 
        """

Game = ProcessGameState()
Game.ingestion()












#print(Game.extract_Weapons())