import requests
import json

def get_cameras_by_neighborhood(url, neighborhoods):
    response = {}
    
    for nbhd in neighborhoods:
        final_url = url + nbhd
        r = requests.get(url = final_url, verify=False)
        if r.status_code == 200:
            response_body = r.text
            response_body = response_body.replace('\\"', '"')
            camera_array = json.loads(response_body[1:-1])
        else:
            camera_array = "Data not found"

        response[nbhd] = camera_array

    return response

def get_camera_URLs(data, neighborhoods):
    response = {}

    for nbhd in neighborhoods:
        URLs = []
        for camera in data[nbhd]:
            URLs.append(camera['ImageUrl'])

        response[nbhd] = URLs

    return response


all_neighborhoods = ["All"] # This seemingly gets all neighborhoods. Doesn't seem to be documented publically
neighborhoods = ["Ballard", "Central", "Delridge", "Downtown", "East", "Greater Duwamish", "Lake Union", "Magnolia/Queen%20Anne", "North", "Northeast", "Northwest", "Southeast", "Southwest"]
# neighborhoods = ["Ballard"]
URL = "https://web.seattle.gov/Travelers/api/Map/GetCamerasByNeighborhood?neighborhood="
streamURL_start = "https://61e0c5d388c2e.streamlock.net:443/live/"
streamURL_end = ".stream/playlist.m3u8"

camera_data = get_cameras_by_neighborhood(URL, neighborhoods)
all_data = get_cameras_by_neighborhood(URL, all_neighborhoods)
URL_data = get_camera_URLs(camera_data, neighborhoods)
all_URLs = get_camera_URLs(all_data, all_neighborhoods)

# Print how many cameras there are
camera_sum = 0
nbhd_cams = []
for nbhd in neighborhoods:
    cameras = URL_data[nbhd]
    for camera in cameras:
        nbhd_cams.append(camera)
    
    camera_sum += len(cameras)
    print(f"{nbhd} has {len(cameras)} cameras")

print(f"There are {camera_sum} cameras total across Seattle")

cameras_found = 0
no_suffix_count = 0
for camera in all_URLs['All']:
    if camera not in nbhd_cams:
        cameras_found += 1

        # Drop JPG/PNG suffix
        if camera[-4:] in [".jpg", ".png"]:
            filename = camera[:-4]
        else:
            filename = camera
            no_suffix_count += 1

        # print(f"New Camera found: {camera}\nURL: {streamURL_start}{filename}{streamURL_end}")

print(f"{cameras_found} new cameras found. {no_suffix_count} did not end in jpg or png")