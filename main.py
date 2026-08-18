import time
import random
import tkinter as tk
from tkinter import ttk, messagebox

# Default pool of sentences
SENTENCES = [
    "The quick brown fox jumps over the lazy dog while a clever wizard quietly examines a box of shiny jewels near the frozen lake.",
    "While the quick brown fox jumps over the lazy dog, five young wizards pack their exotic jewels into a bright yellow box for a mysterious journey.",
    "A quick-minded wizard named Jack quietly packed five dozen bright blue jewels, gold coins, and exotic vases into a heavy wooden box before the lazy fox jumped away.",
    "The adventurous queen quickly gazed at a beautiful jungle landscape while six clever foxes jumped over a lazy brown dog near the quiet village.",
    "During a quiet evening, the quick brown fox carefully jumped over a lazy dog while a group of young wizards explored a mysterious jungle filled with exotic plants, colorful birds, and shiny quartz rocks.",
    "When the clever wizard quickly opened the ancient wooden box, he discovered five dozen sparkling jewels, a golden key, a small bronze clock, and a mysterious map hidden beneath the dusty velvet cloth."
]

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("920x680")
        self.root.minsize(800, 600)
        self.root.configure(bg="#181825")

        # Application State
        self.target_sentence = ""
        self.start_time = None
        self.timer_running = False
        self.completed = False
        self.timer_job = None

        # Color Palette (Catppuccin Mocha Theme)
        self.COLOR_BG = "#181825"
        self.COLOR_SURFACE = "#1e1e2e"
        self.COLOR_CARD = "#313244"
        self.COLOR_ACCENT = "#89b4fa"
        self.COLOR_ACCENT_HOVER = "#b4befe"
        self.COLOR_TEXT = "#cdd6f4"
        self.COLOR_TEXT_MUTED = "#a6adc8"
        self.COLOR_CORRECT = "#a6e3a1"
        self.COLOR_INCORRECT_BG = "#f38ba8"
        self.COLOR_INCORRECT_FG = "#11111b"
        self.COLOR_UNTYPED = "#6c7086"
        self.COLOR_CURRENT_BG = "#45475a"

        self.setup_ui()
        self.new_test()

    def setup_ui(self):
        # Header Section
        header_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        header_frame.pack(fill="x", pady=(20, 0))

        title_label = tk.Label(
            header_frame,
            text="⚡ TYPING SPEED TEST",
            font=("Segoe UI", 24, "bold"),
            fg=self.COLOR_ACCENT,
            bg=self.COLOR_BG
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Test your speed and accuracy in real-time. Start typing below to begin!",
            font=("Segoe UI", 11),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_BG
        )
        subtitle_label.pack(pady=(4, 0))

        # Metrics Section (Cards)
        metrics_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        metrics_frame.pack(fill="x", padx=40, pady=10)
        metrics_frame.columnconfigure((0, 1, 2), weight=1)

        # Card 1: Time Taken
        self.time_card, self.time_val_lbl = self.create_metric_card(
            metrics_frame, 0, "TIME ELAPSED", "0.0s", "#89b4fa"
        )
        # Card 2: Speed (WPM)
        self.wpm_card, self.wpm_val_lbl = self.create_metric_card(
            metrics_frame, 1, "TYPING SPEED", "0 WPM", "#a6e3a1"
        )
        # Card 3: Accuracy
        self.acc_card, self.acc_val_lbl = self.create_metric_card(
            metrics_frame, 2, "ACCURACY", "100%", "#f9e2af"
        )

        # Content Area
        content_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        content_frame.pack(fill="both", expand=True, padx=40, pady=15)

        # Target Text Label & Display Container
        target_header_lbl = tk.Label(
            content_frame,
            text="TARGET TEXT",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_BG,
            anchor="w"
        )
        target_header_lbl.pack(fill="x", pady=(0, 5))

        target_container = tk.Frame(content_frame, bg=self.COLOR_SURFACE, bd=0, highlightthickness=1, highlightbackground=self.COLOR_CARD)
        target_container.pack(fill="x", pady=(0, 15))

        self.target_text_widget = tk.Text(
            target_container,
            font=("Consolas", 14),
            wrap="word",
            height=4,
            bg=self.COLOR_SURFACE,
            fg=self.COLOR_UNTYPED,
            bd=0,
            padx=16,
            pady=16,
            highlightthickness=0,
            state="disabled",
            cursor="arrow"
        )
        self.target_text_widget.pack(fill="both", expand=True)

        # Text Tag Configs
        self.target_text_widget.tag_configure("correct", foreground=self.COLOR_CORRECT, background="")
        self.target_text_widget.tag_configure("incorrect", foreground=self.COLOR_INCORRECT_FG, background=self.COLOR_INCORRECT_BG)
        self.target_text_widget.tag_configure("current", background=self.COLOR_CURRENT_BG, underline=True)
        self.target_text_widget.tag_configure("untyped", foreground=self.COLOR_UNTYPED)

        # User Typing Input Area
        input_header_lbl = tk.Label(
            content_frame,
            text="START TYPING HERE",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_BG,
            anchor="w"
        )
        input_header_lbl.pack(fill="x", pady=(0, 5))

        input_container = tk.Frame(content_frame, bg=self.COLOR_CARD, bd=0, highlightthickness=1, highlightbackground=self.COLOR_ACCENT)
        input_container.pack(fill="both", expand=True)

        self.user_entry = tk.Text(
            input_container,
            font=("Consolas", 14),
            wrap="word",
            height=4,
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_ACCENT,
            bd=0,
            padx=16,
            pady=16,
            highlightthickness=0,
            undo=True
        )
        self.user_entry.pack(fill="both", expand=True)

        # Event Bindings
        self.user_entry.bind("<KeyPress>", self.on_key_press)
        self.user_entry.bind("<KeyRelease>", self.on_key_release)

        # Controls & Bottom Action Frame
        bottom_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        bottom_frame.pack(fill="x", padx=40, pady=20)

        self.restart_btn = tk.Button(
            bottom_frame,
            text="🔄 Restart Test",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_ACCENT,
            fg="#11111b",
            activebackground=self.COLOR_ACCENT_HOVER,
            activeforeground="#11111b",
            bd=0,
            padx=24,
            pady=10,
            cursor="hand2",
            command=self.new_test
        )
        self.restart_btn.pack(side="right")

        self.status_lbl = tk.Label(
            bottom_frame,
            text="Click input box and type to begin timer",
            font=("Segoe UI", 11, "italic"),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_BG
        )
        self.status_lbl.pack(side="left")

    def create_metric_card(self, parent, col, title, initial_val, val_color):
        card = tk.Frame(parent, bg=self.COLOR_CARD, bd=0, padx=15, pady=12)
        card.grid(row=0, column=col, padx=10, sticky="ew")

        title_lbl = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_CARD
        )
        title_lbl.pack(anchor="w")

        val_lbl = tk.Label(
            card,
            text=initial_val,
            font=("Segoe UI", 20, "bold"),
            fg=val_color,
            bg=self.COLOR_CARD
        )
        val_lbl.pack(anchor="w", pady=(2, 0))

        return card, val_lbl

    def new_test(self):
        # Cancel any active timer loop
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        # Reset states
        self.target_sentence = random.choice(SENTENCES)
        self.start_time = None
        self.timer_running = False
        self.completed = False

        # Reset UI
        self.time_val_lbl.config(text="0.0s")
        self.wpm_val_lbl.config(text="0 WPM")
        self.acc_val_lbl.config(text="100%")
        self.status_lbl.config(text="Start typing to begin...", fg=self.COLOR_TEXT_MUTED)

        # Enable text entry & clear
        self.user_entry.config(state="normal")
        self.user_entry.delete("1.0", tk.END)
        self.user_entry.focus_set()

        # Update target text display
        self.render_target_text("")

    def render_target_text(self, user_text):
        self.target_text_widget.config(state="normal")
        self.target_text_widget.delete("1.0", tk.END)
        self.target_text_widget.insert("1.0", self.target_sentence)

        # Reset tags
        self.target_text_widget.tag_remove("correct", "1.0", tk.END)
        self.target_text_widget.tag_remove("incorrect", "1.0", tk.END)
        self.target_text_widget.tag_remove("current", "1.0", tk.END)
        self.target_text_widget.tag_remove("untyped", "1.0", tk.END)

        typed_len = len(user_text)
        target_len = len(self.target_sentence)

        for i in range(target_len):
            idx_start = f"1.0 + {i} chars"
            idx_end = f"1.0 + {i + 1} chars"

            if i < typed_len:
                if user_text[i] == self.target_sentence[i]:
                    self.target_text_widget.tag_add("correct", idx_start, idx_end)
                else:
                    self.target_text_widget.tag_add("incorrect", idx_start, idx_end)
            elif i == typed_len:
                self.target_text_widget.tag_add("current", idx_start, idx_end)
            else:
                self.target_text_widget.tag_add("untyped", idx_start, idx_end)

        self.target_text_widget.config(state="disabled")

    def on_key_press(self, event):
        if self.completed:
            return "break"

        # Prevent Tab key navigation inside text area
        if event.keysym == "Tab":
            return "break"

    def on_key_release(self, event):
        if self.completed:
            return

        user_text = self.user_entry.get("1.0", "end-1c")

        # Start timer on first keystroke if non-empty
        if not self.timer_running and len(user_text) > 0:
            self.start_time = time.time()
            self.timer_running = True
            self.status_lbl.config(text="⏱️ Test in progress...", fg=self.COLOR_ACCENT)
            self.update_timer()

        self.render_target_text(user_text)
        self.calculate_metrics(user_text)

        # Check for test completion
        if len(user_text) >= len(self.target_sentence):
            self.finish_test()

    def update_timer(self):
        if self.timer_running and not self.completed:
            elapsed = time.time() - self.start_time
            self.time_val_lbl.config(text=f"{elapsed:.1f}s")
            
            # Recalculate metrics on tick
            user_text = self.user_entry.get("1.0", "end-1c")
            self.calculate_metrics(user_text)

            self.timer_job = self.root.after(100, self.update_timer)

    def calculate_metrics(self, user_text):
        if not self.start_time:
            return

        time_taken = max(time.time() - self.start_time, 0.1)
        
        # Word count & WPM Calculation
        words_typed = len(user_text.split())
        wpm = (words_typed / (time_taken / 60))
        self.wpm_val_lbl.config(text=f"{int(wpm)} WPM")

        # Accuracy Calculation
        correct_characters = 0
        min_len = min(len(self.target_sentence), len(user_text))

        for i in range(min_len):
            if self.target_sentence[i] == user_text[i]:
                correct_characters += 1

        if len(user_text) > 0:
            accuracy = (correct_characters / len(user_text)) * 100
        else:
            accuracy = 100.0

        self.acc_val_lbl.config(text=f"{accuracy:.1f}%")

    def finish_test(self):
        self.timer_running = False
        self.completed = True

        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        time_taken = max(time.time() - self.start_time, 0.1)
        user_text = self.user_entry.get("1.0", "end-1c")

        # Final WPM and Accuracy
        words_typed = len(user_text.split())
        wpm = words_typed / (time_taken / 60)

        correct_characters = sum(
            1 for i in range(min(len(self.target_sentence), len(user_text)))
            if self.target_sentence[i] == user_text[i]
        )
        accuracy = (correct_characters / len(self.target_sentence)) * 100

        self.time_val_lbl.config(text=f"{time_taken:.2f}s")
        self.wpm_val_lbl.config(text=f"{wpm:.1f} WPM")
        self.acc_val_lbl.config(text=f"{accuracy:.1f}%")

        self.user_entry.config(state="disabled")
        self.status_lbl.config(text="🎉 Test completed! Click Restart to try again.", fg=self.COLOR_CORRECT)

        # Show Results Popup
        self.show_results_dialog(time_taken, wpm, accuracy)

    def show_results_dialog(self, time_taken, wpm, accuracy):
        # Grade performance
        if wpm >= 80:
            rating = "🚀 Speed Demon!"
        elif wpm >= 50:
            rating = "🔥 Professional Typist!"
        elif wpm >= 30:
            rating = "👍 Good Job!"
        else:
            rating = "🌱 Keep Practicing!"

        result_msg = (
            f"Performance: {rating}\n\n"
            f"⏱️ Time Taken: {time_taken:.2f} seconds\n"
            f"⚡ Speed: {wpm:.2f} WPM\n"
            f"🎯 Accuracy: {accuracy:.2f}%\n"
        )
        messagebox.showinfo("Test Results", result_msg)

def main():
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()