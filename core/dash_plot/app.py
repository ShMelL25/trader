import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from .login import login_layout, validate_login
from .home import home_layout, render_protected_page
from .register import register_user, register_layout
from dash import Dash
from flask import Flask, session
from flask_session import Session
from datetime import timedelta
from .logout import logout_layout, validate_logout

# Flask сервер для сессии
server = Flask(__name__)
server.config['SECRET_KEY'] = 'your_secret_key'  # Установите секретный ключ
server.config['SESSION_TYPE'] = 'filesystem'    # Хранение сессий на диске
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Session(server)  # Инициализация Flask-сессии

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server, use_pages=True, pages_folder=".")
app.title = "Multi-Page Login App"

# App Layout to Set the Routing Location
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content")
    ]
)

# Update the Page Based on URL
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/home":
        return home_layout
    elif pathname == "/register":
        return register_layout
    elif pathname == "/logout":
        return logout_layout
    else:
        return login_layout  # Default is login page
    

# Callback for Login Validation (from login.py)
app.callback(
    Output("login-message", "children"),
    Output("url", "href"),
    Input("login-button", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value")
)(validate_login)

app.callback(
    Output("register-message", "children"),
    Input("register-button", "n_clicks"),
    State("register-username", "value"),
    State("register-password", "value"),
)(register_user)

app.callback(
    Output("protected-page-content", "children"),
    Input("url", "pathname")
)(render_protected_page)

app.callback(
    Output("logout-content", "children"),
    Input("url", "pathname")
)(validate_logout)

# Run server
'''if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)'''
