"""
1. Write a python class called ProcessGameState that will accomplish the
following:
    a. Handle file ingestion and ETL (if deemed necessary)
    b. Return whether or not each row falls within a provided boundary
        i. Be as efficient as possible (minimize runtime)
        ii. Reduce dependencies outside of standard Python libraries unless
        you can prove significant improvements.
    c. Extract the weapon classes from the inventory json column
"""



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

    def is_within_boundary(self, vector1, vector2): #b
        """
        return whether or not each row falls within a provided boundary

        Parameters:
            vector1: vector of (x,y) coordinates 
            vector2: vector of (x,y) coordinates 

        Returns:
            boundaryCheck: a dict mapping row index to a bool value indicating whether it falls within the given boundary
        """
        if self.gameData is None:
            print("Game data has not been loaded. Please handle file ingestion first.")

        #seperate and sort the x vectors and y vectors 
        x_coords = sorted([vector1[0], vector2[0]])
        y_coords = sorted([vector1[1], vector2[1]])

        boundaryCheck = {}

        for index, row in self.gameData.iterrows():
            x = row['x']
            y = row['y']

            #check specific boundary and store its bool value 
            boundaryCheck[index] = bool( x_coords[0] <= x <= x_coords[1] and y_coords[0] <= y <= y_coords[1] )

        return boundaryCheck

    def extract_Weapons(self): #c
        """
        Extract the weapon classes from the inventory json column,
        update inventory to have a list of weapons

        Updates the inventory in game_data and returns the weapon_classes dictionary.
        """
        weaponClasses = {}
        if self.gameData is None:
            print("Game data has not been loaded. Please handle file ingestion first.")
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
        """
        this is written based on the knowledge of there is no specific gun information given
        for example: the player has a rifle, but we do not know what type of rifle

        if each weapon has an attribute telling us what type of rifle, pistol, etc 
        this code can easily be modified to hold that information
        but i assume we do not care what type of rifle, smg, pistol, etc they have. just that they have one. 
        """