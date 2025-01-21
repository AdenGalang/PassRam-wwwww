Features

    Real-time Monitoring:
        Live CPU and RAM usage with color-coded thresholds.
        Dynamic GUI updates for quick insights.
        Terminal-based system usage output with customizable color indicators.

    Custom RAM Benchmarking:
        Set desired RAM allocation size (in GB).
        Configure benchmark duration.
        Allocates and deallocates memory to test system performance under stress.
        Outputs average memory allocation time and final memory usage.

    User-friendly GUI:
        Built using Tkinter for a clean and interactive design.
        Configurable input fields for benchmark parameters.

Requirements
Python Libraries:

    time
    tkinter
    messagebox
    numpy
    psutil
    Pillow
    colorama
    subprocess
    threading

Additional Tools:

    Windows Command Prompt (for terminal updates).

    -Usage-
Start Monitoring

    Monitoring begins automatically when the application starts.
    Live updates are displayed in the GUI and terminal.

Run Benchmark

    Enter the desired memory allocation size (in GB).
    Set the benchmark duration (in seconds).
    Click the Start Benchmark button to begin.
    The button toggles to Stop Benchmark during the process and back once completed.
