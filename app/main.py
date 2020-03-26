import pandas as pd
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server = app, url_base_pathname = '/')

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/' +
                 'master/csse_covid_19_data/csse_covid_19_time_series/' +
                 'time_series_covid19_confirmed_global.csv'
                )

dash_app.css.append_css({"external_url" : "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

countries = df['Country/Region'].unique()

dash_app.layout = html.Div(
    [
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
            'annotations': [{
                'x': 0.1, 'y': 1, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }


@dash_app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')]
    )
def update_timeseries(dropdown_value):
    dff = df[df['Country/Region'] == dropdown_value]

    date = [col for col in dff.iloc[:,4:].head()]
    dff = pd.melt(dff, id_vars=['Country/Region'], value_vars=date)

    title = '<b>{}</b>'.format(dropdown_value)
    return create_time_series(dff, title)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
