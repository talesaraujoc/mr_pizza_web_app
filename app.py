from dash import dash, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


import plotly as plt
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# Servidor
load_figure_template("minty")

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])


# DataFrame =================

from globals import *

# Pré-layout ================
card_faturamento = dbc.Card([
        dbc.CardImg(src="/assets/money_up.png", top=True, style={'max-width':'58px','max-height':'58px', 'padding-left':'20px', 'padding-top':'20px'}),
        
        dbc.CardBody([
                html.H4("Faturamento", className="card-title"),
                html.H2(faturamento)
            ]),
    ],
    style={"width": "90%", 'height':'100%'})

card_n_pedidos = dbc.Card([
        dbc.CardImg(src="/assets/money_up.png", top=True, style={'max-width':'58px','max-height':'58px', 'padding-left':'20px', 'padding-top':'20px'}),
        
        dbc.CardBody([
                html.H4("N° Pedidos", className="card-title"),
                html.H2(n_pedidos)
            ]),
    ],
    style={"width": "90%", 'height':'100%'})

card_n_pizzas = dbc.Card([
        dbc.CardImg(src="/assets/money_up.png", top=True, style={'max-width':'58px','max-height':'58px', 'padding-left':'20px', 'padding-top':'20px'}),
        
        dbc.CardBody([
                html.H4("Pizzas Vendidas", className="card-title"),
                html.H2(n_pizzas_vendidas)
            ]),
    ],
    style={"width": "90%", 'height':'100%'})

card_avg_dia = dbc.Card([
        dbc.CardImg(src="/assets/money_up.png", top=True, style={'max-width':'58px','max-height':'58px', 'padding-left':'20px', 'padding-top':'20px'}),
        
        dbc.CardBody([
                html.H4("Faturamento/dia", className="card-title"),
                html.H2(avg_dia)
            ]),
    ],
    style={"width": "90%", 'height':'100%'})

fig_grafico_vendas_mes = px.bar(data_frame=faturamento_by_mes, x='month_extenso', y='total_price', title="Faturamento Mensal", text_auto='.2s')

# Layout    =================
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
                    dbc.Row([
                        dbc.Col([dbc.Card(card_faturamento, color="primary")], lg=3), 
                        dbc.Col([dbc.Card(card_n_pedidos, color="primary")], lg=3), 
                        dbc.Col([dbc.Card(card_n_pizzas, color="primary")], lg=3), 
                        dbc.Col([dbc.Card(card_avg_dia, color="primary")], lg=3)
                        ]), 
                    
                    dbc.Row(dcc.Graph(figure=fig_grafico_vendas_mes, id='grafico-01-r2/c1/r2')), 
                    
                    dbc.Row([
                        dcc.Dropdown(options=lista_meses, value=lista_meses[0], id='dpd-01-lista_meses', style={'width':'50%'}),
                        html.Hr(style={'margin-top':'15px'}),
                        dcc.Graph(id='grafico-02-r2/c1/r3')
                        ])
                ], 
        lg=6),
        
        
        dbc.Col([
                dbc.Row([dbc.Col([
                                dcc.DatePickerSingle(
                                id='my-date-picker-single',
                                month_format='DD MM, YYYY',
                                min_date_allowed=date(2015, 1, 1),
                                max_date_allowed=date(2015, 12, 31),
                                date=date(2015, 7, 1)),
                                ], lg=2),
                         
                         dbc.Col([dcc.Graph(id='grafico-03-data')], lg=6),
                         
                         dbc.Col(dcc.Graph(id='grafico-04-pizza'), lg=4)
                         ]), 
                 
                dbc.Row(html.Div(id='table'))], 
        lg=6)
        
    ], style={'margin':'8px'})
])



# Callbacks =================
@app.callback(
    Output('grafico-02-r2/c1/r3', 'figure'),
    Input('dpd-01-lista_meses', 'value')
)
def update_grafico_02(mes_escolhido):
    df_mes_escolhido = df.loc[df['month_extenso']==mes_escolhido]
    df_mes_escolhido = df_mes_escolhido.groupby('day', sort=False).agg({'total_price':'sum'})
    df_mes_escolhido = df_mes_escolhido.reset_index()
    
    fig = px.line(data_frame=df_mes_escolhido, x='day', y='total_price')
    
    return fig

@app.callback(
    Output('grafico-03-data', 'figure'),
    Input('my-date-picker-single', 'date')
)
def mostrar_data(data):
    date_object = date.fromisoformat(data)
    dia = date_object.day
    mes = date_object.month
    
    df_analise_dia = df.loc[(df['day']==dia) & (df['month']==mes)]
    df_analise_dia = df_analise_dia.groupby('hour').agg({'total_price':'sum'})
    df_analise_dia = df_analise_dia.reset_index()
    
    fig = px.bar(data_frame=df_analise_dia, x='hour', y='total_price')
    
    return fig

@app.callback(
    Output('grafico-04-pizza', 'figure'),
    Input('my-date-picker-single', 'date')
)
def update_pizza(data):
    date_object = date.fromisoformat(data)
    dia = date_object.day
    mes = date_object.month
    
    df_analise_dia = df.loc[(df['day']==dia) & (df['month']==mes)]
    
    fig = px.pie(data_frame=df_analise_dia, names='pizza_category', values='total_price', hole=.5)
    
    return fig
    
    
@app.callback(
    Output('table', 'children'),
    Input('my-date-picker-single', 'date')
)
def update_table(data):
    date_object = date.fromisoformat(data)
    dia = date_object.day
    mes = date_object.month
    
    df_analise_dia = df.loc[(df['day']==dia) & (df['month']==mes)]
    df_analise_dia = df_analise_dia.groupby('pizza_name').agg({'order_details_id':'count', 'quantity':'sum', 'total_price':'sum'})
    df_analise_dia = df_analise_dia.sort_values(by='total_price', ascending=False)
    df_analise_dia = df_analise_dia.reset_index()
    df_analise_dia = df_analise_dia.iloc[0:9]
    
    children = dash_table.DataTable(df_analise_dia.to_dict('records'), [{"name": i, "id": i} for i in df_analise_dia.columns])
    
    return children
    

# Servidor  =================
if __name__=='__main__':
    app.run_server(debug=False)
