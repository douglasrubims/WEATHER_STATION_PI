# -*- coding:utf-8 -*-

from weather import *
from news import *
from display import *
import json
from dotenv import load_dotenv
import os

load_dotenv()

debug = int(os.getenv("DEBUG"))
api_key_weather = os.getenv("WEATHER_API_KEY")
api_key_news = os.getenv("NEWS_API_KEY")
lat = os.getenv("LOCATION_LATITUDE")
lon = os.getenv("LOCATION_LONGITUDE")

if debug == 0:
    from waveshare_epd import epd7in5b_V2
else:
    pass

def map_resize(val, in_mini, in_maxi, out_mini, out_maxi):
    if in_maxi - in_mini != 0:
        out_temp = (val - in_mini) * (out_maxi - out_mini) // (in_maxi - in_mini) + out_mini
    else:
        out_temp = out_mini
    return out_temp


def main():
    ##################################################################################################################
    # FRAME
    display.draw_black.rectangle((5, 5, 795, 475), fill=255, outline=0, width=2)  # INNER FRAME
    display.draw_black.line((350, 5, 350, 290), fill=0, width=1)  # VERTICAL SEPARATION slim
    display.draw_black.line((5, 290, 795, 290), fill=0, width=1)  # HORIZONTAL SEPARATION

    # UPDATED AT
    display.draw_black.text((10, 8), "Atualizado em " + weather.current_time(), fill=0, font=font10)

    ###################################################################################################################
    # CURRENT WEATHER
    display.draw_icon(20, 35, "r", 75, 75,
                      weather.weather_description(weather.current_weather())[0])  # CURRENT WEATHER ICON
    display.draw_black.text((120, 15), weather.current_temp(), fill=0, font=font48)  # CURRENT TEMP
    display.draw_black.text((230, 15), weather.current_hum(), fill=0, font=font48)  # CURRENT HUM
    display.draw_black.text((245, 65), "Humidade", fill=0, font=font12)  # LABEL "HUMIDITY"
    display.draw_black.text((120, 75), weather.current_wind()[0] + " " + weather.current_wind()[1], fill=0, font=font24)

    display.draw_icon(120, 105, "b", 35, 35, "sunrise")  # SUNRISE ICON
    display.draw_black.text((160, 110), weather.current_sunrise(), fill=0, font=font16)  # SUNRISE TIME
    display.draw_icon(220, 105, "b", 35, 35, "sunset")  # SUNSET ICON
    display.draw_black.text((260, 110), weather.current_sunset(), fill=0, font=font16)  # SUNSET TIME

    ###################################################################################################################
    # HOURLY FORECAST
    display.draw_black.text((30, 140), "+3h", fill=0, font=font16)  # +3h LABEL
    display.draw_black.text((150, 140), "+6h", fill=0, font=font16)  # +6h LABEL
    display.draw_black.text((270, 140), "+12h", fill=0, font=font16)  # +12h LABEL
    # 3H
    display.draw_icon(25, 160, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[0])  # +3H WEATHER ICON
    display.draw_black.text((25, 210), weather.weather_description(weather.hourly_forecast()["+3h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +3h
    display.draw_black.text((30, 225), weather.hourly_forecast()["+3h"]["temp"], fill=0, font=font16)  # TEMP +3H
    display.draw_black.text((30, 240), weather.hourly_forecast()["+3h"]["pop"], fill=0, font=font16)  # POP +3H
    # +6h
    display.draw_icon(145, 160, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[0])  # +6H WEATHER ICON
    display.draw_black.text((145, 210), weather.weather_description(weather.hourly_forecast()["+6h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +6h
    display.draw_black.text((150, 225), weather.hourly_forecast()["+6h"]["temp"], fill=0, font=font16)  # TEMP +6H
    display.draw_black.text((150, 240), weather.hourly_forecast()["+6h"]["pop"], fill=0, font=font16)  # POP +6H
    # +12h
    display.draw_icon(265, 160, "r", 50, 50,
                      weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[0])  # +12H WEATHER ICON
    display.draw_black.text((265, 210), weather.weather_description(weather.hourly_forecast()["+12h"]["id"])[1], fill=0,
                            font=font12)  # WEATHER DESCRIPTION +12h
    display.draw_black.text((270, 225), weather.hourly_forecast()["+12h"]["temp"], fill=0, font=font16)  # TEMP +12H
    display.draw_black.text((270, 240), weather.hourly_forecast()["+12h"]["pop"], fill=0, font=font16)  # POP +12H

    ###################################################################################################################
    # ALERT AND POLLUTION

    ###################################################################################################################
    # NEWS UPDATE
    news_selected = news.selected_title()
    display.draw_black.text((360, 10), "Notícias", fill=0, font=font24)

    line_height = 16  # Height of each line of text
    spacing_between_news = 13  # Additional space between news items
    y_base = 50

    for i, news_item in enumerate(news_selected):
        if i == 5:
            break

        if len(news_selected) == 1:
            display.draw_black.text((360, y_base), news_selected[0], fill=0, font=font14)
            break
        else:
            num_lines = min(3, len(news_item))  # Limits the number of lines to a maximum of 3
            for j in range(num_lines):
                text = news_item[j] if j < 2 else news_item[j] + "[...]"  # Adds '...' to the last line if there are more than 3 items
                display.draw_black.text((360, y_base + j * line_height), text, fill=0, font=font14)
            y_base += num_lines * line_height + spacing_between_news

    ###################################################################################################################
    print("Updating screen...")
    if debug == 0:
        epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
    else:
        display.im_black.show()
        display.im_red.show()
    return True


if __name__ == "__main__":
    global been_reboot
    been_reboot=1
    while True:
        try:
            weather = Weather(lat, lon, api_key_weather)
            news = News()
            break
        except:
            current_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            print("INITIALIZATION PROBLEM- @" + current_time)
            time.sleep(2)
    if debug == 0:
        epd = epd7in5b_V2.EPD()
    while True:
        # Defining objects
        current_time = time.strftime("%d/%m/%Y %H:%M", time.localtime())
        print("Begin update @" + current_time)
        print("Creating display")
        display = Display()
        # Update values
        weather.update()
        print("Weather Updated")
        news.update(api_key_news)
        print("News Updated")
        print("Main program running...")
        if debug == 0:
            epd.init()
        main()
        if debug == 0:
            print("Going to sleep...")
            epd.sleep()
            print("Sleeping ZZZzzzzZZZzzz")
        print("Done")
        print("------------")
        time.sleep(1800)
