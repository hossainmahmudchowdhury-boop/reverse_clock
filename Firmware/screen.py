import time
from datetime import datetime
import requests
from PIL import Image, ImageDraw, ImageFont
import ST7789
import RPi.GPIO as GPIO


TFT_CS  = 15
TFT_DC  = 4
TFT_RST = 2
TFT_BL  = 5


API_KEY  = "YOUR_RAPIDAPI_KEY"
API_HOST = "weatherapi-com.p.rapidapi.com"
LAT = 28.63          
LON = 77.22          


BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
CYAN    = (0, 255, 255)
YELLOW  = (255, 255, 0)
RED     = (255, 50, 50)
GREEN   = (50, 255, 50)
GRAY    = (120, 120, 120)


disp = ST7789.ST7789(
    port=0,
    cs=TFT_CS,
    dc=TFT_DC,
    rst=TFT_RST,
    backlight=TFT_BL,
    width=240,
    height=240,
    rotation=90,         
    spi_speed_hz=80_000_000
)
disp.begin()


image = Image.new("RGB", (240, 240), BLACK)
draw  = ImageDraw.Draw(image)


try:
    font_time  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    font_ampm  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    font_day   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    font_date  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    font_temp  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    font_status= ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except:
    font_time = font_ampm = font_day = font_date = font_temp = font_small = font_status = ImageFont.load_default()


temperature = "--"
last_weather_update = 0
WEATHER_INTERVAL = 300     


def fetch_temperature():
    global temperature
    try:
        url = f"https://weatherapi-com.p.rapidapi.com/current.json?q={LAT}%2C{LON}"
        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": API_HOST
        }
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            data = r.json()
            temperature = str(int(data["current"]["temp_c"]))
        else:
            temperature = "--"
    except Exception as e:
        print("Weather error:", e)
        temperature = "--"


def draw_screen(status_text="AWAKE", status_color=GREEN):

    draw.rectangle((0, 0, 240, 240), fill=BLACK)

    now = datetime.now()

        
    minute = now.strftime("%M")
    ampm = now.strftime("%p")

    time_str = f"{hour}:{minute}"

    bbox = draw.textbbox((0, 0), time_str, font=font_time)
    tw = bbox[2] - bbox[0]
    draw.text(((240 - tw) // 2 - 10, 18), time_str, font=font_time, fill=WHITE)

    # AM/PM
    draw.text((175, 38), ampm, font=font_ampm, fill=CYAN)


    day_name = now.strftime("%a")   
    day_num  = now.strftime("%d")
    month    = now.strftime("%b")
    year     = now.strftime("%Y")

    draw.text((18, 95), day_name, font=font_day, fill=YELLOW)
    draw.text((18, 130), f"{day_num} {month}", font=font_date, fill=WHITE)
    draw.text((18, 160), year, font=font_date, fill=GRAY)


    temp_str = f"{temperature}°C"
    bbox = draw.textbbox((0, 0), temp_str, font=font_temp)
    tw = bbox[2] - bbox[0]
    draw.text((240 - tw - 15, 125), temp_str, font=font_temp, fill=CYAN)


    # Background bar
    draw.rectangle((0, 200, 240, 240), fill=(20, 20, 20))
    bbox = draw.textbbox((0, 0), status_text, font=font_status)
    tw = bbox[2] - bbox[0]
    draw.text(((240 - tw) // 2, 208), status_text, font=font_status, fill=status_color)

 
    disp.display(image)

def main():
    print("Smart Desk Clock started...")
    fetch_temperature()       

    while True:
  
        if time.time() - last_weather_update > WEATHER_INTERVAL:
            fetch_temperature()
            last_weather_update = time.time()

        draw_screen(status_text="AWAKE", status_color=GREEN)

        time.sleep(1)          

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user")
        GPIO.cleanup()
