import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import mysql.connector
import pandas as pd

my_connection = mysql.connector.connect(
    user="root", password="harshanand31", host="localhost", database="MusicTest"
)
cursor_object = my_connection.cursor()

# Sample list of preset SQL queries
preset_queries = [
    {
        "label": "List the number of songs by each artist with a duration of less than 5 minutes",
        "value": """select A.ArtistName, COUNT(S.TrackID) 
                    from Songs as S inner join Artists as A on S.ArtistID = A.ArtistID 
                    where S.Duration < 300
                    group by ArtistName;
                """,
    },
    {
        "label": "List record labels ordered by the number of streams of all produced songs in descending order",
        "value": """select R.LabelName, SUM(St.NumberOfStreams) as NumStreams
                    from RecordLabels as R inner join Songs as S on R.LabelID = S.LabelID
                    inner join Streams as St on S.TrackID = St.TrackID
                    group by R.LabelName
                    order by NumStreams DESC;
                """,
    },
    {
        "label": "List the top 10 artists with the greatest number of songs in descending order",
        "value": """select A.ArtistName, COUNT(C.TrackID) as NumSongs
                    from Compose as C inner join Artists as A on C.ArtistID = A.ArtistID
                    group by A.ArtistName
                    order by NumSongs desc
                    limit 10;
                """,
    },
    {
        "label": "List the number of albums recorded each year by a particular artist",
        "value": """select YEAR(A.ReleaseDate), COUNT(A.AlbumID)
                    from Albums as A inner join Artists as Ar on A.ArtistID = Ar.ArtistID
                    where Ar.ArtistName = '?'
                    group by YEAR(A.ReleaseDate);
                """,
    },
    {
        "label": "List the artist and album for which there are no songs with more than 10000 streams",
        "value": """select Ar.ArtistName, A.AlbumName
                    from Artists as Ar inner join Albums as A on Ar.ArtistID = A.ArtistID
                    where Ar.ArtistID in
                    (select S.ArtistID
                    from Streams as St inner join Songs as S on St.TrackID = S.TrackID
                    where NumberOfStreams > 10000); 
                """,
    },
    {
        "label": "List the genres sorted by the average number of streams per song in that genre",
        "value": """select G.Name, AVG(St.NumberOfStreams)
                    from Genres as G inner join Songs as S on G.GenreID = S.GenreID
                    inner join Streams as St on S.TrackID = St.TrackID
                    group by G.Name;
                """,
    },
    {
        "label": "List the number of songs per genre grouped by artist",
        "value": """select Ar.ArtistName, G.Name, COUNT(S.TrackID)
                    from Artists as Ar inner join Songs as S on Ar.ArtistID = S.ArtistID
                    inner join Genres as G on S.GenreID = G.GenreID
                    group by Ar.ArtistName, G.Name;
                """,
    },
    {
        "label": "List the number of albums where number of songs are greater than 10 for a given genre",
        "value": """select COUNT(B.AlbumID) FROM
                    (select A.AlbumID, COUNT(S.TrackID) as NumSongs
                    from Albums as A inner join Songs as S on A.AlbumID = S.AlbumID
                    inner join Genres as G on G.GenreID = S.GenreID
                    where G.Name = '?'
                    group by A.AlbumID
                    having NumSongs > 10) AS B;
                """,
    },
    {
        "label": "List the number of songs for an artist on different streaming platforms along with their average duration and number of streams",
        "value": """select P.PlatformName, COUNT(S.TrackID), AVG(S.Duration), SUM(St.NumberOfStreams)
                    from StreamingPlatforms as P inner join Streams as St on P.PlatformID = St.PlatformID
                    inner join Songs as S on S.TrackID = St.TrackID
                    inner join Artists as A on A.ArtistID = S.ArtistID
                    where A.ArtistName = '?'
                    group by P.PlatformName;
                """,
    },
    {
        "label": "List the number of albums released each year sorted in ascending order",
        "value": """select YEAR(ReleaseDate) as YearOfRelease, COUNT(AlbumID)
                    from Albums
                    group by YearOfRelease
                    order by COUNT(AlbumID);
                """,
    },
    {
        "label": "List the 5 youngest artists with greater than 15 songs and greater than 2 albums",
        "value": """select A.ArtistName, A.DOB, COUNT(C.TrackID) as NumSongs, COUNT(Al.AlbumID) as NumAlbums
                    from Artists as A inner join Compose as C on A.ArtistID = C.ArtistID
                    inner join Albums as Al on Al.ArtistID = A.ArtistID
                    group by A.ArtistName, A.DOB
                    having NumSongs > 15 and NumAlbums > 2
                    order by A.DOB DESC
                    limit 5;
                """,
    },
    {
        "label": "List the number of songs which have greater than or equal to 3 artists from each record label, with their average number of streams",
        "value": """
                """,
    },
]

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"backgroundColor": "pink", "width": "100%", "height": "100vh"},
    children=[
        html.Br(),
        html.H1(
            "Music Database",
            style={
                "textAlign": "center",
                "color": "black",
            },
        ),
        html.Br(),
        html.Div(
            style={
                "display": "flex",
                "flex-direction": "column",
                "alignItems": "center",
                "backgroundColor": "#F9F6EE",
                "width": "60%",
                "border": "3px solid",
                "border-radius": "16px",
                "margin": "auto",
            },
            children=[
                html.Label(
                    "Please select the SQL query:",
                    style={
                        "margin-top": "20px",
                    },
                ),
                html.Br(),
                html.Div(
                    children=[
                        dcc.RadioItems(
                            id="query-radio",
                            options=[
                                {"label": q["label"], "value": q["value"]}
                                for q in preset_queries
                            ],
                            value=None,
                            style={"margin-bottom": "20px"},
                        )
                    ]
                ),
                html.Div(
                    id="input-div",
                    children=[
                        dcc.Input(
                            id="user-input",
                            placeholder="Enter input",
                            style={"margin": "auto"},
                        )
                    ],
                    style={"display": "none"},
                ),
                html.Div(
                    children=[
                        html.Button(
                            "Run",
                            id="submit-button",
                            n_clicks=0,
                            style={
                                "height": "50px",
                                "width": "100px",
                                "backgroundColor": "black",
                                "margin": "20px",
                                "border-radius": "10px",
                                "color": "white",
                            },
                        ),
                        html.Button(
                            "Reset",
                            id="reset-button",
                            n_clicks=0,
                            style={
                                "height": "50px",
                                "width": "100px",
                                "backgroundColor": "black",
                                "margin": "20px",
                                "border-radius": "10px",
                                "color": "white",
                            },
                        ),
                    ],
                    style={"display": "flex", "justifyContent": "center"},
                ),
                html.Br(),
                html.Br(),
                # Div to output graphs when generated - gets updated when button clicked
                html.Div(
                    id="output-div",
                    style={
                        "color": "black",
                        # "height": "100vh"
                    },
                ),
            ],
        ),
    ],
)


@app.callback(Output("input-div", "style"), [Input("query-radio", "value")])
def display_input_field(selected_query):
    # Display input field only for specific query
    if selected_query and "?" in selected_query:
        return {"display": "block", "margin-buttom": "20px"}
    else:
        return {"display": "none"}


def run_query(query, input=None):
    if input:
        query = query.replace("?", input)
        print(query)
        cursor_object.execute(query)
    else:
        cursor_object.execute(query)

    res = cursor_object.fetchall()
    column_names = [column[0] for column in cursor_object.description]
    return res, column_names


# Callback to display the selected query
@app.callback(
    Output("output-div", "children"),
    [Input("submit-button", "n_clicks"), Input("reset-button", "n_clicks")],
    [State("query-radio", "value"), State("user-input", "value")],
)
def display_query(submit_clicks, reset_clicks, selected_query, user_input):
    # Check which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Display the selected query if Submit button was clicked
    if button_id == "submit-button":
        if selected_query:
            output, columns = run_query(selected_query, user_input)
            df = pd.DataFrame(output, columns=columns)

            # Create DataTable to display the result
            return html.Div(
                style={"padding": "20px"},
                children=[
                    html.H4("Result of the SQL Query:"),
                    dash_table.DataTable(
                        id="table",
                        columns=[{"name": col, "id": col} for col in df.columns],
                        data=df.to_dict("records"),
                    ),
                ],
            )
            #

        else:
            return html.Div("Please select a query first.", style={"padding": "20px"})

    # Clear the output if Reset button was clicked
    elif button_id == "reset-button":
        return html.Div()


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
