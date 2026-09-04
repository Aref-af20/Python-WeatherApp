import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

def getWeather():
    try:
        city = textfield.get().strip()
        if not city:
            messagebox.showerror('Weather App', 'please enter a city name')
            return
            
        geolocator = Nominatim(user_agent="weather_app", timeout=10)
        location = geolocator.geocode(city)
        
        if location is None:
            messagebox.showerror('Weather App', 'City not found! Please check the city name and try again.')
            return
            
        lat = location.latitude
        lng = location.longitude
        
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=lng, lat=lat)
        
        
        city_name = result.split('/')[-1] if result and '/' in result else result or city
        city_label.config(text=city_name)

        
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime('%I:%M %p')
        clock.config(text=current_time)

        
        api_key = 'ece56dd8d43f34d928d84bdeced52b20'
        api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=metric"
        
        response = requests.get(api)
        json_data = response.json()
        
        if json_data.get('cod') != 200:
            messagebox.showerror('Weather App', f'error: {json_data.get("message", "Invalid response from the weather service.")}')
            return

        
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'])
        feels_like = int(json_data['main']['feels_like'])
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        
        temp_label.config(text=f'{temp}°C')
        feels_like_label.config(text=f'Feels like: {feels_like}°C')
        condition_label.config(text=condition)
        description_label.config(text=description.capitalize())
        wind_label.config(text=f'{wind} m/s')
        humidity_label.config(text=f'{humidity}%')
        pressure_label.config(text=f'{pressure} hPa')

    except requests.exceptions.RequestException:
        messagebox.showerror('Weather App', 'Network error! Please check your internet connection and try again.')
    except Exception as error:
        print(f"Error: {error}")
        messagebox.showerror('Weather App', 'Entry error! Please check the city name and try again.')


root = tk.Tk()
root.title('Weather App')
root.geometry('1000x650+300+100')
root.resizable(False, False)
root.configure(bg='#f0f4f8')


header_frame = tk.Frame(root, bg='#2c3e50', height=120)
header_frame.pack(fill='x', side='top')


title_label = tk.Label(
    header_frame, 
    text='🌤️ Weather App', 
    font=('Segoe UI', 28, 'bold'), 
    fg='white', 
    bg='#2c3e50'
)
title_label.place(x=50, y=30)


search_frame = tk.Frame(header_frame, bg='white', bd=0, highlightthickness=0)
search_frame.place(x=500, y=40, width=420, height=50)

textfield = tk.Entry(
    search_frame, 
    font=('Segoe UI', 16), 
    fg='#2c3e50', 
    bg='white',
    bd=0,
    highlightthickness=0
)
textfield.pack(side='left', fill='both', expand=True, padx=(15, 5), pady=5)


search_btn = tk.Button(
    search_frame, 
    text='🔍', 
    font=('Segoe UI', 18), 
    bg='#3498db', 
    fg='white',
    bd=0,
    cursor='hand2',
    command=getWeather,
    activebackground='#2980b9',
    activeforeground='white'
)
search_btn.pack(side='right', padx=2, pady=2, ipadx=15, ipady=5)


main_frame = tk.Frame(root, bg='#f0f4f8')
main_frame.pack(fill='both', expand=True, padx=40, pady=30)


left_frame = tk.Frame(main_frame, bg='#f0f4f8')
left_frame.pack(side='left', fill='both', expand=True)


city_label = tk.Label(
    left_frame, 
    text='City', 
    font=('Segoe UI', 48, 'bold'), 
    fg='#2c3e50', 
    bg='#f0f4f8'
)
city_label.pack(anchor='w', pady=(0, 5))


clock = tk.Label(
    left_frame, 
    text='--:-- --', 
    font=('Segoe UI', 32), 
    fg='#7f8c8d', 
    bg='#f0f4f8'
)
clock.pack(anchor='w')


temp_label = tk.Label(
    left_frame, 
    text='--°C', 
    font=('Segoe UI', 80, 'bold'), 
    fg='#e74c3c', 
    bg='#f0f4f8'
)
temp_label.pack(anchor='w', pady=(20, 0))


feels_like_label = tk.Label(
    left_frame, 
    text='Feels like: --°C', 
    font=('Segoe UI', 18), 
    fg='#7f8c8d', 
    bg='#f0f4f8'
)
feels_like_label.pack(anchor='w')


condition_label = tk.Label(
    left_frame, 
    text='--', 
    font=('Segoe UI', 24, 'bold'), 
    fg='#2c3e50', 
    bg='#f0f4f8'
)
condition_label.pack(anchor='w', pady=(20, 0))


description_label = tk.Label(
    left_frame, 
    text='--', 
    font=('Segoe UI', 18), 
    fg='#7f8c8d', 
    bg='#f0f4f8'
)
description_label.pack(anchor='w')


right_frame = tk.Frame(main_frame, bg='#f0f4f8')
right_frame.pack(side='right', fill='both', expand=True, padx=(30, 0))


def create_info_card(parent, icon, title, row, col):
    card = tk.Frame(
        parent, 
        bg='white', 
        relief='raised', 
        bd=0,
        highlightthickness=1,
        highlightcolor='#e0e0e0'
    )
    card.grid(row=row, column=col, padx=15, pady=15, ipadx=20, ipady=15, sticky='nsew')
    
    
    icon_label = tk.Label(card, text=icon, font=('Segoe UI', 32), bg='white')
    icon_label.pack()
    
    
    title_label = tk.Label(card, text=title, font=('Segoe UI', 12), fg='#7f8c8d', bg='white')
    title_label.pack()
    
    
    value_label = tk.Label(card, text='--', font=('Segoe UI', 22, 'bold'), fg='#2c3e50', bg='white')
    value_label.pack()
    
    return value_label


wind_label = create_info_card(right_frame, '💨', 'Wind Speed', 0, 0)
humidity_label = create_info_card(right_frame, '💧', 'Humidity', 0, 1)


pressure_label = create_info_card(right_frame, '📊', 'Pressure', 1, 0)
uv_label = create_info_card(right_frame, '🌡️', 'UV Index', 1, 1)


right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_columnconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)


footer_frame = tk.Frame(root, bg='#ecf0f1', height=40)
footer_frame.pack(fill='x', side='bottom')

footer_label = tk.Label(
    footer_frame, 
    text='© 2026 Weather App | Powered by OpenWeatherMap', 
    font=('Segoe UI', 10), 
    fg='#95a5a6', 
    bg='#ecf0f1'
)
footer_label.pack(pady=10)


root.bind('<Return>', lambda event: getWeather())


root.mainloop()