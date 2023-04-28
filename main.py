import codecs
from contextlib import closing
import csv
import requests
from datetime import datetime, timedelta
from termcolor import colored as coloured
import plotext as plt


def grade_check(values):
    limits = [[50, 350, 1000],   # SO2
              [25, 70, 100],     # PM10
              [15, 35, 50],      # PM1
              [50, 300, 600],    # NO2
              [3, 15, 50],       # H2S
              [30, 50, 70]]     # PM2

    colours = []
    for value, limit in zip(values, limits):
        try:
            value = float(value)
        except Exception:
            value = -404
        if value < limit[0]:
            colours.append('green')
            continue
        if value < limit[1]:
            colours.append('yellow')
            continue
        if value < limit[2]:
            colours.append('orange')
            continue
        else:
            colours.append('red')

    return colours


def fancy_print(comps, values, colours):
    for comp, value, colour in zip(comps[1:], values[1:], colours):
        string = "{}: {}".format(comp, value)
        print(coloured(string, colour), end="   ")
    print('')


def plot(comps, data, time):
    colours = ['red', 'indigo', 'artic', 'lilac', 'gold', 'basil']
    # Transpose to list of compound
    data = list(map(list, zip(*data)))
    times = data[0]
    times.reverse()
    data_t = data[1:7]

    # Convert all items to float
    data_t = [list(map(float, sublist)) for sublist in data_t]
    for comp, y, colour in zip(comps[1:7], data_t, colours):
        y.reverse()
        plt.plot(y, line_marker="*", line_color=colour, label=comp)
    # plt.nocolor()
    plt.canvas_color('none')
    plt.axes_color('none')
    plt.ticks_color('none')
    plt.xlabel("time (UTC)")
    plt.ylabel("amount (/µg per m³)")
    plt.figsize(80, 30)

    # Set ticks
    times = [datetime.strptime(time, "%Y-%m-%d %H:%M") for time in times]
    plt.ticks(23)
    xticks = list(range(23))
    xlabels = [(str(x.hour) + ':00' if i % 2 == 0 else '') for i, x in enumerate(times)]
    plt.xticks(xticks, xlabels)
    plt.show()


def main():
    url = "https://loftgaedi.is/station/csv?filter%5BstationId%5D=35"

    data = []
    try:
        with closing(requests.get(url, stream=True)) as r:
            reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter='\t')
            for row in reader:
                row = row[0].split(';')
                row = [x.replace(",", ".") for x in row]
                data.append(row)
    except Exception:
        print('Data not available.')
        quit()
    if data[1][1] == '':
        selected_data = data[2:]
    else:
        selected_data = data[1:]
    colours = grade_check(selected_data[0][1:8])
    print("Updated at: {}".format(selected_data[0][0]))
    fancy_print(data[0], selected_data[0], colours)
    try:
        plot(data[0], selected_data, selected_data[0][0])
    except Exception:
        print('Plot not available.')


if __name__ == "__main__":
    main()
