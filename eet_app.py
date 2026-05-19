import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

# Import Matplotlib modules for Tkinter integration
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class EETDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("EET Application Support Dashboard")
        self.root.geometry("850x650") 
        
        # Main application header
        title = ttk.Label(self.root, text="EET Circuit Analysis Tool", font=("Arial", 16, "bold"))
        title.pack(pady=5)
        
        # Create tab notebook layout
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initialize the three main modules
        self.setup_ohm_power_tab()
        self.setup_ac_graph_tab()
        self.setup_resistor_tab()
        
    def setup_ohm_power_tab(self):
        """Tab 1: DC Ohm's Law & Power Calculator"""
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="Ohm's Law & Power")
        
        instruction = ttk.Label(calc_frame, text="Enter exactly TWO values to calculate the rest:", font=("Arial", 10, "italic"))
        instruction.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # Input Form Layout
        ttk.Label(calc_frame, text="Voltage (V):").grid(row=1, column=0, padx=10, pady=8, sticky='w')
        self.v_entry = ttk.Entry(calc_frame)
        self.v_entry.grid(row=1, column=1, padx=10, pady=8)
        
        ttk.Label(calc_frame, text="Current (I) [A]:").grid(row=2, column=0, padx=10, pady=8, sticky='w')
        self.i_entry = ttk.Entry(calc_frame)
        self.i_entry.grid(row=2, column=1, padx=10, pady=8)
        
        ttk.Label(calc_frame, text="Resistance (R) [Ω]:").grid(row=3, column=0, padx=10, pady=8, sticky='w')
        self.r_entry = ttk.Entry(calc_frame)
        self.r_entry.grid(row=3, column=1, padx=10, pady=8)
        
        ttk.Label(calc_frame, text="Power (P) [W]:").grid(row=4, column=0, padx=10, pady=8, sticky='w')
        self.p_entry = ttk.Entry(calc_frame)
        self.p_entry.grid(row=4, column=1, padx=10, pady=8)
        
        calc_btn = ttk.Button(calc_frame, text="Calculate", command=self.calculate_circuit)
        calc_btn.grid(row=5, column=0, columnspan=2, pady=15)
        
        clear_btn = ttk.Button(calc_frame, text="Clear Fields", command=self.clear_fields)
        clear_btn.grid(row=6, column=0, columnspan=2, pady=5)

    def calculate_circuit(self):
        v_str, i_str = self.v_entry.get().strip(), self.i_entry.get().strip()
        r_str, p_str = self.r_entry.get().strip(), self.p_entry.get().strip()
        
        vals = {'V': v_str, 'I': i_str, 'R': r_str, 'P': p_str}
        filled_keys = [k for k, v in vals.items() if v != ""]
        
        if len(filled_keys) != 2:
            messagebox.showerror("Error", f"Please enter exactly TWO values. You entered {len(filled_keys)}.")
            return
            
        try:
            v = float(v_str) if 'V' in filled_keys else None
            i = float(i_str) if 'I' in filled_keys else None
            r = float(r_str) if 'R' in filled_keys else None
            p = float(p_str) if 'P' in filled_keys else None
            
            # Mathematical core formulas
            if v is not None and i is not None:
                r = v / i if i != 0 else 0
                p = v * i
            elif v is not None and r is not None:
                i = v / r if r != 0 else 0
                p = (v ** 2) / r if r != 0 else 0
            elif v is not None and p is not None:
                i = p / v if v != 0 else 0
                r = (v ** 2) / p if p != 0 else 0
            elif i is not None and r is not None:
                v = i * r
                p = (i ** 2) * r
            elif i is not None and p is not None:
                v = p / i if i != 0 else 0
                r = p / (i ** 2) if i != 0 else 0
            elif r is not None and p is not None:
                v = math.sqrt(p * r)
                i = math.sqrt(p / r) if r != 0 else 0

            # Safe insertion without overwriting initial inputs
            if 'V' not in filled_keys:
                self.v_entry.insert(0, f"{v:.2f}")
            if 'I' not in filled_keys:
                self.i_entry.insert(0, f"{i:.2f}")
            if 'R' not in filled_keys:
                self.r_entry.insert(0, f"{r:.2f}")
            if 'P' not in filled_keys:
                self.p_entry.insert(0, f"{p:.2f}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Math Error: Division by zero is not allowed.")

    def clear_fields(self):
        self.v_entry.delete(0, tk.END)
        self.i_entry.delete(0, tk.END)
        self.r_entry.delete(0, tk.END)
        self.p_entry.delete(0, tk.END)

    def setup_ac_graph_tab(self):
        """Tab 2: AC Waveform Plotter module"""
        ac_frame = ttk.Frame(self.notebook)
        self.notebook.add(ac_frame, text="AC Waveform Plotter")
        
        # Left-side configuration panel
        input_frame = ttk.LabelFrame(ac_frame, text="Waveform Parameters")
        input_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        ttk.Label(input_frame, text="Amplitude (V peak):").pack(anchor='w', padx=5, pady=5)
        self.amp_entry = ttk.Entry(input_frame)
        self.amp_entry.pack(fill='x', padx=5, pady=2)
        self.amp_entry.insert(0, "10") 
        
        ttk.Label(input_frame, text="Frequency (Hz):").pack(anchor='w', padx=5, pady=5)
        self.freq_entry = ttk.Entry(input_frame)
        self.freq_entry.pack(fill='x', padx=5, pady=2)
        self.freq_entry.insert(0, "60") # Standard North American Frequency
        
        plot_btn = ttk.Button(input_frame, text="Plot Waveform", command=self.plot_ac_wave)
        plot_btn.pack(fill='x', padx=5, pady=15)
        
        # Right-side canvas frame for matplotlib chart
        self.graph_container = ttk.Frame(ac_frame)
        self.graph_container.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Display an initial default plot on startup
        self.plot_ac_wave()

    def plot_ac_wave(self):
        try:
            amplitude = float(self.amp_entry.get())
            frequency = float(self.freq_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for AC parameters.")
            return

        # Clear old canvas reference if it exists
        for widget in self.graph_container.winfo_children():
            widget.destroy()

        # Build the Matplotlib figure layout
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Map out sine wave data points (2 full periods)
        period = 1 / frequency if frequency > 0 else 1
        t = np.linspace(0, 2 * period, 500)
        v_t = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Draw the grid line configuration
        ax.plot(t * 1000, v_t, color='blue', lw=2, label=f"{frequency} Hz Signal")
        ax.axhline(0, color='black', lw=0.5, ls='--')
        ax.set_title("AC Voltage Over Time")
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Voltage (V)")
        ax.grid(True, linestyle=':')
        
        # Render into Tkinter interface container
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def setup_resistor_tab(self):
        """Tab 3: 4-Band Resistor Calculator"""
        res_frame = ttk.Frame(self.notebook)
        self.notebook.add(res_frame, text="Resistor Color Code")
        
        self.colors = ["Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Gray", "White"]
        self.multipliers = {"Black": 1, "Brown": 10, "Red": 100, "Orange": 1000, "Yellow": 10000, "Green": 100000, "Blue": 1000000}
        self.tolerances = {"Brown": "1%", "Red": "2%", "Gold": "5%", "Silver": "10%"}
        
        ttk.Label(res_frame, text="Band 1 (Digit):").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.b1_combo = ttk.Combobox(res_frame, values=self.colors, state="readonly")
        self.b1_combo.grid(row=0, column=1, padx=10, pady=10)
        self.b1_combo.current(1)
        
        ttk.Label(res_frame, text="Band 2 (Digit):").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.b2_combo = ttk.Combobox(res_frame, values=self.colors, state="readonly")
        self.b2_combo.grid(row=1, column=1, padx=10, pady=10)
        self.b2_combo.current(0)
        
        ttk.Label(res_frame, text="Band 3 (Multiplier):").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.b3_combo = ttk.Combobox(res_frame, values=list(self.multipliers.keys()), state="readonly")
        self.b3_combo.grid(row=2, column=1, padx=10, pady=10)
        self.b3_combo.current(2)
        
        ttk.Label(res_frame, text="Band 4 (Tolerance):").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.b4_combo = ttk.Combobox(res_frame, values=list(self.tolerances.keys()), state="readonly")
        self.b4_combo.grid(row=3, column=1, padx=10, pady=10)
        self.b4_combo.current(2)

        calc_res_btn = ttk.Button(res_frame, text="Calculate Resistance", command=self.calculate_resistance)
        calc_res_btn.grid(row=4, column=0, columnspan=2, pady=15)
        
        self.res_result_label = ttk.Label(res_frame, text="Value: -- Ω", font=("Arial", 12, "bold"))
        self.res_result_label.grid(row=5, column=0, columnspan=2, pady=5)

    def calculate_resistance(self):
        d1 = self.colors.index(self.b1_combo.get())
        d2 = self.colors.index(self.b2_combo.get())
        mult = self.multipliers[self.b3_combo.get()]
        tol = self.tolerances[self.b4_combo.get()]
        
        base_value = (d1 * 10) + d2
        total_ohms = base_value * mult
        
        if total_ohms >= 1000000:
            formatted_ohms = f"{total_ohms / 1000000:.1f} MΩ"
        elif total_ohms >= 1000:
            formatted_ohms = f"{total_ohms / 1000:.1f} kΩ"
        else:
            formatted_ohms = f"{total_ohms} Ω"
            
        self.res_result_label.config(text=f"Value: {formatted_ohms} ± {tol}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EETDashboard(root)
    root.mainloop()