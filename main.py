import asyncio
import customtkinter as ctk
import cookiebot


def fetch_and_display_user_stats(user_id, frame):
    try:
        api = cookiebot.CookieAPI()
        user_stats = asyncio.run(api.get_user_stats(user_id))
    except cookiebot.UserNotFound:
        error_label = ctk.CTkLabel(frame, text="User not found.", font=("Helvetica", 15, "bold"))
        frame.after(0, error_label.pack)
        return
    except cookiebot.InvalidAPIKey:
        error_label = ctk.CTkLabel(frame, text="Invalid API key.", font=("Helvetica", 15, "bold"), text_color="red")
        frame.after(0, error_label.pack)
        return
    except Exception as e:
        error_label = ctk.CTkLabel(frame, text=f"Error: {e}", font=("Helvetica", 15, "bold"), text_color="red")
        frame.after(0, error_label.pack)
        return

    def update_frame():
        for widget in frame.winfo_children():
            widget.destroy()

        frame.configure(corner_radius=10)

        stats_text = "\n".join([
            f"User ID: {user_stats.user_id}",
            f"Max Streak: {user_stats.max_streak}",
            f"Current Streak: {user_stats.streak}",
            f"Cookies: {user_stats.cookies}",
            f"Career: {user_stats.career}",
            f"Total Shifts: {user_stats.total_shifts}",
            f"Job: {user_stats.job}",
        ])

        stats_label = ctk.CTkLabel(frame, text=stats_text, font=("Helvetica", 15), anchor='center')
        stats_label.pack(expand=True, fill='both')

    frame.after(0, update_frame)
    asyncio.run(api.close())


def on_button_click(entry, frame):
    user_id = entry.get()
    if user_id.isdigit():
        fetch_and_display_user_stats(int(user_id), frame)
    else:
        error_label = ctk.CTkLabel(frame, text="User ID must be a number.", font=("Helvetica", 15, "bold"))
        error_label.pack()


def setup_gui():
    root = ctk.CTk()
    root.geometry("400x400")
    root.title("User Stats Display")
    root.iconbitmap("icon.ico")
    root.resizable(False, False)

    stats_frame = ctk.CTkFrame(root)
    stats_frame.configure(width=380, height=200)
    stats_frame.pack(pady=10)
    stats_frame.pack_propagate(False)

    entry = ctk.CTkEntry(root, placeholder_text="Enter User ID")
    entry.pack(pady=20)

    fetch_button = ctk.CTkButton(root, text="Fetch User Stats", command=lambda: on_button_click(entry, stats_frame))
    fetch_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    setup_gui()
