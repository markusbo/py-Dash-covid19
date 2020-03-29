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

dfInf = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' +
                 'master/csse_covid_19_data/csse_covid_19_time_series/' +
                 'time_series_covid19_confirmed_global.csv'
                )

dfDeath = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' +
                 'master/csse_covid_19_data/csse_covid_19_time_series/' +
                 'time_series_covid19_deaths_global.csv'
                )

dfRec = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' +
                 'master/csse_covid_19_data/csse_covid_19_time_series/' +
                 'time_series_covid19_recovered_global.csv'
                )

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

countries = dfInf['Country/Region'].unique()

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
            ], style={'width':150}
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

def create_time_series(dffInf, dffDeath, dffRec, title):
    return {
        'data': [
            dict(
                #x=dfInff['variable'],
                x=dffInf[dffInf['value']>0]['variable'],
                #y=dfInff['value'],
                y=dffInf[dffInf['value']>0]['value'],
                mode='lines+markers',
                name='Infected'
            ),
            dict(
                #x=dffDeath['variable'],
                x=dffDeath[dffDeath['value']>0]['variable'],
                #y=dffDeath['value'],
                y=dffDeath[dffDeath['value']>0]['value'],
                mode='lines+markers',
                name='Deaths'
            ),
             dict(
                #x=dffRec['variable'],
                x=dffRec[dffRec['value']>0]['variable'],
                #y=dffRec['value'],
                y=dffRec[dffRec['value']>0]['value'],
                mode='lines+markers',
                name='Recovered'
            )
        ],
        'layout': {
            'height': 500,
            'margin': {'l': 50, 'b': 70, 'r': 50, 't': 50},
            'title' : title,
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

def set_date(dff):
    date = [col for col in dff.iloc[:,4:].head()]
    return (pd.melt(dff, id_vars=['Country/Region'], value_vars=date))

@dash_app.callback(
    [dash.dependencies.Output('x-time-series', 'figure'),
    dash.dependencies.Output('growthf', 'children')],
    [dash.dependencies.Input('dropdown', 'value')]
    )
def update_timeseries(dropdown_value):
    dffInf = set_date(dfInf[dfInf['Country/Region'] == dropdown_value].agg(['sum']))
    dffDeath = set_date(dfDeath[dfDeath['Country/Region'] == dropdown_value].agg(['sum']))
    dffRec = set_date(dfRec[dfRec['Country/Region'] == dropdown_value].agg(['sum']))

    title = '<b>{}</b>'.format(dropdown_value)
    growthfactor = (dffInf['value'].iloc[-1] - dffInf['value'].iloc[-2]) / (dffInf['value'].iloc[-3] - dffInf['value'].iloc[-4])
    return create_time_series(dffInf, dffDeath, dffRec, title), ("Current Infected Growth factor: " + str(round(growthfactor, 2)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
