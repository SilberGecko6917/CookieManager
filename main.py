import customtkinter as ctk
import utils
from utils.config import *

class CookieManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x500")
        self.root.title("Cookie Manager")
        self.root.iconbitmap("utils/data/assets/icon.ico")
        self.root.resizable(False, False)
        self.show_home_window()

    def show_home_window(self):
        self.clear_window()
        self.root.geometry("600x500")
        self.root.configure(bg=WINDOW_BG_COLOR)

        self.create_label(self.root, "Cookie Manager", FONT_LARGE, TEXT_COLOR, pady=20)

        button_frame = self.create_frame(self.root, FRAME_BG_COLOR, pady=20, padx=20, fill='both', expand=True)

        buttons = [
            ("User Stats", self.on_user_stats_click),
            ("Member Stats", self.on_member_stats_click),
            ("Member Activity", self.on_member_activity_click),
            ("Guild Activity", self.on_guild_activity_click)
        ]

        for text, command in buttons:
            self.create_button(button_frame, text, command, BUTTON_FG_COLOR, BUTTON_HOVER_COLOR,
                               TEXT_COLOR, pady=10, padx=10, fill='x')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_user_stats_click(self):
        self.show_stats_window("User Stats", self.fetch_user_stats)

    def on_member_stats_click(self):
        self.show_stats_window("Member Stats", self.fetch_member_stats, True)

    def on_member_activity_click(self):
        self.show_stats_window("Member Activity", self.fetch_member_activity, True)

    def on_guild_activity_click(self):
        self.show_stats_window("Guild Activity", self.fetch_guild_activity)

    def show_stats_window(self, title, fetch_command, require_guild_id=False):
        self.clear_window()
        self.root.geometry("600x600")

        self.create_label(self.root, title, FONT_MEDIUM, TEXT_COLOR, pady=20)

        stats_frame = self.create_frame(self.root, FRAME_BG_COLOR, width=500, height=300, pady=10)
        stats_frame.pack_propagate(False)

        user_id_entry = self.create_entry(self.root, "Enter User ID", pady=10)

        guild_id_entry = None
        if require_guild_id:
            guild_id_entry = self.create_entry(self.root, "Enter Guild ID", pady=10)

        self.create_button(self.root, f"Fetch {title}",
                           lambda: fetch_command(user_id_entry, guild_id_entry, stats_frame),
                           BUTTON_FG_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR, pady=10)
        self.create_button(self.root, "Back",
                           self.show_home_window, BUTTON_FG_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR, pady=10)

    def fetch_user_stats(self, user_id_entry, guild_id_entry, frame):
        user_id = user_id_entry.get()
        if user_id.isdigit():
            utils.fetch_stats("user_stats", frame, user_id=int(user_id))
        else:
            self.show_error(frame, "User ID must be a number.")

    def fetch_member_stats(self, user_id_entry, guild_id_entry, frame):
        user_id = user_id_entry.get()
        guild_id = guild_id_entry.get()
        if user_id.isdigit() and guild_id.isdigit():
            utils.fetch_stats("member_stats", frame, user_id=int(user_id), guild_id=int(guild_id))
        else:
            self.show_error(frame, "User ID and Guild ID must be numbers.")

    def fetch_member_activity(self, user_id_entry, guild_id_entry, frame):
        user_id = user_id_entry.get()
        guild_id = guild_id_entry.get()
        if user_id.isdigit() and guild_id.isdigit():
            utils.fetch_stats("member_activity", frame, user_id=int(user_id), guild_id=int(guild_id))
        else:
            self.show_error(frame, "User ID and Guild ID must be numbers.")

    def fetch_guild_activity(self, user_id_entry, guild_id_entry, frame):
        guild_id = user_id_entry.get()
        if guild_id.isdigit():
            utils.fetch_stats("guild_activity", frame, guild_id=int(guild_id))
        else:
            self.show_error(frame, "Guild ID must be a number.")

    def show_error(self, frame, message):
        self.create_label(frame, message, FONT_SMALL, ERROR_TEXT_COLOR, pady=10)

    def create_label(self, parent, text, font, text_color, **kwargs):
        label = ctk.CTkLabel(parent, text=text, font=font, text_color=text_color)
        label.pack(**kwargs)
        return label

    def create_frame(self, parent, bg_color, **kwargs):
        frame = ctk.CTkFrame(parent, fg_color=bg_color, bg_color=WINDOW_BG_COLOR, corner_radius=10)
        frame.pack(**{k: v for k, v in kwargs.items() if k not in ['width', 'height']})
        frame.configure(width=kwargs.get('width'), height=kwargs.get('height'))
        return frame

    def create_button(self, parent, text, command, fg_color, hover_color, text_color, **kwargs):
        button = ctk.CTkButton(parent, text=text, command=command,
                               fg_color=fg_color, hover_color=hover_color, text_color=text_color)
        button.pack(**kwargs)
        return button

    def create_entry(self, parent, placeholder_text, **kwargs):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder_text)
        entry.pack(**kwargs)
        return entry

if __name__ == "__main__":
    root = ctk.CTk()
    app = CookieManagerApp(root)
    root.mainloop()