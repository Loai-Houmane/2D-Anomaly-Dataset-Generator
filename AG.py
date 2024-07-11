import tkinter as tk
from tkinter import ttk
from tkinter import messagebox , filedialog
import random
from PIL import Image, ImageTk
import numpy as np

image_path = "logo.png"

def apply_noise(image):
    img_array = np.array(image)
    mean = 0
    var = 10
    sigma = var ** 0.5
    gaussian = np.random.normal(mean, sigma, img_array.shape)
    noisy_img = img_array + gaussian
    s_vs_p = 0.5
    amount = 0.004
    out = np.copy(noisy_img)
    num_salt = np.ceil(amount * img_array.size * s_vs_p).astype(int)
    coords = [np.random.randint(0, i - 1, num_salt) for i in img_array.shape]
    out[tuple(coords)] = 1
    num_pepper = np.ceil(amount * img_array.size * (1. - s_vs_p)).astype(int)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in img_array.shape]
    out[tuple(coords)] = 0
    noisy_image_pil = Image.fromarray(np.clip(out, 0, 255).astype('uint8'), 'RGBA')
    return noisy_image_pil

def place_image_randomly(base_image_path, overlay_image_path, mask_image_path, i):
    
    if overlay_image_path == "None":
        return  # Skip processing if "None" is selected
    base_image = Image.open(base_image_path).convert("RGBA")
    overlay_image = Image.open(overlay_image_path).convert("RGBA")
    mask_image = Image.open(mask_image_path).convert("RGBA")

    # Resize base and overlay images to 4000x4000
    base_image = base_image.resize((4000, 4000))

    scale_factor = random.uniform(0.5, 2)
    overlay_image = overlay_image.resize((int(overlay_image.width * scale_factor), int(overlay_image.height * scale_factor)))
    mask_image = mask_image.resize((int(mask_image.width * scale_factor), int(mask_image.height * scale_factor)))
    rotation_angle = random.randint(0, 360)
    overlay_image = overlay_image.rotate(rotation_angle, expand=True)
    mask_image = mask_image.rotate(rotation_angle, expand=True)
    if random.choice([True, False]):
        overlay_image = Image.Image.transpose(overlay_image, Image.FLIP_LEFT_RIGHT)
        mask_image = Image.Image.transpose(mask_image, Image.FLIP_LEFT_RIGHT)
    if random.choice([True, False]):
        overlay_image = Image.Image.transpose(overlay_image, Image.FLIP_TOP_BOTTOM)
        mask_image = Image.Image.transpose(mask_image, Image.FLIP_TOP_BOTTOM)
    base_width, base_height = base_image.size
    overlay_width, overlay_height = overlay_image.size
    # Ensure overlay image is not larger than base image
    if overlay_width > base_width or overlay_height > base_height:
        overlay_image = overlay_image.resize((base_width, base_height))
        mask_image = mask_image.resize((base_width, base_height))
        overlay_width, overlay_height = overlay_image.size
    random_x = random.randint(0, base_width - overlay_width)
    random_y = random.randint(0, base_height - overlay_height)
    result_image = Image.new('RGBA', base_image.size)
    result_image.paste(base_image, (0, 0))
    result_image.paste(overlay_image, (random_x, random_y), mask=overlay_image)
    scale = scale_var.get()
    if scale:
        width, height = map(int, scale.split('*'))
        result_image = result_image.resize((width, height))
    # Apply noise if selected
    result_folder = "results"  # Folder for result images
    mask_folder = "masks"      # Folder for mask images
    
    if noise_var.get():
        result_image = apply_noise(result_image)
    result_image.save(f'{result_folder}/result_{i}.png', "PNG")
    
    result_mask_image = Image.new('L', base_image.size, 0)
    result_mask_image.paste(mask_image, (random_x, random_y), mask=mask_image)
    if scale:
        result_mask_image = result_mask_image.resize((width, height))
    result_mask_image.save(f'{mask_folder}/mask_{i}.png')

def generate_anomalies():
    global anomaly_list  # Add this if anomaly_list is used outside this function as well
    anomaly_list = anomaly_images[1:]  # Exclude "None" from the list
    anomaly = anomaly_var.get()
    if anomaly == "None":
        messagebox.showinfo("Info", "No anomaly selected.")
        return
    if anomaly in anomaly_list:
        mask = f'{anomaly.replace("an", "mask")}'
        num_anomalies_str = num_var.get()
        if num_anomalies_str == '':
            messagebox.showerror("Error", "Please enter a number for the number of anomalies.")
            return
        num_anomalies = int(num_anomalies_str)
        if num_anomalies > 0:
            messagebox.showinfo("Selection", f"You selected {anomaly}. Corresponding mask is {mask}")
            for i in range(num_anomalies):
                place_image_randomly(image_path, anomaly, mask, i)


root = tk.Tk()
root.title("Anomaly Generator")

# Load and display the logo
original_image = Image.open("logo.png")  # Open the image file
resized_image = original_image.resize((int(original_image.width / 2), int(original_image.height / 2)))  # Resize the image
logo = ImageTk.PhotoImage(resized_image)  # Convert the resized image to PhotoImage
logo_label = tk.Label(root, image=logo)
logo_label.pack()

frame = ttk.Frame(root, padding="10")
frame.pack()

# Button to select image
def select_image():
    global image_path  # Declare image_path as global to modify the global variable
    image_path = tk.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        ttk.Label(frame, text="✅ Image selected successfully", foreground="green").grid(row=0, column=1, sticky=tk.W)
        print("Selected image:", image_path)
    else :
        ttk.Label(frame, text=" ❌ NO Image selected", foreground="red").grid(row=0, column=1, sticky=tk.W)

select_button = ttk.Button(frame, text="Select Image", command=select_image)
select_button.grid(row=0, column=0, sticky=tk.W)
# if image_path:
#     ttk.Label(frame, text="Image selected successfully").grid(row=0, column=1, sticky=tk.W)
# Anomaly selection
anomaly_var = tk.StringVar(value="None")  # Default selection is None

anomalies_frame = ttk.Frame(frame)
anomalies_frame.grid(row=3, column=0, columnspan=2)

# Define anomalies including a "None" option
anomaly_images = ["None", "an/an1.png", "an/an2.png", "an/an3.png"]
anomaly_icons = {"None": None}  # Start with None option

# Load each anomaly image, create a PhotoImage, and add to the dictionary
for anomaly_path in anomaly_images[1:]:  # Skip "None"
    img = Image.open(anomaly_path)
    img = img.resize((50, 50))  # Resize for display
    img = ImageTk.PhotoImage(img)
    anomaly_icons[anomaly_path] = img

# Create a radiobutton for each anomaly including "None"
for anomaly_path in anomaly_images:
    img = anomaly_icons[anomaly_path]
    rb = tk.Radiobutton(anomalies_frame, image=img, variable=anomaly_var, value=anomaly_path, indicatoron=0)
    rb.grid(row=1, column=anomaly_images.index(anomaly_path))

num_var = tk.StringVar()
ttk.Label(frame, text="Number of Anomalies:").grid(row=1, column=0, sticky=tk.W)
num_entry = ttk.Entry(frame, textvariable=num_var)
num_entry.grid(row=1, column=1, sticky=tk.W)

ttk.Label(frame, text="The Scale of image:").grid(row=2, column=0, sticky=tk.W)
scale_var = tk.StringVar()
scale_var.set(None)
scale_list = ["1024*1024", "512*512", "256*256"]
scale_dropdown = ttk.OptionMenu(frame, scale_var, *([None]+scale_list))
scale_dropdown.grid(row=2, column=1, sticky=tk.W)
noise_var = tk.BooleanVar()
noise_checkbox = ttk.Checkbutton(frame, text="Apply Low Noise", variable=noise_var)
noise_checkbox.grid(row=4, column=0, sticky=tk.W)
generate_button = ttk.Button(frame, text="Generate", command=generate_anomalies)
generate_button.grid(row=5, column=0, sticky=tk.W)



root.mainloop()