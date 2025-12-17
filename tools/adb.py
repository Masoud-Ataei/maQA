import subprocess

ADB = "~\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"

def adb(cmd: str):
    full_cmd = ADB + f" {cmd}"
    print(f"[ADB] {full_cmd}")
    subprocess.run(full_cmd, shell=True, check=False)

def tap(x, y):
    adb(f"shell input tap {x} {y}")

def swipe(x1, y1, x2, y2, duration=300):
    adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")

def type_text(text):
    safe = text.replace(" ", "%s")
    adb(f"shell input text {safe}")

def screenshot(path="screen.png"):
    adb(f"exec-out screencap -p > {path}")
    return path
