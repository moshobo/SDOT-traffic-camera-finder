import json
import requests
import time
from copy import deepcopy

ALL_NEIGHBORHOODS = ["All"] # This seemingly gets all neighborhoods. Doesn't seem to be documented publically
NEIGHBORHOODS = ["Ballard", "Central", "Delridge", "Downtown", "East", "Greater Duwamish", "Lake Union", "Magnolia/Queen%20Anne", "North", "Northeast", "Northwest", "Southeast", "Southwest"]
CAMERA_URL = "https://web.seattle.gov/Travelers/api/Map/GetCamerasByNeighborhood?neighborhood="
STREAM_URL_START = "https://61e0c5d388c2e.streamlock.net/live/"
STREAM_URL_END = ".stream/playlist.m3u8"

def make_get_request(url):
    req_count = 0
    max_req = 5

    while req_count < max_req:
        try:
            r = requests.get(url, timeout=(5, 10))
            return r
        except:
            time.sleep(5)
            req_count += 1
            print(f"Retrying Request to {url}: Request {req_count} of {max_req}")
    
    return None

def get_cameras_by_neighborhood(url, neighborhoods):
    response = {}
    
    for nbhd in neighborhoods:
        r = make_get_request(url + nbhd)

        if r.status_code == 200:
            response_body = r.text
            response_body = response_body.replace('\\"', '"')
            camera_array = json.loads(response_body[1:-1])
        else:
            camera_array = "Data not found"

        response[nbhd] = camera_array

    return response

def get_camera_ImageURLs(data, neighborhoods):
    response = {}

    for nbhd in neighborhoods:
        URLs = []
        for camera in data[nbhd]:
            URLs.append(camera['ImageUrl'])

        response[nbhd] = URLs

    return response

def convert_ImageURL(startURL, endURL, ImageURL):
    if ImageURL[-4:] in ['.jpg', '.png']:
        url = startURL + ImageURL[:-4] + endURL
    else:
        url = startURL + ImageURL + endURL
    
    return url

def get_stream_dict(data, neighborhoods):
    camera_dict = {}
    for nbhd in neighborhoods:
        for camera in data[nbhd]:
            streamURL = convert_ImageURL(STREAM_URL_START, STREAM_URL_END, camera)
            status = get_camera_status(streamURL)
            address = camera.replace('_', ' ')[:-4]
            camera_dict[camera] = {
                "Address": address,
                "url": streamURL,
                "status": status,
                "neighborhood": nbhd
            }

    return camera_dict

def get_camera_status(url):
    """Determine whether camera is online by response status code"""
    r = make_get_request(url)
    if r.status_code == 200:
        status = 'online'
    else:
        status = 'offline'
    
    return status

def group_streams_by_neighborhood(dict):
    neighborhoods = {}
    for name, details in dict.items():
        neighborhood = details['neighborhood']
        if neighborhood not in neighborhoods:
            neighborhoods[neighborhood] = []
        neighborhoods[neighborhood].append(details)

    # Sort by status, then name
    for nbhd, cameras in neighborhoods.items():
        neighborhoods[nbhd] = sorted(cameras, key=lambda x: (x['status'] == 'offline', x['Address']))

    return neighborhoods

def find_alt_cameras(cameras):
    """Find new cameras by using alternate suffixes"""
    suffixes = ["NS", "EW", "NWC", "NEC", "SEC", "SWC"]
    alt_cameras = []
    for camera in cameras:
        suffixes_mod = deepcopy(suffixes)
        no_sfx = camera.rsplit("_", 1)[0]

        # remove original suffix from list
        try:
            original_sfx = camera.rsplit("_", 1)[1].rsplit(".", 1)[0]
            suffixes_mod.remove(original_sfx)
        except:
            continue

        for sfx in suffixes_mod:
            alt_url = STREAM_URL_START + no_sfx + "_" + sfx + STREAM_URL_END
            if get_camera_status(alt_url) == 'online':
                final_camera = no_sfx + "_" + sfx + ".jpg"
                if final_camera not in cameras:
                    print(f"New Camera Found: {final_camera}")
                    alt_cameras.append(final_camera)

    return alt_cameras

def log_camera_stats(all_URLs, URL_data, neighborhoods):
    # Print how many cameras there are
    camera_sum = 0
    nbhd_cams = []
    if len(neighborhoods) != 0:
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

            # print(f"New Camera found: {camera}\nURL: {STREAM_URL_START}{filename}{STREAM_URL_END}")

    print(f"{cameras_found} new cameras found. {no_suffix_count} did not end in jpg or png")

if __name__ == "__main__":
    pass