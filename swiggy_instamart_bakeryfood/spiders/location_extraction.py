import os
from datetime import date

import pandas as pd
import pymysql
import requests
import scrapy
from scrapy.cmdline import execute


class LocationExtractionSpider(scrapy.Spider):
    name = "location_extraction"

    def __init__(self):
        try:
            self.conn = pymysql.Connect(
                host='localhost',
                user='root',
                password='actowiz',
                database='swiggy_instamart_bakeryfood'
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    def start_requests(self):
        excel_file=r'C:\Shalu\LiveProjects\swiggy_instamart_bakeryfood\input_files\pincodes.xlsx'
        df = pd.read_excel(excel_file)  # Adjust sheet name as necessary

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():

                city = row['city']
                pincode = row['pincode']
                storeid = row['storeid']

                cookies = {
                    '__SW': 'W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh',
                    '_device_id': '75be40f9-a0c3-4e0e-1c86-d1f2ced0c907',
                    '_gcl_au': '1.1.406511299.1718791436',
                    '_fbp': 'fb.1.1719233702143.931722654449798998',
                    'fontsLoaded': '1',
                    'deviceId': 's%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs',
                    'versionCode': '1200',
                    'platform': 'web',
                    'subplatform': 'dweb',
                    'statusBarHeight': '0',
                    'bottomOffset': '0',
                    'genieTrackOn': 'false',
                    'isNative': 'false',
                    'openIMHP': 'false',
                    'addressId': 's%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s',
                    'webBottomBarHeight': '0',
                    '_ga_4BQKMMC7Y9': 'GS1.2.1723546342.9.1.1723546348.54.0.0',
                    '_gid': 'GA1.2.1530605234.1724130474',
                    'dadl': 'true',
                    'ally-on': 'false',
                    'strId': '',
                    'LocSrc': 's%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y',
                    'accessibility-enabled': 'false',
                    '_ga': 'GA1.1.11593828.1718791436',
                    'tid': 's%3Aa0ec8a5e-a510-4ce7-9167-2fbc9823cea4.%2FWtOKG7zvm4Y3d6qefovzR5Na%2BYDCcxJqQaimWarY28',
                    '_guest_tid': 'e134639e-874f-463b-9e43-9a2bc2fe62ad',
                    '_is_logged_in': '',
                    '_sid': 'fnrba103-46f7-409b-94ff-b1de28328ab6',
                    'sid': 's%3Afnrba103-46f7-409b-94ff-b1de28328ab6.cQS1EjMJJipYyiPDaIdqrnNaMxOdD3SZFvszKa%2BfpIQ',
                    # 'lat': 's%3A12.9698066.6cGBOZX22PZX3ODVeXG8s4H5x2%2F%2BaYIepEppMh%2F3N%2Fs',
                    # 'lng': 's%3A77.7499632.H6doFYjT%2BXs4XCWBq%2B4S8bEAxREsdFffaZE7e93t348',
                    # 'address': 's%3ABengaluru%2C%20Karnataka%20560066%2C%20India.DBHueM31jaCmQJBDxC5dOLRScPt0iXumL56rfzgp%2Fd4',
                    # 'userLocation': '%7B%22address%22%3A%22Bengaluru%2C%20Karnataka%20560066%2C%20India%22%2C%22lat%22%3A12.9698066%2C%22lng%22%3A77.7499632%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D',
                    '_ga_34JYJ0BCRN': 'GS1.1.1724236380.39.0.1724236380.0.0.0',
                    'imOrderAttribution': '{%22entryId%22:null%2C%22entryName%22:null%2C%22entryContext%22:null%2C%22hpos%22:null%2C%22vpos%22:null%2C%22utm_source%22:null%2C%22utm_medium%22:null%2C%22utm_campaign%22:null}',
                    '_ga_8N8XRG907L': 'GS1.1.1724236383.35.0.1724236764.0.0.0',
                }

                headers = {
                    '__fetch_req__': 'true',
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'content-type': 'application/json',
                    # 'cookie': '__SW=W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh; _device_id=75be40f9-a0c3-4e0e-1c86-d1f2ced0c907; _gcl_au=1.1.406511299.1718791436; _fbp=fb.1.1719233702143.931722654449798998; fontsLoaded=1; deviceId=s%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs; versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; isNative=false; openIMHP=false; addressId=s%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s; webBottomBarHeight=0; _ga_4BQKMMC7Y9=GS1.2.1723546342.9.1.1723546348.54.0.0; _gid=GA1.2.1530605234.1724130474; dadl=true; ally-on=false; strId=; LocSrc=s%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y; accessibility-enabled=false; _ga=GA1.1.11593828.1718791436; tid=s%3Aa0ec8a5e-a510-4ce7-9167-2fbc9823cea4.%2FWtOKG7zvm4Y3d6qefovzR5Na%2BYDCcxJqQaimWarY28; _guest_tid=e134639e-874f-463b-9e43-9a2bc2fe62ad; _is_logged_in=; _sid=fnrba103-46f7-409b-94ff-b1de28328ab6; sid=s%3Afnrba103-46f7-409b-94ff-b1de28328ab6.cQS1EjMJJipYyiPDaIdqrnNaMxOdD3SZFvszKa%2BfpIQ; lat=s%3A12.9698066.6cGBOZX22PZX3ODVeXG8s4H5x2%2F%2BaYIepEppMh%2F3N%2Fs; lng=s%3A77.7499632.H6doFYjT%2BXs4XCWBq%2B4S8bEAxREsdFffaZE7e93t348; address=s%3ABengaluru%2C%20Karnataka%20560066%2C%20India.DBHueM31jaCmQJBDxC5dOLRScPt0iXumL56rfzgp%2Fd4; userLocation=%7B%22address%22%3A%22Bengaluru%2C%20Karnataka%20560066%2C%20India%22%2C%22lat%22%3A12.9698066%2C%22lng%22%3A77.7499632%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D; _ga_34JYJ0BCRN=GS1.1.1724236380.39.0.1724236380.0.0.0; imOrderAttribution={%22entryId%22:null%2C%22entryName%22:null%2C%22entryContext%22:null%2C%22hpos%22:null%2C%22vpos%22:null%2C%22utm_source%22:null%2C%22utm_medium%22:null%2C%22utm_campaign%22:null}; _ga_8N8XRG907L=GS1.1.1724236383.35.0.1724236764.0.0.0',
                    'pragma': 'no-cache',
                    'priority': 'u=1, i',
                    'referer': 'https://www.swiggy.com/',
                    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                }

                params = {
                    'input': 'Delhi\t110017',
                    'types': '',
                }

                r1 = requests.get(f'https://www.swiggy.com/dapi/misc/place-autocomplete?input={city}%09{pincode}&types=',
                                        cookies=cookies, headers=headers).json()
                data=r1['data']
                for each_data in data:
                    description=each_data['description']
                    place_id=each_data['place_id']

                    print()

                    cookies = {
                        '__SW': 'W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh',
                        '_device_id': '75be40f9-a0c3-4e0e-1c86-d1f2ced0c907',
                        '_gcl_au': '1.1.406511299.1718791436',
                        '_fbp': 'fb.1.1719233702143.931722654449798998',
                        'fontsLoaded': '1',
                        'deviceId': 's%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs',
                        'versionCode': '1200',
                        'platform': 'web',
                        'subplatform': 'dweb',
                        'statusBarHeight': '0',
                        'bottomOffset': '0',
                        'genieTrackOn': 'false',
                        'isNative': 'false',
                        'openIMHP': 'false',
                        'addressId': 's%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s',
                        'webBottomBarHeight': '0',
                        '_ga_4BQKMMC7Y9': 'GS1.2.1723546342.9.1.1723546348.54.0.0',
                        '_gid': 'GA1.2.1530605234.1724130474',
                        'dadl': 'true',
                        'ally-on': 'false',
                        'strId': '',
                        'LocSrc': 's%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y',
                        'accessibility-enabled': 'false',
                        'tid': 's%3Aa0ec8a5e-a510-4ce7-9167-2fbc9823cea4.%2FWtOKG7zvm4Y3d6qefovzR5Na%2BYDCcxJqQaimWarY28',
                        '_guest_tid': 'e134639e-874f-463b-9e43-9a2bc2fe62ad',
                        '_sid': 'fnrba103-46f7-409b-94ff-b1de28328ab6',
                        'sid': 's%3Afnrba103-46f7-409b-94ff-b1de28328ab6.cQS1EjMJJipYyiPDaIdqrnNaMxOdD3SZFvszKa%2BfpIQ',
                        'imOrderAttribution': '{%22entryId%22:null%2C%22entryName%22:null%2C%22entryContext%22:null%2C%22hpos%22:null%2C%22vpos%22:null%2C%22utm_source%22:null%2C%22utm_medium%22:null%2C%22utm_campaign%22:null}',
                        'lat': 's%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k',
                        'lng': 's%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk',
                        'address': 's%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs',
                        '_ga': 'GA1.1.11593828.1718791436',
                        'userLocation': '%7B%22address%22%3A%22New%20Delhi%2C%20Delhi%20110017%2C%20India%22%2C%22lat%22%3A28.5279118%2C%22lng%22%3A77.20889869999999%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D',
                        '_ga_34JYJ0BCRN': 'GS1.1.1724236380.39.1.1724237869.0.0.0',
                        '_ga_8N8XRG907L': 'GS1.1.1724236383.35.1.1724237871.0.0.0',
                    }

                    headers = {
                        '__fetch_req__': 'true',
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'cache-control': 'no-cache',
                        'content-type': 'application/json',
                        # 'cookie': '__SW=W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh; _device_id=75be40f9-a0c3-4e0e-1c86-d1f2ced0c907; _gcl_au=1.1.406511299.1718791436; _fbp=fb.1.1719233702143.931722654449798998; fontsLoaded=1; deviceId=s%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs; versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; isNative=false; openIMHP=false; addressId=s%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s; webBottomBarHeight=0; _ga_4BQKMMC7Y9=GS1.2.1723546342.9.1.1723546348.54.0.0; _gid=GA1.2.1530605234.1724130474; dadl=true; ally-on=false; strId=; LocSrc=s%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y; accessibility-enabled=false; tid=s%3Aa0ec8a5e-a510-4ce7-9167-2fbc9823cea4.%2FWtOKG7zvm4Y3d6qefovzR5Na%2BYDCcxJqQaimWarY28; _guest_tid=e134639e-874f-463b-9e43-9a2bc2fe62ad; _sid=fnrba103-46f7-409b-94ff-b1de28328ab6; sid=s%3Afnrba103-46f7-409b-94ff-b1de28328ab6.cQS1EjMJJipYyiPDaIdqrnNaMxOdD3SZFvszKa%2BfpIQ; imOrderAttribution={%22entryId%22:null%2C%22entryName%22:null%2C%22entryContext%22:null%2C%22hpos%22:null%2C%22vpos%22:null%2C%22utm_source%22:null%2C%22utm_medium%22:null%2C%22utm_campaign%22:null}; lat=s%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k; lng=s%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk; address=s%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs; _ga=GA1.1.11593828.1718791436; userLocation=%7B%22address%22%3A%22New%20Delhi%2C%20Delhi%20110017%2C%20India%22%2C%22lat%22%3A28.5279118%2C%22lng%22%3A77.20889869999999%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D; _ga_34JYJ0BCRN=GS1.1.1724236380.39.1.1724237869.0.0.0; _ga_8N8XRG907L=GS1.1.1724236383.35.1.1724237871.0.0.0',
                        'pragma': 'no-cache',
                        'priority': 'u=1, i',
                        'referer': 'https://www.swiggy.com/',
                        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    }

                    params = {
                        'place_id': 'ChIJxeVSwPXhDDkR9CesZhracFM',
                    }
                    # https://www.swiggy.com/dapi/misc/address-recommend?place_id=ChIJxeVSwPXhDDkR9CesZhracFM
                    r2 = requests.get(f'https://www.swiggy.com/dapi/misc/address-recommend?place_id={place_id}',
                                            cookies=cookies, headers=headers).json()
                    data=r2['data']
                    for each_data in data:
                        address=each_data['formatted_address']
                        lat=each_data['geometry']['location']['lat']
                        lng=each_data['geometry']['location']['lng']

                        cookies = {
                            '__SW': 'W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh',
                            '_device_id': '75be40f9-a0c3-4e0e-1c86-d1f2ced0c907',
                            '_gcl_au': '1.1.406511299.1718791436',
                            '_fbp': 'fb.1.1719233702143.931722654449798998',
                            'fontsLoaded': '1',
                            'deviceId': 's%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs',
                            'versionCode': '1200',
                            'platform': 'web',
                            'subplatform': 'dweb',
                            'statusBarHeight': '0',
                            'bottomOffset': '0',
                            'genieTrackOn': 'false',
                            'isNative': 'false',
                            'openIMHP': 'false',
                            'addressId': 's%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s',
                            'webBottomBarHeight': '0',
                            '_ga_4BQKMMC7Y9': 'GS1.2.1723546342.9.1.1723546348.54.0.0',
                            '_gid': 'GA1.2.1530605234.1724130474',
                            'dadl': 'true',
                            'ally-on': 'false',
                            'strId': '',
                            'LocSrc': 's%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y',
                            'accessibility-enabled': 'false',
                            'tid': 's%3Aa0ec8a5e-a510-4ce7-9167-2fbc9823cea4.%2FWtOKG7zvm4Y3d6qefovzR5Na%2BYDCcxJqQaimWarY28',
                            '_guest_tid': 'e134639e-874f-463b-9e43-9a2bc2fe62ad',
                            '_sid': 'fnrba103-46f7-409b-94ff-b1de28328ab6',
                            'sid': 's%3Afnrba103-46f7-409b-94ff-b1de28328ab6.cQS1EjMJJipYyiPDaIdqrnNaMxOdD3SZFvszKa%2BfpIQ',
                            # 'lat': 's%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k',
                            # 'lng': 's%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk',
                            # 'address': 's%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs',
                            '_ga': 'GA1.1.11593828.1718791436',
                            '_ga_8N8XRG907L': 'GS1.1.1724236383.35.1.1724237871.0.0.0',
                            # 'userLocation': '%7B%22address%22%3A%22New%20Delhi%2C%20Delhi%20110017%2C%20India%22%2C%22lat%22%3A28.5279118%2C%22lng%22%3A77.20889869999999%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D',
                            '_ga_34JYJ0BCRN': 'GS1.1.1724240254.40.0.1724240254.0.0.0',
                        }

                        headers = {
                            'accept': '*/*',
                            'accept-language': 'en-US,en;q=0.9',
                            'cache-control': 'no-cache',
                            # 'cookie': '__SW=W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh; _device_id=75be40f9-a0c3-4e0e-1c86-d1f2ced0c907; _gcl_au=1.1.406511299.1718791436; _fbp=fb.1.1719233702143.931722654449798998; fontsLoaded=1; deviceId=s%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs; versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; isNative=false; openIMHP=false; addressId=s%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s; webBottomBarHeight=0; _ga_4BQKMMC7Y9=GS1.2.1723546342.9.1.1723546348.54.0.0; _gid=GA1.2.1530605234.1724130474; dadl=true; ally-on=false; strId=; LocSrc=s%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y; accessibility-enabled=false; tid=s%3Aa0ec8a5e-a510-4ce7-9167-2fbc9823cea4.%2FWtOKG7zvm4Y3d6qefovzR5Na%2BYDCcxJqQaimWarY28; _guest_tid=e134639e-874f-463b-9e43-9a2bc2fe62ad; _sid=fnrba103-46f7-409b-94ff-b1de28328ab6; sid=s%3Afnrba103-46f7-409b-94ff-b1de28328ab6.cQS1EjMJJipYyiPDaIdqrnNaMxOdD3SZFvszKa%2BfpIQ; lat=s%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k; lng=s%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk; address=s%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs; _ga=GA1.1.11593828.1718791436; _ga_8N8XRG907L=GS1.1.1724236383.35.1.1724237871.0.0.0; userLocation=%7B%22address%22%3A%22New%20Delhi%2C%20Delhi%20110017%2C%20India%22%2C%22lat%22%3A28.5279118%2C%22lng%22%3A77.20889869999999%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D; _ga_34JYJ0BCRN=GS1.1.1724240254.40.0.1724240254.0.0.0',
                            'entrycontext': '',
                            'entryid': '',
                            'entryname': '',
                            'hpos': '',
                            'matcher': 'dd8dd8e9b9b79cbeba8bf97',
                            'pragma': 'no-cache',
                            'priority': 'u=1, i',
                            'referer': 'https://www.swiggy.com/instamart/',
                            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                            'utm_campaign': '',
                            'utm_medium': '',
                            'utm_source': '',
                            'vpos': '',
                        }

                        params = {
                            'clientId': 'INSTAMART-APP',
                        }
                        # https://www.swiggy.com/api/instamart/home?clientId=INSTAMART-APP
                        r3 = requests.get('https://www.swiggy.com/api/instamart/home?clientId=INSTAMART-APP',
                                                cookies=cookies, headers=headers).json()
                        print()


                        print()
                # except Exception as e:
                #     print(e)


    def parse(self, response):
        pass

if __name__ == '__main__':
    execute('scrapy crawl location_extraction'.split())
