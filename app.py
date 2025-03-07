import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load the processed data
df  = pd.read_csv("data/processed_data.csv")

# convert data to datetime
df['date'] = pd.to_datetime(df['date'])

#sort the data by date
df =  df.sort_values(by = 'date')

# Create a Dash app
app = dash.Dash(__name__)

# Create a line figure with a vertical line at the price increase date
fig = px.line(df, x='date', y='sales', color='region', title='Pink Morsel Sales Over Time')
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Sales',
)

# Convert price increase date to epoch time
price_increase_date = pd.to_datetime('2021-01-15')
price_increase_epoch = int(price_increase_date.timestamp() * 1000)

# Add a vertical line for the price increase date
fig.add_vrect(
    x0=price_increase_epoch - 86400000,  # One day before
    x1=price_increase_epoch + 86400000,  # One day after
    line_width=0,
    fillcolor="red",
    opacity=0.2,
    annotation_text="Price Increase",
    annotation_position="top left",
    annotation_font_size=16,
)

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1(children='Pink Morsel Sales Visualizer', style={'textAlign': 'center', 'color': 'blue','text':'bold'}),
        html.P(children='This dashboard shows the sales of Pink Morsel over time, with a vertical line indicating a price increase on January 15, 2021.', style={'textAlign': 'center'}),
        
        dcc.Graph(
            id='sales-graph',
            figure=fig
        )
    ],
    style={'width': '80%', 'margin': 'auto'}
)

if __name__ == '__main__':
    app.run_server(debug=True)