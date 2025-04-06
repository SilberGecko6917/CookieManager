import customtkinter as ctk
from utils.fetch import fetch_stats
from utils.config import *

def back_to_home(root):
    for widget in root.winfo_children():
        widget.destroy()
    home_window(root)

def home_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x500")
    root.configure(bg=WINDOW_BG_COLOR)

    home_label = ctk.CTkLabel(root, text="Cookie Manager", font=FONT_LARGE, text_color=TEXT_COLOR)
    home_label.pack(pady=20)

    button_frame = ctk.CTkFrame(root, fg_color=FRAME_BG_COLOR, bg_color=WINDOW_BG_COLOR, corner_radius=10)
    button_frame.pack(pady=20, padx=20, fill='both', expand=True)

    buttons = [
        ("User Stats", on_user_stats_click),
        ("Member Stats", on_member_stats_click),
        ("Member Activity", on_member_activity_click),
        ("Guild Activity", on_guild_activity_click)
    ]

    for text, command in buttons:
        button = ctk.CTkButton(button_frame, text=text,
                               command=lambda cmd=command: cmd(root), fg_color=BUTTON_FG_COLOR,
                               hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
        button.pack(pady=10, padx=10, fill='x')

def on_user_stats_button_click(entry, frame):
    user_id = entry.get()
    if user_id.isdigit():
        fetch_stats("user_stats", frame, user_id=int(user_id))
    else:
        error_label = ctk.CTkLabel(frame, text="User ID must be a number.", font=FONT_SMALL, text_color=ERROR_TEXT_COLOR)
        error_label.pack(pady=10)

def on_user_stats_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    home_label = ctk.CTkLabel(root, text="User Stats", font=FONT_MEDIUM, text_color=TEXT_COLOR)
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root, fg_color=FRAME_BG_COLOR, bg_color=WINDOW_BG_COLOR, corner_radius=10)
    stats_frame.configure(width=500, height=200)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    entry = ctk.CTkEntry(root, placeholder_text="Enter User ID")
    entry.pack(pady=20)

    fetch_button = ctk.CTkButton(root, text="Fetch User Stats",
                                 command=lambda: on_user_stats_button_click(entry, stats_frame), fg_color=BUTTON_FG_COLOR,
                                 hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    fetch_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Back",
                                command=lambda: back_to_home(root), fg_color=BUTTON_FG_COLOR,
                                hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    back_button.pack(pady=10)

def on_member_stats_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    home_label = ctk.CTkLabel(root, text="Member Stats", font=FONT_MEDIUM, text_color=TEXT_COLOR)
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root, fg_color=FRAME_BG_COLOR, bg_color=WINDOW_BG_COLOR, corner_radius=10)
    stats_frame.configure(width=500, height=200)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    user_id_entry = ctk.CTkEntry(root, placeholder_text="Enter User ID")
    user_id_entry.pack(pady=10)

    guild_id_entry = ctk.CTkEntry(root, placeholder_text="Enter Guild ID")
    guild_id_entry.pack(pady=10)

    fetch_button = ctk.CTkButton(root, text="Fetch Member Stats",
                                 command=lambda: on_member_stats_button_click(user_id_entry, guild_id_entry, stats_frame),
                                 fg_color=BUTTON_FG_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    fetch_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Back",
                                command=lambda: back_to_home(root), fg_color=BUTTON_FG_COLOR,
                                hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    back_button.pack(pady=10)

def on_member_stats_button_click(user_id_entry, guild_id_entry, frame):
    user_id = user_id_entry.get()
    guild_id = guild_id_entry.get()
    if user_id.isdigit() and guild_id.isdigit():
        fetch_stats("member_stats", frame, user_id=int(user_id), guild_id=int(guild_id))
    else:
        error_label = ctk.CTkLabel(frame, text="User ID and Guild ID must be numbers.", font=FONT_SMALL,
                                   text_color=ERROR_TEXT_COLOR)
        error_label.pack(pady=10)

def on_member_activity_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x600")

    home_label = ctk.CTkLabel(root, text="Member Activity", font=FONT_MEDIUM, text_color=TEXT_COLOR)
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root, fg_color=FRAME_BG_COLOR, bg_color=WINDOW_BG_COLOR, corner_radius=10)
    stats_frame.configure(width=500, height=300)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    user_id_entry = ctk.CTkEntry(root, placeholder_text="Enter User ID")
    user_id_entry.pack(pady=10)

    guild_id_entry = ctk.CTkEntry(root, placeholder_text="Enter Guild ID")
    guild_id_entry.pack(pady=10)

    fetch_button = ctk.CTkButton(root, text="Fetch Member Activity",
                                 command=lambda: on_member_activity_button_click(user_id_entry, guild_id_entry, stats_frame),
                                 fg_color=BUTTON_FG_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    fetch_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Back",
                                command=lambda: back_to_home(root), fg_color=BUTTON_FG_COLOR,
                                hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    back_button.pack(pady=10)

def on_member_activity_button_click(user_id_entry, guild_id_entry, frame):
    user_id = user_id_entry.get()
    guild_id = guild_id_entry.get()
    if user_id.isdigit() and guild_id.isdigit():
        fetch_stats("member_activity", frame, user_id=int(user_id), guild_id=int(guild_id))
    else:
        error_label = ctk.CTkLabel(frame, text="User ID and Guild ID must be numbers.", font=FONT_SMALL,
                                   text_color=ERROR_TEXT_COLOR)
        error_label.pack(pady=10)

def on_guild_activity_click(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x600")

    home_label = ctk.CTkLabel(root, text="Guild Activity", font=FONT_MEDIUM, text_color=TEXT_COLOR)
    home_label.pack(pady=20)

    stats_frame = ctk.CTkFrame(root, fg_color=FRAME_BG_COLOR, bg_color=WINDOW_BG_COLOR, corner_radius=10)
    stats_frame.configure(width=500, height=300)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    guild_id_entry = ctk.CTkEntry(root, placeholder_text="Enter Guild ID")
    guild_id_entry.pack(pady=10)

    fetch_button = ctk.CTkButton(root, text="Fetch Guild Activity",
                                 command=lambda: on_guild_activity_button_click(guild_id_entry, stats_frame),
                                 fg_color=BUTTON_FG_COLOR, hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    fetch_button.pack(pady=10)
    back_button = ctk.CTkButton(root, text="Back",
                                command=lambda: back_to_home(root), fg_color=BUTTON_FG_COLOR,
                                hover_color=BUTTON_HOVER_COLOR, text_color=TEXT_COLOR)
    back_button.pack(pady=10)

def on_guild_activity_button_click(guild_id_entry, frame):
    guild_id = guild_id_entry.get()
    if guild_id.isdigit():
        fetch_stats("guild_activity", frame, guild_id=int(guild_id))
    else:
        error_label = ctk.CTkLabel(frame, text="Guild ID must be a number.", font=FONT_SMALL,
                                   text_color=ERROR_TEXT_COLOR)
        error_label.pack(pady=10)