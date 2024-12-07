from dash import html, dcc, Input, Output, State
from flask import session

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
    # Если пользователь авторизован, показываем защищенное содержимое
    return html.Div([
        html.Div([
            html.Img(src='assets/icons8-сумка-с-евро-80.png', alt='image')
            ], style={'background-color':'red'}),
        html.H3(f"Добро пожаловать, {session['username']}!", style={"textAlign": "center"}),
        html.Div("Это защищённая страница", style={"textAlign": "center"}),
        dcc.Link("Выйти", href="/logout"),
    ])