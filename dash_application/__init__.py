import pandas as pd
import sqlite3
import sqlalchemy
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date, datetime

# current_date = date.today()
#
# engine = sqlalchemy.create_engine('sqlite:///seizure.db')
# df = pd.read_sql("Seizures", engine)
#
# df['date'] = pd.to_datetime(df['date'])
# df['date'] = df['date'].dt.date
#
# frequency_count = df.groupby(['date'])['seizure_type'].value_counts().to_frame(name='frequency').reset_index()
#
# frequency_count.set_index('date', inplace=True)
#
# # TODO I think I need to fill in the missing dates? Or there is a conflict between the datetime objects and the input strings?
#
# frequency_fig = px.bar(frequency_count,
#                        x=frequency_count.index,
#                        y='frequency',
#                        color='seizure_type',
#                        title="Frequency of Seizure's per day")
#
# frequency_fig.update_layout(xaxis_title='Days of the Month',
#                             yaxis_title='Number of seizures')
#
# seizure_type_count = df.seizure_type.value_counts()
#
# pie_fig = px.pie(labels=seizure_type_count.index,
#                  values=seizure_type_count.values,
#                  title="Percentage of Seizures by Type in October",
#                  names=seizure_type_count.index,
#                  hole=0.4,
#                  )
#
# pie_fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
#
#
# # pie_fig.show()

def create_dash_application(flask_app):
    dash_app = dash.Dash(
        server=flask_app, name='Dashboard', url_base_pathname='/dashboard/',
    )

    dash_app.layout = html.Div([
        html.H6("Change the value in the text box to see callbacks in action!"),
        html.Div([
            "Input: ",
            dcc.Input(id='my-input', value='initial value', type='text')
        ]),
        html.Br(),
        html.Div(id='my-output'),

    ])

    @dash_app.callback(
        Output(component_id='my-output', component_property='children'),
        Input(component_id='my-input', component_property='value')
    )
    def update_output_div(input_value):
        return 'Output: {}'.format(input_value)

    return dash_app


    # dash_app = dash.Dash(__name__,
    #                      server=flask_app, name="Dashboard", url_base_pathname='/dashboard/',
    #                      external_stylesheets=[dbc.themes.BOOTSTRAP],
    #                      meta_tags=[{'name': 'viewport',
    #                                  'content': 'width=device-width, initial-scale=1.0'}]
    #                      )
    #
    # # App Layout: Bootstrap
    #
    # dash_app.layout = dbc.Container([
    #     dbc.Row([
    #         dbc.Col(html.H1("Seizure Report Dashboard",
    #                         className="text-center text-primary mb-4"),
    #                 width=12),
    #     ]),
    #
    #     dbc.Row([
    #         dbc.Col([
    #             dcc.DatePickerRange(
    #                 id='my-date-picker-range',
    #                 end_date_placeholder_text="End Date",
    #                 min_date_allowed=date(2000, 1, 1),
    #                 max_date_allowed=date(2100, 1, 1),
    #                 initial_visible_month=current_date,
    #             ),
    #
    #             dcc.Graph(id="frequency_fig"),
    #             # Can only have a maximum of 12 cols including offsets etc.
    #             # Order determines int the order of rendered components
    #
    #         ], width={'size': 5, 'offset': 1, 'order': 1}),
    #
    #     ], justify='around'),
    #
    #     dbc.Row([
    #         dbc.Col([
    #             dcc.Graph(id="pie_fig",
    #                       figure=pie_fig),
    #         ], width={'size': 5, 'offset': 0, 'order': 2})
    #     ], justify='around'),
    # ])
    #
    # # Call back
    #
    # # @app.callback(
    # #     Output('frequency_fig', 'figure'),
    # #     [Input('my-date-picker-range', 'start_date'),
    # #      Input('my-date-picker-range', 'end_date')]
    # # )
    # # def update_output():
    # #     pass
    #
    # if __name__ == "__main__":
    #     dash_app.run_server(debug=True)
    #
    # return dash_app
