import pandas as pd
import sqlite3
import sqlalchemy
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date, datetime

# Get Today's Date
current_date = date.today()

# Create df from seizure.db
engine = sqlalchemy.create_engine('sqlite:///seizure.db')
df = pd.read_sql("Seizures", engine)
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.date
frequency_count = df.groupby(['date'])['seizure_type'].value_counts().to_frame(name='frequency').reset_index()
# print(frequency_count.frequency.sum())



# Create the dash app to be render in flask
def create_dash_application(flask_app):

    # Styles
    DATEPICKER_STYLE = {
        'padding': "10px",
        'margin': "10px",
        'margin-left': "50px",
    }

    FIGS = {
        'border-radius': '25px',
        'border': '2px solid #ccc',
        'padding': "10px",
        'margin': "10px",
        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',

    }

    TOTALS = {
        'border-radius': '25px',
        'border': '2px solid #ccc',
        'padding': "10px",
        'padding-top': "20px",
        'margin': "10px",
        'margin-top': "20px",
        'margin-bottom': "20px",
        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
        'justify-content': 'center',
        'align-items': 'center',

    }

    #Components
    dash_app = dash.Dash(
        server=flask_app, name='Dashboard', url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[{'name': 'viewport',
                    'content': 'width=device-width, initial-scale=1.0'}]
    )

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("New Entry", href="https://matthewseizuretrackingapp.herokuapp.com/new-entry")),
            dbc.NavItem(dbc.NavLink("Calendar", href="https://matthewseizuretrackingapp.herokuapp.com/calendar")),
        ],
        brand="Dashboard",
        color="primary",
        dark=True,
    )

    totals = html.Div(
        [
            dbc.Alert([
                html.H1("Number of Seizures: "),
                html.H1(id='totals')
            ],
                color="light"),
        ],
    )

    download = html.Div(
        [
            dbc.Alert([html.H1("EXPORT")], color="light")
        ],

    )

    # App Layout: Bootstrap

    dash_app.layout = dbc.Container([
        dbc.Row([navbar]),
        dbc.Row([
            dbc.Col([
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    end_date_placeholder_text="End Date",
                    min_date_allowed=date(2000, 1, 1),
                    max_date_allowed=date(2100, 1, 1),
                    initial_visible_month=current_date,
                ),
            ], style=DATEPICKER_STYLE, width={'size': 3})
        ], justify='start'),

        dbc.Row([
            dbc.Col([
                totals
            ], style=TOTALS, xs=12, sm=12, md=12, lg=5, xl=5),
        ], justify='center'),

        dbc.Row([

            dbc.Col([
                dcc.Graph(id="frequency_fig")
            ], style=FIGS, xs=12, sm=12, md=12, lg=5, xl=5),


            dbc.Col([
                dcc.Graph(id="pie_fig"),
            ], style=FIGS, xs=12, sm=12, md=12, lg=5, xl=5)

        ], justify='around'),


    ])

    @dash_app.callback(
        Output('frequency_fig', 'figure'),
        [Input('my-date-picker-range', 'start_date'),
         Input('my-date-picker-range', 'end_date')]
    )
    def f_figupdate(start_date, end_date):
        df = frequency_count
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        f_fig = px.bar(df,
                       x='date',
                       y='frequency',
                       color='seizure_type',
                       title="Frequency of Seizures")

        f_fig.update_layout(xaxis_title='Days of the Month',
                            yaxis_title='Number of seizures')
        return f_fig

    @dash_app.callback(
        Output('pie_fig', 'figure'),
        [Input('my-date-picker-range', 'start_date'),
         Input('my-date-picker-range', 'end_date')]
    )
    def p_figupdate(start_date, end_date):
        df = frequency_count
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        seizure_type_count = df.seizure_type.value_counts()

        p_fig = px.pie(df,
                       labels=seizure_type_count.index,
                       values=seizure_type_count.values,
                       title="Percentage of Seizures by Type",
                       names=seizure_type_count.index,
                       hole=0.4,
                       )

        p_fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')

        return p_fig

    @dash_app.callback(
        Output(component_id='totals', component_property='children'),
        [Input('my-date-picker-range', 'start_date'),
         Input('my-date-picker-range', 'end_date')]
    )
    def total_update(start_date, end_date):
        df = frequency_count
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        total_number = df.frequency.sum()
        return f'{total_number}'

    return dash_app
