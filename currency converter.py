import requests
import tkinter as tk
from tkinter import ttk, messagebox

def fetch_currencies():
    url = "https://open.er-api.com/v6/latest/USD"  # Free endpoint
    try:
        response = requests.get(url)
        data = response.json()

        # Debug output
        print("API response for currencies:", data)

        if 'rates' not in data:
            messagebox.showerror("API Error", "No 'rates' found in API response.")
            return []

        return list(data['rates'].keys())
    except Exception as e:
        messagebox.showerror("Connection Error", f"Unable to fetch currencies: {e}")
        return []

def convert_currency():
    from_curr = from_currency.get()
    to_curr = to_currency.get()
    amount_val = amount.get()

    if not from_curr or not to_curr or not amount_val:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        float_amount = float(amount_val)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    url = f"https://open.er-api.com/v6/latest/{from_curr}"
    try:
        response = requests.get(url)
        data = response.json()

        print("Conversion data:", data)

        if 'rates' in data and to_curr in data['rates']:
            rate = data['rates'][to_curr]
            converted = float_amount * rate
            result_label.config(text=f"{amount_val} {from_curr} = {converted:.2f} {to_curr}")
        else:
            messagebox.showerror("Conversion Error", "Currency not found in exchange rates.")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

# GUI setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x250")

currencies = fetch_currencies()

from_currency = ttk.Combobox(root, values=currencies)
from_currency.set("From Currency")
from_currency.pack(pady=10)

to_currency = ttk.Combobox(root, values=currencies)
to_currency.set("To Currency")
to_currency.pack(pady=10)

amount = tk.Entry(root)
amount.insert(0, "Enter amount")
amount.pack(pady=10)

convert_btn = tk.Button(root, text="Convert", command=convert_currency)
convert_btn.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()