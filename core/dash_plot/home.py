from dash import html, dcc, Input, Output, State
from flask import session
from .core import create_graph as cg
from core.base.dach_bd import Data_Base_Dash
import numpy as np
import pandas as pd


# Layout для защищенной страницы
home_layout = html.Div(id="protected-page-content")

# Callback для проверки авторизации

def render_protected_page(pathname):
    if not session.get('logged_in'):  # Если пользователь не авторизован
        return html.Div([
            html.H3("403 - Доступ запрещен"),
            html.Div("Вы не авторизованы для доступа к этой странице.", style={"color": "red"}),
            dcc.Link("Войти", href="/")
        ])
        
    return html.Div([
            html.Div([
                html.Div(children=[
                    
                ], style={'display': 'flex',
                        'width': '100%',
                        'background-color': 'black',
                        'justify-content': 'center'}),
                html.Div(children=[
                    html.Div(children=[html.Img(src='assets/icons8-money-100.png', alt='image'),],
                             )
                ], style={'display': 'flex',
                        'width': '100%',
                        'justify-content': 'center'}),
                html.Div(children=[
                    html.Div(children=[
                            dcc.Link(children=[
                                html.Img(src='assets/icons8-exit-50.png', alt='image')
                            ], href="/logout")]
                             , style={'padding-right':'1%'})
                    
                ], style={'display': 'flex',
                        'width': '100%',
                        'justify-content': 'right'}),
                
            ], style={'display': 'flex',
                    'background-color': 'black',
                    'justify-content': 'center',
                    'align-items': 'center',}),
            
            html.H3(f"Добро пожаловать!", style={"textAlign": "center"}),
            
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(options=np.sort(Data_Base_Dash().get_date_transaction_dash(session['username']).T[0]),
                                    value = np.sort(Data_Base_Dash().get_date_transaction_dash(session['username']).T[0])[-1],
                                    id='date_drop_down_pie'),
                        ], 
                        id='Filter', 
                        style={'width':'20%'}),
                    html.Div([
                        html.Div([
                            html.Div(
                                id="info-container-per-month",
                                style={
                                    'border': '2px solid black',
                                    'borderRadius': '5px',
                                    'padding': '10px',
                                    'backgroundColor': '#f5f5f5',
                                    'fontSize': '20px',
                                    'textAlign': 'center',
                                    'height': '18%'
                                }
                            ),
                            html.Div(children=[
                                html.Div(id="div_pie_plot", style={"textAlign": "center"})
                            ]),
                        ], style={'display':'flex', 'justify-content': 'center'}),
                        html.Div(children=[
                            html.Div(id="div_bar_plot", style={"textAlign": "center"})
                        ])
                    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '80%'})
                    
                ], style={'display':'flex'}),
                
            ]),
            
            
        ])
    
    
        
def generate_plotly_div(data_time:str):
    
    if not session.get('logged_in'):  # Если пользователь не авторизован
        return '', '/login'
    
    pie_fig = cg.pie_plot_transaction(
                            telegram_id=session['username'],
                            date_add=data_time)
    
    return dcc.Graph(figure=pie_fig), ''

def generate_plotly_div_bar(data_time:str):
    
    pie_fig = cg.bar_plot_transaction(
                            telegram_id=session['username'],
                            date_add=None)
    
    return dcc.Graph(figure=pie_fig)

def generate_plate_info_(data_time:str):
    
    text = cg.plate_info_transaction_per_month(
                            telegram_id=session['username'],
                            date_add=data_time)
    
    return html.Div([html.Div(text[0]), html.Div(text[1]), html.Div(text[2])], 
                    style={'display': 'flex', 
                            'flex-direction': 'column'})