import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot_python import plot_heatmaps, get_specific_pointset, get_specific_discrepancy

# Can have only 20 figures at once or else memory rip

# Global variables for multiple heatmaps
heatmaps = []  # Now stores tuples of (figure, symmetry)
current_heatmap_idx = 0
canvas = None

def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        # Get current symmetry from heatmaps list
        current_symmetry = heatmaps[current_heatmap_idx][1]
        try:
            decimal_places = int(decimal_entry.get())
            if not 2 <= decimal_places <= 7:
                decimal_places = 2
        except ValueError:
            decimal_places = 2

        remove_duplicates_choice = duplicates_var.get()
        
        pointset = get_specific_pointset(current_symmetry, remove_duplicates_var=remove_duplicates_choice, 
                                       x=event.xdata, y=event.ydata, decimal_points=decimal_places)
        discrepancy = get_specific_discrepancy(pointset)

        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, 
            f"Symmetry: {current_symmetry}\n"
            f"Pointset at ({event.xdata:.{decimal_places}f}, {event.ydata:.{decimal_places}f}):\n{pointset}\n"
            f"Max discrepancy: {discrepancy:.{decimal_places}f}")
        text_output.config(state=tk.DISABLED)

def update_heatmap_display():
    global canvas, current_heatmap_idx
    if canvas:
        canvas.get_tk_widget().destroy()
    
    if heatmaps:
        current_fig, current_symmetry = heatmaps[current_heatmap_idx]
        canvas = FigureCanvasTkAgg(current_fig, main_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2, column=0, columnspan=2, sticky="nsew")
        canvas.mpl_connect("button_press_event", on_click)
        update_nav_buttons()

def update_nav_buttons():
    prev_button.config(state='normal' if current_heatmap_idx > 0 else 'disabled')
    next_button.config(state='normal' if current_heatmap_idx < len(heatmaps) - 1 else 'disabled')

def prev_heatmap():
    global current_heatmap_idx
    if current_heatmap_idx > 0:
        current_heatmap_idx -= 1
        update_heatmap_display()

def next_heatmap():
    global current_heatmap_idx
    if current_heatmap_idx < len(heatmaps) - 1:
        current_heatmap_idx += 1
        update_heatmap_display()

def update_plot():
    global heatmaps, current_heatmap_idx
    heatmaps.clear()
    current_heatmap_idx = 0
    
    cmap_choice = cmap_var.get()
    interpolation_choice = interpolation_var.get()
    selected_resolution = int(resolution_var.get())
    remove_duplicates_choice = duplicates_var.get()
    
    try:
        decimal_places_choice = int(decimal_entry.get())
        if not 1 <= decimal_places_choice <= 7:
            raise ValueError
    except ValueError:
        decimal_places_choice = 2

    # Store both figure and symmetry in heatmaps list
    for input_text, var in check_vars.items():
        if var.get():
            fig = plot_heatmaps(
                input_text,
                selected_interpolation=interpolation_choice,
                selected_cmap=cmap_choice,
                resolution=selected_resolution,
                remove_duplicates=remove_duplicates_choice,
                decimal_places=decimal_places_choice
            )
            heatmaps.append((fig, input_text))  # Store tuple of (figure, symmetry)
    
    if heatmaps:
        update_heatmap_display()

# Create main window
root = tk.Tk()
root.title("Heatmap Plotting")
root.geometry("1000x750")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=5, font=("Arial", 10))
style.configure("Sidebar.TLabel", background="#e0e0e0", font=("Arial", 10))

root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)

sidebar = ttk.Frame(root, padding=10, relief="flat", style="Sidebar.TFrame")
sidebar.grid(row=0, column=1, sticky="ns")

nav_frame = ttk.Frame(main_frame)
nav_frame.grid(row=0, column=0, columnspan=2, pady=5)
prev_button = ttk.Button(nav_frame, text="← Previous", command=prev_heatmap)
prev_button.grid(row=0, column=0, padx=5)
button = ttk.Button(nav_frame, text="Generate Plots", command=update_plot)
button.grid(row=0, column=1, padx=5)
next_button = ttk.Button(nav_frame, text="Next →", command=next_heatmap)
next_button.grid(row=0, column=2, padx=5)

text_output = tk.Text(main_frame, height=6, wrap="word", font=("Arial", 11), bg="#ffffff", relief="flat", borderwidth=1)
text_output.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
text_output.config(state=tk.DISABLED)

# Sidebar Settings
settings_label = ttk.Label(sidebar, text="Graph Settings", font=("Arial", 12, "bold"), style="Sidebar.TLabel")
settings_label.grid(row=0, column=0, pady=(0, 10))

ttk.Label(sidebar, text="Colormap:", style="Sidebar.TLabel").grid(row=1, column=0, sticky="w", pady=2)
cmap_var = tk.StringVar(value="seismic")
cmap_dropdown = ttk.Combobox(sidebar, textvariable=cmap_var, 
                            values=["seismic", "viridis", "plasma", "coolwarm", "gray"], 
                            state='readonly')
cmap_dropdown.grid(row=2, column=0, pady=2, sticky="ew")

ttk.Label(sidebar, text="Interpolation:", style="Sidebar.TLabel").grid(row=3, column=0, sticky="w", pady=2)
interpolation_var = tk.StringVar(value="gaussian")
interpolation_dropdown = ttk.Combobox(sidebar, textvariable=interpolation_var, 
                                    values=["gaussian", "nearest", "bilinear", "bicubic"],
                                    state='readonly')
interpolation_dropdown.grid(row=4, column=0, pady=2, sticky="ew")

ttk.Label(sidebar, text="Resolution:", style="Sidebar.TLabel").grid(row=5, column=0, sticky="w", pady=2)
resolution_var = tk.StringVar(value="100")
resolution_dropdown = ttk.Combobox(sidebar, textvariable=resolution_var, 
                                 values=[10, 25, 50, 100, 250, 500, 1000],
                                 state='readonly')
resolution_dropdown.grid(row=6, column=0, pady=2, sticky="ew")

ttk.Label(sidebar, text="Decimal Places (1-7):", style="Sidebar.TLabel").grid(row=7, column=0, sticky="w", pady=2)
decimal_entry = tk.Entry(sidebar)
decimal_entry.grid(row=8, column=0, pady=2, sticky="ew")
decimal_entry.insert(0, "7")

duplicates_var = tk.BooleanVar(value=False)
duplicates_checkbox = ttk.Checkbutton(sidebar, text="Exclude Duplicate Points", variable=duplicates_var)
duplicates_checkbox.grid(row=9, column=0, pady=5, sticky="w")

valid_inputs_label = ttk.Label(sidebar, font=("Arial", 12, "bold"), text="Select Symmetries:", style="Sidebar.TLabel")
valid_inputs_label.grid(row=10, column=0, pady=(10, 2), sticky="w")

canvas_frame = tk.Canvas(sidebar, width=150, height=200)
scrollbar = ttk.Scrollbar(sidebar, orient="vertical", command=canvas_frame.yview)
checkbox_frame = ttk.Frame(canvas_frame)
canvas_frame.configure(yscrollcommand=scrollbar.set)

scrollbar.grid(row=11, column=1, sticky="ns")
canvas_frame.grid(row=11, column=0, sticky="nsew")
canvas_frame.create_window((0, 0), window=checkbox_frame, anchor="nw")

valid_inputs = "1a, 2e, 3c, 4a, 5b, 6i, 6he, 6hf, 6gf, 6ge, 6fe, 7d, 8c, 9f, 9ed, 10d, 11g, 11fe, 11fd, 11ed, 12d, 13d, 14e, 15d, 16d, 17f, 17ed"
check_vars = {}
for i, input_val in enumerate(valid_inputs.split(", ")):
    var = tk.BooleanVar()
    check_vars[input_val] = var
    ttk.Checkbutton(checkbox_frame, text=input_val, variable=var).grid(row=i, column=0, sticky="w", padx=5, pady=2)

def configure_scroll_region(event):
    canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))

checkbox_frame.bind("<Configure>", configure_scroll_region)

root.mainloop()