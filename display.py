#!/usr/bin/env python3
import time
import datetime
import requests
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont

# Matrix configuration
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 3

matrix = RGBMatrix(options=options)

# Fonts - using smaller sizes to fit on 64x32
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)  # Reduced from 16
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)  # Reduced from 12
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)  # Reduced from 10
except IOError:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
      font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Weather API (OpenWeatherMap)
def get_weather():
    return "Weather feature needs API key"

# F1 API (Ergast Developer API)
def get_f1_data():
    try:
        # Get current season schedule
        schedule_url = "http://ergast.com/api/f1/current.json"
        schedule_response = requests.get(schedule_url)
        schedule_data = schedule_response.json()

        # Find next race
        races = schedule_data["MRData"]["RaceTable"]["Races"]
        next_race = None
        current_date = datetime.datetime.now()

        for race in races:
            # Parse race date
            race_date = datetime.datetime.strptime(race['date'], "%Y-%m-%d")
            if race_date > current_date:
                next_race = race
            if race_date > current_date:
                next_race = race
                break

        if next_race:
            race_name = next_race["raceName"].split("Grand Prix")[0].strip()
            date_str = datetime.datetime.strptime(next_race["date"], "%Y-%m-%d").strftime("%b %d")
            return {
                "race_name": race_name,
                "circuit": next_race["Circuit"]["circuitName"],
                "date": date_str,
                "location": next_race["Circuit"]["Location"]["locality"]
            }
        else:
            return None

    except Exception as e:
        print(f"Error getting F1 data: {e}")
        return None

def draw_time_screen(image, draw):
    # Draw the time and date screen
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A")
    day_str = now.strftime("%B %d")
    date_str = now.strftime("%A")
    day_str = now.strftime("%B %d")

    # Center the time
    time_width = draw.textlength(time_str, font=font_large)
    draw.text(((64 - time_width) // 2, 3), time_str, font=font_large, fill=(255, 0, 0))

    # Draw the day of week
    date_width = draw.textlength(date_str, font=font_medium)
    draw.text(((64 - date_width) // 2, 16), date_str, font=font_medium, fill=(0, 255, 0))

    # Draw the date
    day_width = draw.textlength(day_str, font=font_small)
    draw.text(((64 - day_width) // 2, 24), day_str, font=font_small, fill=(0, 255, 255))

def draw_weather_screen(image, draw):
    # Draw the weather screen - more compact layout
    draw.text((2, 5), "WEATHER", font=font_medium, fill=(0, 128, 255))
    draw.text((2, 18), weather_str[:18], font=font_small, fill=(255, 255, 255))

def draw_f1_screen(image, draw):
    # Draw the F1 screen - more compact layout
    draw.text((2, 3), "FORMULA 1", font=font_medium, fill=(255, 0, 0))

    if isinstance(f1_data, dict):
        draw.text((2, 15), f1_data["race_name"][:10], font=font_small, fill=(255, 165, 0))
    if isinstance(f1_data, dict):
        draw.text((2, 15), f1_data["race_name"][:10], font=font_small, fill=(255, 165, 0))
        draw.text((2, 23), f1_data["date"], font=font_small, fill=(255, 255, 255))
    else:
        draw.text((2, 18), "No upcoming races", font=font_small, fill=(255, 255, 255))

def draw_screen():
    # Create a blank image
    image = Image.new("RGB", (options.cols, options.rows))
    draw = ImageDraw.Draw(image)

    # Determine which screen to show based on time
    seconds = int(time.time()) % 30  # Rotate every 30 seconds (10 sec per screen)

    if seconds < 10:
        draw_time_screen(image, draw)
    elif seconds < 20:
        draw_weather_screen(image, draw)
    else:
        draw_f1_screen(image, draw)

    # Display on matrix
    matrix.SetImage(image)

# Initialize data
weather_str = get_weather()
# Initialize data
weather_str = get_weather()
f1_data = get_f1_data()

# Update data every 10 minutes
last_update = 0

# Main loop
try:
    print("Press CTRL+C to stop")
    while True:
        # Update data every 10 minutes
        current_time = time.time()
        if current_time - last_update > 600:  # 600 seconds = 10 minutes
            weather_str = get_weather()
            f1_data = get_f1_data()
            last_update = current_time
            print("Data updated")

        draw_screen()
        time.sleep(0.5)  # Update every half second
except KeyboardInterrupt:
    print("Exiting...")
    matrix.Clear()
