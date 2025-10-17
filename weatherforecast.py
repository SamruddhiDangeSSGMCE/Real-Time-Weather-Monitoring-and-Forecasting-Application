import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# --- API details ---
API_KEY = "a2bf0dc47dad12111c5d154896604aeb"
BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast"

# --- Function to get current weather ---
def get_weather(city):
    try:
        url = f"{BASE_URL_CURRENT}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "City": data["name"],
                "Temperature": data["main"]["temp"],
                "Weather": data["weather"][0]["description"].capitalize(),
                "Humidity": data["main"]["humidity"],
            }
        elif response.status_code == 404:
            return "City not found."
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# --- Function to get 5-day forecast ---
def get_forecast(city):
    try:
        url = f"{BASE_URL_FORECAST}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_data = []
            seen_dates = set()
            for item in data["list"]:
                date_str = item["dt_txt"].split(" ")[0]
                time = item["dt_txt"].split(" ")[1]
                if date_str not in seen_dates and time.startswith("12:00"):
                    seen_dates.add(date_str)
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d/%m/%Y")
                    forecast_data.append({
                        "date": formatted_date,
                        "temp": item["main"]["temp"],
                        "weather": item["weather"][0]["description"].capitalize()
                    })
            return forecast_data[:5]
        else:
            return None
    except:
        return None

# --- Icon chooser ---
def get_icon(weather):
    w = weather.lower()
    if "cloud" in w: return "☁️"
    elif "rain" in w: return "🌧️"
    elif "clear" in w: return "☀️"
    elif "snow" in w: return "❄️"
    elif "storm" in w or "thunder" in w: return "🌩️"
    elif "mist" in w or "fog" in w: return "🌫️"
    else: return "🌍"

# --- Weather message based on condition ---
def weather_message(weather):
    w = weather.lower()
    if "clear" in w:
        return "Great day today! Enjoy the sunshine ☀️"
    elif "rain" in w:
        return "Carry your umbrella today! 🌧️"
    elif "cloud" in w:
        return "It is cloudy today ☁️"
    elif "snow" in w:
        return "It is snowy outside ❄️"
    elif "storm" in w or "thunder" in w:
        return "Stay at home! ⚡"
    elif "mist" in w or "fog" in w:
        return "Go slow today, it is foggy 🌫️"
    else:
        return ""

# --- Display weather function ---
def show_weather(event=None):
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    result = get_weather(city)
    if isinstance(result, str):
        messagebox.showerror("Error", result)
        return

    forecast_data = get_forecast(city)
    if not forecast_data:
        messagebox.showerror("Error", "Could not fetch forecast data.")
        return

    # Current weather display
    weather_icon = get_icon(result["Weather"])
    message = weather_message(result["Weather"])
    current_weather_label.config(
        text=f"{weather_icon} {result['City']}\n"
             f"🌡 Temperature: {result['Temperature']}°C\n"
             f"☁ Weather: {result['Weather']}\n"
             f"💧 Humidity: {result['Humidity']}%\n\n"
             f"{message}",
        fg="#263238"
    )

    # Clear old forecast cards
    for widget in forecast_frame.winfo_children():
        widget.destroy()

    for day in forecast_data:
        icon = get_icon(day["weather"])
        card = tk.Frame(forecast_frame, bg="#f0f4f8", width=140, height=140, bd=2, relief="raised")
        card.pack(side="left", padx=15, pady=10)
        card.pack_propagate(False)
        tk.Label(card, text=f"{day['date']}", bg="#f0f4f8", fg="#1565c0", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Label(card, text=f"{icon}", bg="#f0f4f8", fg="#1565c0", font=("Arial", 22)).pack()
        tk.Label(card, text=f"{day['temp']}°C", bg="#f0f4f8", fg="#263238", font=("Arial", 13, "bold")).pack()
        tk.Label(card, text=f"{day['weather']}", bg="#f0f4f8", fg="#37474f", font=("Arial", 10)).pack()

# --- Main window ---
root = tk.Tk()
root.title("🌤 Weather Dashboard 🌤")
root.geometry("960x700")
root.resizable(False, False)

# Gradient background
gradient = tk.Canvas(root, width=960, height=700)
gradient.pack(fill="both", expand=True)
for i in range(700):
    r = min(255, 220 + i // 15)
    g = min(255, 240 - i // 20)
    b = min(255, 255 - i // 20)
    color = f"#{r:02x}{g:02x}{b:02x}"
    gradient.create_line(0, i, 960, i, fill=color)

# City input
input_frame = tk.Frame(root, bg="#bbdefb")
input_frame.place(relx=0.5, rely=0.08, anchor="center")
tk.Label(input_frame, text="Enter City:", bg="#bbdefb", fg="#0d47a1", font=("Arial", 14, "bold")).pack(side="left", padx=5)
city_entry = tk.Entry(input_frame, font=("Arial", 14), width=22, bg="#e3f2fd", relief="flat")
city_entry.pack(side="left", padx=5)
city_entry.bind("<Return>", show_weather)
tk.Button(input_frame, text="Get Weather", bg="#1565c0", fg="white", font=("Arial", 12, "bold"),
          command=show_weather, relief="flat", cursor="hand2").pack(side="left", padx=5)

# Current Weather
current_weather_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#bbdefb", justify="center")
current_weather_label.place(relx=0.5, rely=0.22, anchor="center")

# Forecast Frame
forecast_frame = tk.Frame(root, bg="#bbdefb")
forecast_frame.place(relx=0.5, rely=0.45, anchor="center")

# Footer
footer = tk.Label(root, text="Made with Python | Samruddhi’s Weather Dashboard",
                  bg="#1565c0", fg="white", font=("Arial", 10, "italic"))
footer.place(relx=0.5, rely=0.95, anchor="center")

root.mainloop()
