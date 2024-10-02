import datetime
import hashlib
import urllib.parse
import json
import os
import time
from datetime import date, datetime
import pymysql
import requests
import scrapy
from scraper_api import ScraperAPIClient
from scrapy.cmdline import execute

from swiggy_instamart_bakeryfood.items import SwiggyInstamartBakeryfoodItem

# client = ScraperAPIClient('64a773e99ca0093e4f80e217a71f821b')
class SpiderSpider(scrapy.Spider):
    name = "spider"

    def __init__(self,start=0,end=0):
        try:
            self.conn = pymysql.Connect(
                host='localhost',
                user='root',
                password='actowiz',
                database='swiggy_instamart_bakeryfood'
            )
            self.cur = self.conn.cursor()
            self.start=start
            self.end=end
        except Exception as e:
            print(e)

    def start_requests(self):

        def adjust_time():
            # Get the current time
            now = datetime.now()

            # Check the hour and adjust the time accordingly
            if now.hour < 10:
                # Set to 10:00 AM today
                next_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
            elif now.hour < 15:
                # Set to 03:00 PM today
                next_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
            elif now.hour < 20:
                # Set to 08:00 PM today
                next_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
            else:
                # Set to 12:00 AM (midnight) the next day
                next_time = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

            # Format the time as requested
            formatted_time = next_time.strftime("%Y_%m_%d_%I_%p")

            return formatted_time

        today_date_time = adjust_time()

        folder_loc = f'C:/Shalu/PageSave/swiggy_instamart_bakeryfood/page_save_{today_date_time}/'

        if not os.path.exists(folder_loc):
            os.mkdir(folder_loc)

        query = f"SELECT * FROM keyword WHERE id BETWEEN {self.start} AND {self.end} "
        self.cur.execute(query)
        keywords = self.cur.fetchall()

        for keyword_row in keywords:
            Keyword = keyword_row[0]

            encoded_keyword = urllib.parse.quote(Keyword)

            query1 = "SELECT * FROM pincodes "
            self.cur.execute(query1)
            pincodes = self.cur.fetchall()

            for pincode_row in pincodes:
                city = pincode_row[0]
                pincode = pincode_row[1]
                storeid = pincode_row[2]
                address=pincode_row[3]
                lat=pincode_row[4]
                long=pincode_row[5]
                Location_info= {
                    "address":address,
                    "lat":lat,
                    "lng":long,
                    }
                if storeid != None:

                    sub_folder_loc = folder_loc + f"{pincode}/"
                    if not os.path.exists(sub_folder_loc):
                        os.mkdir(sub_folder_loc)

                    page = 0
                    count=0
                    main_loc=sub_folder_loc
                    page_loc = main_loc + f"{Keyword}_{page}.json"
                    meta = {
                        "pincode": pincode,
                        "Keyword": Keyword,
                        "city": city,
                        "storeid": storeid,
                        "page_loc": page_loc,
                        "page": page,

                    }

                    if not os.path.isfile(page_loc):
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
                            # 'addressId': 's%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s',
                            'webBottomBarHeight': '0',
                            '_ga_4BQKMMC7Y9': 'GS1.2.1723546342.9.1.1723546348.54.0.0',
                            'ally-on': 'false',
                            'strId': '',
                            'LocSrc': 's%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y',
                            'tid': 's%3A0b3d3345-da43-4bd9-bfe3-f9ae77a13c33.7%2F4US8beLQ%2BkgqzEZveXPI7jwkI05GRAnfkrTf2t%2F4Q',
                            'sid': 's%3Afkbb3a81-ff97-4c1a-8068-7c3286057685.qMLtW8B75%2By2WSh8ew3PrNjpLSJKLt7haGea%2FywpCf4',
                            'accessibility-enabled': 'false',
                            '_guest_tid': 'f4d12fcf-4809-4d47-bd00-515a20c0ef37',
                            '_sid': 'fkb1b388-6938-49e3-a677-37c1345630b9',
                            '_gid': 'GA1.2.1117864398.1723786726',
                            '_ga': 'GA1.1.11593828.1718791436',
                            'dadl': 'true',
                            # 'lat': 's%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k',
                            # 'lng': 's%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk',
                            # 'address': 's%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs',
                            # 'userLocation': '%7B%22address%22%3A%22New%20Delhi%2C%20Delhi%20110017%2C%20India%22%2C%22lat%22%3A28.5279118%2C%22lng%22%3A77.20889869999999%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22other%22%2C%22name%22%3A%22%22%7D',
                            'userLocation': json.dumps(Location_info),
                            '_ga_34JYJ0BCRN': 'GS1.1.1723786725.32.1.1723786773.0.0.0',
                            'imOrderAttribution': '{%22entryId%22:null%2C%22entryName%22:null%2C%22entryContext%22:null%2C%22hpos%22:null%2C%22vpos%22:null%2C%22utm_source%22:null%2C%22utm_medium%22:null%2C%22utm_campaign%22:null}',
                            '_ga_8N8XRG907L': 'GS1.1.1723786702.22.1.1723793680.0.0.0',
                        }

                        headers = {
                            'accept': '*/*',
                            'accept-language': 'en-US,en;q=0.9',
                            'cache-control': 'no-cache',
                            'content-type': 'application/json',
                            'matcher': 'cgfa98e9aegadf8abadddeb',
                            'origin': 'https://www.swiggy.com',
                            'pragma': 'no-cache',
                            'priority': 'u=1, i',
                            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                        }


                        json_data = {
                            'facets': {},
                            'sortAttribute': '',
                        }
                        time.sleep(0.2)
                        response = requests.post(
                            url=f'https://www.swiggy.com/api/instamart/search?pageNumber={page}&searchResultsOffset=0&limit=40&query={encoded_keyword}&age'
                                f'Consent=false&layoutId=3990&pageType=INSTAMART_AUTO_SUGGEST_PAGE&isPreSearchTag=false&highConfidencePageNo=0&lowConfidencePageNo=0&voiceSearchTrackingId=&storeId={storeid}',
                            cookies=cookies,
                            headers=headers,
                            json=json_data,
                        )
                        if response.status_code == 200:
                            with open(page_loc, 'wb') as file:
                                file.write(response.text.encode('utf-8'))
                        if storeid:
                            yield scrapy.Request(
                                url="file://" + page_loc,
                                callback=self.parse,
                                dont_filter=True,
                                meta = {
                                "pincode": pincode,
                                "Keyword": Keyword,
                                "city": city,
                                "storeid": storeid,
                                "main_loc": main_loc,
                                "page": page,
                                "count":count,
                                "Location_info":Location_info,
                                "encoded_keyword":encoded_keyword
                            }
                            )
                        else:
                            yield scrapy.Request(
                                url='https://books.toscrape.com/',
                                callback=self.parse,
                                dont_filter=True,
                                meta={
                                    "pincode": pincode,
                                    "Keyword": Keyword,
                                    "city": city,
                                    "storeid": storeid,
                                    "main_loc": main_loc,
                                    "page": page,
                                    "count": count,
                                    "Location_info": Location_info,
                                    "encoded_keyword": encoded_keyword
                                }
                            )

                    else:
                        yield scrapy.Request(
                            url="file://" + page_loc,
                            callback=self.parse,
                            dont_filter=True,
                            meta={
                                "pincode": pincode,
                                "Keyword": Keyword,
                                "city": city,
                                "storeid": storeid,
                                "main_loc": main_loc,
                                "page": page,
                                "count": count,
                                "Location_info": Location_info,
                                "encoded_keyword": encoded_keyword

                            }
                        )

                else:
                    yield scrapy.Request(
                        url='https://books.toscrape.com/',
                        callback=self.parse,
                        dont_filter=True,
                        meta={
                              "pincode": pincode,
                              "Keyword": Keyword,
                              "city":city,
                              "id": id
                              }
                    )

    def parse(self, response):

        Keyword=response.meta.get('Keyword')
        encoded_keyword=response.meta.get('encoded_keyword')
        storeid=response.meta.get('storeid')
        pincode=response.meta.get('pincode')
        city=response.meta.get('city')
        main_loc=response.meta.get('main_loc')
        page=response.meta.get('page')
        count=response.meta.get('count')
        Location_info=response.meta.get('Location_info')

        date = datetime.now()

        try:
            item = SwiggyInstamartBakeryfoodItem()
            result = json.loads(response.text)
            data = result['data']['widgets'][0]['data']
            for each_data in data:
                if count < 40:
                    count += 1
                    product_id = each_data['product_id']
                    product_name=each_data['display_name']
                    stock=each_data['in_stock']
                    badge = each_data.get('badges', [])

                    badge_text = ""
                    if badge:
                        for each_badges in badge:
                            badge_text = each_badges['badge_text']
                    variations=each_data['variations']
                    for each_varations in variations:
                        item['platform']="SwiggyInstamart"
                        item['pincode']=pincode
                        item['Keyword']=Keyword
                        formatted_date = date.strftime("%d-%b-%y")
                        item['dateOfScrap'] = formatted_date
                        # item['scrapedtime']="10:00 AM"
                        item['scrapedtime'] = "03:00 PM"
                        # item['scrapedtime'] = "08:00 PM"

                        item['productName'] = product_name
                        item['productId'] = product_id
                        item['rank'] = count
                        brand = each_varations['brand']
                        item['brand'] = brand
                        item['price'] = each_varations['price']['offer_price']
                        item['mrp'] = each_varations['price']['mrp']

                        if brand == "The Baker's Dozen":

                            item['isBrandProduct'] = 'True'
                        else:
                            item['isBrandProduct'] = 'False'
                        item['unit'] = each_varations['sku_quantity_with_combo']
                        item['quantity'] = each_varations['max_allowed_quantity']
                        # item['stock']=each_data['in_stock']

                        if stock==True:
                            item['stock'] = 'True'
                        else:
                            item['stock'] = 'False'

                        item['sponsored'] = 'True' if badge_text else 'False'
                        item['rating'] = ''
                        item['review_count'] = ''
                        yield item
                        break

            page += 1
            if page <= 1:

                page_loc = main_loc + f"{Keyword}_{page}.json"

                if not os.path.isfile(page_loc):
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
                        # 'addressId': 's%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s',
                        'webBottomBarHeight': '0',
                        '_ga_4BQKMMC7Y9': 'GS1.2.1723546342.9.1.1723546348.54.0.0',
                        'ally-on': 'false',
                        'strId': '',
                        'LocSrc': 's%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y',
                        'tid': 's%3A0b3d3345-da43-4bd9-bfe3-f9ae77a13c33.7%2F4US8beLQ%2BkgqzEZveXPI7jwkI05GRAnfkrTf2t%2F4Q',
                        'sid': 's%3Afkbb3a81-ff97-4c1a-8068-7c3286057685.qMLtW8B75%2By2WSh8ew3PrNjpLSJKLt7haGea%2FywpCf4',
                        'accessibility-enabled': 'false',
                        '_guest_tid': 'f4d12fcf-4809-4d47-bd00-515a20c0ef37',
                        '_sid': 'fkb1b388-6938-49e3-a677-37c1345630b9',
                        '_gid': 'GA1.2.1117864398.1723786726',
                        '_ga': 'GA1.1.11593828.1718791436',
                        'dadl': 'true',
                        # 'lat': 's%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k',
                        # 'lng': 's%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk',
                        # 'address': 's%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs',
                        'userLocation': json.dumps(Location_info),
                        '_ga_34JYJ0BCRN': 'GS1.1.1723786725.32.1.1723786773.0.0.0',
                        '_ga_8N8XRG907L': 'GS1.1.1723786702.22.1.1723793680.0.0.0',
                        'imOrderAttribution': '{%22entryId%22:%22cake%22%2C%22entryName%22:%22instamartOpenSearch%22}',
                    }

                    headers = {
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'cache-control': 'no-cache',
                        'content-type': 'application/json',
                        # 'cookie': '__SW=W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh; _device_id=75be40f9-a0c3-4e0e-1c86-d1f2ced0c907; _gcl_au=1.1.406511299.1718791436; _fbp=fb.1.1719233702143.931722654449798998; fontsLoaded=1; deviceId=s%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs; versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; isNative=false; openIMHP=false; addressId=s%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s; webBottomBarHeight=0; _ga_4BQKMMC7Y9=GS1.2.1723546342.9.1.1723546348.54.0.0; ally-on=false; strId=; LocSrc=s%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y; tid=s%3A0b3d3345-da43-4bd9-bfe3-f9ae77a13c33.7%2F4US8beLQ%2BkgqzEZveXPI7jwkI05GRAnfkrTf2t%2F4Q; sid=s%3Afkbb3a81-ff97-4c1a-8068-7c3286057685.qMLtW8B75%2By2WSh8ew3PrNjpLSJKLt7haGea%2FywpCf4; accessibility-enabled=false; _guest_tid=f4d12fcf-4809-4d47-bd00-515a20c0ef37; _sid=fkb1b388-6938-49e3-a677-37c1345630b9; _gid=GA1.2.1117864398.1723786726; _ga=GA1.1.11593828.1718791436; dadl=true; lat=s%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k; lng=s%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk; address=s%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs; userLocation=%7B%22address%22%3A%22New%20Delhi%2C%20Delhi%20110017%2C%20India%22%2C%22lat%22%3A28.5279118%2C%22lng%22%3A77.20889869999999%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D; _ga_34JYJ0BCRN=GS1.1.1723786725.32.1.1723786773.0.0.0; _ga_8N8XRG907L=GS1.1.1723786702.22.1.1723793680.0.0.0; imOrderAttribution={%22entryId%22:%22cake%22%2C%22entryName%22:%22instamartOpenSearch%22}',
                        'matcher': '99fe78e9aegaeb7c9d9afc7',
                        'origin': 'https://www.swiggy.com',
                        'pragma': 'no-cache',
                        'priority': 'u=1, i',
                        # 'referer': 'https://www.swiggy.com/instamart/search?custom_back=true&query=cake',
                        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    }

                    json_data = {
                        'facets': {},
                        'sortAttribute': '',
                    }

                    response = requests.post(
                        url=f'https://www.swiggy.com/api/instamart/search?pageNumber={page}&searchResultsOffset=20&limit=40&query={encoded_keyword}&ageConsent=false&layoutId=3990&pageType=INSTAMART_AUTO_SUGGEST_PAGE&isPreSearchTag=false&highConfidencePageNo=0&lowConfidencePageNo=0&voiceSearchTrackingId=&storeId={storeid}',
                        cookies=cookies,
                        headers=headers,
                        json=json_data
                    )

                    if response.status_code == 200:
                        with open(page_loc, 'wb') as file:
                            file.write(response.text.encode('utf-8'))

                    yield scrapy.Request(
                        url="file://" + page_loc,
                        callback=self.parse,
                        dont_filter=True,
                        meta={
                            "pincode": pincode,
                            "Keyword": Keyword,
                            "city": city,
                            "storeid": storeid,
                            "main_loc": main_loc,
                            "page": page,
                            "count": count,
                            "Location_info": Location_info
                        }
                    )
                else:
                    yield scrapy.Request(
                        url="file://" + page_loc,
                        callback=self.parse,
                        dont_filter=True,
                        meta={
                            "pincode": pincode,
                            "Keyword": Keyword,
                            "city": city,
                            "storeid": storeid,
                            "main_loc": main_loc,
                            "page": page,
                            "count": count,
                            "Location_info": Location_info
                        }
                    )



        except Exception as e:
            item = SwiggyInstamartBakeryfoodItem()
            item['platform'] = "SwiggyInstamart"
            item['pincode'] = response.request.meta['pincode']
            item['Keyword'] =response.request.meta['Keyword']

            formatted_date = date.strftime("%d-%b-%y")
            item['dateOfScrap'] = formatted_date
            # item['scrapedtime'] = "10:00 AM"
            item['scrapedtime'] = "03:00 PM"
            # item['scrapedtime'] = "08:00 PM"

            item['productName'] = ''
            item['productId'] = ''
            item['rank'] = ''

            item['brand'] = ''
            item['price'] = ''
            item['mrp'] = ''
            item['isBrandProduct'] = ''
            item['unit'] = ''
            item['quantity'] = ''
            item['stock'] = ''
            item['sponsored'] = ''
            item['rating'] = ''
            item['review_count'] = ''
            yield item



if __name__ == '__main__':

    def adjust_time():
        # Get the current time
        now = datetime.now()

        # Check the hour and adjust the time accordingly
        if now.hour < 10:
            # Set to 10:00 AM today
            next_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
        elif now.hour < 15:
            # Set to 03:00 PM today
            next_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
        elif now.hour < 20:
            # Set to 08:00 PM today
            next_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
        else:
            # Set to 12:00 AM (midnight) the next day
            next_time = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        # Format the time as requested
        formatted_time = next_time.strftime("%Y_%m_%d_%I_%p")

        return formatted_time


    today_date_time = adjust_time()

    folder_loc = f'C:/Shalu/LiveProjects/swiggy_instamart_bakeryfood/data_files/{today_date_time}/'

    if not os.path.exists(folder_loc):
        os.mkdir(folder_loc)

    execute(f'scrapy crawl spider -a start=0 -a end=20 '.split())
