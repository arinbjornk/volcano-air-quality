import codecs
from contextlib import closing
import csv
import requests
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
        except:
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


def plot(comps, data):
    colours = ['red', 'indigo', 'artic', 'lilac', 'gold', 'basil']
    # Transpose to list of compound
    data_t = list(map(list, zip(*data)))[1:7]

    # Convert all items to float
    data_t = [list(map(float, sublist)) for sublist in data_t]
    for comp, y, colour in zip(comps[1:7], data_t, colours):
        y.reverse()
        plt.plot(y, line_marker = "*", line_color=colour, label=comp)
    # plt.nocolor()
    plt.canvas_color('none')
    plt.axes_color('none')
    plt.ticks_color('none')
    plt.xlabel("time (/h)")
    plt.ylabel("amount (/µg per m³)")
    plt.figsize(80, 30)
    plt.ticks(24)
    xticks = list(range(24))
    xlabels = [str(i - 23) for i in range(24)]
    xlabels = [(x if i%2 == 1 else '') for i, x in enumerate(xlabels)]
    # [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    # xlabels = ['' if i in enumerate(xlabels) % 7 != 0]
    plt.xticks(xticks, xlabels)
    plt.show()


def main():
    url = "https://loftgaedi.is/station/csv?filter%5BstationId%5D=72"

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

    colours = grade_check(data[1][1:8])
    print("Updated at: {}".format(data[1][0]))
    fancy_print(data[0], data[1], colours)
    plot(data[0], data[1:])
    try:
        plot(data[0], data[1:])
    except Exception:
        print('Plot not available.')


if __name__ == "__main__":
    main()
