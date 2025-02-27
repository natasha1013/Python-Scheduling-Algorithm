import tkinter as tk
from tkinter import ttk, Canvas

# Function to simulate the Round Robin scheduling algorithm
def round_robin(processes, burst_times, arrival_times, quantum):
    n = len(processes)  # Number of processes
    remaining_burst = burst_times[:]  # Copy of burst times to track remaining burst times
    completion_times = [0] * n  # Completion times for each process
    time = 0  # Current time in the simulation
    queue = []  # Queue to manage the processes in round-robin order
    in_queue = [False] * n  # Track whether a process is in the queue
    execution_log = []  # Log to store the execution order and time intervals

    while True:
        done = True  # Flag to check if all processes are completed

        # Add processes to the queue that have arrived and are not already in it
        for i in range(n):
            if arrival_times[i] <= time and not in_queue[i] and remaining_burst[i] > 0:
                queue.append(i)
                in_queue[i] = True

        # If the queue is empty but some processes are not completed, increment time
        if not queue and any(remaining_burst):
            time += 1
            continue

        # Process the first process in the queue
        if queue:
            current = queue.pop(0)
            done = False

            # If the process needs more time than the quantum
            if remaining_burst[current] > quantum:
                execution_log.append((processes[current], time, time + quantum))  # Log execution
                time += quantum
                remaining_burst[current] -= quantum
            else:  # Process completes within the quantum
                execution_log.append((processes[current], time, time + remaining_burst[current]))
                time += remaining_burst[current]
                remaining_burst[current] = 0
                completion_times[current] = time

            # Add newly arrived processes to the queue
            for i in range(n):
                if arrival_times[i] <= time and remaining_burst[i] > 0 and not in_queue[i]:
                    queue.append(i)
                    in_queue[i] = True

            # Re-add the current process to the queue if it is not completed
            if remaining_burst[current] > 0:
                queue.append(current)
            else:
                in_queue[current] = False

        # Break the loop if all processes are completed
        if done:
            break

    # Calculate turnaround times and waiting times
    turnaround_times = [completion_times[i] - arrival_times[i] for i in range(n)]
    waiting_times = [turnaround_times[i] - burst_times[i] for i in range(n)]

    return completion_times, turnaround_times, waiting_times, execution_log


# Function to simulate the SJN scheduling algorithm
def sjn(processes, burst_times, arrival_times):
    n = len(processes) # number of processes
    remaining_burst = burst_times[:] # copy of burst time
    turnaround_times = [0] * n  # Turnaround times for each process
    waiting_times = [0] * n  # Waiting times for each process
    completion_times = [0] * n  # Completion times for each process
    time = 0  # Current time in the simulation
    queue = []  # Queue to manage the processes in round-robin order
    in_queue = [False] * n  # Track whether a process is in the queue
    execution_log = []  # Log to store the execution order and time intervals

    while True:
        done = True # Flag to check if all processes are completed

        # Add processes to the queue that have arrived and are not already in it
        for i in range(n):
            if arrival_times[i] <= time and not in_queue[i] and remaining_burst[i] > 0:
                queue.append(i)
                in_queue[i] = True

        # If the queue is empty and there are still processes to complete, move the time forward
        if not queue and any(remaining_burst):
            time += 1
            continue

        # Process the first process in the queue
        if queue:

            # Sort queue based on remaining burst time (Shortest Job Next)
            queue.sort(key=lambda x: remaining_burst[x])
            current = queue.pop(0)  # Get the process with the shortest burst time
            done = False

            # Process the selected process
            remaining_burst[current] = 0  # Mark the burst time as completed
            completion_times[current] = time + burst_times[current]  # Set completion time
            turnaround_times[current] = completion_times[current] - arrival_times[current]  # Calculate turnaround time
            waiting_times[current] = turnaround_times[current] - burst_times[current]  # Calculate waiting time

            # Add the execution log with the process name and the time interval it was executed
            execution_log.append((processes[current], time, time + burst_times[current]))
            
            # update the current time
            time += burst_times[current]

        if done:
            break

    return completion_times, turnaround_times, waiting_times, execution_log

# Function to simulate the SRT scheduling algorithm
def srt(processes, burst_times, arrival_times):
    n = len(processes)  # Number of processes
    remaining_burst = burst_times[:]  # Copy of burst times to track remaining burst time
    turnaround_times = [0] * n  # Turnaround times for each process
    waiting_times = [0] * n  # Waiting times for each process
    completion_times = [0] * n  # Completion times for each process
    time = 0  # Current time in the simulation
    in_queue = [False] * n  # Track whether a process has arrived
    execution_log = []  # Log to store the execution order and time intervals

    last_process = None  # To track the last executed process
    last_process_start_time = 0  # To track the time when the current process started

    while True:
        done = True  # Flag to check if all processes are completed

        # Add processes to the queue that have arrived and are not already in the queue
        for i in range(n):
            if arrival_times[i] <= time and not in_queue[i] and remaining_burst[i] > 0:
                in_queue[i] = True
                done = False  # Mark that not all processes are done

        # If there are no remaining processes to execute and no processes are incomplete, break the loop
        if done and all(b == 0 for b in remaining_burst):
            break

        # Find the process with the shortest remaining burst time
        available_processes = [(i, remaining_burst[i]) for i in range(n) if in_queue[i] and remaining_burst[i] > 0]
        if available_processes:
            # Sort the processes by remaining burst time
            available_processes.sort(key=lambda x: x[1])
            current = available_processes[0][0]  # Get the process with the shortest remaining burst time

            # If the process has changed, log the previous process execution
            if last_process is None or current != last_process:
                if last_process is not None:
                    execution_log.append((processes[last_process], last_process_start_time, time))  # Log previous process
                last_process_start_time = time  # Set the start time of the new process

            # Execute the process for 1 time unit
            remaining_burst[current] -= 1  # Decrease remaining burst time
            time += 1  # Update the current time

            # If the process is completed, calculate completion time, turnaround time, and waiting time
            if remaining_burst[current] == 0:
                completion_times[current] = time  # Set completion time
                turnaround_times[current] = completion_times[current] - arrival_times[current]  # Calculate turnaround time
                waiting_times[current] = turnaround_times[current] - burst_times[current]  # Calculate waiting time

            # Update last_process to the current process
            last_process = current
        else:
            # If no processes are ready to execute, increment the time
            time += 1

    # After the loop, log the last process
    if last_process is not None:
        execution_log.append((processes[last_process], last_process_start_time, time))

    return completion_times, turnaround_times, waiting_times, execution_log

# Non-Preemptive Priority Scheduling Function
def non_preemptive_priority(processes, burst_times, arrival_times, priorities):

    n = len(processes)  # Number of processes
    remaining_burst = burst_times[:]  # Copy of burst times to track remaining burst time
    turnaround_times = [0] * n  # Turnaround times for each process
    waiting_times = [0] * n  # Waiting times for each process
    completion_times = [0] * n  # Completion times for each process
    time = 0  # Current time in the simulation
    completed = 0
    execution_log = []  # Log to store the execution order and time intervals
    is_completed = [False] * n

    while completed < n:
        # Find the highest priority process that has arrived
        idx = -1
        for i in range(n):
            if arrival_times[i] <= time and not is_completed[i]:
                if idx == -1 or priorities[i] < priorities[idx]:
                    idx = i

        if idx != -1:
            # Process the selected process
            process = processes[idx]
            start_time = max(time, arrival_times[idx])
            finish_time = start_time + remaining_burst[idx]

            completion_times[idx] = finish_time
            turnaround_times[idx] = completion_times[idx] - arrival_times[idx]
            waiting_times[idx] = turnaround_times[idx] - burst_times[idx]

            execution_log.append((process, start_time, finish_time))

            time = finish_time
            is_completed[idx] = True
            completed += 1
        else:
            time += 1

    return completion_times, turnaround_times, waiting_times, execution_log


# Function to create the GUI and handle user inputs
def create_simulation():

    # start simulations
    def start_simulation():
        try:
            # Retrieve user inputs for number of processes and quantum time
            num_processes = int(num_processes_entry.get())
            quantum = int(quantum_entry.get())

            # Validate the number of processes
            if not (3 <= num_processes <= 10):
                raise ValueError("Number of processes must be between 3 and 10.")

            # Generate process names, if added the name, then use the name, else default PN
            process_names_input = process_name_entry.get().split()
            processes = [process_names_input[i] if i < len(process_names_input) else f"P{i}" for i in range(num_processes)]
            
            # parse burst times and arrival times
            burst_times = list(map(int, burst_time_entry.get().split()))
            arrival_times = list(map(int, arrival_time_entry.get().split()))
            priority = list(map(int, priority_entry.get().split())) 

            # Validate the inputs for burst and arrival times
            if len(burst_times) != num_processes or len(arrival_times) != num_processes or len(priority) != num_processes:
                raise ValueError("Mismatch in number of processes and input details.")

            # Run the algorithms
            rr_result = round_robin(processes, burst_times, arrival_times, quantum) # rr_completion_times, rr_turnaround_times, rr_waiting_times, rr_execution_log
            rr_result_stats = calc_stats(rr_result, num_processes)  # total_turnaround, avg_turnaround, total_waiting, avg_waiting

            sjn_result = sjn(processes, burst_times, arrival_times)
            sjn_result_stats = calc_stats(sjn_result, num_processes)

            srt_result = srt(processes, burst_times, arrival_times)
            srt_result_stats = calc_stats(sjn_result, num_processes)

            # Add to the list of algorithm results
            priority_result = non_preemptive_priority(processes, burst_times, arrival_times, priority)
            priority_result_stats = calc_stats(priority_result, num_processes)

            # Add to the results and stats list
            results = [rr_result, sjn_result, srt_result, priority_result]
            results_stats = [rr_result_stats, sjn_result_stats, srt_result_stats, priority_result_stats]
            
            # Display the results in a new window
            display_results(processes, burst_times, arrival_times, priority, results,results_stats)

        except ValueError as e:
            # Display error messages for invalid inputs
            error_label.config(text=f"Error: {str(e)}")

    def calc_stats(result, num_processes):
        total_turnaround = sum(result[1])
        avg_turnaround = total_turnaround / num_processes
        total_waiting = sum(result[2])
        avg_waiting = total_waiting / num_processes

        return total_turnaround, avg_turnaround, total_waiting, avg_waiting
        
    def display_results(processes, burst_times, arrival_times, priority, results, result_stats):
        
        # Create a new window to display the results
        results_window = tk.Toplevel(root)
        results_window.title("Simulation Results")
        results_window.geometry("800x800")
        results_window.configure(bg="#f4ede5")

        
        canvas = tk.Canvas(results_window, bg="#f4ede5")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(results_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link the scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas for content
        content_frame = tk.Frame(canvas, bg="#f4ede5")
        canvas.create_window((0, 0), window=content_frame, anchor="n")

        def resize_canvas(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", resize_canvas)
       # content_frame.pack(expand=True, fill="both", anchor="center")


        title_label = ttk.Label(content_frame, text="Gantt Chart", font=("Arial", 14, "bold"), background="#f4ede5")
        title_label.pack(pady=(30, 0), anchor="center") 

        # algorithm names
        algorithm_names = ["Round Robin", "Shortest Job Next (SJN)", "Shortest Remaining Time (SRT)", "Non-Preemptive Priority"]

        # canvases for Gantt charts
        canvas_frame = tk.Frame(content_frame, bg="#f4ede5")
        canvas_frame.pack(pady=(0, 10))

        # create canvas dynamically
        gantt_canvases = []
        for index, result in enumerate(results):
            scheduling_label = ttk.Label(canvas_frame, text=f"{chr(97 + index)}) {algorithm_names[index]}", 
                                     font=("Arial", 10, "italic"), background="#f4ede5")
            scheduling_label.pack(pady=(5, 0))

            canvas_width = len(result[3]) * 60
            gantt_canvas = Canvas(
                canvas_frame, 
                width=canvas_width, 
                height=80, 
                bg="#f4ede5", 
                highlightthickness=1, 
                highlightbackground="#f4ede5"
            )
            gantt_canvas.pack(fill="both", expand=True, pady=(0, 10))

            draw_gantt_chart(gantt_canvas, result, index)
            gantt_canvases.append((gantt_canvas, result, result_stats[index]))

        # Center the starting position based on the canvas width
        # Bind the resize event to redraw the Gantt chart dynamically
        # gantt_canvas_rr.bind("<Configure>", lambda event: draw_gantt_chart(gantt_canvas_rr, result))
        

        # Display process table
        # Create a frame to hold the table and statistics
        
        label_title = ttk.Label(content_frame, text="Process Table", font=("Arial", 14, "bold"), background="#f4ede5")
        label_title.pack(pady=(0, 10))
        #ttk.Label(content_frame, text="Process Table", font=("Arial", 14, "bold"), background="#f4ede5").pack(pady=(0,10))
        
        process_table_frame = tk.Frame(content_frame, bg="#f4ede5")
        process_table_frame.pack(pady=(10,20))

        def update_process_table(result, result_stat):
            # Clear the current content
            for widget in process_table_frame.winfo_children():
                widget.destroy()

            # add new process table
            proc_table(process_table_frame, processes, burst_times, arrival_times, priority, result, result_stat)

        def dropdown_with_results(results_window, gantt_canvases):
            dropdown_frame = ttk.Frame(results_window)
            dropdown_frame.pack(pady=(0,10))

            ttk.Label(dropdown_frame, text="Select a Process Table to View:").pack(side="left", padx=5)
            
            # Create dropdown options
            options = algorithm_names
            
            # Define a variable to track the selected option
            selected_option = tk.StringVar()
            selected_option.set(options[0])  # Set the default value

            # Dropdown combobox
            dropdown = ttk.Combobox(dropdown_frame, values=options, textvariable=selected_option, state="readonly", width=25)
            dropdown.pack(side="left", padx=5)

            # Button to trigger update based on selected dropdown option
            
            def on_selection(event = None):
                # Get the selected algorithm
                selected_algorithm = selected_option.get()
                
                # Update the label title to reflect the selected algorithm
                label_title.config(text=f"{selected_algorithm} Process Table")
                
                # Update the process table based on the selection
                index = options.index(selected_option.get())
                _, result, result_stat = gantt_canvases[index]
                update_process_table(result, result_stat)

            dropdown.bind("<<ComboboxSelected>>", on_selection)
            on_selection()

        # Display the first process table by default
        if gantt_canvases:
            first_result, first_stat = gantt_canvases[0][1], gantt_canvases[0][2]
            dropdown_with_results(content_frame, gantt_canvases)

    def proc_table(content_frame, processes, burst_times, arrival_times, priority, result, result_stat):
        completion_times = result[0]
        turnaround_times = result[1]
        waiting_times = result[2]
        execution_log = result[3]
        total_turnaround = result_stat[0]
        avg_turnaround = result_stat[1]
        total_waiting = result_stat[2]
        avg_waiting = result_stat[3]

        # Process table (aligned to the left)
        table_frame = tk.Frame(content_frame, bg="#f4ede5")
        table_frame.grid(row=0, column=0, padx=20, sticky="nw")
        
        

        tree = ttk.Treeview(
            table_frame,
            columns=("Process", "Arrival Time", "Burst Time", "Priority", "Completion Time", "Turnaround Time", "Waiting Time"),
            show="headings",
            height=8
        )
        tree.heading("Process", text="Process")
        tree.heading("Arrival Time", text="Arrival Time")
        tree.heading("Burst Time", text="Burst Time")
        tree.heading("Priority", text="Priority")
        tree.heading("Completion Time", text="Finishing Time")
        tree.heading("Turnaround Time", text="Turnaround Time")
        tree.heading("Waiting Time", text="Waiting Time")

        tree.column("Process", width=100, anchor=tk.CENTER)
        tree.column("Arrival Time", width=100, anchor=tk.CENTER)
        tree.column("Burst Time", width=100, anchor=tk.CENTER)
        tree.column("Priority", width=100, anchor=tk.CENTER)
        tree.column("Completion Time", width=100, anchor=tk.CENTER)
        tree.column("Turnaround Time", width=120, anchor=tk.CENTER)
        tree.column("Waiting Time", width=120, anchor=tk.CENTER)

        for i in range(len(processes)):
            tree.insert(
                "",
                tk.END,
                values=(
                    processes[i],
                    arrival_times[i],
                    burst_times[i],
                    priority[i],
                    completion_times[i],
                    turnaround_times[i],
                    waiting_times[i],
                ),
                
            )

        tree.pack()

        # Statistics summary (aligned to the right)
        summary_frame = tk.Frame(content_frame, bg="#f4ede5")
        summary_frame.grid(row=0, column=1, padx=50, sticky="ne")

        ttk.Label(summary_frame, text="Statistics Summary", font=("Arial", 14, "bold"), background="#f4ede5").grid(row=0, column=0, pady=10, sticky="w")
        ttk.Label(summary_frame, text=f"Total Turnaround Time: {total_turnaround}", font=("Arial", 10), background="#f4ede5").grid(row=1, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Average Turnaround Time: {avg_turnaround:.2f}", font=("Arial", 10),background="#f4ede5").grid(row=2, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Total Waiting Time: {total_waiting}", font=("Arial", 10),background="#f4ede5").grid(row=3, column=0, sticky="w")
        ttk.Label(summary_frame, text=f"Average Waiting Time: {avg_waiting:.2f}", font=("Arial", 10), background="#f4ede5").grid(row=4, column=0, sticky="w")
    
    def draw_gantt_chart(gantt_canvas, result, chart_index):
        execution_log = result[3]
        chart_height = 50
        y_offset = 20
        # y_offset = chart_index * chart_height + 10

        # Calculate total chart width
        total_chart_width = sum((end - start) * 20 for _, start, end in execution_log)
        # gantt_canvas.delete("all")  # Clear previous drawings if resized
        canvas_actual_width = gantt_canvas.winfo_width()
        # gantt_canvas.config(width=canvas_actual_width, height=chart_height + 50)

        start_x = max((canvas_actual_width - total_chart_width) // 2, 20)  # Ensure it doesn't go offscreen

        for i, (process, start, end) in enumerate(execution_log):
            width = (end - start) * 20
            gantt_canvas.create_rectangle(start_x, y_offset, start_x + width, y_offset + 30, fill="#f1968e", outline="#000")
            gantt_canvas.create_text(start_x + width / 2, y_offset + 15, text=process, font=("Arial", 10))
            gantt_canvas.create_text(start_x, y_offset + 40, text=start, anchor=tk.NW, font=("Arial", 8))
            start_x += width

        # Ensure the final rectangle's end time is displayed
        if i == len(execution_log) - 1:
            gantt_canvas.create_text(start_x, y_offset + 40, text=end, anchor=tk.NW, font=("Arial", 8))


    # Create the main window
    root = tk.Tk()
    root.title("Scheduling Simulator")
    root.configure(bg="#f4ede5")
    root.geometry("700x400")

    ttk.Label(root, text="Scheduling Simulator", font=("Arial", 16, "bold"), background="#f4ede5").pack(pady=(40,10))

    form_frame = tk.Frame(root, bg="#f4ede5") 
    form_frame.pack(pady=10)

    ttk.Label(form_frame, text="Number of Processes (3-10):", font=("Arial", 11, "bold"), background="#f4ede5").grid(row=0, column=0, sticky=tk.W, pady=5)
    num_processes_entry = ttk.Entry(form_frame, font=("Arial", 11, "bold"))
    num_processes_entry.grid(row=0, column=1, pady=5)

    ttk.Label(form_frame, text="Process names (space-separated, optional):", font=("Arial", 11, "bold"), background="#f4ede5").grid(row=1, column=0, sticky=tk.W, pady=5)
    process_name_entry = ttk.Entry(form_frame, font=("Arial", 11, "bold"))
    process_name_entry.grid(row=1, column=1, pady=5)

    ttk.Label(form_frame, text="Burst Times (space-separated):", font=("Arial", 11, "bold"), background="#f4ede5").grid(row=2, column=0, sticky=tk.W, pady=5)
    burst_time_entry = ttk.Entry(form_frame, font=("Arial", 11, "bold"))
    burst_time_entry.grid(row=2, column=1, pady=5)

    ttk.Label(form_frame, text="Arrival Times (space-separated):", font=("Arial", 11, "bold"), background="#f4ede5").grid(row=3, column=0, sticky=tk.W, pady=5)
    arrival_time_entry = ttk.Entry(form_frame, font=("Arial", 11, "bold"))
    arrival_time_entry.grid(row=3, column=1, pady=5)

    # put at last because time quantum is only for round robin
    ttk.Label(form_frame, text="Time Quantum:", font=("Arial", 11, "bold"), background="#f4ede5").grid(row=4, column=0, sticky=tk.W, pady=5)
    quantum_entry = ttk.Entry(form_frame, font=("Arial", 11, "bold"))
    quantum_entry.grid(row=4, column=1, pady=5)

    # for priority
    ttk.Label(form_frame, text="Priority (space-separated):", font=("Arial", 11, "bold"), background="#f4ede5").grid(row=5, column=0, sticky=tk.W, pady=5)
    priority_entry = ttk.Entry(form_frame, font=("Arial", 11, "bold"))
    priority_entry.grid(row=5, column=1, pady=5)

    

    error_label = tk.Label(root, text="", fg="red", bg="#f4ede5", font=("Arial", 10))
    error_label.pack()
    
    style = ttk.Style()
    style.theme_use("clam")  # Try "alt", "default", or "classic" as well
    style.configure("Custom.TButton", background="#f29491", foreground="black", font=("Arial", 10, "bold"), highlightthickness=1, highlightbackground="#f4ede5")

    ttk.Button(root, text="Start Simulation", style="Custom.TButton", command=start_simulation).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    create_simulation()
