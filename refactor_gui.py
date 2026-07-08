import os

with open('nse_downloader.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('class DownloaderGUI:'):
        break
    new_lines.append(line)

gui_code = """class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NSE Data Downloader")
        self.root.geometry("1100x800")
        
        # Configure CTk appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.downloader = NSEDownloader(gui=self)
        self.scheduler_thread = None
        
        # Initialize selection variables
        self.selected_downloads = {}
        self.weekend_downloads_var = tk.BooleanVar(value=self.downloader.weekend_downloads_enabled)
        
        self.create_widgets()
        
        # Auto-start scheduler if auto mode is enabled and time is between 8 AM and 8 PM
        if self.downloader.auto_mode:
            self.check_and_start_auto_mode()
            
    def create_widgets(self):
        # Title - Apple tight headline
        title_label = ctk.CTkLabel(
            self.root,
            text="NSE Data Downloader",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create Notebook (Tabs)
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create Tabs
        self.dashboard_tab = self.notebook.add("Dashboard")
        self.settings_tab = self.notebook.add("Settings")
        
        # --- DASHBOARD TAB ---
        
        # Date Selection Section
        date_frame = ctk.CTkFrame(self.dashboard_tab)
        date_frame.pack(fill=tk.X, pady=5, padx=5)
        ctk.CTkLabel(date_frame, text="Select Date", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        
        # Date Picker (Day, Month, Year)
        date_inner_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        date_inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ctk.CTkLabel(date_inner_frame, text="Date:").pack(side=tk.LEFT, padx=(0,10))
        
        # Day
        self.day_var = tk.StringVar(value=datetime.now().strftime("%d"))
        days = [f"{i:02d}" for i in range(1, 32)]
        self.day_cb = ctk.CTkComboBox(date_inner_frame, variable=self.day_var, values=days, width=70)
        self.day_cb.pack(side=tk.LEFT, padx=5)
        
        # Month
        self.month_var = tk.StringVar(value=datetime.now().strftime("%B"))
        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        self.month_cb = ctk.CTkComboBox(date_inner_frame, variable=self.month_var, values=months, width=120)
        self.month_cb.pack(side=tk.LEFT, padx=5)
        
        # Year
        current_year = int(datetime.now().strftime("%Y"))
        self.year_var = tk.StringVar(value=str(current_year))
        years = [str(y) for y in range(current_year - 5, 2100)]
        self.year_cb = ctk.CTkComboBox(date_inner_frame, variable=self.year_var, values=years, width=80)
        self.year_cb.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(date_inner_frame, text="Set Today", command=self.set_today, width=100, corner_radius=50).pack(side=tk.LEFT, padx=20)

        # Download Selection Section
        select_frame = ctk.CTkFrame(self.dashboard_tab)
        select_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ctk.CTkLabel(select_frame, text="Select Downloads", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        
        # Default downloads (Always selected)
        default_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        default_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        ctk.CTkLabel(default_frame, text="Default (Always Downloaded):", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        ctk.CTkLabel(default_frame, text="• NIFTY 50, NIFTY 500, Market Indices", text_color="gray").pack(anchor=tk.W, padx=15)
        
        # Optional downloads
        opt_header_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        opt_header_frame.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkLabel(opt_header_frame, text="Optional Downloads:", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        
        # Helper buttons
        ctk.CTkButton(opt_header_frame, text="Clear All", command=self.deselect_all, width=100, corner_radius=50, fg_color="transparent", border_width=1, text_color=("black", "white")).pack(side=tk.RIGHT)
        ctk.CTkButton(opt_header_frame, text="Select All", command=self.select_all, width=100, corner_radius=50, fg_color="transparent", border_width=1, text_color=("black", "white")).pack(side=tk.RIGHT, padx=5)
        ctk.CTkButton(opt_header_frame, text="Download Selected", command=self.download_optionals, width=150, corner_radius=50).pack(side=tk.RIGHT, padx=5)
        
        # Frame for checkboxes
        checkbox_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        checkbox_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.source_names = {}
        for k in self.downloader.direct_urls.keys():
            if k == 'cm_high_low':
                self.source_names[k] = 'CM 52wk HighLow'
            elif k == 'corporates_pit':
                self.source_names[k] = 'Corporates PIT'
            elif k == 'bse_cash_bhavcopy':
                self.source_names[k] = 'BSE Cash Bhavcopy'
            else:
                self.source_names[k] = k.replace('_', ' ').title()
        
        row = 0
        col = 0
        self.checkbox_widgets = {}
        for key, name in self.source_names.items():
            is_checked = key in self.downloader.enabled_downloads
            var = tk.BooleanVar(value=is_checked)
            self.selected_downloads[key] = var
            cb = ctk.CTkCheckBox(
                checkbox_frame, 
                text=name, 
                variable=var, 
                command=lambda k=key: self.on_checkbox_toggle(k)
            )
            cb.grid(row=row, column=col, sticky=tk.W, padx=20, pady=10)
            self.checkbox_widgets[key] = cb
            
            col += 1
            if col > 2: # 3 columns
                col = 0
                row += 1

        # Optional Progress Bar
        opt_prog_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        opt_prog_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ctk.CTkLabel(opt_prog_frame, text="Optional Progress:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        
        self.opt_progress_bar = ctk.CTkProgressBar(
            opt_prog_frame,
            corner_radius=50,
            progress_color="#28a745", # Green
            height=12
        )
        self.opt_progress_bar.set(0)
        self.opt_progress_bar.pack(fill=tk.X, pady=5)
        
        self.opt_progress_label = ctk.CTkLabel(
            opt_prog_frame, 
            text="Ready", 
            font=("Helvetica", 12)
        )
        self.opt_progress_label.pack(anchor=tk.W)

        self.opt_schedule_label = ctk.CTkLabel(
            opt_prog_frame,
            text=f"Auto-download runs daily at {self.downloader.optional_download_time}",
            font=("Helvetica", 11),
            text_color="gray"
        )
        self.opt_schedule_label.pack(anchor=tk.W)

        # Time Schedule Section
        time_frame = ctk.CTkFrame(self.dashboard_tab)
        time_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ctk.CTkLabel(time_frame, text="Schedule Times", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        
        time_inner_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        time_inner_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Auto Mode Checkbox
        self.auto_mode_var = tk.BooleanVar(value=self.downloader.auto_mode)
        self.auto_mode_check = ctk.CTkCheckBox(
            time_inner_frame,
            text="Auto Mode (8 AM - 8 PM, auto-start scheduler)",
            variable=self.auto_mode_var,
            command=self.toggle_auto_mode
        )
        self.auto_mode_check.pack(anchor=tk.W, pady=5)
        
        # Weekend Downloads Checkbox
        self.weekend_check = ctk.CTkCheckBox(
            time_inner_frame,
            text="Enable Weekend Downloads (Saturday & Sunday)",
            variable=self.weekend_downloads_var,
            command=self.toggle_weekend_downloads
        )
        self.weekend_check.pack(anchor=tk.W, pady=5)
        
        ctk.CTkLabel(time_inner_frame, text="Times (HH:MM, 24-hour, comma separated):", font=("Helvetica", 12)).pack(anchor=tk.W, pady=(10,0))
        
        self.time_var = tk.StringVar(value=", ".join(self.downloader.scheduled_times))
        time_entry = ctk.CTkEntry(time_inner_frame, textvariable=self.time_var, width=400)
        time_entry.pack(anchor=tk.W, pady=5)
        
        ctk.CTkLabel(time_inner_frame, text="Example: 09:30, 12:00, 15:30", font=("Helvetica", 11), text_color="gray").pack(anchor=tk.W)

        # Control Buttons
        button_frame = ctk.CTkFrame(self.dashboard_tab, fg_color="transparent")
        button_frame.pack(pady=15)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Start Scheduler",
            command=self.start_scheduler,
            width=140, height=40, corner_radius=50,
            font=("Helvetica", 13, "bold")
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="Stop Scheduler",
            command=self.stop_scheduler,
            state="disabled",
            width=140, height=40, corner_radius=50,
            font=("Helvetica", 13, "bold")
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        self.manual_btn = ctk.CTkButton(
            button_frame,
            text="Download Now",
            command=self.manual_download,
            width=160, height=40, corner_radius=50,
            font=("Helvetica", 13, "bold")
        )
        self.manual_btn.pack(side=tk.LEFT, padx=10)
        
        # Progress Bar Section
        progress_frame = ctk.CTkFrame(self.dashboard_tab)
        progress_frame.pack(fill=tk.X, pady=5, padx=5)
        
        ctk.CTkLabel(progress_frame, text="Main Progress", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        
        prog_inner = ctk.CTkFrame(progress_frame, fg_color="transparent")
        prog_inner.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(prog_inner, text="Main (NIFTY 50, NIFTY 500 & Indices):", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        self.progress_bar = ctk.CTkProgressBar(
            prog_inner,
            height=16,
            corner_radius=50,
            progress_color="#28a745" # Green
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5, fill=tk.X)
        
        self.progress_label = ctk.CTkLabel(
            prog_inner, 
            text="Ready", 
            font=("Helvetica", 12)
        )
        self.progress_label.pack(anchor=tk.W)
        
        info_label = ctk.CTkLabel(
            self.dashboard_tab,
            text="Downloaded files will be organized into folders by date inside your Downloads directory.",
            font=("Helvetica", 11),
            text_color="gray"
        )
        info_label.pack(pady=10)
        
        # --- SETTINGS TAB ---
        self.create_settings_widgets()

    def create_settings_widgets(self):
        settings_container = ctk.CTkFrame(self.settings_tab, fg_color="transparent")
        settings_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File Types Section
        file_frame = ctk.CTkFrame(settings_container)
        file_frame.pack(fill=tk.X, pady=5)
        ctk.CTkLabel(file_frame, text="Conversion Settings", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        
        file_inner = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_inner.pack(fill=tk.X, padx=10, pady=10)
        
        self.convert_excel_var = tk.BooleanVar(value=self.downloader.convert_to_excel)
        self.excel_check = ctk.CTkCheckBox(
            file_inner,
            text="Convert ALL downloaded CSV files to Excel (.xlsx)",
            variable=self.convert_excel_var,
            command=self.save_settings
        )
        self.excel_check.pack(anchor=tk.W, pady=5)
        
        ctk.CTkLabel(file_inner, text="Note: Converting to Excel requires 'pandas' and 'openpyxl'. Falls back to CSV if they fail.", font=("Helvetica", 11), text_color="gray").pack(anchor=tk.W)
        
        # Advanced Section
        adv_frame = ctk.CTkFrame(settings_container)
        adv_frame.pack(fill=tk.X, pady=15)
        ctk.CTkLabel(adv_frame, text="Advanced Logging", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        
        adv_inner = ctk.CTkFrame(adv_frame, fg_color="transparent")
        adv_inner.pack(fill=tk.X, padx=10, pady=10)
        
        self.log_btn = ctk.CTkButton(
            adv_inner,
            text="Open Log Folder",
            command=self.open_log_folder,
            width=150, corner_radius=50, fg_color="transparent", border_width=1, text_color=("black", "white")
        )
        self.log_btn.pack(anchor=tk.W, pady=5)
        
        ctk.CTkLabel(adv_inner, text=f"Logs are saved to: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')}", font=("Helvetica", 11), text_color="gray").pack(anchor=tk.W)

    def save_settings(self):
        self.downloader.convert_to_excel = self.convert_excel_var.get()
        self.downloader.save_config()
        self.update_progress(0, "Settings saved successfully", bar="main")

    def open_log_folder(self):
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        import subprocess
        if sys.platform == "win32":
            os.startfile(log_dir)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", log_dir])
        else:
            subprocess.Popen(["xdg-open", log_dir])

    def set_today(self):
        now = datetime.now()
        self.day_var.set(now.strftime("%d"))
        self.month_var.set(now.strftime("%B"))
        self.year_var.set(now.strftime("%Y"))
        
    def on_checkbox_toggle(self, changed_key=None):
        enabled = []
        for key, var in self.selected_downloads.items():
            if var.get():
                enabled.append(key)
        self.downloader.enabled_downloads = enabled
        self.downloader.save_config()
        
    def select_all(self):
        for key, var in self.selected_downloads.items():
            var.set(True)
        self.on_checkbox_toggle()
        
    def deselect_all(self):
        for key, var in self.selected_downloads.items():
            var.set(False)
        self.on_checkbox_toggle()
        
    def on_source_change(self, event):
        source = self.source_var.get()
        source_key = next((k for k, v in self.source_names.items() if v == source), None)
        if source_key:
            self.download_path_var.set(self.downloader.download_paths.get(source_key, ""))
            
    def browse_current_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path_var.set(folder)
            source = self.source_var.get()
            source_key = next((k for k, v in self.source_names.items() if v == source), None)
            if source_key:
                self.downloader.download_paths[source_key] = folder
                self.downloader.save_config()
                
    def get_selected_date(self):
        try:
            date_str = f"{self.day_var.get()} {self.month_var.get()} {self.year_var.get()}"
            return datetime.strptime(date_str, "%d %B %Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date selected")
            return None
            
    def manual_download(self):
        date = self.get_selected_date()
        if not date:
            return
            
        self.downloader.target_date = date
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="disabled")
        self.manual_btn.configure(state="disabled")
        
        threading.Thread(target=self.run_download_thread, args=('defaults',), daemon=True).start()
        
    def download_optionals(self):
        date = self.get_selected_date()
        if not date:
            return
            
        self.downloader.target_date = date
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="disabled")
        self.manual_btn.configure(state="disabled")
        
        threading.Thread(target=self.run_download_thread, args=('optionals',), daemon=True).start()
        
    def update_progress(self, value, message="", bar="main"):
        display_text = f"[{value}%] {message}" if message else f"{value}%"
        
        if bar == "main":
            self.progress_bar.set(value / 100.0)
            self.progress_label.configure(text=display_text)
        elif bar == "optional":
            self.opt_progress_bar.set(value / 100.0)
            self.opt_progress_label.configure(text=display_text)
            
        self.root.update_idletasks()
        
    def reset_progress(self):
        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready")
        self.opt_progress_bar.set(0)
        self.opt_progress_label.configure(text="Ready")
        
        if not getattr(self, 'is_running', False):
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            if not getattr(self.downloader, 'auto_mode', False):
                self.manual_btn.configure(state="normal")
        else:
            self.stop_btn.configure(state="normal")
            self.start_btn.configure(state="disabled")
            if not getattr(self.downloader, 'auto_mode', False):
                self.manual_btn.configure(state="normal")
            
    def validate_time(self, time_str):
        try:
            datetime.strptime(time_str.strip(), "%H:%M")
            return True
        except ValueError:
            return False
            
    def validate_times(self, times_str):
        times = [t.strip() for t in times_str.split(",")]
        return all(self.validate_time(t) for t in times)
        
    def start_scheduler(self):
        times_str = self.time_var.get()
        if not self.validate_times(times_str):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM (24-hour)")
            return
            
        self.downloader.scheduled_times = [t.strip() for t in times_str.split(",")]
        self.downloader.save_config()
        self.downloader.schedule_download()
        
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self.downloader.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.update_progress(100, f"Scheduler running (Next: {schedule.next_run()})")
        
    def stop_scheduler(self):
        self.downloader.is_running = False
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        schedule.clear()
        self.update_progress(0, "Scheduler stopped")
        
    def run_download_thread(self, mode='all'):
        try:
            self.downloader.download_data(mode)
        except Exception as e:
            logging.error(f"Error during download: {str(e)}")
            self.update_progress(100, f"Error: {str(e)}", bar="main" if mode != 'optionals' else "optional")
        finally:
            self.root.after(0, self.reset_progress)
            
    def toggle_auto_mode(self):
        self.downloader.auto_mode = self.auto_mode_var.get()
        self.downloader.save_config()
        if self.downloader.auto_mode:
            self.check_and_start_auto_mode()
        else:
            if getattr(self, 'is_running', False):
                self.stop_scheduler()

    def toggle_weekend_downloads(self):
        self.downloader.weekend_downloads_enabled = self.weekend_downloads_var.get()
        self.downloader.save_config()

    def check_and_start_auto_mode(self):
        now = datetime.now()
        current_time = now.time()
        start_time = datetime.strptime("08:00", "%H:%M").time()
        end_time = datetime.strptime("20:00", "%H:%M").time()

        if start_time <= current_time <= end_time:
            if not self.downloader.is_running:
                self.start_scheduler()
                self.update_progress(100, "[Auto Mode] Scheduler started automatically")
        else:
            self.update_progress(0, "[Auto Mode] Outside active hours (8 AM - 8 PM)")


def main():
    # Use CTk instead of Tk
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = DownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
"""

new_lines.append(gui_code)

with open('nse_downloader.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
