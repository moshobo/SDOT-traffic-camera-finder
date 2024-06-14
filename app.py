from flask import Flask, render_template, jsonify
from main import get_camera_ImageURLs, get_cameras_by_neighborhood, get_stream_dict, group_streams_by_neighborhood, find_alt_cameras

app = Flask(__name__, static_url_path='/static')

@app.route('/app')
def index():
    URL = "https://web.seattle.gov/Travelers/api/Map/GetCamerasByNeighborhood?neighborhood="
    neighborhoods = ["Ballard", "Central", "Delridge", "Downtown", "East", "Greater Duwamish", "Lake Union", "Magnolia/Queen%20Anne", "North", "Northeast", "Northwest", "Southeast", "Southwest"]
    camera_data = get_cameras_by_neighborhood(URL, neighborhoods)
    URL_data = get_camera_ImageURLs(camera_data, neighborhoods)
    cameras = get_stream_dict(URL_data, neighborhoods)
    nbhd_dict = group_streams_by_neighborhood(cameras)

    return render_template('index.html', neighborhoods=nbhd_dict)

@app.route('/unlisted-cameras')
def run_python_function():
    URL = "https://web.seattle.gov/Travelers/api/Map/GetCamerasByNeighborhood?neighborhood="
    neighborhoods = ["Ballard", "Central", "Southeast", "East", "Greater Duwamish", "Lake Union", "Delridge", "Downtown", "East", "Greater Duwamish", "Lake Union", "Magnolia/Queen%20Anne", "North", "Northeast", "Northwest", "Southeast", "Southwest"]
    camera_data = get_cameras_by_neighborhood(URL, neighborhoods)
    URL_data = get_camera_ImageURLs(camera_data, neighborhoods)

    cam_list = []
    for key in URL_data.keys():
        cam_list = cam_list + URL_data[key]
    
    alt_cameras = find_alt_cameras(cam_list)
    alt_cam_dict = {"unlisted": alt_cameras}
    cameras = get_stream_dict(alt_cam_dict, ["unlisted"])

    return jsonify({"cameras": cameras})

if __name__ == '__main__':
    print(app.static_folder)
    app.run(debug=True)
