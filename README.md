# SDOT-traffic-camera-finder
A tool to find and view traffic cameras run by the Seattle Dept. of Transportation (SDOT)

The code uses the `/Travelers/api/Map/GetCamerasByNeighborhood` endpoint to find listed cameras.

# Example
Running app.py will run the application at locally at `http://127.0.0.1:5000/app`. From here, you will be able to see all the cameras available, grouped by the neighborhood SDOT uses to classify them.

Within the UI, click on a neighborhood to view its cameras. Then click on a camera to view the feed. Cameras that aren't responding are shown as offline.
<img width="1440" alt="Screenshot_SDOT_Camera_Viewer-2" src="https://github.com/moshobo/SDOT-traffic-camera-finder/assets/52591849/a1dda1c4-8bc6-4b48-b240-977cccf4c6b7">
