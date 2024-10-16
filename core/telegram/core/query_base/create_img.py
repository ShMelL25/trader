import seaborn as sns
import matplotlib.pyplot as plt

def create_rate_plot(data, telegram_id):
    
    fig, ax = plt.subplots()  # create figure & 1 axis
    ax.plot(data['date'], data['rate'])
    fig.savefig(f'/home/pmonk-1487/projects/trader/core/telegram/log/{telegram_id}.png')   # save the figure to file
    plt.close(fig)
    
    