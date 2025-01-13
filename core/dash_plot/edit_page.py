from dash import html, dcc, Input, Output, State
import dash
from dash.dash_table import DataTable
from flask import session
from .core import create_graph as cg
from core.base.dach_bd import Data_Base_Dash
import numpy as np
import pandas as pd


# Layout для защищенной страницы
edit_layout = html.Div(id="edit-page-content")

# Callback для проверки авторизации

def render_edit_protected_page(pathname):
    if not session.get('logged_in'):  # Если пользователь не авторизован
        return html.Div([
            html.H3("403 - Доступ запрещен"),
            html.Div("Вы не авторизованы для доступа к этой странице.", style={"color": "red"}),
            dcc.Link("Войти", href="/")
        ])
    
    df = Data_Base_Dash().get_transaction_dash(
                            telegram_id=session['username'],
                            date_add=None).sort_values('id')
    
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
            html.Div([
                dcc.Input(id='input-value', type='text', placeholder='Введите значение'),
                
                dcc.Dropdown(options=np.sort(Data_Base_Dash().get_date_transaction_dash(session['username']).T[0]),
                                    value = np.sort(Data_Base_Dash().get_date_transaction_dash(session['username']).T[0])[-1],
                                    id='drop_down_type_transaction'),
                
                dcc.Dropdown(options=np.sort(Data_Base_Dash().get_date_transaction_dash(session['username']).T[0]),
                                    value = np.sort(Data_Base_Dash().get_date_transaction_dash(session['username']).T[0])[-1],
                                    id='drop_down_text_expenses'),
                
                html.Button('Добавить', id='add-button'),
                
                html.Div([
                        DataTable(
                            id='datatable',
                            columns=[
                                {"name": "ID", "id": "id"},
                                {"name": "Дата", "id": "year_month"},
                                {"name": "Значение", "id": "sum_enrolment_expenses"},
                                {"name": "Тип", "id": "type_transaction"},
                                {"name": "Текст", "id": "text_expenses"}
                            ],
                            data=df.to_dict('records'),
                            editable=True,
                            row_deletable=True,  # Позволяет удалять строки
                            sort_action='native'
                        )
                    ],id='div-table-container')
                
            ])
        ])
    
    

def update_table(add_clicks, 
                 previous_data, 
                 current_data,
                 type_transaction,
                 text_expenses):
    
    ctx = dash.callback_context
    
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Добавление новой записи
    if triggered_id == 'add-button' and current_data:
        new_value = current_data[-1]['sum_enrolment_expenses'] if current_data else ''
        Data_Base_Dash().update_add_table(
                    telegram_id=session['username'], 
                    value=new_value,
                    type_transaction=type_transaction, 
                    text_expenses=text_expenses)
        

    # Проверка на удаленные строки
    if previous_data is not None:
        # Получаем только удаленные строки
        deleted_rows = [row for row in previous_data if row not in current_data]
        
        for row in deleted_rows:
            row_id = row['id']
            Data_Base_Dash().update_dell_table(id_=row_id)

    # Обновляем данные из БД
    return Data_Base_Dash().get_transaction_dash(
                            telegram_id=session['username'],
                            date_add=None).to_dict('records')