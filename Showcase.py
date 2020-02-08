import tkinter, ctypes, keyboard, os, time

# If not Windows, stop running
if os.name != 'nt':
    raise(OSError("OS not compatible!"))

# Force the display to be on
# Documentation: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def disableDisplayOff():
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)

def enableDisplayOff():
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS)

class Showcase:
    def __init__(self):

        # Regular tk frame
        self.tk = tkinter.Tk()
        self.frame = tkinter.Frame(self.tk)
        self.frame.pack()

        self.tk.attributes("-fullscreen", True) # Fullscreen

        self.tk.resizable(False, False) # Prevent resizing

        self.tk.wm_attributes("-topmost", True) # The layer stays on top

        self.tk.attributes("-alpha", 1/255) # Transparency of the layer set to low value. Should be between 0.0 to 1.0

        self.tk.config(cursor="none") # Hide cursor

        self.tk.focus_force() # Focus on layer

        # Add hotkeys for Ctrl+Alt+Del and Win+L
        keyboard.add_hotkey('ctrl+alt+del', self.exit, args=[])
        keyboard.add_hotkey('Win+L', self.exit, args=[])

        # Keep screen on
        disableDisplayOff()

    # Exit
    def exit(self):
        ctypes.windll.user32.LockWorkStation()
        enableDisplayOff()
        keyboard.unhook_all_hotkeys()
        print('Done.')
        self.tk.destroy()
        

if __name__ == '__main__':
    # Wait 10 seconds for users to setup their showcase
    print("Waiting 10 seconds before locking the showcase.")
    time.sleep(10)

    # Disable keyboard and mouse inputs
    x = ctypes.windll.user32.BlockInput(True)

    # A workaround for input bugs - Inputs other than keyboard and mouse (e.g. touchpad / touchscreen) are not blocked
    w = Showcase()
    w.tk.mainloop()