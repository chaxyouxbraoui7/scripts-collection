# A script to convert images to circular type

from PIL import Image, ImageDraw
from tkinter import filedialog, Tk

root = Tk()
root.withdraw()
# dialog
file_path = filedialog.askopenfilename(
    title="Select an image",
     filetypes=[("Image files", ("*.png", "*.jpg", "*.jpeg", "*.webp", "*.svg", "*.bmp", "*.gif"))]
)

if file_path:  # checking
    img = Image.open(file_path).convert("RGBA") # making the img transparency support
    result = Image.new('L', img.size, 0) # makint the bg transparent with the same size
    # drawing a white circle
    draw = ImageDraw.Draw(result)
    draw.ellipse((0, 0) + img.size, fill=255)
    # apply
    output = Image.new("RGBA", img.size)
    output.paste(img, (0, 0), result)
    output.save("circular_one.png")
    print("Done")
else:
    print("No file selected.")