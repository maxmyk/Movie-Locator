"""
lab1_task2
main.py
Main module
"""

from cmath import asin, cos, sin
from math import radians
import os
import argparse
import sys
import parser  # parser module
import map_creator  # module that creates a map

"""
Importing necessary libraries
"""


def args_parser():
    """
    args_parser()
    Parses positional arguments
    """
    parser = argparse.ArgumentParser(description='main.py parser')

    parser.add_argument("year", type=str, help="Production year")
    parser.add_argument("latitude", type=str, help="Latitude")
    parser.add_argument("longtitude", type=str, help="Longtitude")
    parser.add_argument("path_to_data", type=str, help='Path to data')
    parser.add_argument('--do_not_use_locations_database', dest='loc_database',
                        action='store_false', help='DON\'T use preinstalled locations database')
    parser.add_argument('--use_cache_data', dest='use_cache_data',
                        action='store_true', help='Use generated data')
    parser.set_defaults(loc_database=True)
    parser.set_defaults(use_cache_data=False)
    return parser.parse_args()


def haversin(lat1: str, lon1: str, lat2: str, lon2: str) -> complex:
    """
    Haversine formula function.
    >>> haversin("48.53115", "25.03649", "34.0980031", "-118.329523")
    (6819.094799649309+0j)
    """
    lat1, lon1 = radians(float(lat1)), radians(float(lon1))
    lat2, lon2 = radians(float(lat2)), radians(float(lon2))
    hs_lat = sin((lat2-lat1)/2)**2
    hs_lon = sin((lon2-lon1)/2)**2
    d_hs = 2*6371*asin(hs_lat + cos(lat1)*cos(lat2)*hs_lon)
    return d_hs


def find_closest_points(lat: str, lon: str, location: str) -> list:
    """
    Finds 10 closest points to home location using Haversine formula.
    >>> type(find_closest_points("34.0980031", "-118.329523", "cache/geocoded_data.txt"))
    <class 'list'>
    """
    distances = set()
    lines = set()
    with open(location, 'r') as f:
        for line in f:
            p_line = eval(line)
            p_line = (p_line[0].replace(' ', ''), p_line[1])
            lines.add(p_line)

    for line in lines:
        d_hs = haversin(lat, lon, line[1][0], line[1][1])
        distances.add((line[0], d_hs, line[1]))
    # print(f' # {len(distances)} Points found!')
    return sorted(list(distances), key=lambda x: x[1].real)


def combine_data(data:dict, points: list, year: str) -> dict:
    """
    Function that combines films and locations.
    Also it returns 10 closest points with all data included.
    >>> import parser; type(combine_data(parser.read_data("locations.list"),\
 find_closest_points("34.0980031", "-118.329523",\
 "cache/geocoded_data.txt"), "2007"))
    <class 'dict'>
    """
    ans = {}
    stop_loop = False
    for num, point in enumerate(points):
        if not stop_loop:
            for elem in data.items():
                if (elem[0].replace(' ', '') == point[0]) and (len(ans.keys()) < 10):
                    for film in elem[1]:
                        if film[1] == year:
                            if num not in ans.keys():
                                ans[num] = [point[0], []]
                                ans[num][1].append((film, point[2]))
                            elif num in ans.keys():
                                ans[num][1].append((film, point[2]))
                elif len(ans.keys()) >= 10:
                    stop_loop = True
                    break
        else:
            break
    # print(f' # Data combined; {len(ans)} {len(data)} {len(points)} {year}')
    return ans


def main(print_time: bool = False):
    """
    Main function
    """
    import time
    now = time.time()
    args = args_parser()

    prod_year = args.year
    lat = args.latitude
    lon = args.longtitude
    path_to_data = args.path_to_data
    use_loc_database = args.loc_database
    use_cache_data = args.use_cache_data

    if not os.path.isfile(path_to_data):
        raise SystemExit(f" ! Usage: {sys.argv[0]} <argument> <argument> <argument> <argument>\n" +
                         " ! path_to_data should be an existing file!")
    if use_loc_database:
        loc_data = 'cache/geocoded_data.txt'
    else:
        loc_data = 'cache/geocoded.txt'
        existing_data = set()
        if use_cache_data:
            if os.path.isfile('cache/geocoded.txt'):
                print(" ! File exists")
                existing_data = parser.read_generated_files(['cache/geocoded.txt'])
        else:
            parser.get_positions(parser.read_data(
                path_to_data), existing_data, False)
    points = find_closest_points(lat, lon, loc_data)
    combined = combine_data(parser.read_data(path_to_data), points, prod_year)
    print(f' # {map_creator.create_map(combined, points, [lat, lon])}')
    if print_time:
        print(f' # Time: {time.time() - now} sec.')
    print('\n # Success!')


if __name__ == '__main__':
    print(f'\n {"#"*58}\n' +
          ' # Hi! This is a script that\'ll help you find             #\n' +
          ' # your favourite film\'s location                         #\n' +
          f' #{"="*56}#\n' +
          ' # If you want to get results faster, start app as usual, #\n' +
          ' # with four parameters.                                  #\n' +
          ' # Else add "--do_not_use_locations_database" to the end  #\n' +
          ' # You can also use "--use_cache_data" in order to store  #\n' +
          ' # already processed addresses.                           #\n' +
          f' {"#"*58}\n')
    # import doctest
    # print(doctest.testmod())
    main()
