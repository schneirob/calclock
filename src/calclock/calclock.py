import click
from datetime import datetime
from dateutil.parser import parse, ParserError
from loguru import logger
from svgutils import transform
import sys



def set_time(svg, hour, minute, second):
    svg.find_id("hour").rotate(360/12*(hour+minute/60+second/(60*60)), 157.63431, 113.4923)
    svg.find_id("minute").rotate(360/60*(minute+second/60), 157.63431, 113.4923)

    return svg

def create_clock(day, hour, minute, second):
    am = ""
    pm = ""
    if hour >= 0 and hour < 12:
        am = "A"
    if hour >= 12 and hour < 24:
        pm = "P"

    with open("./art/calclock.svg", "r") as file:
        svg = file.read().replace("$$day$$", str(day)).replace("$$AM$$", am).replace("$$PM$$", pm)

    svg = transform.fromstring(svg)
    return set_time(svg, hour, minute, second)

@click.command()
@click.option("--date", "-d", type=str, default=None, show_default=False, help="Date string, year first, month first")
@click.option("--fromfile", "-f", type=str, default=None, show_default=False, help="Read date string line by line from file")

def main(date, fromfile):
    if fromfile is not None:
        logger.debug("Readin time values from file {}", fromfile)
        with open(fromfile, "r") as times:
            times = times.readlines()

        count = 0
        for time in times:
            try:
                # date = parse(time, fuzzy=True, dayfirst=False, yearfirst=True)
                time_format = "%Y%m%d-%H%M%S"
                date = datetime.strptime((time.split("."))[0], time_format)
                logger.debug("Creating image for {}", date)
                filename = "./images/" + \
                        ("0"*8 + str(count))[-8:] + \
                        ".svg"
                        # "-" + \
                        # date.strftime("%Y%m%d-%H%M%S") + \
                create_clock(date.day, date.hour, date.minute, date.second).save(filename)
                count += 1
            except ParserError:
                logger.exception("Failed to recognize timestring")
        sys.exit(0)

    if date is None:
        date = datetime.now()
    else:
        try:
            date = parse(date, fuzzy=True, dayfirst=False, yearfirst=True)
        except ParserError:
            logger.exception("Failed to recognize timestring")
            sys.exit(1)
    logger.debug("Creating image for time {}", date)

    create_clock(date.day, date.hour, date.minute, date.second).save("./images/" + date.strftime("%Y%m%d-%H%M%S") + ".svg")

