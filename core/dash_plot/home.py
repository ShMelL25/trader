from dash import html, dcc, Input, Output, State
from flask import session
from .core import create_graph as cg
from core.base.dach_bd import Data_Base_Dash


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
                    html.Div(children=[html.Img(src='assets/icons8-сумка-с-евро-80.png', alt='image'),],
                             style={'background-color': 'white',})
                ], style={'display': 'flex',
                        'width': '100%',
                        'justify-content': 'center'}),
                html.Div(children=[
                    html.Div(children=[
                            dcc.Link(children=[
                                html.Img(src='assets/icons8-выход-50.png', alt='image')
                            ], href="/logout")],
                            style={'background-color': 'white',})
                    
                ], style={'display': 'flex',
                        'width': '100%',
                        'justify-content': 'right'}),
                
            ], style={'display': 'flex',
                    'background-color': 'black',
                    'justify-content': 'center',
                    'align-items': 'center',}),
            
            html.H3(f"Добро пожаловать!", style={"textAlign": "center"}),
            
            html.Div([
                html.Div(children=[
                    dcc.Dropdown(options=Data_Base_Dash().get_date_transaction_dash(session['username']).T[0],
                            value = Data_Base_Dash().get_date_transaction_dash(session['username']).T[0][-1],
                            id='date_drop_down_pie'),
                    html.Div(id="div_pie_plot", style={"textAlign": "center"})
                ]),
                html.Div(children=[
                    html.Div(id="div_bar_plot", style={"textAlign": "center"})
                ])
            ])
            
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