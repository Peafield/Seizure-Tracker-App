import pandas as pd
import sqlite3
import sqlalchemy
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

engine = sqlalchemy.create_engine('sqlite:///seizure.db')
df = pd.read_sql("Seizures", engine)

df['date'] = pd.to_datetime(df['date'])
df['date_column'] = df['date'].dt.date
df = df[(df['date'] > '2021-10-01') & (df['date'] <= '2021-10-28')]

# print(df.groupby(['date_column'])['seizure_type'].value_counts())
# df["freq"] = df.groupby(['seizure_type', 'date_column'])['date_column'].transform("count")

frequency_count = df.groupby(['date_column'])['seizure_type'].value_counts().to_frame(name='frequency').reset_index()

print(frequency_count)

frequency_fig = px.bar(frequency_count,
                       x='date_column',
                       y='frequency',
                       color='seizure_type',
                       title="WIN?")

frequency_fig.update_layout(xaxis_title='Days of the Month',
                            yaxis_title='Number of seizures')
frequency_fig.show()

seizure_type_count = df.seizure_type.value_counts()
#

pie_fig = px.pie(labels=seizure_type_count.index,
             values=seizure_type_count.values,
             title="Percentage of Seizures by Type in October",
             names=seizure_type_count.index,
             hole=0.4,
             )

pie_fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')

pie_fig.show()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    dbc.Button("Success", color="success", className="mr-1")
)

if __name__ == "__main__":
    app.run_server()
