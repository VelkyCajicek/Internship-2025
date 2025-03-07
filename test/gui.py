import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plot_python import plot_heatmaps, get_specific_pointset

def on_click(event):
    """Displays the clicked coordinates and the corresponding pointset in a scrollable text box."""
    if event.xdata is not None and event.ydata is not None:
        input_text = entry.get()  # Get user input from the entry field
        pointset = get_specific_pointset(input_text, event.xdata, event.ydata)

        # Clear previous text and insert new output
        text_output.config(state=tk.NORMAL)  # Enable editing
        text_output.delete(1.0, tk.END)  # Clear previous content
        text_output.insert(tk.END, f"Pointset at ({event.xdata:.2f}, {event.ydata:.2f}):\n{pointset}")
        text_output.config(state=tk.DISABLED)  # Disable editing again

def update_plot():
    """Updates the heatmap when the button is clicked."""
    input_text = entry.get()  # Get input from entry field
    fig = plot_heatmaps([input_text])  # Generate new figure

    global canvas
    if canvas:  
        canvas.get_tk_widget().destroy()  # Remove old plot

    # Embed the new figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

    # Connect the click event to the figure
    fig.canvas.mpl_connect("button_press_event", on_click)

# Create main application window
root = tk.Tk()
root.title("Heatmap Plotting")
root.geometry("600x700")  # Increased height for text output

# Input field
entry = tk.Entry(root)
entry.pack()

# Button to update plot
button = ttk.Button(root, text="Plot", command=update_plot)
button.pack()

# Scrollable text widget to display clicked coordinates and pointset
text_output = tk.Text(root, height=6, wrap="word", font=("Arial", 12))
text_output.pack(fill="both", expand=True)
text_output.config(state=tk.DISABLED)  # Disable editing

canvas = None  # Initialize canvas as None, no initial figure

root.mainloop()