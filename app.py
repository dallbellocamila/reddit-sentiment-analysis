import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json

# Load JSON data
with open('post_sentiment_per_state.json') as f:
    raw_data = json.load(f)
    data = json.loads(raw_data)

# Normalize state names in state_to_code
state_to_code = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
    "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
    "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH",
    "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC",
    "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN",
    "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY"
}
normalized_state_to_code = {state.replace(" ", "").lower(): code for state, code in state_to_code.items()}

map_data = pd.DataFrame({
    'State': [normalized_state_to_code[state.lower()] for state in data.keys()],
    'Dominant Sentiment': [data[state]['sentiment'] for state in data.keys()],
    'Average Sentiment': [data[state]['avg_sentiment'] for state in data.keys()]
})

# Define color mapping
color_discrete_map = {
    "positive": "#9AD3A2",  # light green
    "neutral": "#ADDFFF",   # light blue
    "negative": "#FFBDBF"   # light red
}


app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#FFFFFF",
        "padding": "20px"
    },
    children=[
        html.H1(
            "US Sentiment Analysis Dashboard",
            style={
                "textAlign": "center",
                "color": "#333",
                "fontSize": "40px",
                "marginBottom": "20px"
            }
        ),
        html.P(
            "This dashboard visualizes the dominant sentiment across U.S. states, derived from Reddit posts and comments. Data is analyzed from three weeks before and after the 2024 presidential election between Donald Trump and Kamala Harris. The dashboard highlights geographical trends in sentiment as observed through Reddit activity.",
            style={
                "textAlign": "center",
                "color": "#666",
                "fontSize": "18px",
                "marginBottom": "30px",
                "maxWidth": "80%",
                "marginLeft": "auto",
                "marginRight": "auto"
            }
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "space-between", "gap": "20px"},
            children=[
                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.H2(
                            "Before the Election",
                            style={"textAlign": "center", "color": "#333", "marginBottom": "10px"}
                        ),
                        dcc.Graph(
                            id='sentiment-map-before',
                            config={"displayModeBar": False}
                        )
                    ]
                ),
                html.Div(
                    style={"flex": "1"},
                    children=[
                        html.H2(
                            "After the Election",
                            style={"textAlign": "center", "color": "#333", "marginBottom": "10px"}
                        ),
                        dcc.Graph(
                            id='sentiment-map-after',
                            config={"displayModeBar": False}
                        )
                    ]
                )
            ]
        ),
        html.Div(
            style={
                "textAlign": "center",
                "color": "#666",
                "fontSize": "18px",
                "marginTop": "30px",
                "maxWidth": "80%",
                "marginLeft": "auto",
                "marginRight": "auto"
            },
            children=[
                html.H3("Methodology", style={"color": "#333"}),
                html.P(
                    "The sentiment analysis was performed on Reddit posts and comments sourced from state-specific subreddits. "
                    "Posts and comments were extracted from a three-week period before and after the election, processed using sentiment analysis algorithms, "
                    "and aggregated to determine the dominant sentiment (positive, neutral, or negative) in each state."
                ),
                html.P(
                    "Due to limitations in Reddit's API, it was not possible to extract the required information for 10 states. "
                    "These limitations include restrictions on API calls and the sheer volume of posts in specific state subreddits, "
                    "which exceeded the API's capacity to process within the designated three-week timeframes."
                )
            ]
        ),
        html.Footer(
            "Data Source: Analysis of Reddit Posts and Comments from State Subreddits",
            style={
                "textAlign": "center",
                "color": "#999",
                "fontSize": "14px",
                "marginTop": "20px"
            }
        )
    ]
)

# Callbacks for the maps
@app.callback(
    Output('sentiment-map-before', 'figure'),
    Input('sentiment-map-before', 'id')
)
def update_map_before(_):
    return generate_map("Dominant Sentiment Before the Election")


@app.callback(
    Output('sentiment-map-after', 'figure'),
    Input('sentiment-map-after', 'id')
)
def update_map_after(_):
    return generate_map("Dominant Sentiment After the Election")


# Function to generate a map
def generate_map(title):
    fig = px.choropleth(
        map_data,
        locations="State",
        locationmode="USA-states",
        color="Dominant Sentiment",
        hover_name="State",
        hover_data={"Dominant Sentiment": True, "Average Sentiment": ":.2f", 'State': False},
        scope="usa",
        color_discrete_map=color_discrete_map
    )
    fig.update_layout(
        title=title,
        title_x=0.5,
        geo=dict(lakecolor="lightblue"),
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial")
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
