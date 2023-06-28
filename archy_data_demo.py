import xarray as xr
from matplotlib import pyplot as plt
import pandas as pd

from archytas.react import ReActAgent, FailedTaskError
from archytas.tools import PythonTool

from easyrepl import REPL

from cartwright.analysis.time_resolution import detect_temporal_resolution
from cartwright.analysis.space_resolution import detect_latlon_resolution

from rich import traceback, print; traceback.install(show_locals=True)





import pdb

def main():
    pr = xr.open_dataset(f'pr_Amon_FGOALS-f3-L_ssp585_r1i1p1f1_gr_201501-210012.nc')
    
    #collect just first few years of the data, and convert to dataframe
    pr = pr.isel(time=slice(0,50))
    df = pr.drop_vars(['time_bnds', 'lat_bnds', 'lon_bnds']).to_dataframe().reset_index()

    #convert time column to string (as if it was read from a csv)
    df['time'] = df['time'].astype(str)


    python = PythonTool(locals={
        'df': df,
        'detect_temporal_resolution': detect_temporal_resolution,
        'detect_latlon_resolution': detect_latlon_resolution}
    )
    agent = ReActAgent(tools=[python], verbose=True)
    agent.add_context(f'''In the python tool the following preexisting locals are available for use: 
- `df`: a dataframe currently loaded. Any times the user mentions data is referring to this dataframe. Before operating on the dataset you should print out the head/columns of the data to get a sense of what it looks like. It's also good to look at the datatypes of the columns.
- `detect_temporal_resolution`: a function with the following signature and docstring:
    ```python
    def detect_temporal_resolution(times:np.ndarray) -> Optional[Resolution]:
        """
        Detect the resolution of temporal data.
        
        @param times: a numpy array of unix times in [SECONDS] (may have duplicates)
        @return: (optional) TimeResolution(uniformity, unit_name, avg_density, avg_error) where 
            - uniformity is a Uniformity enum 
            - unit_name is a TimeUnits enum
            - avg_density is the median density of the data in (unit_name) units
            - avg_error is the mean error in (unit_name) units   
        """
        # Full implementation omitted for brevity
        ...
    ```
- `detect_latlon_resolution`: a function with the following signature and docstring:
    ```python
    def detect_latlon_resolution(lat:np.ndarray, lon:np.ndarray) -> Optional[GeoSpatialResolution]:
        """
        Detect if the lat/lon coordinates are drawn from a uniform grid.

        @param lat: a numpy array of latitudes in [DEGREES]
        @param lon: a numpy array of longitudes in [DEGREES]

        @return: (optional) GeoSpatialResolution with either 
            - square = Resolution
            - lat = Resolution, lon = Resolution
            
        where `square` indicates that the detected grid has the same resolution in both dimensions
        while `lat`/`lon` indicate that the detected grid has different resolutions for lat/lon
        """
        # Full implementation omitted for brevity
        ...
    ```
''')

    # run the REPL
    for query in REPL(history_file='chat_history.txt'):
        try:
            answer = agent.react(query)
            print(f'[green]{answer}[/green]')
        except FailedTaskError as e:
            print(f"[red]{e}[/red]")
        except KeyboardInterrupt:
            print('[yellow]KeyboardInterrupt[/yellow]')




if __name__ == '__main__':
    main()
