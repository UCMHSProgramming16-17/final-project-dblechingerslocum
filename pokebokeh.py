# importing necessary modules
import pandas as pd
import numpy as np

# making a dataframe by reading a csv file
pokedf = pd.read_csv('pokemon.csv')

# list of all pokemon types
Types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']

# for loop creating a new column for every type
for x in range(18):

    poketype = str(Types[x])
    Types[x] = []
# runs through every pokemon and either puts a 1 or a 0 depending on if the pokemon is the specified type
    for n in range(1061):
        if pokedf.at[n, 'type1'] == poketype or pokedf.at[n, 'type2'] == poketype:
            Types[x].append(1)
        else:
            Types[x].append(0)
    pokedf.insert(0, poketype, Types[x])

# converting the weight and height column contents to decimal values
pokedf['weight'] = pokedf['weight'].str.replace(' lbs.','')
pokedf['height'] = pokedf['height'].str.replace('"','')
pokedf['height'] = pokedf['height'].str.replace("'",'')
for n in range(1061):
      inch = float(pokedf.at[n, 'height'][-2:])
      inch /= 12
      newheight = float(pokedf.at[n, 'height'][0:-2]) + float(inch)
      pokedf.set_value(n, 'height', newheight)
pokedf['height'] = pokedf['height'].astype(float)

# creating two lists  with the average weights and heights of each type
avgweight = []
avgheight = []
typedata = [avgweight, avgheight]
pokedata = ['weight', 'height']
for i in range(2):
    x = typedata[i]
    data = pokedata[i]
    for item in Types:
        typenum = 0
        typesum = 0
        for n in range(1061):
            if item[n] == 1:
                typenum += 1
                typesum += float(pokedf.at[n, str(data)])
        x.append(float(typesum/typenum))
            
# making a list of all types again because the previous one became a list of lists for some reason
Types = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']

# creating a new dataframe with the avg weights and heights of each types
typedf = pd.DataFrame(avgweight, Types, ['Average Weight'])
typedf.insert(1, 'Average Height', avgheight)

# creating a bar chart of average weight per type
from bokeh.charts import Bar, Donut, save, show, output_file, Line, Scatter
weightbar = Bar(typedf, values = 'Average Weight', title = 'Average Pokemon Weight by Type', ylabel = "Average Weight (lbs)", legend = False)
output_file("PokeWeightBar.html")
save(weightbar)

# another bar chart with average height by type
heightbar = Bar(typedf, values = 'Average Height', title = 'Average Pokemon Height by Type', ylabel = "Average Height (feet)", legend = False)
output_file("PokeHeightBar.html")
save(heightbar)

# scatter chart showing the relationship between weight and height
pokescatter = Scatter(pokedf, x='weight', y = 'height', color = 'type1', marker = 'type2', legend = 'bottom_right')
output_file('PokeScatter.html')
save(pokescatter)