from dash import html, dcc
import dash
import bcrypt
from flask import session

#dash.register_page(__name__)

# Hardcoded credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# Login Page Layout
login_layout = html.Div(
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
                html.H2("Login", style={"textAlign": "center"}),

                # Username Input
                html.Label("Username:"),
                dcc.Input(
                    id="login-username",
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

# Login Validation Logic (Used in the Callback)
def validate_login(n_clicks, username, password):
    
    if n_clicks > 0:
        if not username or not password:
            return "Пожалуйста, заполните все поля.", "/"
        if username not in 'admin':
            return "Пользователь не существует.", "/"
        if password in 'admin':
            # Устанавливаем сессионное состояние пользователя
            session['logged_in'] = True
            session['username'] = username
            return "","/home"  # Редирект в защищенную зону
        else:
            return "Неправильный пароль.", "/"
    return "", "/"
