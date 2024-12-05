from dash import html, dcc, Input, Output, State
import bcrypt

# Mock база данных пользователей
users_db = {"test": bcrypt.hashpw(b"1234", bcrypt.gensalt())}

#dash.register_page(__name__)
# Layout страницы регистрации
register_layout = html.Div(
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
                html.H2("Registration", style={"textAlign": "center"}),

                # Username Input
                html.Label("Username:"),
                dcc.Input(
                    id="register-username",
                    type="text",
                    placeholder="Enter your username",
                    style={"width": "100%", "padding": "10px", "margin-bottom": "10px"},
                ),

                # Password Input
                html.Label("Password:"),
                dcc.Input(
                    id="register-password",
                    type="password",
                    placeholder="Enter your password",
                    style={"width": "100%", "padding": "10px", "margin-bottom": "20px"},
                ),

                # Login Button
                html.Button("register", id="register-button", n_clicks=0,
                            style={"width": "100%", "padding": "10px", "background": "#007BFF",
                                   "color": "white", "border": "none", "cursor": "pointer"}),

                # Alert for wrong credentials
                html.Div(id="register-alert", style={"margin-top": "20px", "textAlign": "center"}),
                html.Br(),
                dcc.Link("Login", href="/login", style={"fontSize": "13px", "display": "block", "textAlign": "center"})
            ]
        )
    ]
)
'''register_layout = html.Div([
    html.H3("Регистрация", style={"textAlign": "center"}),
    html.Div([
        html.Label("Новое имя пользователя:"),
        dcc.Input(id="register-username", type="text", placeholder="Введите имя пользователя", style={"width": "100%"}),
        html.Br(),
        html.Label("Пароль:"),
        dcc.Input(id="register-password", type="password", placeholder="Введите пароль", style={"width": "100%"}),
        html.Br(),
        html.Button("Зарегистрироваться", id="register-button", n_clicks=0, style={"marginTop": "10px"}),
        html.Div(id="register-message", style={"color": "green", "marginTop": "10px"}),
        html.Br(),
        dcc.Link("Перейти на Вход", href="/", style={"fontSize": "13px", "display": "block", "textAlign": "center"}),
    ])
])'''

# Callback на добавление нового пользователя
def register_user(n_clicks, username, password):
    
    if n_clicks > 0:
        if not username or not password:
            return "Имя пользователя или пароль не могут быть пустыми."
        if username in users_db:
            return "Имя пользователя уже занято."
        # Хэшируем пароль
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        users_db[username] = hashed_password
        return "Успешная регистрация! Теперь вы можете войти."
    return ""
