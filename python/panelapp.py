import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn

primary_color = "#007285"
secondary_color = "B54300"
csv = ("https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
)


pn.extension(design="material", sizing_mode = "stretch_width")

#get the data
@pn.cache 
def get_data():
    return pd.read_csv(csv, parse_dates=['date'], index_col="date")
data = get_data()

data.tail() 

def transform_data(variable, window, sigma):
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return avg, avg[outliers]

def get_plot(variable="Temperature", window=30, sigma=10):
    avg, highlight = transform_data(variable, window, sigma)
    return avg.hvplot(
        height=300, legend=False, color=primary_color) * highlight.gvplot.scatter(color=secondary_color, padding=0.1, legend=False)
get_plot(variable="Temperature", window=20, sigma=10)

#creating sliders

variable_widget = pn.widgets.Select(name="variable", value="Temperature", options=list(data.columns))
    -