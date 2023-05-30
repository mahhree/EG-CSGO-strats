"""
2. Using the created class, answer the following questions:
    a. Is entering via the light blue boundary a common strategy used by
        Team2 on T (terrorist) side?
    b. What is the average timer that Team2 on T (terrorist) side enters
        “BombsiteB” with least 2 rifles or SMGs?
    c. Now that we haveve gathered data on Team2 T side, let's examine their CT
        (counter-terrorist) Side. Using the same data set, tell our coaching
        staff where you suspect them to be waiting inside “BombsiteB”
            i. Hint: Try a heatmap
"""

#question 2 will be coded and answered here

from Q1 import ProcessGameState
import pandas as pd
import numpy as np

Game = ProcessGameState()
Game.ingestion()

"""

a. 

"""

#given boundaries for light blue area
boundaries = {
    13: [-1735, 250],
    14: [-2024, 398],
    15: [-2806, 742],
    16: [-2472, 1233],
    17: [-1565, 580]
}

#collect all the x and y values from the boundaries dictionary
#create two separate lists, x_coords to store all the x values and 
#y_coords to store all the y values
x_coords = [coord[0] for coord in boundaries.values()]
y_coords = [coord[1] for coord in boundaries.values()]


#determine min and max values for the x and y coordinates 
#min and max values are stored in vector1 and vector2 respectively
vector1 = (min(x_coords), min(y_coords))
vector2 = (max(x_coords), max(y_coords))

#check if Team2 enters within the boundaries 
    #note that checks for ALL players not only Team2 on T side
isBoundary = Game.is_within_boundary(vector1, vector2)

maxRows = len(isBoundary) #total num of rows
threshold = 0.5  #i would think above 50% is common and below is uncommon but this can of course be changed

if maxRows > 0:
    team2 = 0 #number of team2 entering through light blue boundary in T side
    total_team2 = 0  #number of team2 on T side

    for index, row in Game.gameData.iterrows(): #we only want team2 on T side data
        if row['team'] == 'Team2' and row['side'] == 'T':
            total_team2 += 1
            if isBoundary.get(index, False):
                team2 += 1

    #i believe the ratio should be team2 on T at boundary/team2 on T side
    #this makes sure we are only taking data for when team2 is on T side
    ratio = team2/total_team2

    if ratio >= threshold:
        print("Entering via the light blue boundary is a common strategy used by Team2 on T side.")
    else:
        print("Entering via the light blue boundary is not a common strategy used by Team2 on T side.")
else:
    print("No entries found within the boundaries for Team2 on T side.")

#Based on the created class ProcessGameState, entering via the light blue boundary is not a common strategy used by Team2 on T side. 


"""

b.

"""
#extract weapons
#check only Team2, T side, and 2 riffles and SMGS
#check BombsiteB location
#find average timer in BombsiteB location

#i believe making a filtered dataset will improve this greatly
#filtered dataset will have Team2, Tside, and >= 2 inventory space 
    #more than 2 in inventory because rifles and SMGs are primary weapons but they may also have a secondary weapon (pistol)
    #note that this can include a pistol and grenade in inventory but we will filter it later 
#after checking BombsiteB
    #futher filter dataset to only include BombsiteB
#take average of times in new filtered dataset

#now that I think about it q2.a can also be modified to have a filtered dataset

Game.extract_Weapons()

location = 'BombsiteB' #this can be changed depending on what location we want to check 

filteredData = Game.gameData[
    (Game.gameData['team'] == 'Team2') & #Team2
    (Game.gameData['side'] == 'T') & #T side
    (Game.gameData['area_name'] == location) & #further filtered data to only include our target location for Team2 on T
    (Game.gameData['inventory'].apply(lambda x: isinstance(x, list) and len(x) >= 2)) #2 or more in inventory
    ]

#print(filteredData['clock_time'])


if location not in filteredData['area_name'].unique():
    print(f"Error: '{location}' not found in dataset.")
else:
    filteredData = filteredData.copy()
    filteredData['clock_time'] = pd.to_datetime(filteredData['clock_time'], format='%M:%S') #clock_time is a str but we need to take the mean so it must be formatted
    #we get a warning for the above line of code SettingWithCopyWarning
    #to bypass this we create filteredData = filteredData.copy()
    
    averageTimer = filteredData['clock_time'].mean()
    averageTimer = averageTimer.strftime('%M:%S')  #format it to look like 00:00 as we see in game
    print(f"The average timer that Team2 on T side enters {location} with at least 2 rifles or SMGs is: {averageTimer}")

"""

c.

"""
#again use filtered data for Team2 CT side in BombsiteB 
#after filtering create a heatmap for all the x,y coordinates use the map provided


