import click
from datetime import datetime
from dateutil.parser import parse, ParserError
from loguru import logger
from svgutils import transform
import sys



def set_time(svg, hour, minute, second):
    svg.find_id("hour").rotate(360/12*hour, 157.63431, 113.4923)
    svg.find_id("minute").rotate(360/60*(minute+second/60), 157.63431, 113.4923)

    return svg

def create_clock(day, hour, minute, second):
    while hour >= 24:
        hour -= 24
    am = ""
    pm = ""
    if hour >= 0 and hour < 12:
        am = "A"
    if hour >= 12 and hour < 24:
        pm = "P"

    while hour >= 12:
        hour -= 12

    with open("./art/calclock.svg", "r") as file:
        svg = file.read().replace("$$day$$", str(day)).replace("$$AM$$", am).replace("$$PM$$", pm)

    svg = transform.fromstring(svg)
    return set_time(svg, hour, minute, second)

@click.command()
@click.option("--date", "-d", type=str, default=None, show_default=False, help="Date string, year first, month first")
def main(date):
    if date is None:
        date = datetime.now()
    else:
        try:
            date = parse(date, fuzzy=True, dayfirst=False, yearfirst=True)
        except ParserError:
            logger.exception("Failed to recognize timestring")
            sys.exit(1)
    logger.debug("Creating image for time {}", date)

    create_clock(date.day, date.hour, date.minute, date.second).save(date.strftime("%Y%m%d-%H%M%S") + ".svg")

