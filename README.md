# Movie Locator
Movie Locator is a simple Python program that allows you to find movies shot nearby in a given year. Also it's capable of showing HeatMap of film shooting spots.

Using this application you can find interesting places to visit and new films to watch.
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary libraries.

```bash
sudo pip install folium
sudo pip install geopy
sudo git clone https://github.com/maxmyk/fp_2022_spring_lab1_task2_GFF
```

## Usage

```
cd fp_2022_spring_lab1_task2_GFF
```
Write 'sudo python main.py "Year" "Latitude" "Longitude" "location of your 'location.list'"' into console.

An example:
```
sudo python main.py 2016 34.0980950 -118.329802 "locations.list"
```
Than open the file called "map_d_m_Y-H:M:S.html"

## Result:
![alt text](https://raw.githubusercontent.com/maxmyk/fp_2022_spring_lab1_task2_GFF/main/example/Screenshot%20from%202022-02-11%2003-26-48.png)
![alt text](https://raw.githubusercontent.com/maxmyk/fp_2022_spring_lab1_task2_GFF/main/example/Screenshot%20from%202022-02-11%2003-27-23.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
