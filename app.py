import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px

# Load the processed data
df = pd.read_csv('data/processed_data.csv')

# Convert date to datetime format
df['date'] = pd.to_datetime(df['date'])

# Sort data by date
df = df.sort_values(by='date')

# Define button options
region_options = [
    {'label': 'North', 'value': 'north'},
    {'label': 'East', 'value': 'east'},
    {'label': 'South', 'value': 'south'},
    {'label': 'West', 'value': 'west'},
    {'label': 'All', 'value': 'all'}
]

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(style={'padding': '20px', 'backgroundColor': '#f2f2f2', 'fontFamily': 'Roboto, sans-serif'}, children=[
    html.H1(children='Pink Morsel Sales Visualizer', style={
        'textAlign': 'center', 
        'color': '#333333',
        'fontSize': '36px',
        'fontWeight': 'bold',
        'marginBottom': '30px'
    }),
    
    html.Div([
        html.Button(
            option['label'],
            id={'type': 'region-button', 'index': option['value']},
            n_clicks=0,
            style={
                'backgroundColor': '#1E90FF',
                'color': 'white',
                'border': 'none',
                'padding': '10px',
                'margin': '5px',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'fontWeight': '500'
            }
        ) for option in region_options
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    dcc.Store(id='selected-region', data='all'),  # Store the selected region
    dcc.Graph(id='sales-graph')
])

# Callback to update the stored region selection
@app.callback(
    Output('selected-region', 'data'),
    [Input({'type': 'region-button', 'index': dash.ALL}, 'n_clicks')],
    [State('selected-region', 'data')]
)
def update_region(n_clicks, current_region):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_region
    
    # Find which button was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_index = eval(button_id)['index']
    
    return button_index  # Store the new region selection

# Callback to update the graph
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('selected-region', 'data')]
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Pivot data for multiple regions
    pivoted_df = filtered_df.pivot(index='date', columns='region', values='sales')
    
    # Create the line chart
    fig = px.line(pivoted_df, title='Pink Morsel Sales Over Time')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Sales',
        plot_bgcolor='#f2f2f2',
        paper_bgcolor='#f2f2f2'
    )
    
    # Define custom colors
    custom_colors = {
        'north': 'green',
        'east': 'blue',
        'south': 'red',
        'west': 'orange'
       
    }
    
    # Apply custom colors
    for i, trace in enumerate(fig.data):
        region = trace.name
        if region in custom_colors:
            fig.data[i].line.color = custom_colors[region]
    
    # Price increase date
    price_increase_date = pd.to_datetime('2021-01-15')
    
    # Add a vertical rectangle for price increase
    fig.add_vrect(
        x0=price_increase_date - pd.Timedelta(days=1),
        x1=price_increase_date + pd.Timedelta(days=1),
        line_width=1,
        fillcolor="black",
        opacity=0.25,
        annotation_text="Price Increase",
        annotation_position="top left",
        annotation_font_size=16,
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
