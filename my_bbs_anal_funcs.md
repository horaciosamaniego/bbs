---
title: Documentation analysis functions for BBS project
author: Horacio Samaniego
date: 5-9-2025
---



# Documentation for `my_bbs_anal_funcs.py`

This is a comprehensive overview and documentation of the functions contained in the `my_bbs_anal_funcs.py` file. The functions are organized into three main categories: Data Loading and Structuring, Time Series Analysis and Filtering, and Webpage Generation.

`docstrings` are provided for each function to explain their purpose, parameters, return values, and usage examples.

## 1. Data Loading and Structuring

### `read_routes_BBS(directory_path)`: 

Loads and combines multiple CSV files from a directory into a single pandas DataFrame. It specifically looks for files starting with 'F' and includes robust error handling to continue processing even if a file fails to load.

```{python}
def read_routes_BBS(directory_path):
    """
    Reads and consolidates BBS data from multiple CSV files into a single DataFrame.

    This function scans a specified directory for all CSV files whose filenames
    start with the letter 'F'. It reads each matching file and concatenates
    their contents into a single, unified pandas DataFrame, which is useful for
    consolidating multi-file datasets like the Breeding Bird Survey (BBS) route data.

    Args:
        directory_path (str): The path to the directory containing the CSV files.
                              This path should be a string that `os.path.join` can use.

    Returns:
        pandas.DataFrame: A single DataFrame containing data from all
                          matching CSV files. The DataFrame will be empty if no
                          matching files are found or if an error occurs during file reading.
                          The index is reset to a default integer index.

    Raises:
        FileNotFoundError: If the specified directory path does not exist. (Implicit, handled by `glob`)

    Example:
        >>> import pandas as pd
        >>> # Assuming 'data/F1.csv' and 'data/F2.csv' exist with valid data.
        >>> combined_df = read_routes_BBS('data')
        >>> # The 'combined_df' now contains all data from both files.
        >>> combined_df.shape
        (20, 5)
    """
```

### `species_to_df(species_id, data)`: 

Transforms raw data to create a time series DataFrame for a specific species. The resulting table has years as rows and survey routes as columns, ideal for analyzing a single species' population trends across multiple locations.

```{python}
def species_to_df(
        species_id: int, 
        data: dict
        ) -> pd.DataFrame:
    """
    Generates a DataFrame for a specific species from a nested data dictionary.

    This function filters a dictionary of bird count data to create a new
    DataFrame structured for a single species. The resulting DataFrame has
    routes as columns and years as the index, with abundance values in the cells.
    This format is ideal for analyzing species abundance trends across different
    geographical routes over time.

    Args:
        species_id (int): The unique AOU code (as an integer) of the species to filter by.
        data (dict): The input dictionary mapping `(species_id, route_id)` tuples
                     to a list of `(year, abundance)` tuples. For example,
                     `{(1234, 567): [(1980, 5), (1981, 7)], ...}`.

    Returns:
        pandas.DataFrame: A DataFrame with years as the index and routes as columns.
                          Returns an empty DataFrame if the species ID is not found in the data.

    Example:
        >>> # Assuming `bird_data` is a dictionary with species data.
        >>> # bird_data = {(1234, 1): [(2000, 10), (2001, 15)], (1234, 2): [(2000, 5)], ...}
        >>> df_species_1234 = species_to_df(1234, bird_data)
        >>> df_species_1234
              Route 1  Route 2
        Year
        2000       10        5
        2001       15      NaN
    """
```


### `route_to_df(route_number, data)`: 

Pivots the data to focus on a single survey route. It generates a time series DataFrame with years as rows and species as columns, which is useful for analyzing the entire bird community on that route over time.

```{python}
def route_to_df(
        route_number: int, 
        data: dict
        ) -> pd.DataFrame:
    """
    Generates a DataFrame for a specific route from a nested data dictionary.

    This function filters a dictionary of bird count data to create a new
    DataFrame structured for a single route. The resulting DataFrame has
    species as columns and years as the index, with abundance values in the cells.
    This format is ideal for analyzing which species were present on a specific
    route and how their abundances changed over time.

    Args:
        route_number (int): The unique ID of the route to filter by.
        data (dict): The input dictionary mapping `(species_id, route_id)` tuples
                     to a list of `(year, abundance)` tuples. For example,
                     `{(1234, 567): [(1980, 5), (1981, 7)], ...}`.

    Returns:
        pandas.DataFrame: A DataFrame with years as the index and species as columns.
                          Returns an empty DataFrame if the route number is not found in the data.

    Example:
        >>> # Assuming `bird_data` is a dictionary with route data.
        >>> # bird_data = {(1234, 1): [(2000, 10), (2001, 15)], (5678, 1): [(2000, 20)], ...}
        >>> df_route_1 = route_to_df(1, bird_data)
        >>> df_route_1
              Species 1234  Species 5678
        Year
        2000            10            20
        2001            15           NaN
    """
```  


### `year_to_df(year_value, data)`: 

Creates a DataFrame that provides a snapshot of the data for a single year. The resulting table has routes as rows and species as columns, which is ideal for spatial analysis or comparing community composition in a specific year.

```{python}
def year_to_df(
        year_value: int, 
        data: dict
        ) -> pd.DataFrame:

        """
        Generates a DataFrame for a single year from a nested data dictionary.

        This function filters a dictionary of bird count data to create a DataFrame
        that represents a snapshot for a single year. The resulting DataFrame has
        routes as the index and species as columns, with abundance values in the cells.
        This format is useful for comparing species abundance across different routes
        within a specific year.

        Args:
            year_value (int): The year (e.g., 2020) to filter the data by.
            data (dict): The input dictionary mapping `(species_id, route_id)` tuples
                        to a list of `(year, abundance)` tuples.

        Returns:
            pandas.DataFrame: A DataFrame with routes as the index and species as columns.
                            Returns an empty DataFrame if the year is not found.

        Example:
            >>> # Assuming `bird_data` contains data for the year 2020.
            >>> # bird_data = {(1234, 1): [(2020, 10)], (5678, 1): [(2020, 20)], (1234, 2): [(2020, 5)], ...}
            >>> df_2020 = year_to_df(2020, bird_data)
            >>> df_2020
                Species 1234  Species 5678
            Route
            1               10            20
            2                5           NaN
        """
   ``` 

---

## 2. Time Series Analysis and Filtering

### `fill_missing_year_data(data_tuples, start_year, end_year)`: 
Addresses missing time series data by filling in any years without data with a value of `0` within a specified range. This creates a continuous time series, which is a common requirement for statistical models.
  
```{python}
def fill_missing_year_data(
    data_tuples: list[tuple[int, int]],
    start_year: int,
    end_year: int
    ) -> list[tuple[int, int]]:
    
    """
    Fills gaps in a time series of year-value tuples.

    This function takes a list of `(year, value)` tuples and creates a new
    list that covers a continuous range of years from a specified start year
    to an end year. For any years within the range that are missing from the
    input list, it inserts a new tuple with a default value of 0. This is
    useful for standardizing time series data for analysis or plotting.

    Args:
        data_tuples (list[tuple[int, int]]): A list of tuples, where each tuple
                                             is `(year, value)`. The order of
                                             tuples does not matter.
        start_year (int): The first year in the desired continuous range (inclusive).
        end_year (int): The last year in the desired continuous range (inclusive).

    Returns:
        list[tuple[int, int]]: A new, sorted list of tuples covering the specified
                               year range. Missing years will have a value of 0.
                               An empty list is returned if `start_year` is
                               greater than `end_year` or if input types are invalid.

    Raises:
        TypeError: If `data_tuples`, `start_year`, or `end_year` are not of the
                   expected types. (Handled internally by the function's checks).

    Example:
        >>> my_data = [(1980, 4), (1968, 20), (1975, 15)]
        >>> filled = fill_missing_year_data(my_data, 1966, 1982)
        >>> # The filled list will contain tuples for every year from 1966 to 1982,
        >>> # with 0s for the missing years.
    """
```



### `plot_ts_routests(spp, sppname, DB, SPP_SUMMARY, plotit=True)`: 

Generates a two-axis plot for a given species, displaying both its total abundance over time and the number of routes where it was observed. It also adds a summary table to the plot for quick reference.

```{python}
def plot_ts_routests(
        spp, sppname, 
        DB, 
        SPP_SUMMARY, 
        plotit=True
        ):

    """
    Generates a dual-axis plot of species abundance and survey routes over time.

    This function creates a matplotlib plot with two vertical axes (twinx).
    The left axis shows the total number of individuals of a specific species (abundance)
    per year. The right axis shows the number of routes on which that species was
    observed per year. This visualization helps to understand population trends
    in the context of sampling effort. A summary table of key statistics for the
    species is added as text on the plot.

    Args:
        spp (int): The AOU code for the species to plot.
        sppname (str): The common name of the species to use as the plot title.
        DB (pd.DataFrame): The main, consolidated BBS data DataFrame. Must contain
                           'AOU', 'Year', 'Number of individuals', and 'ruta' columns.
        SPP_SUMMARY (pd.DataFrame): A summary DataFrame containing key statistics
                                    for each species. Must contain 'AOU' and the
                                    summary columns used for the text box (e.g., 'n_rutas', 'first_year').
        plotit (bool, optional): If `True`, the plot is displayed. If `False`,
                                 it is saved to a file in the 'figs/' directory.
                                 Defaults to `True`.

    Returns:
        None: This function saves or displays a plot and does not return a value.

    Raises:
        ValueError: If `DB` or `SPP_SUMMARY` do not contain the required columns.

    Example:
        >>> # Assume DB and SPP_SUMMARY are properly structured DataFrames.
        >>> plot_ts_routests(3730, 'American Robin', DB, SPP_SUMMARY)
        # This will display a plot for the American Robin.
        >>> plot_ts_routests(4740, 'House Finch', DB, SPP_SUMMARY, plotit=False)
        # This will save a PNG file of the plot for the House Finch.
    """
```

### `filter_bbs_data(df, abundance_col='Number of individuals')`: 

Performs key data cleaning and filtering to create a high-quality subset for analysis. It removes data from years before 1980 and the year 2020 (due to COVID-19), filters for a specific survey protocol (`RPID == 101`), and can exclude species not well-sampled by standard methods.

```{python}
    
def filter_bbs_data(
        df: pd.DataFrame, 
        abundance_col: str = 'Number of individuals'
        ) -> pd.DataFrame:
    
    """
    Applies quality and temporal filters to a BBS consolidated DataFrame.

    This function cleans a raw BBS dataset by applying a series of filters
    to ensure the data is suitable for robust time series analysis. Filters
    include restricting the time frame (e.g., years 1980 onwards), excluding
    known problematic years (e.g., 2020 due to COVID-19), and removing
    species that are not reliably sampled by standard BBS protocols (e.g.,
    nocturnal or aquatic birds).

    Args:
        df (pd.DataFrame): The input DataFrame. It is expected to contain
                           columns for 'AOU', 'RPID', 'Year', 'ruta', 'Latitude',
                           'Longitude', and a column for abundance.
        abundance_col (str, optional): The name of the column that contains
                                       species abundance or count data.
                                       Defaults to 'Number of individuals'.

    Returns:
        pd.DataFrame: A new, filtered DataFrame that meets the specified criteria.

    Raises:
        ValueError: If the input DataFrame is missing any of the required columns
                    or if the specified `abundance_col` is not found.

    Example:
        >>> # Assuming `bbs_raw_data` is a large DataFrame from `read_routes_BBS`.
        >>> filtered_df = filter_bbs_data(bbs_raw_data)
        >>> filtered_df.shape
        (25000, 7) # Expected shape will vary, but should be smaller.
    """
```

### `calculate_species_presence(df_filtered, abundance_col, presence_threshold=0.9)`: 

Calculates the proportion of years a species was observed on a specific route. It uses a defined threshold to determine if a species is "continuously present," a key metric for identifying high-quality time series for analysis.

```{python}
def calculate_species_presence(
        df_filtered: pd.DataFrame, 
        abundance_col: str = 'Number of individuals', 
        presence_threshold: float = 0.9
        ) -> pd.DataFrame:

    """
    Calculates presence metrics for each species on each route.

    This function analyzes a filtered BBS dataset to determine how consistently
    each species was observed on each route. It computes a ratio of
    "years with presence" (years where the species was observed with a count > 0)
    to the "total years the route was surveyed." This metric is used to identify
    species that are considered "continuously present" based on a specified threshold.

    Args:
        df_filtered (pd.DataFrame): A DataFrame that has been cleaned and filtered
                                    by the `filter_bbs_data` function.
        abundance_col (str, optional): The name of the column containing species
                                       abundance/count. Defaults to 'Number of individuals'.
        presence_threshold (float, optional): The minimum proportion of survey years
                                              a species must be present on a route to be
                                              considered "continuously present."
                                              Defaults to 0.9 (90%).

    Returns:
        pd.DataFrame: A new DataFrame with columns for `ruta`, `AOU`,
                      `total_survey_years_for_route`, `years_with_presence`,
                      `presence_ratio`, and a boolean flag `is_continuously_present`.

    Raises:
        ValueError: If the input DataFrame does not contain the required columns.

    Example:
        >>> # Assuming `filtered_df` is the output of `filter_bbs_data`.
        >>> presence_df = calculate_species_presence(filtered_df, presence_threshold=0.8)
        >>> # The `presence_df` will have a row for each species-route combination.
  ```

### `identify_long_timeseries_routes(df_filtered, species_presence_results, abundance_col)`: 

Ranks survey routes based on the number of "continuously present" species and the length of their time series. This function helps identify the most valuable routes for long-term ecological analysis.

```{python}
def identify_long_timeseries_routes(
        df_filtered: pd.DataFrame,
        species_presence_results: pd.DataFrame,
        abundance_col: str = 'Number of individuals'
        ) -> pd.DataFrame:

    """
    Identifies routes with the longest time series of continuously present species.

    This function consolidates the results of the filtering and presence
    calculation steps to find the highest-quality routes for long-term trend
    analysis. It counts the number of "continuously present" species on each
    route and determines the length of the survey history. The routes are then
    ranked, prioritizing those with the most continuously present species and
    the longest time series.

    Args:
        df_filtered (pd.DataFrame): The filtered BBS data DataFrame, which is used
                                    to determine the total survey years for each route.
        species_presence_results (pd.DataFrame): The DataFrame generated by
                                                 `calculate_species_presence` that
                                                 contains the presence metrics.
        abundance_col (str, optional): The name of the column containing species
                                       abundance/count. Defaults to 'Number of individuals'.

    Returns:
        pd.DataFrame: A summary DataFrame of the top routes, sorted by the number
                      of continuously present species and then by the length of their
                      time series. It also includes the `ruta` ID, latitude, and longitude.

    Raises:
        ValueError: If the input DataFrames do not contain the required columns.

    Example:
        >>> # Assuming `filtered_df` and `presence_df` are ready.
        >>> top_routes = identify_long_timeseries_routes(filtered_df, presence_df)
        >>> top_routes.head()
           ruta  num_continuous_species  num_survey_years  Latitude  Longitude
        0   1234                      15                40     35.12     -90.15
        1   5678                      12                42     40.05    -105.28
    """
```



## 3. Webpage Generation

### `generate_species_webpage(csv_file_path, figs_dir_path, output_html_file='species_webpage.html')`: 
Creates an interactive HTML webpage to visualize the results. It generates a sortable table from a CSV file, links to corresponding time series plots, and includes a modal window to display larger versions of the images.

```{python}
def generate_species_webpage(
        csv_file_path, 
        figs_dir_path, 
        output_html_file='species_webpage.html'
        ):

    """
    Generates a dynamic HTML webpage from a species data CSV file.

    This function reads species data from a specified CSV file and creates a
    searchable, sortable HTML table. The table includes columns for species data
    and a special "Time Series" column that displays thumbnail images. Clicking
    a thumbnail opens a modal window to view the full-size image. This is
    useful for creating browsable reports for large datasets of species with
    associated visualizations.

    Args:
        csv_file_path (str): The path to the input CSV file containing species data.
                             This file is expected to have an 'AOU' column.
        figs_dir_path (str): The path to the directory containing image files.
                             Images are expected to be named in the format
                             '<AOU>routes+tts.png' (e.g., '3730routes+tts.png').
        output_html_file (str, optional): The name of the HTML file to be generated.
                                          Defaults to 'species_webpage.html'.

    Returns:
        None: This function generates a file and does not return a value.

    Raises:
        FileNotFoundError: If the input `csv_file_path` does not exist.
        ValueError: If the 'AOU' column is not found in the CSV file.

    Example:
        >>> # Assuming 'species_summary.csv' and a 'figs' directory exist.
        >>> generate_species_webpage('species_summary.csv', 'figs')
        # This will generate a new file named 'species_webpage.html'.
    """
```