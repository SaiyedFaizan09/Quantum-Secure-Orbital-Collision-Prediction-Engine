import os
import json
import time
import asyncio
import aiohttp
from dotenv import load_dotenv

# Importing our separated concerns
from core_shared.constants.api_constants import AUTH_ENDPOINT, LOGOUT_ENDPOINT, ISS_TLE_QUERY, LEO_DEBRIS_QUERY
from core_shared.exceptions.api_exceptions import AuthenticationError, RateLimitExceededError

class TLEIngestionService:
    """Handles secure async authentication, caching, and ingestion of TLE data from Space-Track.org."""

    def __init__(self):
        # 1. Load environment variables securely
        load_dotenv()
        self.username = os.getenv("SPACE_TRACK_USERNAME")
        self.password = os.getenv("SPACE_TRACK_PASSWORD")
        
        # 2. Define cache directories
        self.cache_dir = "space_station_node/data"
        self.iss_cache_file = os.path.join(self.cache_dir, "iss_tle_cache.json")
        self.leo_cache_file = os.path.join(self.cache_dir, "leo_tle_cache.json")

    def is_cache_valid(self, file_path: str, max_age_seconds: int = 3600) -> bool:
        """Checks if the local cache file exists and is newer than max_age_seconds (1 hour)."""
        if not os.path.exists(file_path):
            return False
            
        file_age = time.time() - os.path.getmtime(file_path)
        return file_age < max_age_seconds

    async def _authenticate(self, session: aiohttp.ClientSession) -> None:
        """Securely logs in via POST request to establish an encrypted async session cookie."""
        payload = {'identity': self.username, 'password': self.password}
        
        async with session.post(AUTH_ENDPOINT, data=payload) as response:
            if response.status != 200:
                raise AuthenticationError(f"Login failed with HTTP Status {response.status}. Check .env credentials.")
            # aiohttp automatically captures and stores the encrypted session cookie from the response.

    async def _fetch_and_cache(self, session: aiohttp.ClientSession, url: str, cache_path: str) -> dict:
        """Asynchronously fetches JSON data from the API and saves it to the local cache."""
        async with session.get(url) as response:
            if response.status in (401, 403):
                raise AuthenticationError("Session cookie invalid or unauthorized.")
            elif response.status in (429, 500, 503):
                raise RateLimitExceededError("Rate limit hit! Limit queries to < 30 per minute and < 300 per hour.")
            
            data = await response.json()
            
            # Save to local cache
            with open(cache_path, 'w') as f:
                json.dump(data, f)
            
            return data

    async def run_ingestion_pipeline(self) -> tuple:
        """Main orchestrator: Checks cache first, and ONLY authenticates if fresh data is needed."""
        iss_data, leo_data = None, None
        
        # Step 1: Check which files actually need downloading
        needs_iss_download = not self.is_cache_valid(self.iss_cache_file)
        needs_leo_download = not self.is_cache_valid(self.leo_cache_file)

        # Step 2: Load valid local caches immediately (Zero Network Calls!)
        if not needs_iss_download:
            file_age_seconds = time.time() - os.path.getmtime(self.iss_cache_file)
            minutes_left = int((3600 - file_age_seconds) / 60)
            print(f'- ISS Data Fetching From Local Cache... (Fresh data available in {minutes_left} minutes)')
            with open(self.iss_cache_file, 'r') as f:
                iss_data = json.load(f)

        if not needs_leo_download:
            file_age_seconds = time.time() - os.path.getmtime(self.leo_cache_file)
            minutes_left = int((3600 - file_age_seconds) / 60)
            print(f'- LEO Data Fetching From Local Cache... (Fresh data available in {minutes_left} minutes)')
            with open(self.leo_cache_file, 'r') as f:
                leo_data = json.load(f)

        # Step 3: ONLY open a network session if a download is explicitly required
        if needs_iss_download or needs_leo_download:
            print('- Cache expired or missing. Opening secure connection to Space-Track.org...')
            async with aiohttp.ClientSession() as session:
                
                # Authenticate once
                await self._authenticate(session)
                tasks = []

                if needs_iss_download:
                    tasks.append(self._fetch_and_cache(session, ISS_TLE_QUERY, self.iss_cache_file))
                
                if needs_leo_download:
                    tasks.append(self._fetch_and_cache(session, LEO_DEBRIS_QUERY, self.leo_cache_file))

                # Execute needed downloads concurrently
                results = await asyncio.gather(*tasks)
                
                # Unpack results safely
                if needs_iss_download and needs_leo_download:
                    iss_data, leo_data = results
                elif needs_iss_download:
                    iss_data = results
                elif needs_leo_download:
                    leo_data = results

                # Securely log out
                await session.get(LOGOUT_ENDPOINT)

        return iss_data, leo_data

# For isolated testing of just this file
if __name__ == "__main__":
    service = TLEIngestionService()
    # In Python, async functions must be executed inside an event loop
    iss, leo = asyncio.run(service.run_ingestion_pipeline())
    print(f"Successfully loaded ISS records: {len(iss)}")
    print(f"Successfully loaded LEO Debris records: {len(leo)}")