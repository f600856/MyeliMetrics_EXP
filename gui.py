import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from data_cleanup import data_cleanup
from fiber_diameter import process_fiber_data
from g_ratio import calculate_g_ratio
from scatter_plot import generate_scatter_plots
from sorted_fiber import sort_fiber_diameter
from display_data import display_dataframe
from PIL import Image, ImageTk
from  subset_create import create_and_save_subsets
import os 
from histogram import plot_all_g_ratio_frequencies,analyze_g_ratio
from modality_test import process_and_plot_kde

# Initialize a global DataFrame
df = None
# Function to load file
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            messagebox.showinfo("Success", "File successfully loaded!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

# Function to handle data cleanup
def cleanup_data_handler():
    global df
    if df is not None:
        experiments = [('EXP1_Ax', 'EXP1_My'), ('EXP2_Ax', 'EXP2_My'), ('EXP3_Ax', 'EXP3_My')]
        status, message = data_cleanup(df, experiments)
        if status == "Success":
            messagebox.showinfo(status, message)
        else:
            messagebox.showerror(status, message)
    else:
        messagebox.showerror("Error", "No data loaded.")

# Function to handle fiber data processing
def process_fiber_data_handler():
    global df
    if df is not None:
        experiments = [('EXP1_Ax', 'EXP1_My'), ('EXP2_Ax', 'EXP2_My'), ('EXP3_Ax', 'EXP3_My')]
        df = process_fiber_data(df, experiments)
        messagebox.showinfo("Success", "Fiber data processed successfully.")
    else:
        messagebox.showerror("Error", "No data loaded to process.")
    
def calculate_g_ratio_handler():
    global df
    if df is not None:
        experiments = [('EXP1_Ax', 'EXP1_My'), ('EXP2_Ax', 'EXP2_My'), ('EXP3_Ax', 'EXP3_My'),('EXP4_Ax', 'EXP4_My')]
        df = calculate_g_ratio(df, experiments)
        messagebox.showinfo("Success", "G-ratio calculated successfully.")
    else:
        messagebox.showerror("Error", "No data loaded to calculate G-ratio.")

def show_scatter_plots_handler():
    global df
    if df is not None:
        experiments = [
            ('FiberDiameter_EXP1', 'EXP1_Ax'),
            ('FiberDiameter_EXP2', 'EXP2_Ax'),
            ('FiberDiameter_EXP3', 'EXP3_Ax'),
            
        ]
        generate_scatter_plots(df, experiments)
    else:
        messagebox.showerror("Error", "No data loaded to generate scatter plots.")


def sort_fiber_diameter_handler():
    global df
    if df is not None:
        experiments = [
            ('FiberDiameter_EXP1', 'EXP1_Ax', 'EXP1_My', 'G-Ratio_EXP1'),
            ('FiberDiameter_EXP2', 'EXP2_Ax', 'EXP2_My', 'G-Ratio_EXP2'),
            ('FiberDiameter_EXP3', 'EXP3_Ax', 'EXP3_My', 'G-Ratio_EXP3'),

        ]
        df = sort_fiber_diameter(df, experiments)
        messagebox.showinfo("Success", "Data sorted by 'FiberDiameter' for each experiment.")
    else:
        messagebox.showerror("Error", "No data loaded to sort.")


# Sort and display 
def sort_and_display_handler():
    global df
    if df is not None:
        experiments = [('FiberDiameter_EXP1', 'EXP1_Ax', 'EXP1_My', 'G-Ratio_EXP1'),
                       ('FiberDiameter_EXP2', 'EXP2_Ax', 'EXP2_My', 'G-Ratio_EXP2'),
                       ('FiberDiameter_EXP3', 'EXP3_Ax', 'EXP3_My', 'G-Ratio_EXP3'),
                        
                    ]
        sorted_df = sort_fiber_diameter(df, experiments)
        display_dataframe(sorted_df, root)
    else:
        messagebox.showerror("Error", "No data loaded.")

def save_sorted_data():
    global df
    if df is not None:
        # Open a file dialog to ask for the save location and file name
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")])
        if file_path:
            try:
                # Use ExcelWriter to save the DataFrame to the chosen path
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                messagebox.showinfo("Success", f"Data saved successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    else:
        messagebox.showerror("Error", "No data to save.")




def process_and_save_subsets_command():
    global df
    if df is not None:
        output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if output_path:
            fiber_size_ranges =[ (0.46,0.71), (0.73,0.8), (0.8,0.87), (0.88,0.97), (0.98,1.14),(1.14,1.8)]
            create_and_save_subsets(df, fiber_size_ranges, output_path)
            messagebox.showinfo("Success", "Data subsets saved successfully.")
        else:
            messagebox.showerror("Error", "No output file specified.")
    else:
        messagebox.showerror("Error", "No data loaded.")


'''def analyze_g_ratio_handler():
    input_file_path = filedialog.askopenfilename(title="Open Excel file for analysis", filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls")])
    output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save G-Ratio analysis results as")
    histogram_folder_path = filedialog.askdirectory(title="Select folder to save histograms")

    if input_file_path and output_file_path and histogram_folder_path:
        try:
            analyze_g_ratio(input_file_path, output_file_path, histogram_folder_path)  
            plot_all_g_ratio_frequencies(input_file_path, histogram_folder_path, display=True)
            messagebox.showinfo("Success", "G-Ratio analysis and histograms saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please ensure you have selected an Excel file, an output file, and a histogram output folder.")'''

def analyze_g_ratio_handler():
    messagebox.showinfo("Select File", "Please select the subsets file for G-Ratio analysis.")
    input_file_path = filedialog.askopenfilename(title="Open Excel file for analysis", filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls")])
    
    if not input_file_path:
        messagebox.showerror("Error", "No input file selected. Please select a file to continue.")
        return

    messagebox.showinfo("Save Results", "Please select or create a file and then save the statistical analysis results.")
    output_file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save G-Ratio analysis results as")
    
    if not output_file_path:
        messagebox.showerror("Error", "No output file selected. Please select a file to save the results.")
        return

    
    code_directory = os.path.dirname(os.path.realpath(__file__))
    histogram_folder_path = os.path.join(code_directory, "Histograms")
    os.makedirs(histogram_folder_path, exist_ok=True)  
    try:
        if os.path.exists(output_file_path):
            
            os.remove(output_file_path)  

        analyze_g_ratio(input_file_path, output_file_path, histogram_folder_path, results_sheet_name="Statistical_analysis")
        plot_all_g_ratio_frequencies(input_file_path, histogram_folder_path, display=False)
        messagebox.showinfo("Success", "G-Ratio analysis and histograms saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    



def modality_test_handler():
   
    messagebox.showinfo("Open File", "Please open subsets file for the Modality Check.")
    
    
    file_path = filedialog.askopenfilename(title="Open File for Modality Check", filetypes=[("Excel files", "*.xlsx;*.xls")])
    
    if not file_path:
        messagebox.showerror("Error", "No file has been loaded. Please load a file first.")
        return

    experiments = ['CTL1', 'CTL2', 'CTL3']  
    num_subsets = 6  
    success = True

    for experiment in experiments:
        xls = pd.ExcelFile(file_path)
        for i in range(1, num_subsets + 1):
            sheet_name = f'{experiment}_Subset{i}'
            if sheet_name in xls.sheet_names:
                try:
                    df_subset = pd.read_excel(xls, sheet_name=sheet_name)
                    fiber_diameter_column = f'FiberDiameter_{experiment}'
                    if fiber_diameter_column in df_subset.columns:
                       process_and_plot_kde(df_subset, fiber_diameter_column, sheet_name)
                    else:
                        print(f"Column {fiber_diameter_column} not found in {sheet_name}.")
                        success = False
                except Exception as e:
                    print(f"An unexpected error occurred while loading {sheet_name}: {e}")
                    success = False
            else:
                print(f"Sheet {sheet_name} does not exist in the file.")
                success = False

    if success:
        messagebox.showinfo("Success", "All subsets have been processed and plots are saved.")
    else:
        messagebox.showwarning("Partial Success", "Some subsets could not be processed. Please check the console for more information.")


# Create the GUI window
root = tk.Tk()
root.title("MyeliMetrics: A Comprehensive Tool for G-Ratio Calculation and Visualization")
root.minsize(1375, 1200)

# Load the logo image
image_path = "logo01.png"  
image = Image.open(image_path)
input_path, output_path = "", ""

# Create a Canvas that will fill the entire window
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

# Function to resize and set background image
def set_background():
    # Get the dimensions of the window
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    if window_width <= 1 or window_height <= 1:
        # If window dimensions are not yet set, wait for 100ms and try again
        root.after(100, set_background)
        return

    # Resize the image to match the window size
    resized_logo_image = image.resize((window_width, window_height), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(resized_logo_image)

    # Use the Canvas to add the background image
    canvas.create_image(0, 0, image=logo_photo, anchor="nw")
    
    # Keep a reference to the image object
    canvas.image = logo_photo

# Call the function to set the background after the event loop starts
root.after(100, set_background)

# Set a common button size
button_width = 17
button_height = 1
button_color = "white"
text_color = "black"

# Create and place the buttons on the Canvas
load_button = tk.Button(root, text="Load File", command=load_file, width=button_width, height=button_height, bg=button_color, fg=text_color)
cleanup_button = tk.Button(root, text="Clean Up Data", command=cleanup_data_handler, width=button_width, height=button_height, bg=button_color, fg=text_color)
process_fiber_button = tk.Button(root, text="Calculate Fiber Data", command=process_fiber_data_handler, width=button_width, height=button_height, bg=button_color, fg=text_color)
calculate_g_ratio_button = tk.Button(root, text="Calculate G-Ratio", command=calculate_g_ratio_handler, width=button_width, height=button_height, bg=button_color, fg=text_color)
show_scatter_plots_button = tk.Button(root, text="Show Scatter Plots", command=show_scatter_plots_handler, width=button_width, height=button_height, bg=button_color, fg=text_color)
sort_fiber_diameter_button = tk.Button(root, text="Sort Fiber Diameter", command=sort_fiber_diameter_handler, width=button_width, height=button_height, bg=button_color, fg=text_color)
sort_display_button = tk.Button(root, text="Display Data", command=sort_and_display_handler, width=button_width, height=button_height, bg=button_color, fg=text_color)
save_sorted_data_button = tk.Button(root, text="Save Sorted Data", command=save_sorted_data, width=button_width, height=button_height, bg=button_color, fg=text_color)
process_subsets_button = tk.Button(root, text="Create and Save Subsets", command=process_and_save_subsets_command, width=button_width, height=button_height, bg=button_color, fg=text_color)
analyze_g_ratio_button = tk.Button(root, text="Analyze G-Ratio", command=analyze_g_ratio_handler, width=button_width, height=button_height, bg=button_color, fg=text_color)
Modality_Test_button = tk.Button(root, text="Check Modality", command=modality_test_handler, width=button_width, height=button_height, bg=button_color, fg=text_color) 
Modality_Test_button.pack(expand=True)

# Place the buttons on the Canvas
button_positions = [(50, load_button), (100, cleanup_button), (150, process_fiber_button), 
                    (200, calculate_g_ratio_button), (250, show_scatter_plots_button), 
                    (300, sort_fiber_diameter_button), (350, sort_display_button), 
                    (400, save_sorted_data_button), (450, process_subsets_button),(500,analyze_g_ratio_button),(550,Modality_Test_button)]

for y, button in button_positions:
    canvas.create_window(100, y, window=button)

input_label = tk.Label(root)
input_label.pack()


output_label = tk.Label(root)
output_label.pack()


# Start the GUI event loop
root.mainloop()