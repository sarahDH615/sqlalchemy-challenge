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
- summary statistics for precipitation data
    - calling .describe() on prcp_data dataframe
- finding the number of stations within the dataset
    - finding the number of stations within the Station table
        - querying the Station table's id column, grouping by the id column, and applying .count()
    - finding the number of stations within the Measurement table
        - querying the Measurement table's station column, grouping by the station column, and applying .count()
    - conducting an inner join and counting the stations from the resulting join
        - joining the Measurement table's station column and the Station table's name column filtering where the two columns match, grouping by the id column, and calling .count()
- creating a histogram of the distribution of the temperature measurements on the most prolific station
    - finding the station with the most measurements
        - querying the Measurement table for the station column and the count of the id column, grouping by the station column, ordering by the count of the id column in descending order, and saving the result to a variable stations_count
        - creating a for loop to print each row in stations_count
        - saving the first item in the first row of stations_count (stations_count[0][0]) as most_active_station_id
    - finding the lowest, highest, and average temperature for the most active station
        - querying the Measurement table's column tobs (temperature observations), applying the function to find the maximum value (func.max), and filtering for rows only where the station column matches most_active_station_id, saving the result to max_temp
        - applying the same query for minimum and average temperature, changing the function to func.min or func.avg, saving the results to min_temp and avg_temp
    - creating a dataframe containing the temperature measurements for the most active station id, for the last 12 months of the dataset
        - querying the Measurement table for the tobs and id columns, filtering for all dates greater than or equal to the year_before variable, and filtering for only the most active station id
        - calling pd.DataFrame() on the results of the query, and saving it to a dataframe, temps_df
        - setting the id column as the index of temps_df
    - graphing the histogram
        - calling .hist() on temps_df, using 12 bins, and a zorder of 3 to have the bars show in front of the grid
    
The goal of app.py was to build on the analysis done in climate_starter.ipynb, and display queries relating to the precipitation, station, and temperature measurements from hawaii.sqlite on static webpages. Additionally, the file would contain routes to create dynamic webpages that would take user input to display temperature statistics for chosen dates. The following steps were taken to achieve these goals:
- setting up the database within the file
    - using create_engine to make a connection with the sqlite database
    - using Base (automap_base()) to reflect the database into the file
    - using Base to save the Measurement and Station tables (already known from previously opening the database within the jupyter notebook) into classes for use in the file
- creating variables for use across multiple routes/functions
    - opening a session with the sqlite database
    - re-using code from jupyter notebook for defining latest_date, ld_year, ld_month, ld_day, year_before, most_active_station_id
    - querying Measurement table's date column, appending the first four digits (the year) within each row's first element to years_list, making a set of and sorting the list to create unique_years_list
- setting up Flask and creation of routes
    - home route to list available routes
        - defining home() function to:
            - print the request made to the Terminal
            - open a session
            - return available routes with descriptions, followed by a note of the format to follow for entering dates for the user-input routes
            - close the session
    - precipitation route to return all the precipitation data for the last year in the dataset
        - defining precipitation() function to:
            - print the request made to the Terminal
            - open a session
            - reuse the code from the jupyter notebook, querying the Measurement table, filtering for all dates greater than or equal to year_before, and save it to the variable pdata
            - create a for loop to append the date from each row in pdata to an empty dictionary prcp_dict
            - close the session
            - return the jsonified prcp_dict
    - stations route to list stations in the database
        - defining stations() function to:
            - print the request made to the Terminal
            - open a session
            - edit code from jupyter notebook, querying to join the Station and Measurement tables, filtering where the Station station column matches the Measurement station column, and select the Measurement table's station column, and the Station table's name column
            - create a for loop over the query to append the second item in each row (each station's name) to an empty list stations_list
            - close the session
            - return the jsonifed stations_list


### challenges/observations