import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from plot_python import plot_heatmaps, get_specific_pointset, get_specific_discrepancy

# Color scheme
selectionbar_color = '#eff5f6'
sidebar_color = '#F5E1FD'
header_color = '#53366b'
visualisation_frame_color = "#ffffff"

class Heatmap_Generator(tk.Tk):
    def __init__(self):
        # Constants
        self.valid_symmetries = ["1a", "2e", "3c", "4a", "5b", "6i", "6he", "6hf", "6gf", "6ge", "6fe", 
                                "7d", "8c", "9f", "9ed", "10d", "11g", "11fe", "11fd", "11ed", 
                                "12d", "13d", "14e", "15d", "16d", "17f", "17ed"]
        
        # UI Setup
        tk.Tk.__init__(self)
        self.title("Heatmap Generator")
        self.geometry("1100x700")
        self.resizable(False, False)
        self.configure(bg=selectionbar_color)
        
        try:
            self.icon = tk.PhotoImage(file="test/logo_icon.png")
            self.iconphoto(True, self.icon)
        except tk.TclError:
            print("Warning: Could not load icon image")

        # Main layout using grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Initialize UI components
        self.initialize_left_sidebar()
        self.initialize_right_sidebar()
        self.initialize_input_frame()
        self.plot_frame = None
        self.current_figure = None

    def initialize_left_sidebar(self):
        """Initialize the left sidebar with consistent padding and styling"""
        self.left_sidebar = tk.Frame(self, 
                                   bg=sidebar_color, 
                                   width=200, 
                                   height=700)
        self.left_sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
        
        self.brand_frame = tk.Frame(self.left_sidebar, 
                                  bg=sidebar_color)
        self.brand_frame.pack(pady=20, fill="x", padx=10)
        
        header_frame = tk.Frame(self.brand_frame, bg=sidebar_color)
        header_frame.pack(fill="x")
        
        if hasattr(self, 'icon'):
            small_icon = self.icon.subsample(12, 12)
            icon_label = tk.Label(header_frame, 
                                image=small_icon, 
                                bg=sidebar_color)
            icon_label.image = small_icon
            icon_label.pack(side="left", padx=(0, 5))
        
        tk.Label(header_frame, 
                text="Heatmap Generator", 
                bg=sidebar_color, 
                font=("Arial", 14, "bold")).pack(side="left")
        
        # Settings section
        self.settings_label = tk.Label(self.left_sidebar,
                                     text="Settings",
                                     bg=sidebar_color,
                                     font=("Arial", 12, "bold"),
                                     anchor="w")
        self.settings_label.pack(fill="x", padx=10, pady=(10, 5))

        tk.Label(self.left_sidebar, text="Colormap", bg=sidebar_color, font=("Arial", 10), anchor="w").pack(fill="x", padx=20, pady=(2, 0))
        self.colormap_combo = ttk.Combobox(self.left_sidebar, 
                                         values=["viridis", "plasma", "inferno", "magma", "seismic"], 
                                         state="readonly", 
                                         width=15)
        self.colormap_combo.set("seismic")
        self.colormap_combo.pack(fill="x", padx=20, pady=2)

        tk.Label(self.left_sidebar, text="Interpolation", bg=sidebar_color, font=("Arial", 10), anchor="w").pack(fill="x", padx=20, pady=(2, 0))
        self.interpolation_combo = ttk.Combobox(self.left_sidebar, 
                                              values=["none", "nearest", "bilinear", "bicubic", "gaussian"], 
                                              state="readonly", 
                                              width=15)
        self.interpolation_combo.set("gaussian")
        self.interpolation_combo.pack(fill="x", padx=20, pady=2)

        tk.Label(self.left_sidebar, text="Resolution", bg=sidebar_color, font=("Arial", 10), anchor="w").pack(fill="x", padx=20, pady=(2, 0))
        self.resolution_combo = ttk.Combobox(self.left_sidebar, 
                                           values=["25", "50", "100", "250", "500", "1000"], 
                                           state="readonly", 
                                           width=15)
        self.resolution_combo.set("100")
        self.resolution_combo.pack(fill="x", padx=20, pady=2)

        self.remove_duplicates_var = tk.BooleanVar(value=False)
        self.remove_duplicates_check = tk.Checkbutton(self.left_sidebar,
                                                    text="Remove duplicates",
                                                    variable=self.remove_duplicates_var,
                                                    bg=sidebar_color,
                                                    font=("Arial", 10),
                                                    anchor="w")
        self.remove_duplicates_check.pack(fill="x", padx=20, pady=2)

        tk.Label(self.left_sidebar, text="Decimal places", bg=sidebar_color, font=("Arial", 10), anchor="w").pack(fill="x", padx=20, pady=(2, 0))
        self.decimal_places_combo = ttk.Combobox(self.left_sidebar, 
                                               values=["1", "2", "3", "4", "5", "6", "7"], 
                                               state="readonly", 
                                               width=15)
        self.decimal_places_combo.set("7")
        self.decimal_places_combo.pack(fill="x", padx=20, pady=2)

        self.save_button = tk.Button(self.left_sidebar,
                                   command=self.save_to_pdf,
                                   text="Save to PDF",
                                   bg=header_color,
                                   fg="white")
        self.save_button.pack(fill="x", padx=20, pady=(10, 0))

    def initialize_right_sidebar(self):
        """Initialize the right sidebar with consistent padding and styling"""
        self.right_sidebar = tk.Frame(self, 
                                    bg=sidebar_color, 
                                    width=200, 
                                    height=700)
        self.right_sidebar.grid(row=0, column=2, rowspan=2, sticky="ns")
        
        tk.Label(self.right_sidebar,
                text="Coordinates",
                bg=sidebar_color,
                font=("Arial", 14, "bold")).pack(pady=(20, 5), fill="x", padx=10)
        
        # Replace Label with Text widget for scrollable output
        self.coord_text = tk.Text(self.right_sidebar,
                                height=10,  # Adjust height as needed
                                width=25,   # Adjust width as needed
                                bg=sidebar_color,
                                font=("Arial", 10),
                                state="disabled")  # Read-only by default
        self.coord_text.pack(fill="x", padx=10, pady=5)

    def initialize_input_frame(self):
        """Initialize the input controls frame"""
        input_frame = tk.Frame(self, 
                             bg=selectionbar_color)
        input_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        input_frame.grid_columnconfigure(0, weight=0)
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(2, weight=0)
        
        self.entry_label = tk.Label(input_frame, 
                                  text="Choose symmetry: ", 
                                  bg=selectionbar_color)
        self.entry_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.user_entry = ttk.Combobox(input_frame, 
                                     width=17, 
                                     values=self.valid_symmetries)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        self.user_entry.set("")
        
        self.plot_button = tk.Button(input_frame, 
                                   command=self.get_plot, 
                                   text="Plot Heatmap",
                                   bg=header_color,
                                   fg="white")
        self.plot_button.grid(row=0, column=2, padx=5, pady=5)

    def save_to_pdf(self):
        """Save the current heatmap to a PDF file"""
        if self.current_figure:
            file_path = tk.filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Heatmap as PDF"
            )
            if file_path:
                self.current_figure.savefig(file_path, format="pdf", bbox_inches="tight")
                print(f"Heatmap saved to {file_path}")
        else:
            print("No heatmap to save. Generate a plot first.")

    def on_heatmap_click(self, event):
        """Display coordinates and pointset info on heatmap click"""
        if event.inaxes and self.current_figure:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                decimal_places = int(self.decimal_places_combo.get())
                pointset = get_specific_pointset(self.user_entry.get(), 
                                               self.remove_duplicates_var.get(), 
                                               x, y, decimal_places)
                discrepancy = get_specific_discrepancy(pointset)

                # Update the Text widget
                self.coord_text.config(state="normal")  # Enable editing
                self.coord_text.delete(1.0, tk.END)     # Clear previous content
                self.coord_text.insert(tk.END, 
                    f"Symmetry: {self.user_entry.get()}\n"
                    f"Pointset at ({x:.{decimal_places}f}, {y:.{decimal_places}f}):\n{pointset}\n"
                    f"Max discrepancy: {discrepancy:.{decimal_places}f}")
                self.coord_text.config(state="disabled")  # Back to read-only

    def get_plot(self):
        """Generate and display the heatmap"""
        symmetry = self.user_entry.get().lower()
        
        if self.plot_frame:
            self.plot_frame.destroy()
            
        self.plot_frame = tk.Frame(self, 
                                 bg=visualisation_frame_color)
        self.plot_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        self.current_figure = plot_heatmaps(symmetry, self.interpolation_combo.get(), self.colormap_combo.get(), 
                                           int(self.resolution_combo.get()), self.remove_duplicates_var.get(), 
                                           int(self.decimal_places_combo.get()))
        
        canvas = FigureCanvasTkAgg(figure=self.current_figure, 
                                 master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        canvas.mpl_connect("button_press_event", self.on_heatmap_click)

if __name__ == "__main__":
    root = Heatmap_Generator()
    root.mainloop()