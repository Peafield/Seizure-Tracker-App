import pandas as pd
import sqlite3
import sqlalchemy
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date, datetime

current_date = date.today()

engine = sqlalchemy.create_engine('sqlite:///seizure.db')
df = pd.read_sql("Seizures", engine)

df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.date

frequency_count = df.groupby(['date'])['seizure_type'].value_counts().to_frame(name='frequency').reset_index()

# frequency_count.set_index('date', inplace=True)

# TODO I think I need to fill in the missing dates? Or there is a conflict between the datetime objects and the input strings?

# frequency_fig = px.bar(frequency_count,
#                        x=frequency_count.index,
#                        y='frequency',
#                        color='seizure_type',
#                        title="Frequency of Seizure's per day")
#
# frequency_fig.update_layout(xaxis_title='Days of the Month',
#                             yaxis_title='Number of seizures')

seizure_type_count = df.seizure_type.value_counts()

pie_fig = px.pie(labels=seizure_type_count.index,
                 values=seizure_type_count.values,
                 title="Percentage of Seizures by Type in October",
                 names=seizure_type_count.index,
                 hole=0.4,
                 )

pie_fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')


# pie_fig.show()

def create_dash_application(flask_app):
    dash_app = dash.Dash(
        server=flask_app, name='Dashboard', url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        meta_tags=[{'name': 'viewport',
                    'content': 'width=device-width, initial-scale=1.0'}]
    )

    # App Layout: Bootstrap

    dash_app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Seizure Report Dashboard",
                            className="text-center text-primary mb-4"),
                    width=12),
        ]),

        dbc.Row([
            dbc.Col([
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    end_date_placeholder_text="End Date",
                    min_date_allowed=date(2000, 1, 1),
                    max_date_allowed=date(2100, 1, 1),
                    initial_visible_month=current_date,
                ),
                html.Div(id='output-container-date-picker-range'),

                dcc.Graph(id="frequency_fig")
                # Can only have a maximum of 12 cols including offsets etc.
                # Order determines int the order of rendered components

            ], width={'size': 5, 'offset': 1, 'order': 1}),

        ], justify='around'),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id="pie_fig",
                          figure=pie_fig),
            ], width={'size': 5, 'offset': 0, 'order': 2})
        ], justify='around'),
    ])

    @dash_app.callback(
        Output('frequency_fig', 'figure'),
        [Input('my-date-picker-range', 'start_date'),
         Input('my-date-picker-range', 'end_date')]
    )
    def figupdate(start_date, end_date):
        df = frequency_count
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df = df[(df['date'] > start_date) & (df['date'] < end_date)]
        f_fig = px.bar(df,
                       x='date',
                       y='frequency',
                       color='seizure_type',
                       title="Frequency of Seizure's per day")

        f_fig.update_layout(xaxis_title='Days of the Month',
                                    yaxis_title='Number of seizures')
        return f_fig

    return dash_app
