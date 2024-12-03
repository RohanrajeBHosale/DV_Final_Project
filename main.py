import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Load datasets from JSON files
dataset_files = {
    "Energy Use Per Person": "cleaned_datasets/energy_use_per_person_cleaned.json",
    "Electricity Generation": "cleaned_datasets/electricity_generation_cleaned.json",
    "Coal Consumption": "cleaned_datasets/coal_consumption_cleaned.json",
    "Renewables": "cleaned_datasets/primary_energy_consumption_from_renewables_cleaned.json",
    "Gas Consumption": "cleaned_datasets/gas_consumption_cleaned.json",
    "Carbon Intensity": "cleaned_datasets/carbon_intensity_cleaned.json",
    "Primary Energy Consumption": "cleaned_datasets/primary_energy_consumption_cleaned.json",
}

datasets = {name: pd.read_json(file) for name, file in dataset_files.items()}

# Define color scales for datasets
color_scales = {
    "Energy Use Per Person": px.colors.sequential.Viridis,
    "Electricity Generation": px.colors.sequential.Plasma,
    "Coal Consumption": px.colors.sequential.Greys,
    "Renewables": px.colors.sequential.Blues,
    "Gas Consumption": px.colors.sequential.Oranges,
    "Carbon Intensity": px.colors.sequential.Reds,
    "Primary Energy Consumption": px.colors.sequential.YlGnBu,
}

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.H3("World Energy Dashboard", className="text-light"),
            html.Hr(),
            html.Label("Metric", className="text-light"),
            dcc.Dropdown(
                id="metric-dropdown",
                options=[{"label": key, "value": key} for key in datasets.keys()],
                value="Energy Use Per Person",
                placeholder="Select a metric",
            ),
            html.Br(),
            html.Label("Year", className="text-light"),
            dcc.Slider(
                id="year-slider",
                min=1970,
                max=2020,
                step=1,
                value=2020,
                marks={year: str(year) for year in range(1970, 2021, 5)},
            ),
            html.Br(),
            html.Label("Data Source", className="text-light"),
            html.P(
                "Data used in this dashboard comes from reliable energy datasets such as Our World in Data.",
                className="text-light",
            ),
            html.A("Learn more", href="https://ourworldindata.org", target="_blank", className="text-light"),
        ], width=3, className="bg-dark p-4"),
        # Map and Controls
        dbc.Col([
            html.H4("3D Energy Distribution by Country", className="text-center"),
            dcc.Graph(id="3d-globe"),
        ], width=9),
    ]),
])

# Callback to update the 3D globe visualization
@app.callback(
    Output("3d-globe", "figure"),
    [Input("metric-dropdown", "value"),
     Input("year-slider", "value")]
)
def update_globe(selected_metric, selected_year):
    # Get the dataset
    dataset = datasets[selected_metric]
    dataset = dataset.rename(columns={"entity": "country", "code": "ISO_A3"})

    # Filter dataset for the selected year
    year_data = dataset[dataset["year"] == selected_year]

    # Select the metric to visualize
    metric = [col for col in year_data.columns if col not in ["country", "year", "ISO_A3"]][0]

    # Generate the 3D globe visualization
    fig = px.choropleth(
        year_data,
        locations="ISO_A3",
        color=metric,
        hover_name="country",
        title=f"{selected_metric} in {selected_year}",
        color_continuous_scale=color_scales[selected_metric],
        projection="orthographic",  # Create the 3D globe effect
    )

    # Customize the globe appearance
    fig.update_geos(
        showcountries=True,
        countrycolor="white",
        showcoastlines=True,
        coastlinecolor="white",
        showocean=True,
        oceancolor="lightblue",
        showland=True,
        landcolor="gray",
    )

    # Layout adjustments
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        template="plotly_white",
        coloraxis_colorbar=dict(title=metric.replace("_", " ").title()),
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

if __name__ == "__main__":
    # Generate a static HTML file for GitHub Pages
    fig = update_globe("Energy Use Per Person", 2020)  # Default metric and year
    fig.write_html("index.html")  # Save as index.html for GitHub Pages
    print("Static HTML file saved as 'index.html'")
