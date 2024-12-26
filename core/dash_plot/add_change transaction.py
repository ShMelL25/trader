from dash import html, dcc, Input, Output, State
from flask import session
from .core import create_graph as cg
from core.base.dach_bd import Data_Base_Dash


# Layout для защищенной страницы
home_transaction = html.Div(id="protected-page-content")

# Callback для проверки авторизации

def render_protected_page(pathname):
    if not session.get('logged_in'):  # Если пользователь не авторизован
        return html.Div([
            html.H3("403 - Доступ запрещен"),
            html.Div("Вы не авторизованы для доступа к этой странице.", style={"color": "red"}),
            dcc.Link("Войти", href="/")
        ])
        
    return html.Div(
    style={"display": "flex",
           "justify-content": "center",
           "align-items": "center",
           "height": "100vh",
           "background": "#f7f7f7"},
    children=[
        html.Div(
            style={"border": "1px solid #ddd",
                   "padding": "30px",
                   "border-radius": "10px",
                   "background": "white",
                   "width": "400px",
                   "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"},
            children=[
                html.H2("Transaciton", style={"textAlign": "center"}),

                # Username Input
                html.Label("Transaction value:"),
                dcc.Input(
                    id="transaction-value",
                    type="text",
                    placeholder="Enter your username",
                    style={"width": "100%", "padding": "10px", "margin-bottom": "10px"},
                ),

                # Password Input
                html.Label("Password:"),
                dcc.Input(
                    id="login-password",
                    type="password",
                    placeholder="Enter your password",
                    style={"width": "100%", "padding": "10px", "margin-bottom": "20px"},
                ),

                # Login Button
                html.Button("Login", id="login-button", n_clicks=0,
                            style={"width": "100%", "padding": "10px", "background": "#007BFF",
                                   "color": "white", "border": "none", "cursor": "pointer"}),
                html.Div(id="login-message", style={"color": "green", "marginTop": "10px"}),

                # Alert for wrong credentials
                html.Div(id="login-alert", style={"margin-top": "20px", "textAlign": "center"}),
                html.Br()
            ]
        )
    ]
)
    
    
        
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