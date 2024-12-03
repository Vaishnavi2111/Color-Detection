import cv2
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Create a simple Tkinter window (hidden)
root = tk.Tk()
root.withdraw()  # Hide the root window

# Use file dialog to open an image
img_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

if not img_path:
    print("No image selected, exiting...")
    exit()  # Exit if no image is selected

# Read the image using OpenCV
img = cv2.imread(img_path)

# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Reading the CSV file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while(1):
    cv2.imshow("image", img)
    if clicked:
        # Draw a rectangle to show the color
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Create text string to display (Color name and RGB values)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # Display the text on the image
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when the user presses 'esc' key    
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
