# QR Code Generator

The QR Code Generator is a simple application that allows you to generate QR codes from URLs, text, or personal data (vCard). It also provides functionality for saving the generated QR codes to your computer.

## Features

- **QR Code Generation**: Generate QR codes from URLs, text, or personal data (e.g., name, phone number, email, address).
- **Personal Data Card**: Generate a QR code for personal data in vCard format (Full Name, Phone Number, Email, Address).
- **Save QR Code**: Save the generated QR codes as PNG images to your computer.
- **Responsive User Interface**: Easy-to-use interface with input fields for text, URLs, and personal data.
- **Data Validation**: Ensures proper input based on selected data type (URL or Text).
- **Dynamic Fields**: Input fields dynamically update based on the selected data type (URL, Text, Personal Data Card).

## How to Use

1. **Select Data Type**: From the dropdown, select the type of data you want to generate a QR code for (URL, Text, or Personal Data Card).
2. **Enter Data**: Depending on the selection:
   - For **URL**, enter a valid URL.
   - For **Text**, enter any non-URL text.
   - For **Personal Data Card**, enter your full name, phone number, email, and address.
3. **Generate QR Code**: Click the "Generate QR Code" button to create the QR code.
4. **Save QR Code**: Once the QR code is generated, you can save it as a PNG file by clicking the "Save QR Code" button.
5. **Clear Fields**: Use the "Clear" button to reset the input fields and the displayed QR code.

## Installation

To run the application, you need to have Python 3.6 or newer installed. You also need to install the following libraries.

### Install dependencies

```bash
pip install -r requirements.txt
