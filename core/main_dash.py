from .dash_plot.app import app

def run_dash():
    """
    Функция запуска Dash-приложения
    """
    app.run_server(debug=True, host='0.0.0.0', port=8050)
    
    
if __name__ == '__main__':
    run_dash()