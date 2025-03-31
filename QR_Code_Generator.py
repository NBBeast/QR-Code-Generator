import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
import qrcode
from PIL import Image, ImageTk
from tkinter import ttk
import re
from tkinter.filedialog import asksaveasfilename

# Function to check for a valid URL
def is_valid_url(url):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://' # HTTP/HTTPS/FTP
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # Domain
        r'localhost|' # Local domains
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # IP address
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # IPv6
        r'(?::\d+)?' # Optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, url) is not None

# Function to generate the QR code
def generate_qr_code():
    selected_option = dropdown.get()
    user_input = entry.get()

    # Check if the user selected an option
    if selected_option == "URL":
        if not user_input or not is_valid_url(user_input):
            messagebox.showerror("Error", "Please enter a valid URL!")
            return
        qr_image = qrcode.make(user_input)

    elif selected_option == "Text":
        if not user_input or is_valid_url(user_input):
            messagebox.showerror("Error", "Please enter text, not a URL!")
            return
        qr_image = qrcode.make(user_input)

    else:
        messagebox.showerror("Error", "Please select a data type.")
        return

    # Set the desired dimensions for the QR code
    qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)

    # Convert the QR code to a format that Tkinter can display
    img_tk = ImageTk.PhotoImage(qr_image)

    # Display the QR code in the window
    qr_label.config(image=img_tk)
    qr_label.image = img_tk  # Keep the reference to the image to avoid deletion

    # Enable the save button
    save_button.config(state="normal")  # Enable the save button for the QR code

# Function to save the QR code
def save_qr_code(window):
    # Open a dialog to choose location and filename for saving
    file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        # Save the QR code as an image
        if window == "main":
            qr_label.image.save(file_path)
        elif window == "personal":
            personal_data_qr_label.image.save(file_path)

# Function to open the personal data entry window
def open_personal_data_window():
    # Disable everything in the main window when "Personal Data Card" is selected
    entry.config(state="disabled")
    dropdown.config(state="disabled")
    generate_button.config(state="disabled")
    clear_button.config(state="disabled")  # Disable the "Clear" button in the main window

    # Create a new window for entering personal data
    personal_data_window = tk.Toplevel(root)
    personal_data_window.title("Enter Personal Data")
    personal_data_window.geometry("600x700")  # Enlarged window size

    # Entry fields for personal data
    tk.Label(personal_data_window, text="Full Name:", font=("Arial", 12)).pack(pady=5)
    global name_entry
    name_entry = tk.Entry(personal_data_window, width=40, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(personal_data_window, text="Phone Number:", font=("Arial", 12)).pack(pady=5)
    global phone_entry
    phone_entry = tk.Entry(personal_data_window, width=40, font=("Arial", 12))
    phone_entry.pack(pady=5)

    tk.Label(personal_data_window, text="Email:", font=("Arial", 12)).pack(pady=5)
    global email_entry
    email_entry = tk.Entry(personal_data_window, width=40, font=("Arial", 12))
    email_entry.pack(pady=5)

    tk.Label(personal_data_window, text="Home Address:", font=("Arial", 12)).pack(pady=5)
    global address_entry
    address_entry = tk.Entry(personal_data_window, width=40, font=("Arial", 12))
    address_entry.pack(pady=5)

    def submit_personal_data():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if not name or not phone or not email or not address:
            messagebox.showwarning("Input Error", "Please enter all personal data!")
            return

        # Create vCard with personal data
        vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nADR:;;{address};;\nEND:VCARD"
        qr_image = qrcode.make(vcard_data)

        # Set the desired dimensions for the QR code
        qr_image = qr_image.resize((200, 200), Image.Resampling.LANCZOS)

        # Convert the QR code to a format that Tkinter can display
        img_tk = ImageTk.PhotoImage(qr_image)

        # Display the QR code in the personal data window
        personal_data_qr_label.config(image=img_tk)
        personal_data_qr_label.image = img_tk  # Keep the reference to the image to avoid deletion

        # Enable the save button in the personal data window
        save_button_personal.config(state="normal")  # Enable the save button for the QR code in the personal data window

    # Button to submit personal data
    submit_button = ttk.Button(personal_data_window, text="Generate QR Code", command=submit_personal_data)
    submit_button.pack(pady=10)

    # Clear button for the personal data window
    def clear_personal_data():
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        personal_data_qr_label.config(image='')  # Clear the QR code
        personal_data_qr_label.image = None  # Reset the QR code reference
        save_button_personal.config(state="disabled")  # Disable the save button

    clear_personal_data_button = ttk.Button(personal_data_window, text="Clear", command=clear_personal_data)
    clear_personal_data_button.pack(pady=10)

    # Add a save QR code button in the personal data window (disabled by default)
    global save_button_personal
    save_button_personal = ttk.Button(personal_data_window, text="Save QR Code", command=lambda: save_qr_code("personal"), state="disabled")
    save_button_personal.pack(pady=10)

    # Add area to display QR code in the personal data window
    global personal_data_qr_label
    personal_data_qr_label = tk.Label(personal_data_window)
    personal_data_qr_label.pack(pady=10)

    # Function to close the window and reset the main window state
    personal_data_window.protocol("WM_DELETE_WINDOW", lambda: enable_main_window(personal_data_window))

# Function to enable the main window when the personal data window is closed
def enable_main_window(personal_data_window):
    personal_data_window.destroy()
    # Enable everything in the main window when the personal data window is closed
    entry.config(state="normal")
    dropdown.config(state="normal")
    generate_button.config(state="normal")
    clear_button.config(state="normal")  # Enable the "Clear" button in the main window
    # Disable manual input in the dropdown list (like initially)
    dropdown.config(state="readonly")
    # Reset the dropdown list to an empty value when closing the personal data window
    dropdown.set('')

# Function to dynamically update the input field
def update_input_field(event):
    selected_option = dropdown.get()
    user_input = entry.get()

    # Clear the previous input field
    entry.delete(0, tk.END)

    # Check for switching between URL and Text
    if selected_option == "URL":
        description_label.config(text="Enter URL:")
        if user_input and not is_valid_url(user_input):
            messagebox.showerror("Error", "If you select URL, please enter a valid URL.")
    elif selected_option == "Text":
        description_label.config(text="Enter text:")
        if user_input and is_valid_url(user_input):
            messagebox.showerror("Error", "If you select Text, please enter text, not a URL.")
    elif selected_option == "Personal Data Card":
        description_label.config(text="")  # Nothing is displayed when "Personal Data Card" is selected
        open_personal_data_window()  # Open the personal data window

# Function to clear the input field and QR code in the main window
def clear_input():
    entry.delete(0, tk.END)  # Clear the input field
    qr_label.config(image='')  # Clear the QR code
    qr_label.image = None  # Reset the QR code reference
    save_button.config(state="disabled")  # Hide the save button

# Creating the GUI application
style = Style(theme='superhero')  # Choose a theme from ttkbootstrap

root = style.master
root.title("QR Code Generator")

# Window size settings
root.geometry("500x600")

# Instructions label above the dropdown
instructions_label = tk.Label(root, text="Select the type of data", font=("Arial", 12))
instructions_label.pack(pady=10)

# Dropdown list for selecting the source (starts empty)
dropdown = ttk.Combobox(root, values=["URL", "Text", "Personal Data Card"], state="readonly", font=("Arial", 12))
dropdown.pack(pady=10)
dropdown.set('')  # Set the initial selection to be empty
dropdown.bind("<<ComboboxSelected>>", update_input_field)

# Label for data entry (will change depending on the selected source)
description_label = tk.Label(root, text="", font=("Arial", 12))  # Initially, the text is empty
description_label.pack(pady=5)

# Define style for buttons to make them the same size
style.configure("TButton", width=20, height=2)  # Set width and height for all buttons

# Entry field for data input (for URL and Text)
entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

# Button to generate QR code (for URL and Text)
generate_button = ttk.Button(root, text="Generate QR Code", command=generate_qr_code, style="TButton")
generate_button.pack(pady=10)

# Clear button
clear_button = ttk.Button(root, text="Clear", command=clear_input, style="TButton")
clear_button.pack(pady=10)

# Button to save the QR code (disabled for now)
save_button = ttk.Button(root, text="Save QR Code", command=lambda: save_qr_code("main"), state="disabled", style="TButton")
save_button.pack(pady=10)

# Area to display the QR code
qr_label = tk.Label(root)
qr_label.pack(pady=20)

# Start the GUI application
root.mainloop()
