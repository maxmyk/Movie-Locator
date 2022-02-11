"""
lab1_task2
parse.py
Parser module for main.py
"""


def read_data(path_to_file: str, write_to_file: bool = False) -> dict:
    """
    Function reads the file
    Returns dict without additional data processing
    >>> type(read_data('cache/geocoded_data.txt'))
    <class 'dict'>
    """
    import re
    f = open(path_to_file, encoding='utf-8', errors='ignore')
    data = f.readline()
    while not data.startswith("=============="):
        data = f.readline()
    data = f.readline()
    ans = {}
    year_splitter = re.compile(r'\(((\d){4})?((\?){4})?(/\D{6})' +
                               '?(/\D{5})?(/\D{4})?(/\D{3})?(/\D{2})?(/\D)?\)')
    for line in f:
        if '-'*8 in line:
            break
        parsed_line = line.strip().split("\t")
        film = parsed_line[0]
        year = year_splitter.search(film).group()
        year = year[1:5]
        if parsed_line[-1][-1] == ')':
            location = parsed_line[-2]
            additional = parsed_line[-1][1:-1]
        else:
            location = parsed_line[-1]
            additional = None
        if 80*'-' not in film:
            if location not in ans.keys():
                ans[location] = [(film, year, additional)]
            else:
                ans[location].append((film, year, additional))
    if write_to_file:
        with open('cache/parsed.txt', 'w', encoding='UTF8', newline='') as f:
            for line in ans.items():
                f.write(str(line)+'\n')
    return ans


def read_generated_files(links: list, write_to_file: bool = False) -> set:
    """
    Reads inputed files. Can write a new file
    consisting of all inputed.
    Returns set of lines
    >>> type(read_generated_files(['cache/geocoded_data.txt']))
    <class 'set'>
    """
    ans = set()
    ans_new = set()
    for link in links:
        with open(link, 'r') as f:
            for line in f:
                if 'Not geocoded' not in line:
                    ans.add(eval(line)[0])
                    ans_new.add(line)
    if write_to_file:
        new_label = f'cache/geocoded_combined_new.txt'
        import os.path
        file_exists = os.path.isfile(new_label)
        if not file_exists:
            with open(new_label, 'w+', encoding='UTF8', newline='') as f:
                for line in list(ans_new):
                    f.write(str(line))
    return ans


def get_positions(data: dict, existing_data: set, loc_database_used: bool = True, write_bad_file: bool = False) -> tuple:
    """
    Function that gets positions in format
    lat, lon from address. Can use existing files with data
    >>> type(get_positions({}, set()))
    <class 'tuple'>
    """
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    locations = {}
    bad_locations = set()
    geolocator = Nominatim(user_agent='lab_request_new')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    counter = 0
    data_old = dict(data)
    for element in data_old.items():
        if element[0] in existing_data:
            data.pop(element[0], None)
    if write_bad_file:
        with open('/cache/not_geocoded.txt', 'w', encoding='UTF8', newline='') as f:
            for element in data.items():
                f.write(str("!!!    Not geocoded    "+element[0]+'\n'))
    if not loc_database_used:
        import os.path
        curpath = os.path.abspath(os.curdir)
        print(f'   =>   {curpath}/cache/geocoded.txt')
        prev_data = []
        with open(f'{curpath}/cache/geocoded.txt', 'r') as f:
            for line in f:
                prev_data.append(line)
        with open(f'{curpath}/cache/geocoded.txt', 'w+', encoding='UTF8', newline='') as f:
            for line in prev_data:
                f.write(line)
            for element in data.items():
                print(f' $ parser.py => Processed: {counter}/{len(data)} locations;\n' +
                      f' $           => From local database used: {len(existing_data)};\n' +
                      f' $           => Physical address: {element[0]}')
                counter += 1
                location = geocode(element[0])
                if location != None:
                    locations[element[0]] = (
                        location.latitude, location.longitude)
                    f.write(
                        str((element[0], (location.latitude, location.longitude)))+'\n')
                else:
                    bad_locations.add(element[0])
                    location = geocode(''.join(element[0].split(' ')[-3:]))
                    if location != None:
                        locations[element[0]] = (
                            location.latitude, location.longitude)
                        f.write(
                            str((element[0], (location.latitude, location.longitude)))+'\n')
                    else:
                        location = geocode(''.join(element[0].split(' ')[-2:]))
                        if location != None:
                            locations[element[0]] = (
                                location.latitude, location.longitude)
                            f.write(
                                str((element[0], (location.latitude, location.longitude)))+'\n')
                        else:
                            location = geocode(
                                ''.join(element[0].split(' ')[-1]))
                            if location != None:
                                locations[element[0]] = (
                                    location.latitude, location.longitude)
                                f.write(
                                    str((element[0], (location.latitude, location.longitude)))+'\n')
                            # else:
                            #     f.write(str("!!!    Not geocoded    "+element[0]+'\n'))

    return locations, bad_locations


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
