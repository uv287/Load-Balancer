import re

# Define the log file path
log_file = "log.txt"

# Regular expression pattern to match "GRAPH: x,y" lines
pattern = r"GRAPH:\s*(\d+),(\d+)"

# Open log file for reading and data.txt for writing
with open(log_file, "r") as f_log, open("data.txt", "w") as f_data:
    # Write header to data.txt
    f_data.write("x,y\n")
    
    # Iterate through each line in the log file
    for line in f_log:
        # Check if the line matches the pattern
        match = re.match(pattern, line)
        if match:
            # Extract x and y values and write them to data.txt
            x, y = match.groups()
            f_data.write(f"{x},{y}\n")

print("Data has been written to data.txt.")
