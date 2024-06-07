from flask import Flask, render_template
from main import get_camera_ImageURLs, get_cameras_by_neighborhood, get_stream_dict, group_streams_by_neighborhood

app = Flask(__name__, static_url_path='/static')

@app.route('/app')
def index():
    try:
        False
    except TypeError:
        print(f"***** HERE is the Static Folder: {app.static_folder}")
    URL = "https://web.seattle.gov/Travelers/api/Map/GetCamerasByNeighborhood?neighborhood="
    neighborhoods = ["Ballard", "Central"] #, "Delridge", "Downtown", "East", "Greater Duwamish", "Lake Union", "Magnolia/Queen%20Anne", "North", "Northeast", "Northwest", "Southeast", "Southwest"]
    camera_data = get_cameras_by_neighborhood(URL, neighborhoods)
    URL_data = get_camera_ImageURLs(camera_data, neighborhoods)
    cameras = get_stream_dict(URL_data, neighborhoods)
    nbhd_dict = group_streams_by_neighborhood(cameras)

    return render_template('index.html', neighborhoods=nbhd_dict)

if __name__ == '__main__':
    print(app.static_folder)
    app.run(debug=True)
