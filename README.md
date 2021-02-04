# sqlalchemy-challenge

### contains
- hawaii.sqlite: source database for dataset containing precipitation data for weather stations in Hawai'i
- climate_starter.ipynb: a jupyter notebook showing analysis of hawaii.sqlite resulting in graphs
- app.py: a script using flask and queries to hawaii.sqlite to display static and dynamic webpages relating to the  precipitation, station, and temperature data

### description
The goal of climate_starter.ipynb was to create a bar graph of rainfall over the last 12 months listed in the dataset, and a histogram of the distribution of temperature measurements taken from the station that had the most measurements. Several preliminary steps were required to process the data from the stations to create the graphs:


The goal of app.py was to build on the analysis done in climate_starter.ipynb, and display queries relating to the precipitation, station, and temperature measurements from hawaii.sqlite on static webpages. Additionally, the file would contain routes to create dynamic webpages that would take user input to display temperature statistics for chosen dates. The following steps were taken to achieve these goals:

### challenges/observations