import aiohttp


class GetRequests:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/api/v1/'

    async def create_car_number(self, parking_id, car_name, car_number, lat, lon, region, is_active=True):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url + 'autos/',
                                        json={"parking_number": parking_id, "car_id": car_number, "car_name": car_name,
                                              "lat": lat, "long": lon, 'category': region,
                                              "is_active": is_active}) as response:
                    if response.status == 201:
                        return await response.json()
                    elif response.status == 404:
                        print(f" {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f" {e}")
            return None

    async def car_search_by_number(self, car_number):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url + f'autos/{car_number}/') as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        print(f"{car_number}toplmadi")
                        return None
                    else:
                        print(f" {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"E{e}")
            return None

    async def get_parking_is_false(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url + 'parkings/') as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        return False
                    else:
                        print(f"Userda xatolik: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"{e}")
            return None

    async def get_regions(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url + 'categoryregions/') as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        return False
                    else:
                        print(f"Userda xatolik: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f": {e}")
            return None

    async def parking_id_true(self, parking_count):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(self.url + f'parkings/{parking_count}/',
                                         json={"is_active": True}) as response:
                    if response.status == 200:
                        return True
                    elif response.status == 404:
                        print(f"{parking_count} toplmadi.")
                        return False
                    else:
                        print(f"{response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"Error updating language: {e}")
            return None

    async def parking_get_location(self, parking_count):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url + f'parkings/{parking_count}/') as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        print(f"{parking_count} not found.")
                        return False
                    else:
                        print(f" {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f": {e}")
            return None

    async def parking_id_false(self, parking_count):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(self.url + f'parkings/{parking_count}/',
                                         json={"is_active": False}) as response:
                    if response.status == 200:
                        return True
                    elif response.status == 404:

                        print(f"{parking_count} Toplmadi")
                        return False
                    else:
                        print(f"{response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f" {e}")
            return None

    async def auto_active_false(self, car_number):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(self.url + f'autos/{car_number}/',
                                         json={"is_active": False}) as response:
                    if response.status == 200:
                        return True
                    elif response.status == 404:
                        print(f"{car_number} toplmadi.")
                        return False
                    else:
                        print(f"{response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f" {e}")
            return None
