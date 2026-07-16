import os
import json
import math
from datetime import datetime, timezone
from sgp4.api import Satrec, WGS84
from core_shared.constants.orbit_analytics_constants import DANGER_RADIUS_KM

class OrbitAnalyticsEngine:
    """Parses JSON TLE data, calculates exact spatial coordinates using SGP4, and filters threats."""

    def __init__(self):
        self.cache_dir = "space_station_node/data"
        self.iss_cache_file = os.path.join(self.cache_dir, "iss_tle_cache.json")
        self.leo_cache_file = os.path.join(self.cache_dir, "leo_tle_cache.json")

    def _load_json_data(self, file_path: str) -> list:
        """Helper method to load cached JSON data."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cache file missing: {file_path}. Run data ingestion first.")
        with open(file_path, 'r') as f:
            return json.load(f)

    def _calculate_euclidean_distance(self, r1: tuple, r2: tuple) -> float:
        """Calculates the precise 3D distance between two X, Y, Z coordinate vectors."""
        # Index 0 = X, Index 1 = Y, Index 2 = Z
        return math.sqrt((r2[0] - r1[0])**2 + (r2[1] - r1[1])**2 + (r2[2] - r1[2])**2)

    def detect_collision_threats(self) -> list:
        """Main analytical function: Compares ISS position against all LEO debris."""
        iss_data = self._load_json_data(self.iss_cache_file)
        leo_data = self._load_json_data(self.leo_cache_file)

        # 1. Initialize the ISS SGP4 Satellite Object
        iss_record = iss_data[0] # Grabs the first (and only) dictionary from the JSON list
        iss_satrec = Satrec.twoline2rv(iss_record['TLE_LINE1'], iss_record['TLE_LINE2'])

        # Get current timezone-aware UTC time for the prediction epoch
        now = datetime.now(timezone.utc)
        jd, fr = jday_from_datetime(now) # Helper function defined below

        # Get exact X, Y, Z for the ISS
        error_iss, r_iss, v_iss = iss_satrec.sgp4(jd, fr)
        if error_iss != 0:
            print("Warning: Could not calculate ISS position.")
            return []

        threats = []
        print(f"\n[ANALYTICS ENGINE] Scanning {len(leo_data)} LEO debris objects against {DANGER_RADIUS_KM}km danger radius...")

        # 2. Iterate through all debris and apply the Spatial Proximity Filter
        for debris in leo_data:
            try:
                deb_satrec = Satrec.twoline2rv(debris['TLE_LINE1'], debris['TLE_LINE2'])
                error_deb, r_deb, v_deb = deb_satrec.sgp4(jd, fr)

                if error_deb == 0:
                    # 3. Calculate distance and check against danger radius threshold
                    distance = self._calculate_euclidean_distance(r_iss, r_deb)
                    
                    if distance <= DANGER_RADIUS_KM:
                        threats.append({
                            "OBJECT_NAME": debris.get('OBJECT_NAME', 'UNKNOWN DEBRIS'),
                            "NORAD_CAT_ID": debris.get('NORAD_CAT_ID'),
                            # "DISTANCE_KM": distance
                            "DISTANCE_KM": round(distance, 2)
                        })
            except (ValueError, KeyError) as e:
                # EXPECTED DATA ERRORS: 
                # KeyError: Space-Track JSON is missing 'TLE_LINE1' or 'TLE_LINE2'
                # ValueError: The SGP4 library cannot mathematically parse the TLE string
                continue
            
            except Exception as e:
                # UNEXPECTED LOGIC ERRORS: 
                # Catches TypeErrors, NameErrors, etc., and forces the script to loudly report it!
                print(f"\n[CRITICAL LOGIC ERROR] Code execution failed on object {debris.get('NORAD_CAT_ID', 'UNKNOWN')}")
                print(f"Error details: {e}")
                raise  # This intentionally crashes the script and prints the exact line that failed
        
        return threats

# Helper mathematical function required by SGP4 to convert Python datetime to Julian Date
def jday_from_datetime(dt: datetime) -> tuple:
    """Converts a standard datetime object into the Julian Date format required by SGP4."""
    year, month, day = dt.year, dt.month, dt.day
    hour, minute, sec = dt.hour, dt.minute, dt.second + dt.microsecond / 1000000.0
    # Standard Julian Date astronomical calculation
    jd = 367.0 * year - int((7 * (year + int((month + 9) / 12.0))) * 0.25) + int(275 * month / 9.0) + day + 1721013.5
    fr = (sec + minute * 60.0 + hour * 3600.0) / 86400.0
    return jd, fr

# For isolated testing of just this file
if __name__ == "__main__":
    analytics = OrbitAnalyticsEngine()
    detected_threats = analytics.detect_collision_threats()
    
    if detected_threats:
        print(f"\n[CRITICAL WARNING] {len(detected_threats)} threats detected within danger radius!")
        for threat in detected_threats:
            print(f" -> {threat['OBJECT_NAME']} (ID: {threat['NORAD_CAT_ID']}) is {threat['DISTANCE_KM']} km away.")
    else:
        print(f"\n[CLEAR] No collision threats detected within {DANGER_RADIUS_KM} km.")