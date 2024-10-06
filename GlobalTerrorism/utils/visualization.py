import plotly.express as px
import plotly.graph_objects as go

def create_yearly_trend_chart(df):
    """
    Create a line chart showing the yearly trend of attacks.
    """
    yearly_counts = df.groupby(df['iyear'].dt.year).size().reset_index(name='count')
    fig = px.line(yearly_counts, x='iyear', y='count', 
                  title='Yearly Trend of Terrorist Attacks',
                  labels={'iyear': 'Year', 'count': 'Number of Attacks'})
    return fig

def create_top_n_bar_chart(df, column, n=10, title=None):
    """
    Create a bar chart showing the top N categories for a given column.
    """
    top_n = df[column].value_counts().head(n)
    fig = px.bar(top_n, x=top_n.index, y=top_n.values, 
                 title=title or f'Top {n} {column}',
                 labels={column: '', 'value': 'Count'})
    return fig

def create_heatmap(df, x_col, y_col, z_col):
    """
    Create a heatmap visualization.
    """
    heatmap_data = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='mean')
    fig = px.imshow(heatmap_data, 
                    labels=dict(x=x_col, y=y_col, color=z_col),
                    title=f'{z_col} Heatmap by {x_col} and {y_col}')
    return fig

def create_scatter_map(df, lat_col, lon_col, size_col=None, color_col=None, hover_name=None):
    """
    Create a scatter map visualization.
    """
    fig = px.scatter_mapbox(df, lat=lat_col, lon=lon_col, 
                            size=size_col, color=color_col, hover_name=hover_name,
                            zoom=1, mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def create_stacked_area_chart(df, x_col, y_col, color_col):
    """
    Create a stacked area chart.
    """
    fig = px.area(df, x=x_col, y=y_col, color=color_col, 
                  labels={x_col: '', y_col: 'Count'},
                  title=f'Stacked Area Chart of {y_col} by {color_col}')
    return fig