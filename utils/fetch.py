import cookie
import customtkinter as ctk

import utils
from utils.config import *


def fetch_stats(stats_type: str, frame, user_id: int = None, guild_id: int = None):
    api = cookie.CookieAPI()
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
    except cookie.NotFound:
        error_label = ctk.CTkLabel(frame, text="User / Guild not found.", font=FONT_SMALL, text_color=ERROR_TEXT_COLOR)
        frame.after(0, error_label.pack)
        return
    except cookie.InvalidAPIKey:
        error_label = ctk.CTkLabel(frame, text="Invalid API key.", font=FONT_SMALL, text_color=ERROR_TEXT_COLOR)
        frame.after(0, error_label.pack)
        return
    except cookie.NoGuildAccess:
        error_label = ctk.CTkLabel(frame, text="No access to guild.", font=FONT_SMALL, text_color=ERROR_TEXT_COLOR)
        frame.after(0, error_label.pack)
        return
    except Exception as e:
        error_label = ctk.CTkLabel(frame, text=f"Error: {e}", font=FONT_SMALL, text_color=ERROR_TEXT_COLOR)
        frame.after(0, error_label.pack)
        return

    def update_frame():
        for widget in frame.winfo_children():
            widget.destroy()

        if stats_type == "user_stats":
            stats_text = "\n".join([
                f"User ID: {user_id}",
                f"Max Streak: {stats.daily.max_streak}",
                f"Current Streak: {stats.daily.streak}",
                f"Cookies: {stats.cookies}",
                f"Career: {stats.job.career}",
                f"Total Shifts: {stats.job.total_shifts}",
                f"Job: {stats.job.job}",
            ])
        elif stats_type == "member_stats":
            stats_text = "\n".join([
                f"User ID: {user_id}",
                f"Guild ID: {guild_id}",
                f"Level: {stats.level.level}",
                f"XP: {stats.level.xp}",
                f"Message Count: {stats.level.msg}",
                f"Message Rank: {stats.level.rank}",
                f"Voice Minutes: {stats.voice.minutes}",
                f"Voice XP: {stats.voice.xp}",
                f"Voice Level: {stats.voice.level}",
                f"Voice Rank: {stats.voice.rank}",
            ])
        elif stats_type == "member_activity" or stats_type == "guild_activity":
            stats_text = None
            utils.plot_activity(stats, frame)
        else:
            stats_text = "Invalid stats type."
        stats_label = ctk.CTkLabel(frame, text=stats_text, font=FONT_SMALL, anchor='center')
        stats_label.pack(expand=True, fill='both')

    frame.after(0, update_frame)