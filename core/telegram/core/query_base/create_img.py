import plotly.graph_objects as go
import plotly.express as px
import os
import numpy as np
    
def create_rate_plot_plolty(data, telegram_id):
    
    data_new = min_max_open_close(data)    
    fig = go.Figure(data=[go.Candlestick(x=data_new[0],
                open=data_new[3],
                high=data_new[2],
                low=data_new[1],
                close=data_new[4])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.write_image(f'/home/pmonk-1487/projects/trader/core/telegram/log/{telegram_id}.png')

def min_max_open_close(data):
    
    date_arr = []
    min_arr = []
    max_arr = []
    open_arr = []
    close_arr = []
    data['date'] = data['date'].astype('datetime64[ns]')
    
    for date in np.sort(data['date'].unique()):
        min_arr.append(min(data.loc[data['date'] == date]['rate'].to_list()))
        max_arr.append(max(data.loc[data['date'] == date]['rate'].to_list()))
        
        open_date = min(data.loc[data['date'] == date]['date_time'].astype('datetime64[ns]').to_list())
        close_date = max(data.loc[data['date'] == date]['date_time'].astype('datetime64[ns]').to_list())
        
        open_arr.append(data.loc[(data['date'] == date)&(data['date_time'].astype('datetime64[ns]')==open_date)]['rate'].to_list()[0])
        close_arr.append(data.loc[(data['date'] == date)&(data['date_time'].astype('datetime64[ns]')==close_date)]['rate'].to_list()[0])
        
        date_arr.append(date)
    
    return [np.array(date_arr).astype(str), min_arr, max_arr, open_arr, close_arr]
        
def pie_plot_create(data, telegram_id):
    fig = px.pie(data, values='sum_enrolment_expenses', names='type_transaction', title='Расходы-Доходы')
    fig.write_image(f'/home/pmonk-1487/projects/trader/core/telegram/log/{telegram_id}.png')
    
def del_img(telegram_id):
    os.remove(f'/home/pmonk-1487/projects/trader/core/telegram/log/{telegram_id}.png')