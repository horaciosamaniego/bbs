import pandas as pd
import os
import glob



def read_routes_BBS(directory_path):
    """
    Reads all CSV files starting with 'F' in a specified directory
    and combines them into a single large Pandas DataFrame.

    Args:
        directory_path (str): The path to the directory containing the CSV files.

    Returns:
        pandas.DataFrame: A single DataFrame containing data from all
                          matching CSV files, or an empty DataFrame if no
                          matching files are found or an error occurs.
    """
    # Construct the search pattern for CSV files starting with 'F'
    search_pattern = os.path.join(directory_path, 'F*.csv')
    
    # Find all files matching the pattern
    csv_files = glob.glob(search_pattern)

    # Check if any files were found
    if not csv_files:
        print(f"No CSV files starting with 'F' found in: {directory_path}")
        return pd.DataFrame() # Return an empty DataFrame

    # List to hold individual DataFrames
    dataframes = []

    print(f"Found {len(csv_files)} CSV files starting with 'F':")
    for file_path in csv_files:
        print(f"  - {os.path.basename(file_path)}")
        try:
            # Read each CSV file into a DataFrame
            df = pd.read_csv(file_path)
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading file {os.path.basename(file_path)}: {e}")
            continue # Continue to the next file even if one fails

    # Concatenate all DataFrames into one large DataFrame
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df
    else:
        print("No DataFrames were successfully loaded.")
        return pd.DataFrame() # Return an empty DataFrame if no data was loaded



def species_to_df(species_id: int, data: dict) -> pd.DataFrame:

    """
    Generates a pandas DataFrame for a given species,
    with routes as columns and years as rows.

    Args:
        species_id (int): The name of the species to filter by.
        data (dict): The input dictionary with (species, route) keys
                     and list of (year, abundance) values.

    Returns:
        pd.DataFrame: A DataFrame with years as index and routes as columns.
                      Returns an empty DataFrame if the species is not found.
    """
    df_data = {}
    years = set()

    for (species, route), abundances in data.items():
        if species == species_id:
            if route not in df_data:
                df_data[route] = {}
            for year, abundance in abundances:
                df_data[route][year] = abundance
                years.add(year)

    if not df_data:
        print(f"No data found for species: {species_id}")
        return pd.DataFrame()

    # Create a DataFrame from the collected data
    df = pd.DataFrame.from_dict(df_data, orient='index').transpose()
    df.index.name = 'Year'
    df.columns.name = 'Route'
    return df.sort_index() # Sort by year    


def route_to_df(route_number: int, data: dict) -> pd.DataFrame:
    """
    Generates a pandas DataFrame for a given route number,
    with species as columns and years as rows.

    Args:
        route_number (int): The route number to filter by.
        data (dict): The input dictionary with (species, route) keys
                     and list of (year, abundance) values.

    Returns:
        pd.DataFrame: A DataFrame with years as index and species as columns.
                      Returns an empty DataFrame if the route is not found.
    """
    df_data = {}
    years = set()

    for (species, route), abundances in data.items():
        if route == route_number:
            if species not in df_data:
                df_data[species] = {}
            for year, abundance in abundances:
                df_data[species][year] = abundance
                years.add(year)

    if not df_data:
        print(f"No data found for route: {route_number}")
        return pd.DataFrame()

    # Create a DataFrame from the collected data
    df = pd.DataFrame.from_dict(df_data, orient='index').transpose()
    df.index.name = 'Year'
    df.columns.name = 'Species'
    return df.sort_index() # Sort by year


def year_to_df(year_value: int, data: dict) -> pd.DataFrame:
    """
    Generates a pandas DataFrame for a given year,
    with species as columns and routes as rows.

    Args:
        year_value (int): The year to filter by.
        data (dict): The input dictionary with (species, route) keys
                     and list of (year, abundance) values.

    Returns:
        pd.DataFrame: A DataFrame with routes as index and species as columns.
                      Returns an empty DataFrame if the year is not found.
    """
    df_data = {}
    routes = set()
    species_set = set()

    for (species, route), abundances in data.items():
        for year, abundance in abundances:
            if year == year_value:
                if route not in df_data:
                    df_data[route] = {}
                df_data[route][species] = abundance
                routes.add(route)
                species_set.add(species)

    if not df_data:
        print(f"No data found for year: {year_value}")
        return pd.DataFrame()

    # Create a DataFrame from the collected data
    df = pd.DataFrame.from_dict(df_data, orient='index')
    df.index.name = 'Route'
    df.columns.name = 'Species'
    return df.sort_index(axis=0).sort_index(axis=1) # Sort by route (rows) and species (columns)





## TESTING THE FUNCTION ##
# my_data = [(1980, 4), (1968, 20), (1975, 15)]
# first_year = 1966
# last_year = 2024

# print(f"Input data: {my_data}")
# print(f"Desired year range: {first_year}-{last_year}")

# filled_data = fill_missing_year_data(my_data, first_year, last_year)

# filled_data



def plot_ts_routests(spp,sppname,DB,SPP_SUMMARY,plotit=True):

    fig, ax1 = plt.subplots(figsize=(20, 8))

    # plot stotal species abundance
    # total abundance
    d = DB[DB['AOU']==spp][['Year','Number of individuals']].groupby('Year').sum().reset_index()#.plot('Year','Number of individuals')
    all_years = pd.DataFrame({'Year': range(d['Year'].min(), d['Year'].max() + 1)})

    dd = pd.merge(all_years, d, on='Year', how='left').fillna(0)

    ax1.plot(dd['Year'],dd['Number of individuals'],linestyle='-', marker='o',
            color='Forestgreen')
    ax1.set_ylabel('Individuals',color='Forestgreen', fontsize=14, fontweight='bold')

    ax1.set_xlabel('')

    ax2 = ax1.twinx()

    # plot routes across years
    DB[DB['AOU']==spp][['Year','ruta']].groupby('Year').count().plot(kind='line', title=sppname,
                                                                            linestyle='--', marker='v',ax=ax2,
                                                                            legend='',color='darkgrey')
    ax2.set_ylabel('Routes',color='darkgrey', fontsize=14, fontweight='bold')

    # ax1.set_xticklabels([])


    # add text to plot
    txt = SPP_SUMMARY[SPP_SUMMARY['AOU']==spp].iloc[:,1:5]#['n_rutas','first_year','last_year','timeseries length']
    # print(txt.T)

    table_text = ""
    for col_name, value in txt.items():
        # Handle datetime objects for cleaner display if needed
        if isinstance(value, pd.Timestamp):
            value_str = value.strftime('%Y-%m-%d') # Format date as YYYY-MM-DD
        else:
            value_str = str(value.item())
        table_text += f"{col_name}: {value_str}\n"
    # Remove the trailing newline character
    table_text = table_text.strip()


    ax1.text(0.02, 0.95, table_text,
            transform=ax1.transAxes, # Essential for relative positioning
            fontsize=12,
            verticalalignment='top',   # Align the top of the text with the y-coordinate
            horizontalalignment='left', # Align the left of the text with the x-coordinate
            bbox=dict(boxstyle='round,pad=0.5', fc='lightgrey', ec='k', lw=1, alpha=0.7) # Optional: Add a box around the text
        )
    if plotit == False:
        # Save the plot to  a file and suppress output with a semicolon     
        the_png = 'figs/'+str(spp)+'routes+tts.png'
        plt.savefig(the_png);
        print('saving AOU:',str(spp),'to:',the_png)
    else:
        plt.show()





##### WEBPAGE GENERATION

def generate_species_webpage(csv_file_path, figs_dir_path, output_html_file='species_webpage.html'):
    """
    Generates an HTML webpage displaying species data from a CSV with
    thumbnail images and a modal for larger image viewing.
    Columns are sortable, 'Unnamed:0' column is removed, and the image column
    is labeled 'Time Series'.

    Args:
        csv_file_path (str): Path to the input CSV file.
        figs_dir_path (str): Path to the directory containing species images.
        output_html_file (str): Name of the output HTML file.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Remove 'Unnamed:0' column if it exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        print("Removed 'Unnamed: 0' column.")

    if 'AOU' not in df.columns:
        print("Error: 'AOU' column not found in the CSV file.")
        return

    # Basic HTML structure and styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Species Data</title>
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                margin: 20px;
                background-color: #f4f7f6;
                color: #333;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                overflow: hidden; /* Ensures rounded corners apply to content */
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px 15px;
                text-align: left;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                cursor: pointer; /* Indicate sortable columns */
                position: relative;
            }}
            th:hover {{
                background-color: #45a049;
            }}
            th .sort-arrow {{
                position: absolute;
                right: 10px;
                top: 50%;
                transform: translateY(-50%);
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            tr:hover {{
                background-color: #e9e9e9;
            }}
            .thumbnail {{
                width: 80px;
                height: 80px;
                object-fit: cover;
                border-radius: 8px;
                cursor: pointer;
                transition: transform 0.2s ease-in-out;
            }}
            .thumbnail:hover {{
                transform: scale(1.05);
            }}

            /* Modal Styles */
            .modal {{
                display: none; /* Hidden by default */
                position: fixed; /* Stay in place */
                z-index: 1000; /* Sit on top */
                left: 0;
                top: 0;
                width: 100%; /* Full width */
                height: 100%; /* Full height */
                overflow: auto; /* Enable scroll if needed */
                background-color: rgba(0,0,0,0.7); /* Black w/ opacity */
                justify-content: center;
                align-items: center;
            }}
            .modal-content {{
                margin: auto;
                display: block;
                max-width: 90%;
                max-height: 90%;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }}
            .modal-close {{
                position: absolute;
                top: 15px;
                right: 35px;
                color: #f1f1f1;
                font-size: 40px;
                font-weight: bold;
                transition: 0.3s;
                cursor: pointer;
            }}
            .modal-close:hover,
            .modal-close:focus {{
                color: #bbb;
                text-decoration: none;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <h1>Species Data Table</h1>
        <table id="speciesTable">
            <thead>
                <tr>
    """

    # Add table headers from DataFrame columns and an extra for 'Time Series'
    for i, col in enumerate(df.columns):
        html_content += f"                    <th data-column-index=\"{i}\">{col}<span class=\"sort-arrow\"></span></th>\n"
    # The image column is the last one, its index will be len(df.columns)
    html_content += f"                    <th data-column-index=\"{len(df.columns)}\">Time Series<span class=\"sort-arrow\"></span></th>\n"
    html_content += """
                </tr>
            </thead>
            <tbody>
    """

    # Populate table rows
    for index, row in df.iterrows():
        html_content += "                <tr>\n"
        aou_value = row['AOU']

        # Find the image file
        # This will look for any PNG file starting with the AOU value in the figs directory
        image_files = glob.glob(os.path.join(figs_dir_path, f"{aou_value}routes+tts.png"))
        
        thumbnail_src = ""
        full_image_src = ""
        image_alt = f"Image for AOU {aou_value}"

        if image_files:
            # Take the first matching image found
            full_image_src = os.path.join(figs_dir_path, os.path.basename(image_files[0]))
            thumbnail_src = full_image_src # Using the same for simplicity, could resize if needed
        else:
            # Placeholder image if no matching file is found
            thumbnail_src = f"https://placehold.co/80x80/cccccc/000000?text=No+Image"
            full_image_src = f"https://placehold.co/600x400/cccccc/000000?text=No+Image+Available"
            image_alt = f"No image available for AOU {aou_value}"

        for col in df.columns:
            html_content += f"                    <td>{row[col]}</td>\n"

        # Add the image column
        html_content += f"""
                    <td>
                        <img src="{thumbnail_src}" alt="{image_alt}" class="thumbnail" data-full-src="{full_image_src}">
                    </td>
        """
        html_content += "                </tr>\n"

    html_content += """
            </tbody>
        </table>

        <!-- The Modal -->
        <div id="imageModal" class="modal">
            <span class="modal-close">&times;</span>
            <img class="modal-content" id="img01">
        </div>

        <script>
            // Get the modal
            const modal = document.getElementById("imageModal");
            const modalImg = document.getElementById("img01");
            const span = document.getElementsByClassName("modal-close")[0];

            // Get all thumbnail images and attach click event
            document.querySelectorAll('.thumbnail').forEach(thumbnail => {
                thumbnail.addEventListener('click', function() {
                    modal.style.display = "flex"; // Use flex to center content
                    modalImg.src = this.getAttribute('data-full-src');
                    modalImg.alt = this.alt;
                });
            });

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
            }

            // When the user clicks anywhere outside of the image, close it
            modal.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.style.display = "none";
                }
            });

            // Table Sorting Logic
            const table = document.getElementById('speciesTable');
            const headers = table.querySelectorAll('th');
            const tbody = table.querySelector('tbody');

            let sortDirection = {}; // Stores the current sort direction for each column

            headers.forEach(header => {
                header.addEventListener('click', function() {
                    const columnIndex = parseInt(this.dataset.columnIndex);
                    const currentSortDirection = sortDirection[columnIndex] || 'asc';
                    const newSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';

                    // Remove existing sort arrows
                    headers.forEach(h => {
                        const arrow = h.querySelector('.sort-arrow');
                        if (arrow) arrow.textContent = '';
                    });

                    // Add new sort arrow
                    const arrow = this.querySelector('.sort-arrow');
                    if (arrow) {
                        arrow.textContent = newSortDirection === 'asc' ? ' ▲' : ' ▼';
                    }

                    const rows = Array.from(tbody.querySelectorAll('tr'));

                    rows.sort((rowA, rowB) => {
                        let cellA, cellB;

                        // Handle the 'Time Series' (image) column specifically
                        if (columnIndex === headers.length - 1) { // Last column is the image column
                            cellA = rowA.cells[columnIndex].querySelector('.thumbnail')?.alt || '';
                            cellB = rowB.cells[columnIndex].querySelector('.thumbnail')?.alt || '';
                        } else {
                            cellA = rowA.cells[columnIndex].textContent.trim();
                            cellB = rowB.cells[columnIndex].textContent.trim();
                        }

                        let comparison = 0;

                        // Try to convert to number for numeric sorting
                        const numA = parseFloat(cellA);
                        const numB = parseFloat(cellB);

                        if (!isNaN(numA) && !isNaN(numB)) {
                            comparison = numA - numB;
                        } else {
                            comparison = cellA.localeCompare(cellB);
                        }

                        return newSortDirection === 'asc' ? comparison : -comparison;
                    });

                    // Re-append sorted rows
                    rows.forEach(row => tbody.appendChild(row));

                    sortDirection[columnIndex] = newSortDirection;
                });
            });
        </script>
    </body>
    </html>
    """

    # Write the HTML content to a file
    try:
        with open(output_html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Webpage '{output_html_file}' generated successfully!")
    except Exception as e:
        print(f"Error writing HTML file: {e}")

# Example Usage (replace with your actual file paths)
# Assuming 'species_data.csv' is in the same directory as this script
# and 'figs/' is a subdirectory containing images.
# generate_species_webpage('species_data.csv', 'figs/')





# --- NEW FUNCTIONS FOR IDENTIFYING HIGH-QUALITY ROUTES ---

def filter_bbs_data(df: pd.DataFrame, abundance_col: str = 'Number of individuals') -> pd.DataFrame:
    """
    Applies quality and temporal filters to the BBS consolidated dataframe.

    Filters include:
    - Years from 1980 onwards.
    - Excludes 2020 data (due to COVID-19 survey changes).
    - RPID (Run Protocol ID) == 101 (standard BBS surveys).
    - Excludes species AOU codes for nocturnal, crepuscular, aquatic birds
      typically not well-sampled by standard BBS (e.g., owls, ducks, shorebirds).
      These ranges are general and may need fine-tuning based on specific analysis needs.

    Args:
        df (pd.DataFrame): The input DataFrame with columns:
                           'AOU', 'RPID', 'Year', 'ruta', 'Latitude', 'Longitude',
                           and an abundance column (default 'Number of individuals').
        abundance_col (str): The name of the column containing species abundance/count.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    if not all(col in df.columns for col in ['AOU', 'RPID', 'Year', 'ruta', 'Latitude', 'Longitude', abundance_col]):
        missing_cols = [col for col in ['AOU', 'RPID', 'Year', 'ruta', 'Latitude', 'Longitude', abundance_col] if col not in df.columns]
        raise ValueError(f"Input DataFrame is missing required columns: {missing_cols}. "
                         f"Please ensure your dataframe has these columns and the correct abundance_col name.")

    print(f"Initial rows: {len(df)}")

    # 1. Filter by Year >= 1980
    df_filtered = df[df['Year'] >= 1980].copy()
    print(f"After filtering Year >= 1980: {len(df_filtered)} rows")

    # 2. Exclude 2020 data
    df_filtered = df_filtered[df_filtered['Year'] != 2020].copy()
    print(f"After excluding 2020: {len(df_filtered)} rows")

    # 3. Filter by RPID == 101 (Standard BBS protocol)
    df_filtered = df_filtered[df_filtered['RPID'] == 101].copy()
    print(f"After filtering RPID == 101: {len(df_filtered)} rows")

    # 4. Exclude AOU codes for species not well-sampled by BBS (nocturnal, crepuscular, aquatic)
    # These are general ranges and might need adjustment based on specific BBS guidance or analysis goals.
    # Typically, these might include owls, nightjars, some waterfowl, gulls, and shorebirds.
    # Example AOU ranges for exclusion (these are illustrative, refer to official BBS AOU lists for specifics):
    # Some common exclusions by general groups:
    # Owls (e.g., 3570-3760 range often covers owls/nightjars, but specific is better)
    # Waterfowl (e.g., 0010-0250) often excluded from terrestrial bird analyses
    # Gulls/Terns (e.g., 0000-0150, 0400-0650 for some waterbirds)
    # Shorebirds (e.g., 0260-0350)
    # A more precise list based on the AOU codes might look like this:
    # Example AOU ranges to exclude (these are approximations, adjust as needed):
    # Divers (Loons), Grebes, some Waterfowl, Seabirds, Shorebirds, Gulls, Terns, Alcids, Owls, Nightjars
    aou_to_exclude = set()
    
    # Loons, Grebes, some Waterfowl (general range for aquatic birds)
    aou_to_exclude.update(range(1, 400)) # e.g., 6 (Red-throated Loon) to 390 (American Kestrel) - too broad, refine!
    # A more targeted exclusion might be:
    # Loons (AOU 7-11), Grebes (AOU 18-24), some Ducks/Geese, Gulls/Terns (AOU 36-69), Shorebirds (AOU 88-290), Owls (AOU 365-385)
    # Use official BBS AOU species lists to create a precise exclusion set.
    # For now, let's use a very limited illustrative set, you should expand this with a proper species list:
    aou_to_exclude_list = [
        7, 8, 9, 10, 11, # Loons
        18, 19, 20, 21, 22, 23, 24, # Grebes
        129, 130, 131, 132, 133, # Some Gulls/Terns
        368, 369, 370, 371, 372, 373, 375, 376, # Typical Owls
        420, 421 # Nighthawks/Poorwills (crepuscular)
        # ... add more specific AOU codes based on a species list
    ]
    aou_to_exclude.update(aou_to_exclude_list)

    df_filtered = df_filtered[~df_filtered['AOU'].isin(aou_to_exclude)].copy()
    print(f"After excluding specific AOU codes: {len(df_filtered)} rows")
    
    # Ensure abundance column is numeric and handle NaNs by filling with 0
    df_filtered[abundance_col] = pd.to_numeric(df_filtered[abundance_col], errors='coerce').fillna(0)
    
    # For robust time series analysis, we often need to ensure all surveyed years for a route are present
    # even if no species were seen. This is implicitly handled by the next function,
    # but important for understanding the data.
    
    return df_filtered


def calculate_species_presence(df_filtered: pd.DataFrame, abundance_col: str = 'Number of individuals', presence_threshold: float = 0.9) -> pd.DataFrame:
    """
    Calculates presence metrics for each species on each route to identify
    "continuously present" species.

    Args:
        df_filtered (pd.DataFrame): The filtered DataFrame from `filter_bbs_data`.
        abundance_col (str): The name of the column containing species abundance/count.
        presence_threshold (float): The minimum proportion of years a species must be
                                    present (abundance > 0) to be considered "continuously present".

    Returns:
        pd.DataFrame: A DataFrame with columns for 'ruta', 'AOU', 'total_survey_years',
                      'years_with_presence', 'presence_ratio', and 'is_continuously_present'.
    """
    if not all(col in df_filtered.columns for col in ['AOU', 'Year', 'ruta', abundance_col]):
        raise ValueError("Input DataFrame for calculate_species_presence must contain 'AOU', 'Year', 'ruta', and abundance_col.")

    print("Calculating species presence metrics...")

    # Determine the actual min and max years observed in the filtered data
    min_year_overall = df_filtered['Year'].min()
    max_year_overall = df_filtered['Year'].max()

    # For each route, find the years it was surveyed
    route_years = df_filtered.groupby('ruta')['Year'].unique().apply(lambda x: sorted(list(x)))
    
    presence_data = []

    # Iterate through each unique (ruta, AOU) combination
    # Use a groupby to efficiently get unique combinations and their associated years/counts
    grouped_species_route = df_filtered.groupby(['ruta', 'AOU'])

    for (ruta, aou), group in grouped_species_route:
        # Get all years this specific route was surveyed
        years_route_surveyed = sorted(list(route_years[ruta]))
        
        # Adjust for 2020: if 2020 is in the range of surveyed years, and it's not excluded already,
        # it *should* not count towards the 'total_survey_years' if we are considering effective survey years for continuity.
        # However, filter_bbs_data already removes 2020.
        
        # Years where this species was observed (count > 0)
        species_presence_years = group[group[abundance_col] > 0]['Year'].unique()

        total_survey_years_for_route = len(years_route_surveyed)
        years_with_presence = len(species_presence_years)

        if total_survey_years_for_route > 0:
            presence_ratio = years_with_presence / total_survey_years_for_route
        else:
            presence_ratio = 0 # Should not happen with valid data

        is_continuously_present = (presence_ratio >= presence_threshold)

        presence_data.append({
            'ruta': ruta,
            'AOU': aou,
            'total_survey_years_for_route': total_survey_years_for_route,
            'years_with_presence': years_with_presence,
            'presence_ratio': presence_ratio,
            'is_continuously_present': is_continuously_present
        })

    species_presence_df = pd.DataFrame(presence_data)
    print(f"Calculated presence metrics for {len(species_presence_df)} species-route combinations.")
    return species_presence_df


def identify_long_timeseries_routes(
    df_filtered: pd.DataFrame,
    species_presence_df: pd.DataFrame,
    abundance_col: str = 'Number of individuals',
    top_n_routes: int = 10
) -> pd.DataFrame:
    """
    Identifies routes with the longest time series of continuously present species.

    Args:
        df_filtered (pd.DataFrame): The filtered raw BBS data.
        species_presence_df (pd.DataFrame): DataFrame from `calculate_species_presence`.
        abundance_col (str): The name of the column containing species abundance/count.
        top_n_routes (int): The number of top routes to return.

    Returns:
        pd.DataFrame: A DataFrame containing the top routes, sorted by
                      number of continuously present species and time series length,
                      with their lat/lon coordinates.
    """
    print("Identifying routes with longest time series of continuously present species...")

    # Filter for only continuously present species
    continuous_species_on_routes = species_presence_df[
        species_presence_df['is_continuously_present'] == True
    ].copy()

    # Count how many continuously present species each route has
    route_continuous_species_counts = continuous_species_on_routes.groupby('ruta').size().reset_index(name='num_continuous_species')

    if route_continuous_species_counts.empty:
        print("No routes found with continuously present species based on the given threshold.")
        return pd.DataFrame()

    # Calculate the overall time series length for each route in the *filtered original data*
    # This should be the span of years a route was surveyed within the filtered data.
    route_time_series_info = df_filtered.groupby('ruta')['Year'].agg(
        min_year=('min', 'Year'),
        max_year=('max', 'Year'),
        num_survey_years=('nunique', 'Year') # Count distinct years surveyed for the route
    ).reset_index()

    # Merge the two summary DataFrames
    route_summary = pd.merge(
        route_continuous_species_counts,
        route_time_series_info,
        on='ruta',
        how='inner'
    )
    
    # Add latitude and longitude to the summary
    # Get unique lat/lon for each ruta from the original filtered df
    route_coords = df_filtered[['ruta', 'Latitude', 'Longitude']].drop_duplicates()
    route_summary = pd.merge(route_summary, route_coords, on='ruta', how='left')

    # Sort the routes: prioritize more continuous species, then longer time series
    route_summary = route_summary.sort_values(
        by=['num_continuous_species', 'num_survey_years'],
        ascending=[False, False]
    ).reset_index(drop=True)

    print(f"Top {min(top_n_routes, len(route_summary))} routes identified.")
    return route_summary.head(top_n_routes)