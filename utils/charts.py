import cookie
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_activity(activity: cookie.GuildActivity | cookie.MemberActivity, frame):
    dates = list(activity.msg_activity.keys())
    msg_counts = list(activity.msg_activity.values())
    voice_minutes = list(activity.voice_activity.values())

    plt.rcParams["figure.figsize"] = [5.0, 3.0]
    plt.rcParams["figure.autolayout"] = True

    fig, ax1 = plt.subplots()

    fig.set_facecolor("#13191E")
    plt.style.use("dark_background")

    color = 'tab:orange'
    ax1.set_xlabel('Date', color='white')
    ax1.set_ylabel('Messages', color=color)
    ax1.plot(dates, msg_counts, color=color, label='Messages')
    ax1.tick_params(axis='y', labelcolor='white', colors='white')
    ax1.tick_params(axis='x', labelcolor='white', colors='white')

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Voice Minutes', color=color)
    ax2.plot(dates, voice_minutes, color=color, label='Voice Minutes')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    fig.autofmt_xdate()

    ax1.set_facecolor("#13191E")
    plt.setp(ax1.spines.values(), linewidth=0.1)
    for spine in ax1.spines.values():
        spine.set_visible(False)

    plt.grid(axis="y", color="grey", linestyle="--", linewidth=0.5)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')