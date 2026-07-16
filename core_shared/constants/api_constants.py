# Base URL for the Space-Track API
BASE_URL = "https://www.space-track.org/"

# Authentication Endpoints
AUTH_ENDPOINT = f"{BASE_URL}ajaxauth/login"
LOGOUT_ENDPOINT = f"{BASE_URL}ajaxauth/logout"

# General Perturbations (GP) Data Queries
# Using JSON format as it is highly extensible and avoids legacy Alpha-5 format issues
ISS_TLE_QUERY = f"{BASE_URL}basicspacedata/query/class/gp/NORAD_CAT_ID/25544/format/json"
LEO_DEBRIS_QUERY = f"{BASE_URL}basicspacedata/query/class/gp/EPOCH/>now-30/MEAN_MOTION/>11.25/format/json"