import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


app = dash.Dash()

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' +
                 'master/csse_covid_19_data/csse_covid_19_time_series/' +
                 'time_series_covid19_confirmed_global.csv'
                )

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div([
    dcc.Graph(
        id='infected-vs-time',
        figure={
            'data': [
               
            ],
            'layout': go.Layout(
               
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
