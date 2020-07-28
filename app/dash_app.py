import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


from run import run_all


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

markdown_1 = """
# JobBuddy!  
_Search the skills that are in demand for your job_  
  
* type in a job title
* press submit
"""

markdown_2 = """

## How does it work?  

![Diagram](https://i.imgur.com/DxlXxhh.png)
"""


#app = dash.Dash()

app.layout = html.Div([
 
    dbc.Container(
    #dbc.Alert("JobBuddy!", color="primary"),
    dcc.Markdown(markdown_1),    
    ),
    

    
    dbc.Container(
    dbc.Input(id='input-1-state', type='text', placeholder='Search job',
             style = {'width':'50%'}),
    )
        ,
    dbc.Container(
    dbc.Button(id='submit-button-state', n_clicks=0, children='Submit', color='primary'),
    ),

    
    dbc.Container(
    dbc.Spinner(html.Div(id="loading-output",
                        children = [html.Div(id='output-state')]), 
                        color='primary'),
                ),
 
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Container(

    dcc.Markdown(markdown_2),    
    )
        ])



def generate_graph(input1, position, count_of_jobs):
    x=[i['y'] for i in input1]
    y=[i['label'] for i in input1]
    trace = go.Bar(x=x,y=y, orientation = 'h', cliponaxis=True)
    data = [trace]
    
    layout = go.Layout(barmode = 'overlay',
                        title = 'Top skills for "{0}" \n (out of {1} jobs)'.format(position,count_of_jobs ),
                        margin={'l': 150, 'b': 20, 't': 50, 'r': 20},
                        xaxis=dict(
                                showgrid=False,
                                zeroline=False,
                                showline=False,
                                ticks='',
                                showticklabels=True
                            ))
    
    return dcc.Graph(figure=go.Figure(data=data, layout=layout),             
                        style = {'float' : 'center',
                              'max-width':'100%',
                            'vertical-align':'middle'},
                        config={
                            'displayModeBar': False    },
                        id='grapha')

@app.callback(Output('loading-output', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value')])

def update_output(n_clicks, input1):
    if input1:
        print('running')
        result, position, count_of_jobs = run_all(input1)
    
        return generate_graph(result, position, count_of_jobs)
    else:
        return ''

    



    
    
    
#app.css.append_css({
#   'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})

#application = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port = 8080)
    #app.run(debug=True, port=8080)
