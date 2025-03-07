import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot_python import plot_heatmaps, get_specific_pointset, get_specific_discrepancy  # Assuming these are defined elsewhere

# Event handler for clicking on the heatmap
def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        input_text = entry.get()
        try:
            decimal_places = int(decimal_entry.get())
            if not 2 <= decimal_places <= 7:
                decimal_places = 2
        except ValueError:
            decimal_places = 2

        pointset = get_specific_pointset(input_text, event.xdata, event.ydata, decimal_points=decimal_places)
        discrepancy = get_specific_discrepancy(pointset)

        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, 
            f"Pointset at ({event.xdata:.{decimal_places}f}, {event.ydata:.{decimal_places}f}):\n{pointset}\n"
            f"Max discrepancy: {discrepancy:.{decimal_places}f}")
        text_output.config(state=tk.DISABLED)

# Update the heatmap based on user settings
def update_plot():
    input_text = entry.get()
    cmap_choice = cmap_var.get()
    interpolation_choice = interpolation_var.get()
    save_pdf = save_var.get()
    remove_duplicates_choice = duplicates_var.get()
    try:
        decimal_places_choice = int(decimal_entry.get())
        if not 1 <= decimal_places_choice <= 7:
            raise ValueError
    except ValueError:
        decimal_places_choice = 2

    try:
        selected_resolution = int(resolution_entry.get())
        if not 10 <= selected_resolution <= 1000:
            raise ValueError
        resolution_label.config(text="Resolution (10-1000):", style="Sidebar.TLabel")
    except ValueError:
        resolution_label.config(text="Resolution (10-1000): *Invalid*", style="Error.TLabel")
        return

    fig = plot_heatmaps(
        [input_text], selected_interpolation=interpolation_choice, selected_cmap=cmap_choice, 
        resolution=selected_resolution, create_pdf_files=save_pdf, remove_duplicates=remove_duplicates_choice,
        decimal_places=decimal_places_choice
    )

    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, main_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=0, columnspan=2, sticky="nsew")
    fig.canvas.mpl_connect("button_press_event", on_click)

# Create main window
root = tk.Tk()
root.title("Heatmap Plotting")
root.geometry("1000x750")  # Fixed size
root.resizable(False, False)  # Lock window size
root.configure(bg="#f0f0f0")  # Light gray background

# Apply a modern theme
style = ttk.Style()
style.theme_use("clam")  # Clean, modern theme
style.configure("TButton", padding=5, font=("Arial", 10))
style.configure("Sidebar.TLabel", background="#e0e0e0", font=("Arial", 10))
style.configure("Error.TLabel", background="#e0e0e0", font=("Arial", 10), foreground="red")
style.configure("Sidebar.TFrame", background="#e0e0e0")  # Subtle gray for sidebar

# Configure grid layout
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# Main Frame
main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(3, weight=1)

# Sidebar Frame
sidebar = ttk.Frame(root, padding=10, relief="flat", style="Sidebar.TFrame")
sidebar.grid(row=0, column=1, sticky="ns")

# Input Section
entry_label = ttk.Label(main_frame, text="Enter symmetry:")
entry_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry = ttk.Entry(main_frame)
entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Plot Button
button = ttk.Button(main_frame, text="Generate Plot", command=update_plot, style="TButton")
button.grid(row=1, column=0, columnspan=2, pady=10)

# Text Output
text_output = tk.Text(main_frame, height=6, wrap="word", font=("Arial", 11), bg="#ffffff", relief="flat", borderwidth=1)
text_output.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
text_output.config(state=tk.DISABLED)

canvas = None  # Placeholder for heatmap

# Sidebar Settings
settings_label = ttk.Label(sidebar, text="Graph Settings", font=("Arial", 12, "bold"), style="Sidebar.TLabel")
settings_label.grid(row=0, column=0, pady=(0, 10))

# Colormap
ttk.Label(sidebar, text="Colormap:", style="Sidebar.TLabel").grid(row=1, column=0, sticky="w", pady=2)
cmap_var = tk.StringVar(value="seismic")
cmap_dropdown = ttk.Combobox(sidebar, textvariable=cmap_var, values=["seismic", "viridis", "plasma", "coolwarm", "gray"])
cmap_dropdown.grid(row=2, column=0, pady=2, sticky="ew")

# Interpolation
ttk.Label(sidebar, text="Interpolation:", style="Sidebar.TLabel").grid(row=3, column=0, sticky="w", pady=2)
interpolation_var = tk.StringVar(value="gaussian")
interpolation_dropdown = ttk.Combobox(sidebar, textvariable=interpolation_var, values=["gaussian", "nearest", "bilinear", "bicubic"])
interpolation_dropdown.grid(row=4, column=0, pady=2, sticky="ew")

# Resolution
resolution_label = ttk.Label(sidebar, text="Resolution (10-1000):", style="Sidebar.TLabel")
resolution_label.grid(row=5, column=0, sticky="w", pady=2)
resolution_entry = ttk.Entry(sidebar)
resolution_entry.grid(row=6, column=0, pady=2, sticky="ew")
resolution_entry.insert(0, "100")

# Decimal Places
ttk.Label(sidebar, text="Decimal Places (1-7):", style="Sidebar.TLabel").grid(row=7, column=0, sticky="w", pady=2)
decimal_entry = tk.Entry(sidebar)
decimal_entry.grid(row=8, column=0, pady=2, sticky="ew")
decimal_entry.insert(0, "2")

# Checkboxes
duplicates_var = tk.BooleanVar(value=False)
duplicates_checkbox = ttk.Checkbutton(sidebar, text="Include Duplicate Points", variable=duplicates_var)
duplicates_checkbox.grid(row=9, column=0, pady=5, sticky="w")

save_var = tk.BooleanVar(value=False)
save_checkbox = ttk.Checkbutton(sidebar, text="Save as PDF", variable=save_var)
save_checkbox.grid(row=10, column=0, pady=5, sticky="w")

valid_inputs_label = ttk.Label(sidebar, text="Valid Symmetry Inputs:", font=("Arial", 12, "bold"), style="Sidebar.TLabel")
valid_inputs_label.grid(row=11, column=0, pady=(10, 2), sticky="w")

valid_inputs = "1a, 2e, 3c, 4a, 5b, 6i, 6he, 6hf, 6gf, 6ge, 6fe, 7d, 8c, 9f, 9ed, 10d, 11g, 11fe, 11fd, 11ed, 12d, 13d, 14e, 15d, 16d, 17f, 17ed"
valid_inputs_text = tk.Text(sidebar, height=5, width=20, wrap="word", font=("Arial", 10), bg="#e0e0e0", relief="flat", borderwidth=0)
valid_inputs_text.grid(row=12, column=0, pady=2, sticky="ew")
valid_inputs_text.insert(tk.END, valid_inputs)
valid_inputs_text.config(state=tk.DISABLED)  # Read-only

# Add scrollbar for valid inputs
scrollbar = ttk.Scrollbar(sidebar, orient="vertical", command=valid_inputs_text.yview)
scrollbar.grid(row=12, column=1, sticky="ns")
valid_inputs_text.config(yscrollcommand=scrollbar.set)

# Start the application
root.mainloop()