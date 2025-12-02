from pynput import keyboard
import asyncio

wasd_state = {
    "w" : 0,
    "a" : 0,
    "s" : 0,
    "d" : 0
}

vel_value = {
    "lin" : 0,
    "ang" : 0
}

# listen button pressed
def on_press(key):
    try:
        if key.char in wasd_state:
            wasd_state[key.char] = 1
    except AttributeError:
        pass

# listen button released
def on_release(key):
    try:
        if key == keyboard.Key.esc:
            return False
        else:
            wasd_state[key.char] = 0
    except AttributeError:
        pass

# Collect events until released

def start_listen_keyboard():
    global listener
    print("LISTENING KEYBOARD")
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def stop_listen_keyboard():
    listener.join()

def update_velocity():
    vel_value["lin"] = wasd_state["w"] - wasd_state["s"]
    vel_value['ang'] = wasd_state["d"] - wasd_state['a']

def get_key():
    #start_listen_keyboard()

    # while True:
    #     update_velocity()
    #     print("VELOCITY: ", vel_value)
    #     asyncio.sleep(0.2)
    update_velocity()
    return vel_value

if __name__ == "__main__":
    #start_listen_keyboard()
    #asyncio.create_task(start_listen_keyboard())
    asyncio.run(wasd_key())