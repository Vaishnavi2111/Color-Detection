import tkinter as tk
from tkinter import filedialog
import cv2
import pandas as pd
import numpy as np

# Tkinter window
root = tk.Tk()
root.title("Color Detection App")
root.geometry("500x200")  # Increased window size

# Global variables
clicked = False
r = g = b = xpos = ypos = 0

# Load the color CSV
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def get_color_name(R, G, B):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = param[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

def upload_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        img = cv2.imread(file_path)

        # Resize the image to fit the screen (max 800x800 or smaller)
        max_height, max_width = 800, 800
        height, width, _ = img.shape
        if height > max_height or width > max_width:
            scale_factor = min(max_height / height, max_width / width)
            img = cv2.resize(img, (int(width * scale_factor), int(height * scale_factor)))

        cv2.namedWindow("Color Detection")
        cv2.setMouseCallback("Color Detection", draw_function, param=img)

        while True:
            if clicked:
                cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
                text = get_color_name(r, g, b) + f' R={r} G={g} B={b}'
                color = (255, 255, 255) if r + g + b < 600 else (0, 0, 0)
                cv2.putText(img, text, (50, 50), 2, 0.8, color, 2, cv2.LINE_AA)
            cv2.imshow("Color Detection", img)
            if cv2.waitKey(20) & 0xFF == 27:  # ESC key to exit
                break
        cv2.destroyAllWindows()

# Add upload button
upload_btn = tk.Button(root, text="Upload Image", command=upload_image, height=2, width=20)  # Make the button larger
upload_btn.pack(pady=40)

root.mainloop()
