from pynput import keyboard
import asyncio

wasd_state = {
    "w" : 0.0,
    "a" : 0.0,
    "s" : 0.0,
    "d" : 0.0
}

vel_value = {
    "lin" : 0.0,
    "ang" : 0.0
}

# listen button pressed
def on_press(key):
    try:
        if key.char in wasd_state:
            wasd_state[key.char] = float(0.5)
    except AttributeError:
        pass

# listen button released
def on_release(key):
    try:
        if key == keyboard.Key.esc:
            return False
        else:
            wasd_state[key.char] = float(0.0)
    except AttributeError:
        pass

# Collect events until released

def start_listen_keyboard():
    global listener
    print("DENGAR KEYBOARD")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def stop_listen_keyboard():
    listener.join()

def update_velocity():
    vel_value["lin"] = float(wasd_state["w"]) - float(wasd_state["s"])
    vel_value['ang'] = (float(wasd_state["d"]) - float(wasd_state['a']))*-1

def get_key():
    #start_listen_keyboard()

    # while True:
    #     update_velocity()
    #     print("VELOCITY: ", vel_value)
    #     asyncio.sleep(0.2)
    update_velocity()
    print(wasd_state)
    return vel_value
