import asyncio

import cookie
import customtkinter as ctk
from cookie import CookieAPI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_activity(activity, frame):
    dates = list(activity.msg_activity.keys())
    msg_counts = list(activity.msg_activity.values())
    voice_minutes = list(activity.voice_activity.values())

    plt.rcParams["figure.figsize"] = [3.8, 3.0]
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


def fetch_stats(stats_type: str, frame, user_id: int = None, guild_id: int = None):
    api = CookieAPI()
    try:
        if stats_type == "user_stats":
            stats = api.get_user_stats(user_id)
        elif stats_type == "member_stats":
            stats = api.get_member_stats(user_id=user_id, guild_id=guild_id)
        elif stats_type == "member_activity":
            stats = api.get_member_activity(user_id=user_id, guild_id=guild_id)
        elif stats_type == "guild_activity":
            stats = api.get_guild_activity(guild_id=guild_id)
        else:
            raise ValueError("Invalid stats type.")
    except cookie.UserNotFound:
        error_label = ctk.CTkLabel(frame, text="User not found.", font=("Helvetica", 15, "bold"), text_color="red")
        frame.after(0, error_label.pack)
        return
    except cookie.GuildNotFound:
        error_label = ctk.CTkLabel(frame, text="Guild not found.", font=("Helvetica", 15, "bold"), text_color="red")
        frame.after(0, error_label.pack)
        return
    except cookie.InvalidAPIKey:
        error_label = ctk.CTkLabel(frame, text="Invalid API key.", font=("Helvetica", 15, "bold"), text_color="red")
        frame.after(0, error_label.pack)
        return
    except cookie.NoGuildAccess:
        error_label = ctk.CTkLabel(frame, text="No access to guild.", font=("Helvetica", 15, "bold"), text_color="red")
        frame.after(0, error_label.pack)
        return
    except Exception as e:
        error_label = ctk.CTkLabel(frame, text=f"Error: {e}", font=("Helvetica", 15, "bold"), text_color="red")
        frame.after(0, error_label.pack)
        return

    def update_frame():
        for widget in frame.winfo_children():
            widget.destroy()

        if stats_type == "user_stats":
            stats_text = "\n".join([
                f"User ID: {stats.user_id}",
                f"Max Streak: {stats.max_streak}",
                f"Current Streak: {stats.streak}",
                f"Cookies: {stats.cookies}",
                f"Career: {stats.career}",
                f"Total Shifts: {stats.total_shifts}",
                f"Job: {stats.job}",
            ])
        elif stats_type == "member_stats":
            stats_text = "\n".join([
                f"User ID: {stats.user_id}",
                f"Guild ID: {stats.guild_id}",
                f"Level: {stats.level}",
                f"XP: {stats.xp}",
                f"Message Count: {stats.msg_count}",
                f"Message Rank: {stats.msg_rank}",
                f"Voice Minutes: {stats.voice_min}",
                f"Voice XP: {stats.voice_xp}",
                f"Voice Level: {stats.voice_level}",
                f"Voice Rank: {stats.voice_rank}",
            ])
        elif stats_type == "member_activity" or stats_type == "guild_activity":
            stats_text = None
            plot_activity(stats, frame)
        else:
            stats_text = "Invalid stats type."
        stats_label = ctk.CTkLabel(frame, text=stats_text, font=("Helvetica", 15), anchor='center')
        stats_label.pack(expand=True, fill='both')

    frame.after(0, update_frame)


def on_user_stats_button_click(entry, frame):
    user_id = entry.get()
    if user_id.isdigit():
        fetch_stats("user_stats", frame, user_id=int(user_id))
    else:
        error_label = ctk.CTkLabel(frame, text="User ID must be a number.", font=("Helvetica", 15, "bold"))
        error_label.pack()


def on_user_stats_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    home_label = ctk.CTkLabel(root, text="User Stats", font=("Helvetica", 20, "bold"), text_color="Orange")
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root)
    stats_frame.configure(width=380, height=145)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    entry = ctk.CTkEntry(root, placeholder_text="Enter User ID")
    entry.pack(pady=20)

    fetch_button = ctk.CTkButton(root, text="Fetch User Stats",
                                 command=lambda: on_user_stats_button_click(entry, stats_frame))
    fetch_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Back", command=lambda: back_to_home(root))
    back_button.pack(pady=10)


def on_member_stats_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("400x500")

    home_label = ctk.CTkLabel(root, text="Member Stats", font=("Helvetica", 20, "bold"), text_color="Orange")
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root)
    stats_frame.configure(width=380, height=200)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    user_id_entry = ctk.CTkEntry(root, placeholder_text="Enter User ID")
    user_id_entry.pack(pady=10)

    guild_id_entry = ctk.CTkEntry(root, placeholder_text="Enter Guild ID")
    guild_id_entry.pack(pady=10)

    fetch_button = ctk.CTkButton(
        root,
        text="Fetch Member Stats",
        command=lambda: on_member_stats_button_click(user_id_entry, guild_id_entry, stats_frame)
    )
    fetch_button.pack(pady=10)

    back_button = ctk.CTkButton(root, text="Back", command=lambda: back_to_home(root))
    back_button.pack(pady=10)


def on_member_stats_button_click(user_id_entry, guild_id_entry, frame):
    user_id = user_id_entry.get()
    guild_id = guild_id_entry.get()
    if user_id.isdigit() and guild_id.isdigit():
        fetch_stats("member_stats", frame, user_id=int(user_id), guild_id=int(guild_id))
    else:
        error_label = ctk.CTkLabel(frame, text="User ID and Guild ID must be numbers.", font=("Helvetica", 15, "bold"))
        error_label.pack()


def on_member_activity_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("400x600")

    home_label = ctk.CTkLabel(root, text="Member Activity", font=("Helvetica", 20, "bold"), text_color="Orange")
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root)
    stats_frame.configure(width=380, height=300)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    user_id_entry = ctk.CTkEntry(root, placeholder_text="Enter User ID")
    user_id_entry.pack(pady=10)

    guild_id_entry = ctk.CTkEntry(root, placeholder_text="Enter Guild ID")
    guild_id_entry.pack(pady=10)

    fetch_button = ctk.CTkButton(
        root,
        text="Fetch Member Activity",
        command=lambda: on_member_activity_button_click(user_id_entry, guild_id_entry, stats_frame)
    )
    fetch_button.pack(pady=10)

    back_button = ctk.CTkButton(root, text="Back", command=lambda: back_to_home(root))
    back_button.pack(pady=10)


def on_member_activity_button_click(user_id_entry, guild_id_entry, frame):
    user_id = user_id_entry.get()
    guild_id = guild_id_entry.get()
    if user_id.isdigit() and guild_id.isdigit():
        fetch_stats("member_activity", frame, user_id=int(user_id), guild_id=int(guild_id))
    else:
        error_label = ctk.CTkLabel(frame, text="User ID and Guild ID must be numbers.", font=("Helvetica", 15, "bold"))
        error_label.pack()


def on_guild_activity_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("400x600")

    home_label = ctk.CTkLabel(root, text="Guild Activity", font=("Helvetica", 20, "bold"), text_color="Orange")
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root)
    stats_frame.configure(width=380, height=300)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    guild_id_entry = ctk.CTkEntry(root, placeholder_text="Enter Guild ID")
    guild_id_entry.pack(pady=10)

    fetch_button = ctk.CTkButton(
        root,
        text="Fetch Guild Activity",
        command=lambda: on_guild_activity_button_click(guild_id_entry, stats_frame)
    )
    fetch_button.pack(pady=10)

    back_button = ctk.CTkButton(root, text="Back", command=lambda: back_to_home(root))
    back_button.pack(pady=10)


def on_guild_activity_button_click(guild_id_entry, frame):
    guild_id = guild_id_entry.get()
    if guild_id.isdigit():
        fetch_stats("guild_activity", frame, guild_id=int(guild_id))
    else:
        error_label = ctk.CTkLabel(frame, text="Guild ID must be a number.", font=("Helvetica", 15, "bold"))
        error_label.pack()


def back_to_home(root):
    for widget in root.winfo_children():
        widget.destroy()

    home_window(root)


def home_window(root):
    root.geometry("400x400")
    home_label = ctk.CTkLabel(root, text="Cookie Manager", font=("Helvetica", 20, "bold"), text_color="Orange")
    home_label.pack(pady=20)

    user_stats_button = ctk.CTkButton(root, text="User Stats", command=lambda: on_user_stats_click(root))
    member_stats_button = ctk.CTkButton(root, text="Member Stats", command=lambda: on_member_stats_click(root))
    member_activity_button = ctk.CTkButton(root, text="Member Activity", command=lambda: on_member_activity_click(root))
    guild_activity_button = ctk.CTkButton(root, text="Guild Activity", command=lambda: on_guild_activity_click(root))

    user_stats_button.pack(pady=10)
    member_stats_button.pack(pady=10)
    member_activity_button.pack(pady=10)
    guild_activity_button.pack(pady=10)


def setup_gui():
    root = ctk.CTk()
    root.geometry("400x400")
    root.title("Cookie Manager")
    root.iconbitmap("icon.ico")
    root.resizable(False, False)

    home_window(root)

    root.mainloop()


if __name__ == "__main__":
    setup_gui()
