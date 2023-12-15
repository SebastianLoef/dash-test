import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from flask import g
import geopandas as gpd
import plotly.express as px
import plotly.graph_objs as go
import requests
import pandas as pd


def get_data(deso: str) -> pd.DataFrame:
    url = "https://deso-scb.happypebble-ce806977.westus2.azurecontainerapps.io/send-data/"
    data = {"deso": deso}

    response = requests.post(url, json=data)
    df = pd.read_json(response.json())
    return df


# Load your geospatial data
gdf = gpd.read_file("data/DeSO_2018_v2.gpkg")

# Project the GeoDataFrame to WGS 84 (latitude and longitude)
gdf = gdf.to_crs(epsg=4326)
gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.005, preserve_topology=True)
geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"deso": deso},
            "geometry": geom.__geo_interface__,
        }  # Use __geo_interface__ to get a serializable format
        for deso, geom in zip(gdf["deso"], gdf["geometry"])
    ],
}
# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        html.Div(
            [dcc.Graph(id="map", clickData=None)],
            style={"width": "50%", "display": "inline-block", "vertical-align": "top"},
        ),
        html.Div(
            [
                dcc.Graph(id="graph1", style={"width": "100%", "height": "10%"}),
                dcc.Graph(
                    id="graph2",
                    style={"width": "100%", "height": "10%"},
                ),
                dcc.Graph(
                    id="graph3",
                    style={
                        "width": "100%", "height": "10%"
                    },
                ),
            ],
            style={
                "width": "45%",
                "display": "inline-block",
                "vertical-align": "top",
                "padding-left": "10px",
            },
        ),
    ]
)


# Set up a simple map centered on Sweden
@app.callback(Output("map", "figure"), [Input("map", "id")])
def display_map(_):
    fig = px.choropleth_mapbox(
        gdf,
        geojson=geojson,
        featureidkey="properties.deso",
        locations="deso",
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": 60.128161, "lon": 18.643501},
    )
    fig.update_layout(
        height=800,  # Adjust the height of the map
        width=800,  # Adjust the width of the map
        margin={
            "r": 10,
            "t": 10,
            "l": 10,
            "b": 10,
        },  # Adjust the margins (right, top, left, bottom)
        geo=dict(
            landcolor="white",
            countrywidth=0.5,
            # You can also adjust other geo-related settings here
        ),
    )
    return fig


# Callback for updating the graphs based on the clicked region
@app.callback(
    [
        Output("graph1", "figure"),
        Output("graph2", "figure"),
        Output("graph3", "figure"),
    ],
    [Input("map", "clickData")],
    [State("map", "figure")],
)
def display_graphs(clickData, map_figure):
    if clickData is None:
        # Default empty figures if no region is clicked
        return [px.scatter(), px.scatter(), px.scatter()]

    # Get clicked region identifier
    clicked_region_id = clickData["points"][0]["location"]
    df = get_data(clicked_region_id)

    # Filter or compute your data based on `clicked_region_id`
    # For this example, let's create dummy figures
    fig1 = px.bar(
        data_frame=df[df["type"] == "age_structure"],
        x="year",
        y="values",
        labels={
            "values": "#apartments",
        },
        title=f"Graph 1 for {clicked_region_id}",
    )
    fig2 = px.bar(
        data_frame=df[df["type"] == "apartments"],
        x="upplåtelseform",
        y="values",
        labels={
            "values": "#apartments",
        },
        title=f"Graph 2 for {clicked_region_id}",
    )
    fig3 = px.bar(
        data_frame=df[df["type"] == "vehicles"],
        x="status",
        y="values",
        labels={
            "values": "#vehicles",
        },
        title=f"Graph 3 for {clicked_region_id}",
    )

    return [fig1, fig2, fig3]


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
