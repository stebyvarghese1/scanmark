# desktop.py
import webview
import threading
import os
import sys

def start_django():
    os.system(f'"{sys.executable}" manage.py runserver 127.0.0.1:8000')

if __name__ == '__main__':
    # Start Django in a separate thread
    t = threading.Thread(target=start_django)
    t.daemon = True
    t.start()

    # Start the desktop window
    webview.create_window(
        "ScanMark",
        "http://127.0.0.1:8000/",
        width=1200,
        height=800,
        resizable=True
    )
    webview.start()