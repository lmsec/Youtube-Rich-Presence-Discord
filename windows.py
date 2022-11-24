import ctypes
from pypresence import Presence
import time, os, sys
from textfilters import useless_words

client_id = ''  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop


window_titles = []


def full():
    print("beginning")
    song_name = None
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    def foreach_window(hwnd, lParams):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            window_titles.append(buff.value)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    title_filter = 'YouTube Music'
    for window_title in window_titles:
        if title_filter in window_title:
            print(window_title)
            song_name = window_title
            for useless_word in useless_words:
                song_name = song_name.replace("(" + useless_word + ")", "")
                song_name = song_name.replace("[" + useless_word + "]", "")
                song_name = song_name.replace(useless_word, "")
                song_name = song_name.replace("  ", " ")
                song_name = song_name.replace("  ", " ")
                song_name = song_name.replace("( )", "")

    if song_name is not None and song_name != '':
        song_name = (song_name[:120] + '..') if len(song_name) > 120 else song_name
        print(RPC.update(state=song_name, details="Listening to",
              large_image="none", large_text="none",
              small_image="none", small_text="none"))
        # Set the presence
        # print(f'RPC.update(state={song_name} + " on Youtube Music", details="Listening to: ")')
    time.sleep(5)  # Can only update rich presence every 15 seconds
    print("ending, let's do it again")
    full()
    print("this should not happen")


try:
    full()
except KeyboardInterrupt:
    print('Closing program')
except UnboundLocalError:
    print('No Youtube Tab Found!')
    print('Please bring tab to foreground or keep it open in a separate browser!')
finally:
    RPC.close()
    print("the end bruv")