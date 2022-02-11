"""
lab1_task2
map_creator.py
Map creator module for main.py
"""


def create_map(data: dict, points: list, cur_pos: list) -> str:
    """
    Creates map using Folium.
    Returns file name in the followin format:
    map_d_m_Y-H:M:S.html
    """
    import folium
    from folium.plugins import HeatMap
    from random import uniform
    map_1 = folium.Map(location=cur_pos, zoom_start=10, control_scale=True)
    folium.Marker(
        location=cur_pos,
        popup='My location',
        icon=folium.Icon(color='green', icon='home'),
    ).add_to(map_1)
    locations = [point[2] for point in points]
    locs = []
    for element in data.values():
        loc = list(element[1][0][1])
        if loc == cur_pos:
            loc = [loc[0]+uniform(-0.002, 0.002), loc[1] +
                   uniform(-0.002, 0.002)]
        while loc in locs:
            loc = [loc[0]+uniform(-0.002, 0.002), loc[1] +
                   uniform(-0.002, 0.002)]
        locs.append(loc)
    for num, element in enumerate(data.values()):
        folium.Marker(
            location=locs[num],
            popup=element[1][0][0][0],
            icon=folium.Icon(color='green', icon='ok-sign'),
        ).add_to(map_1)
    HeatMap(locations, name='All films locations HeatMap',
            control=True, show=False).add_to(map_1)
    folium.LayerControl().add_to(map_1)
    from datetime import datetime
    now = datetime.now()
    new_label = f'map_{"".join(now.strftime(f"%d_%m_%Y-%H:%M:%S"))}.html'
    map_1.save(new_label)
    return f'Map file is {new_label}'
