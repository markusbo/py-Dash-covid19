import pandas as pd
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


app = flask.Flask(__name__)
dash_app = dash.Dash(
    __name__, 
    server = app, 
    url_base_pathname = '/',
    external_stylesheets=[dbc.themes.CERULEAN]
    )

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' +
                 'master/csse_covid_19_data/csse_covid_19_time_series/' +
                 'time_series_covid19_confirmed_global.csv'
                )

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

countries = df['Country/Region'].unique()

growthfactor = "test"

dash_app.layout = html.Div(
    [
        html.Div(
            [
                html.H1('Covid-19 Infected graph')
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in countries],
                    value='Sweden',
                    #multi=True, 
                    placeholder='Filter by country...'
                )
            ]
        ),
        html.Div(
            [
                html.P(id='growthf')
            ]
        ),
        html.Div(
            [
                dcc.Graph(id='x-time-series'),
            ],
        )
    ]
)

def create_time_series(dff, title):
    return {
        'data': [dict(
            #x=dff['variable'],
            x=dff[dff['value']>0]['variable'],
            #y=dff['value'],
            y=dff[dff['value']>0]['value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 500,
            'margin': {'l': 50, 'b': 70, 'r': 50, 't': 50},
            'title' : title,
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }


@dash_app.callback(
    [dash.dependencies.Output('x-time-series', 'figure'),
    dash.dependencies.Output('growthf', 'children')],
    [dash.dependencies.Input('dropdown', 'value')]
    )
def update_timeseries(dropdown_value):
    global growthfactor
    dff = df[df['Country/Region'] == dropdown_value]

    date = [col for col in dff.iloc[:,4:].head()]
    dff = pd.melt(dff, id_vars=['Country/Region'], value_vars=date)

    title = '<b>{}</b>'.format(dropdown_value)
    growthfactor = (dff['value'].iloc[-1] - dff['value'].iloc[-2]) / (dff['value'].iloc[-3] - dff['value'].iloc[-4])
    return create_time_series(dff, title), ("Current Growth factor: " + str(round(growthfactor, 2)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
