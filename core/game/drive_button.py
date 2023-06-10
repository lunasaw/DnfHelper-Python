import time
import ctypes

user32 = ctypes.windll.user32

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_EXTENDEDKEY = 0x0001


class KeyboardInputKi(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]


class KeyboardInput(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ki", KeyboardInputKi)
    ]


def drive_button(vk_code, send_type, func_type):
    ki = KeyboardInputKi()
    ki.wVk = vk_code
    ki.wScan = user32.MapVirtualKeyW(vk_code, 0)
    ki.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))

    if send_type == 0 or send_type == 1:
        ki.dwFlags = KEYEVENTF_EXTENDEDKEY if func_type else 0
        ki.time = int(time.time() * 1000)
        inp = KeyboardInput(type=INPUT_KEYBOARD, ki=ki)
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    if send_type == 0 or send_type == 2:
        ki.dwFlags = KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP if func_type else KEYEVENTF_KEYUP
        ki.time = int(time.time() * 1000)
        inp = KeyboardInput(type=INPUT_KEYBOARD, ki=ki)
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
