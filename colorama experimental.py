import time
import tkinter as tk
from tkinter import messagebox
import numpy as np
import psutil
from PIL import Image, ImageTk
from colorama import init, Fore
import threading
import subprocess

init(autoreset=True)
global stop_flag
stop_flag = False 


def get_usage_color(percentage):
    if percentage < 50:
        return Fore.GREEN
    elif percentage < 80:
        return Fore.YELLOW
    else:
        return Fore.RED

def update_terminal():
    try:
        terminal = subprocess.Popen(['cmd', '/K', 'color 0A'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            cpu_color = get_usage_color(cpu_usage)
            ram_color = get_usage_color(ram_usage)
            
            terminal.stdin.write(f"{cpu_color}CPU Usage: {cpu_usage:.2f}%  {ram_color}RAM Usage: {ram_usage:.2f}%\n")
            terminal.stdin.flush()

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nTerminated by user.")
        return

def update_gui_usage():
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            cpu_usage_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")
            ram_usage_label.config(text=f"RAM Usage: {ram_usage:.2f}%")

            if cpu_usage < 50:
                cpu_usage_label.config(fg="green", bg="#F9EEAB")
            elif cpu_usage < 80:
                cpu_usage_label.config(fg="yellow", bg="#4F7073")
            else:
                cpu_usage_label.config(fg="red", bg="#494069")

            if ram_usage < 50:
                ram_usage_label.config(fg="green", bg="#F9EEAB")
            elif ram_usage < 80:
                ram_usage_label.config(fg="yellow", bg="#4F7073")
            else:
                ram_usage_label.config(fg="red", bg="#494069")

    except Exception as e:
            print(f"Monitoring error: {e}")
    return

def toggle_benchmark():
    global stop_event
    if benchmark_button["text"] == "Start Benchmark":
        start_benchmark_thread()
        benchmark_button.config(text="Stop Benchmark", bg="#A22469")
    else:
        stop_benchmark()
        benchmark_button.config(text="Start Benchmark", bg="lightcoral")

def memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / 1024 ** 2

def stop_benchmark():
    global stop_event
    stop_event.set()

def create_large_array(size_in_gb):
    size = int(size_in_gb * 1024 ** 3 // 8)
    array = np.empty((size,), dtype=np.float64)
    slice_size = 10 * 1024 ** 2
    for i in range(0, size, slice_size):
        if stop_event.is_set():
            raise InterruptedError("Benchmark stopped by user.")
        array[i:i + slice_size] = np.random.rand(min(slice_size, size - i))
    return array

def update_output(text):
    text_output.insert(tk.END, text + "\n")
    text_output.yview(tk.END)

def start_benchmark_thread():
    threading.Thread(target=run_benchmark, daemon=True).start()

def run_benchmark():
    global stop_event
    stop_event.clear()
    try:
        size_in_gb = float(entry.get())
        if size_in_gb <= 0:
            raise ValueError("RAM size must be greater than 0.")
        duration = int(duration_entry.get())
        text_output.delete(1.0, tk.END)
        update_output(f"Starting to queue bit dump ({size_in_gb} GB) into RAM:\n")
        update_output(f"Attempting to allocate {size_in_gb} GB of data...\n")

        benchmark_duration = 10
        end_time = time.time() + duration
        allocation_times = []
        start_time = time.time()
        
        
        while time.time() < end_time and not stop_flag:
            try:
                start_time_alloc = time.time()
                array = create_large_array(size_in_gb)
                allocation_time = time.time() - start_time_alloc
                allocation_times.append(allocation_time)

                update_output(f"Allocated {size_in_gb} GB of data.")
                time.sleep(1)

                del array
                update_output(f"Deallocated {size_in_gb} GB of data.")
            except MemoryError:
                update_output("Failed due to insufficient memory.")
                break

        if allocation_times:
            avg_allocation_time = sum(allocation_times) / len(allocation_times)
            update_output(f"Average memory allocation time: {avg_allocation_time:.2f} seconds")
        else:
            update_output("No successful allocations.")

        update_output("Benchmark completed.")
       
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")



root = tk.Tk()
root.title("PassMemory")
root.geometry("600x470")
bg_image = Image.open("C:\\Users\\Adenn\\Pictures\\pixiv\\116700126_p0.png")
bg_image_tk = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_image_tk)
bg_label.place(relwidth=1, relheight=1)
#bg_label.place(x=140, y=144)

available_memory_gb = psutil.virtual_memory().total / 1024 ** 3
label = tk.Label(root, text=f"RAM Bench. (MAX available: {available_memory_gb:.2f} GB):")
label.pack(pady=10)
label.place(x=370, y=90)

duration_label = tk.Label(root, text="Benchmark Duration (seconds):", font=("Helvetica", 9))
duration_label.pack(pady=5)
duration_label.place(x=420, y=20)

duration_entry = tk.Entry(root, width=17)
duration_entry.insert(0, "10")  # Default value
duration_entry.pack(pady=5)
duration_entry.place(x=420, y=49)
entry = tk.Entry(root)
entry.pack(pady=5)
entry.place(x=420, y=120)

benchmark_button = tk.Button(root, text="Start Benchmark", command=toggle_benchmark, bg="lightcoral", width=20, height=2)
benchmark_button.pack(pady=10)
benchmark_button.place(x=420, y=144)


text_output = tk.Text(root, height=15, width=70)
text_output.pack(pady=10)
text_output.place(x=16, y=200)

cpu_usage_label = tk.Label(root, text="CPU Usage: 0%", font=("Helvetica", 14))
cpu_usage_label.pack(side='left', pady=20)
cpu_usage_label.place(x=20, y=20)

ram_usage_label = tk.Label(root, text="RAM Usage: 0%", font=("Helvetica", 14))
ram_usage_label.pack(side='left', pady=20)
ram_usage_label.place(x=20, y=60)


threading.Thread(target=update_gui_usage, daemon=True).start()
terminal_thread = threading.Thread(target=update_terminal, daemon=True)
terminal_thread.start()

stop_event = threading.Event()

root.mainloop()
