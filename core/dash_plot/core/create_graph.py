import plotly.express as px
import plotly.graph_objects as go
from core.base.dach_bd import Data_Base_Dash

def pie_plot_transaction(telegram_id:int, 
                         date_add)->go.Figure:
    
    df = Data_Base_Dash().get_transaction_dash(telegram_id, date_add)
    fig = px.pie(df, values='sum_enrolment_expenses', names='type_transaction')
    Data_Base_Dash().close_connect()
    
    return fig

def bar_plot_transaction(telegram_id:int, 
                         date_add)->go.Figure:
    
    df = Data_Base_Dash().get_transaction_dash(telegram_id, date_add)
    fig = px.bar(df, x="year_month", y="sum_enrolment_expenses", color="type_transaction",
                 barmode='group')
    Data_Base_Dash().close_connect()
    
    return fig