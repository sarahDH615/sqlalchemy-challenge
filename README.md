# sqlalchemy-challenge

### contains
- hawaii.sqlite: source database for dataset containing precipitation data for weather stations in Hawai'i
- climate_starter.ipynb: a jupyter notebook showing analysis of hawaii.sqlite resulting in graphs
- app.py: a script using flask and queries to hawaii.sqlite to display static and dynamic webpages relating to the  precipitation, station, and temperature data

### description
The goal of climate_starter.ipynb was to create a bar graph of rainfall over the last 12 months listed in the dataset, and a histogram of the distribution of temperature measurements taken from the station that had the most measurements. Several preliminary steps were required to process the data from the stations to create the graphs:
- Reflection of tables within hawaii.sqlite into SQLAlchemy:
    - using create_engine to establish a connection to the sqlite database
    - using Base (automap_base) to reflect the tables
- Investigating the contents of the sqlite database:
    - using Base.classes.keys() to reveal the names of the tables (Measurement, Station), and set those table names as classes within SQLAlchemy
    - opening a session for making queries to the sqlite database
    - querying the first row of each table as a dictionary to reveal the column names, and the sort of data found within each column
- Creating a bar graph of the precipitation data for the last 12 months in the dataset:
    - finding the date range of the last 12 months of the dataset
        - finding the last date in the dataset
            - querying the date column in the Measurement table, ordering the dates in descending order, and returning the first result (the 'greatest' date, or, the most recent date); saving that result to the variable latest_date
            - separating latest_date into year, month, and day components (ld_year, ld_month, ld_day) for use within datetime
        - finding the date a year before the final date
            - creating a datetime object out of the components of latest_date (dt.date(ld_year, ld_month, ld_day))
            - creating another datetime object that would be a year before latest_date (dt.timedelta(days=365))
            - subtracting the second datetime object from the first, and formatting it to fit the date structure within the Measurement date column (.strftime('%Y-%m-%d))


The goal of app.py was to build on the analysis done in climate_starter.ipynb, and display queries relating to the precipitation, station, and temperature measurements from hawaii.sqlite on static webpages. Additionally, the file would contain routes to create dynamic webpages that would take user input to display temperature statistics for chosen dates. The following steps were taken to achieve these goals:

### challenges/observations