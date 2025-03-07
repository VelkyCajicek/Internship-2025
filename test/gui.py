import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot_python import plot_heatmaps, get_specific_pointset, get_specific_discrepancy

def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        input_text = entry.get()  # Get user input

        # Get decimal rounding (default to 2 if invalid)
        try:
            decimal_places = int(decimal_entry.get())
            if decimal_places < 2 or decimal_places > 7:
                decimal_places = 2  # Default fallback
        except ValueError:
            decimal_places = 2  # Default fallback

        # Fetch the pointset with user-defined settings
        pointset = get_specific_pointset(input_text, event.xdata, event.ydata, decimal_points=decimal_places)
        
        discrepancy = get_specific_discrepancy(pointset)

        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, 
            f"Pointset at ({event.xdata:.{decimal_places}f}, {event.ydata:.{decimal_places}f}):\n{pointset}\n"
            f"Max discrepancy: {discrepancy:.{decimal_places}f}")
        text_output.config(state=tk.DISABLED)

def update_plot():
    input_text = entry.get()
    cmap_choice = cmap_var.get()  # Get colormap choice
    interpolation_choice = interpolation_var.get()  # Get interpolation choice
    save_pdf = save_var.get()  # Check if the user wants to save the plot
    remove_duplicates_choice = duplicates_var.get()
    decimal_places_choice = int(decimal_entry.get())

    # Validate resolution input
    try:
        selected_resolution = int(resolution_entry.get())
        if selected_resolution < 10 or selected_resolution > 1000:
            raise ValueError
        resolution_label.config(text="Resolution (10-1000):", fg="black")
    except ValueError:
        resolution_label.config(text="Resolution (10-1000): *Invalid*", fg="red")
        return

    # Generate the heatmap with user settings
    fig = plot_heatmaps(
        [input_text], selected_interpolation=interpolation_choice, selected_cmap=cmap_choice, 
        resolution=selected_resolution, create_pdf_files=save_pdf, remove_duplicates=remove_duplicates_choice,
        decimal_places=decimal_places_choice
    )

    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()

    # Embed the new figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, main_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=0, sticky="nsew")  # Ensuring it expands properly

    # Connect click event
    fig.canvas.mpl_connect("button_press_event", on_click)

# Create main application window
root = tk.Tk()
root.title("Heatmap Plotting")
root.geometry("900x700")  # Increased width for settings panel

# Configure grid layout
root.columnconfigure(0, weight=3)  # Main frame gets more space
root.columnconfigure(1, weight=1)  # Sidebar gets less space
root.rowconfigure(0, weight=1)

# Main Frame
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

# Sidebar for settings
sidebar = tk.Frame(root, padx=10, pady=10, relief="sunken", borderwidth=2)
sidebar.grid(row=0, column=1, sticky="ns")

# Configure main frame grid to expand
main_frame.rowconfigure(3, weight=1)  # Heatmap should expand

# Input field
entry_label = tk.Label(main_frame, text="Enter symmetry:")
entry_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry = tk.Entry(main_frame)
entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Button to update plot
button = ttk.Button(main_frame, text="Plot", command=update_plot)
button.grid(row=1, column=0, columnspan=2, pady=5)

# Scrollable text widget for pointset info
text_output = tk.Text(main_frame, height=6, wrap="word", font=("Arial", 12))
text_output.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
text_output.config(state=tk.DISABLED)

canvas = None  # Initialize empty plot

# Settings Panel (Sidebar)
tk.Label(sidebar, text="Graph Settings", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)

# Colormap Dropdown
tk.Label(sidebar, text="Colormap:").grid(row=1, column=0, pady=2, sticky="w")
cmap_var = tk.StringVar(value="seismic")  # Default colormap
cmap_dropdown = ttk.Combobox(sidebar, textvariable=cmap_var, values=["seismic", "viridis", "plasma", "coolwarm", "gray"])
cmap_dropdown.grid(row=2, column=0, pady=2, sticky="ew")

# Interpolation Dropdown
tk.Label(sidebar, text="Interpolation:").grid(row=3, column=0, pady=2, sticky="w")
interpolation_var = tk.StringVar(value="gaussian")  # Default interpolation
interpolation_dropdown = ttk.Combobox(sidebar, textvariable=interpolation_var, values=["gaussian", "nearest", "bilinear", "bicubic"])
interpolation_dropdown.grid(row=4, column=0, pady=2, sticky="ew")

# Resolution Input
resolution_label = tk.Label(sidebar, text="Resolution (10-1000):")
resolution_label.grid(row=5, column=0, pady=2, sticky="w")
resolution_entry = tk.Entry(sidebar)
resolution_entry.grid(row=6, column=0, pady=2, sticky="ew")
resolution_entry.insert(0, "100")  # Default resolution value

# Decimal Rounding Input
tk.Label(sidebar, text="Decimal Places (1-7):").grid(row=7, column=0, pady=2, sticky="w")
decimal_entry = tk.Entry(sidebar)
decimal_entry.grid(row=8, column=0, pady=2, sticky="ew")
decimal_entry.insert(0, "2")  # Default decimal places value

# Include Duplicate Points Option
duplicates_var = tk.BooleanVar(value=False)
duplicates_checkbox = tk.Checkbutton(sidebar, text="Include Duplicate Points", variable=duplicates_var)
duplicates_checkbox.grid(row=9, column=0, pady=5)

# Save as PDF Option
save_var = tk.BooleanVar(value=False)
save_checkbox = tk.Checkbutton(sidebar, text="Save as PDF", variable=save_var)
save_checkbox.grid(row=10, column=0, pady=5)

root.mainloop()
