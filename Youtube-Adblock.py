# Made by Jesse Mogg 01/11/23

# As of 20/03/2026, it's likely that this exploit no longer works.


# How to use:
#  - Run this script, either by pressing fn + f5 or going to 'run -> run module'
#  - Copy the link of the yt video you want to watch
#    + Either right click the thumbnail and copy link, or copy url from the top
#  - Press the big 'Generate Youtube Video' button and voila, website pops up

# Note: some yt videos might not work, and I don't know why

# --- MacOS VERSION ---
# -- Shitty 10 minute code for bypassing youtube's adblock blocker --
# Exploits embedded youtube elements not showing ads

import webbrowser, os
import tkinter as tk

def generate():
    url = root.clipboard_get()
    
    x = 32
    if not url.startswith("https"):
        x -= 12

    if "=" in url:
        code = url[x:x+11]
    else:
        code = url[17:]

    p1 = r"""<!DOCTYPE html>
    <html>
        <head>
            <style>
                .youtube-video {
                    aspect-ratio: 16 / 7.3;
                    width: 100%;
                }
            </style>
        </head>
        <body style="background-color:black">
            <iframe class="youtube-video" src="https://www.youtube.com/embed/"""

    p2 = """" frameborder=0 allowfullscreen></iframe>
        <p style="color: white; text-align: center">Youtube Ad Bypass - Created by Jesse Mogg 1/11/23 - MacOS Version</p>
        </body>
    </html>"""

    html = p1 + code + p2

    with open("Adblock.html", "w") as file:
        file.write(html)

    webbrowser.open(f"file://{os.getcwd()}/Adblock.html")


# -- Stupid tkinter window made with ChatGPT lol --
# Create the main tkinter window
root = tk.Tk()
root.title("Generate Button")

# Set the window size and position it in the center of the screen
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a button and link it to the generate function, set its size and center it with padding
button = tk.Button(root, text="Generate Youtube Video", command=generate, width=20, height=3)
button.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Start the tkinter event loop
root.mainloop()
