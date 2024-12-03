import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Load datasets (assuming cleaned files are in the "cleaned_datasets/" directory)
dataset_files = {
    "Energy Use Per Person": "cleaned_datasets/energy_use_per_person_cleaned.csv",
    # Add other datasets here if needed for line charts
}

datasets = {name: pd.read_csv(file) for name, file in dataset_files.items()}

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    html.H1("Energy Trends Over Time", className="text-center my-4"),
    dbc.Row([
        dbc.Col([
            html.Label("Select Dataset"),
            dcc.Dropdown(
                id="line-dataset-dropdown",
                options=[{"label": name, "value": name} for name in datasets.keys()],
                value=list(datasets.keys())[0],  # Default dataset
            ),
        ], width=3),
        dbc.Col([
            html.Label("Select Countries"),
            dcc.Dropdown(
                id="line-country-dropdown",
                multi=True,
                placeholder="Select countries",
            ),
        ], width=3),
        dbc.Col([
            html.Label("Select Metric"),
            dcc.Dropdown(
                id="line-metric-dropdown",
                placeholder="Select a metric",
            ),
        ], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="line-chart"),
        ], width=12),
    ]),
], fluid=True)


# Update country and metric dropdowns based on dataset
@app.callback(
    [Output("line-country-dropdown", "options"),
     Output("line-metric-dropdown", "options")],
    Input("line-dataset-dropdown", "value")
)
def update_line_dropdowns(selected_dataset):
    dataset = datasets[selected_dataset]
    country_options = [{"label": country, "value": country} for country in dataset["entity"].unique()]
    metric_options = [{"label": col, "value": col} for col in dataset.columns if col not in ["entity", "year", "code"]]
    return country_options, metric_options


# Generate line chart with animation
@app.callback(
    Output("line-chart", "figure"),
    [Input("line-dataset-dropdown", "value"),
     Input("line-country-dropdown", "value"),
     Input("line-metric-dropdown", "value")]
)
def update_line_chart(selected_dataset, selected_countries, selected_metric):
    if not all([selected_dataset, selected_countries, selected_metric]):
        return px.line(title="Please select a dataset, countries, and metric.")

    dataset = datasets[selected_dataset]
    filtered_data = dataset[dataset["entity"].isin(selected_countries)]

    fig = px.line(
        filtered_data,
        x="year",
        y=selected_metric,
        color="entity",
        line_group="entity",
        markers=True,
        title=f"{selected_metric} Trends Over Time",
        labels={"year": "Year", selected_metric: selected_metric.replace("_", " ").title()},
    )
    fig.update_layout(template="plotly_white", xaxis_title="Year",
                      yaxis_title=selected_metric.replace("_", " ").title())
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)