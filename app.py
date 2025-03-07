import pandas as pd
import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

# Load the processed data
df = pd.read_csv('data/processed_data.csv')

# Convert date to datetime format
df['date'] = pd.to_datetime(df['date'])

# Sort data by date
df = df.sort_values(by='date')

# Define button options
regions = ['north', 'east', 'south', 'west', 'all']
region_options = [{'label': r.capitalize(), 'value': r} for r in regions]

# Initialize the Dash app
app = dash.Dash(__name__)

def get_button_style(selected, current):
    return {
        'backgroundColor': '#FFD700' if selected == current else '#1E90FF',
        'color': 'white',
        'border': 'none',
        'padding': '10px',
        'margin': '5px',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'fontSize': '16px',
        'fontWeight': '500'
    }

# Define the app layout
app.layout = html.Div(style={'padding': '20px', 'backgroundColor': '#121212', 'color': 'white', 'fontFamily': 'Roboto, sans-serif'}, children=[
    html.H1('Pink Morsel Sales Visualizer', style={'textAlign': 'center', 'color': 'white', 'fontSize': '36px', 'marginBottom': '30px'}),
    
    html.Div([
        html.Button(option['label'], id={'type': 'region-button', 'index': option['value']}, n_clicks=0)
        for option in region_options
    ], id='button-container', style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    dcc.Store(id='selected-region', data='all'),  # Store selected region
    dcc.Graph(id='sales-graph')
])

# Callback to update the stored region selection
@app.callback(
    Output('selected-region', 'data'),
    [Input({'type': 'region-button', 'index': dash.ALL}, 'n_clicks')],
    [State('selected-region', 'data')]
)
def update_region(n_clicks, current_region):
    if not ctx.triggered:
        return current_region
    
    button_id = ctx.triggered_id['index']
    return button_id  # Store the new region selection

# Callback to update button styles
@app.callback(
    Output('button-container', 'children'),
    [Input('selected-region', 'data')]
)
def update_button_styles(selected_region):
    return [
        html.Button(option['label'],
                    id={'type': 'region-button', 'index': option['value']},
                    n_clicks=0,
                    style=get_button_style(selected_region, option['value']))
        for option in region_options
    ]

# Callback to update the graph
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('selected-region', 'data')]
)
def update_graph(selected_region):
    filtered_df = df if selected_region == 'all' else df[df['region'] == selected_region]
    
    # Pivot data safely
    pivoted_df = filtered_df.pivot(index='date', columns='region', values='sales').reindex(columns=['north', 'east', 'south', 'west'], fill_value=0)
    
    fig = go.Figure()
    custom_colors = {'north': 'green', 'east': 'blue', 'south': 'red', 'west': 'orange'}
    line_styles = {'north': 'solid', 'east': 'dash', 'south': 'dot', 'west': 'dashdot'}
    
    for region in pivoted_df.columns:
        fig.add_trace(go.Scatter(
            x=pivoted_df.index, y=pivoted_df[region],
            mode='lines',
            name=region.capitalize(),
            line=dict(color=custom_colors.get(region, 'gray'), dash=line_styles.get(region, 'solid')),
            hovertemplate=f'<b>{region.capitalize()} Sales</b>: %{{y}}<extra></extra>'
        ))
    
    # Price increase annotation
    price_increase_date = pd.to_datetime('2021-01-15')
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
    
    fig.update_layout(
        title='Pink Morsel Sales Over Time',
        xaxis_title='Date',
        yaxis_title='Sales',
        plot_bgcolor='#121212',
        paper_bgcolor='#121212',
        font=dict(color='white')
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
