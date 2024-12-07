from dash import html, dcc
from flask import session
from dash.dependencies import Input, Output

logout_layout = html.Div([
    html.Div(id="logout-content"),
])


def validate_logout(pathname):
    if pathname == "/logout":
        session.clear()  # Полностью очищаем сессию
        return html.Div([
            html.H3("Сеанс завершён. Вы вышли из системы.", style={"textAlign": "center"}),
            dcc.Link("Вернуться к входу", href="/", style={"textAlign": "center"})
        ])
    return None