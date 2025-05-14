import plotly.express as px
import plotly.graph_objects as go
from core.base.dach_bd import Data_Base_Dash

def pie_plot_transaction(telegram_id:int, 
                         date_add)->go.Figure:
    
    df = Data_Base_Dash().get_transaction_dash(telegram_id, date_add)
    fig = px.pie(df, 
                 values='sum_enrolment_expenses', 
                 names='type_transaction')
    
    fig.update_layout(width=600, height=400)
    Data_Base_Dash().close_connect()
    
    return fig

def bar_plot_transaction(telegram_id:int, 
                         date_add)->go.Figure:
    
    df = Data_Base_Dash().get_transaction_dash(telegram_id, date_add)
    df['year_month'] = df['year_month'].astype('datetime64[ns]')
    df = df.groupby(['year_month', 'type_transaction']).sum().reset_index()
    fig = px.bar(df, 
                 x="year_month", 
                 y="sum_enrolment_expenses", 
                 color="type_transaction",
                 barmode='group',
                 text=df['sum_enrolment_expenses'],
                 orientation='v')
    
    fig.update_layout(xaxis_tickformat='%B %Y')
    fig.update_xaxes(tickvals=df['year_month'], ticktext=df['year_month'].dt.strftime('%B %Y'))

    Data_Base_Dash().close_connect()
    
    return fig

def plate_info_transaction_per_month(telegram_id:int, 
                                     date_add)->go.Figure:
    
    df = Data_Base_Dash().get_transaction_dash(telegram_id, date_add)
    
    return [f"enrolment: {df.loc[df['type_transaction']=='enrolment']['sum_enrolment_expenses'].sum()}", 
            f"expenses: {df.loc[df['type_transaction']=='expenses']['sum_enrolment_expenses'].sum()}", 
            f"delta: {df.loc[df['type_transaction']=='enrolment']['sum_enrolment_expenses'].sum()-df.loc[df['type_transaction']=='expenses']['sum_enrolment_expenses'].sum()}"
            ]
                
            