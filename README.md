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
            - subtracting the second datetime object from the first, and formatting it to fit the date structure within the Measurement date column (.strftime('%Y-%m-%d)), and saving the result to variable year_before
        - creating a dataframe of the last 12 months precipitation data to graph from
            - querying the Measurement table
                - opening a query on the Measurement table, filtering for the date being greater than or equal to year_before
            - creating and cleaning up lists to make into the dataframe
                - conducting a for loop on the query and appending date and prcp (precipitation) columns in each row to empty lists dates_list and precips_list
                - using a list comprehension to replace 'none' values in the precips_list with zeros, and saving the new list to precips_list_fix
            - creating the dataframe
                - making the dataframe prcp_data out of a dictionary containing the dates_list and precips_list_fix
                - setting the date column as the index, and sorting the index so that dates will be sequential
        - graphing the precipitation data for the last 12 months in the dataset
            - graph labelling experimentation and set-up
                - testing to see if each date in prcp_data has an equal number of data points for labelling every nth value
                    - using the .unique() function on prcp_data.index in a list comprehension, saved as each_date, to have a list of all the unique dates in the dataframe
                    - for loop to append the number of rows each date has to a list, num_measurements, taking the set of that list (unique_no_measurements), which contains four different lengths -- the dates have different numbers of rows attached to them
                - setting xticks and labels for only every 250 data points
                    - using the numpy arange function to create a list (nums_of_x) from 1 to the length of the precipitation column in the prcp_data dataframe, plus  1 (since the dataframe will start at index 0), taking steps of 250
                    - using a list comprehension to append all the dates in prcp_data.index to list x_names
                    - using nums_of_x and x_names to append the value within x_names at the index of each number within nums_of_x to list x_labels
            - creating the bar graph 'precipitation by date between 23 August 2016 and 23 August 2017'
                - using list num_of_x to set the xticks
                - using list x_labels to set the xtick labels
                - using zorder to set the grid behind the bars


The goal of app.py was to build on the analysis done in climate_starter.ipynb, and display queries relating to the precipitation, station, and temperature measurements from hawaii.sqlite on static webpages. Additionally, the file would contain routes to create dynamic webpages that would take user input to display temperature statistics for chosen dates. The following steps were taken to achieve these goals:

### challenges/observations