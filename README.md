# SDOT-traffic-camera-finder
A tool to find traffic cameras run by the Seattle Dept. of Transportation (SDOT)

The code uses the `/Travelers/api/Map/GetCamerasByNeighborhood` endpoint to find listed cameras.

# Example
Running `main.py` will return you a console output that looks something like this:

```
Ballard has 7 cameras
Central has 16 cameras
Delridge has 10 cameras
Downtown has 95 cameras
East has 36 cameras
Greater Duwamish has 82 cameras
Lake Union has 38 cameras
Magnolia/Queen%20Anne has 29 cameras
North has 12 cameras
Northeast has 28 cameras
Northwest has 24 cameras
Southeast has 24 cameras
Southwest has 15 cameras
There are 416 cameras total across Seattle
```