import json
import os
import time
from datetime import date, datetime

import pymysql
import scrapy
from scrapy.cmdline import execute

from swiggy_instamart_bakeryfood.items import SwiggyInstamartBakeryfoodItem1


class Spider1Spider(scrapy.Spider):
    name = "spider1"
    # allowed_domains = ["swiggy.com"]
    # start_urls = ["https://swiggy.com"]

    def __init__(self,start=0,end=0):
        # Connect to MySQL database
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='actowiz',
            database='swiggy_instamart_bakeryfood'
        )
        self.cursor = self.conn.cursor()
        self.start=start
        self.end=end


    def start_requests(self):


        def adjust_time():
            # Get the current time
            now = datetime.now()

            # Check the hour and adjust the time accordingly
            if now.hour < 10:
                # Set to the next hour, less than 10:00 AM
                next_time = now.replace(hour=10, minute=0, second=0, microsecond=0)
            elif now.hour < 15:
                # Set to the next hour, less than 03:00 PM
                next_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
            elif now.hour < 20:
                # Set to the next hour, less than 08:00 PM
                next_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
            elif now.hour < 22:
                # Set to the next hour, less than 08:00 PM
                next_time = now.replace(hour=22, minute=0, second=0, microsecond=0)

            # Format the time as requested
            formatted_time = next_time.strftime("%Y_%m_%d_%I_%p")

            return formatted_time


        today_date_time = adjust_time()

        folder_loc = f'C:/Shalu/PageSave/swiggy_instamart_bakeryfood/page_save_{today_date_time}/product_page/'

        if not os.path.exists(folder_loc):
            os.mkdir(folder_loc)
        # query = f"SELECT *FROM product_data{today_date_time} where status='pending' and product_url='' limit 1"
        query = f"SELECT * FROM product_data{today_date_time} WHERE status='pending' AND id BETWEEN {self.start} AND {self.end}"

        print(query)

        # Execute the query
        self.cursor.execute(query)

        # Fetch all rows at once
        rows = self.cursor.fetchall()

        # Iterate through each row in the result set
        for row in rows:
            id=row[0]
            pincode=row[5]
            city=row[4]
            rank=row[3]
            sponsored=row[2]
            product_id=row[1]
            location=row[8]
            storeid=row[6]
            prod_url=row[7]
            Keyword=row[9]
            platform=row[10]

            sub_folder_loc = folder_loc + f"{pincode}/"
            if not os.path.exists(sub_folder_loc):
                os.mkdir(sub_folder_loc)
            page_loc = sub_folder_loc + f"{product_id}.html"
            if storeid==None:
                yield scrapy.Request(
                    # url=urls[0],
                    url='https://www.google.com/',
                    # cookies=cookies,
                    # headers=headers,
                    # body=json.dumps(json_data),
                    # url=f'https://www.swiggy.com/api/instamart/search?pageNumber={page}&searchResultsOffset=0&limit=40&query={encoded_keyword}&ageConsent=false&layoutId=3990&pageType=INSTAMART_AUTO_SUGGEST_PAGE&isPreSearchTag=false&highConfidencePageNo=0&lowConfidencePageNo=0&voiceSearchTrackingId=&storeId={storeid}',
                    callback=self.parse,
                    dont_filter=True,
                    meta={"page_loc": page_loc,
                          "pincode": pincode,
                          "city": city,
                          "rank": rank,
                          "sponsored": sponsored,
                          "product_id": product_id,
                          "storeid": storeid,
                          "platform": platform,
                          "Keyword": Keyword,
                          "prod_url": prod_url,
                          "id":id
                          # "proxyy": True
                    }
                )
            else:
                if not os.path.isfile(page_loc):
                    cookies = {
                        '__SW': 'W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh',
                        '_device_id': '75be40f9-a0c3-4e0e-1c86-d1f2ced0c907',
                        '_gcl_au': '1.1.406511299.1718791436',
                        '_fbp': 'fb.1.1719233702143.931722654449798998',
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
                        'ally-on': 'false',
                        'strId': '',
                        'LocSrc': 's%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y',
                        'dadl': 'true',
                        'accessibility-enabled': 'false',
                        'tid': 's%3Ac5c94a77-b0c9-4bfd-b5c5-b144727b79fc.%2Fk%2FtKgMA%2BOrHIospa7o0G9GT45vKy16pMOjzOjBS6MA',
                        '_guest_tid': 'a5c1ff9b-5847-45ff-8329-2cfc0da3ed51',
                        '_sid': 'fpn93f59-0168-4076-8823-067f124ee03a',
                        'fontsLoaded': '1',
                        '_ga': 'GA1.1.11593828.1718791436',
                        'sid': 's%3Afpn93f59-0168-4076-8823-067f124ee03a.wtSESWg%2FlHBsVZ5do1kNik0Tj%2FA7dr0soGpRg6%2FKezA',
                        # 'lat': 's%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k',
                        # 'lng': 's%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk',
                        # 'address': 's%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs',
                        'userLocation': json.dumps(location),
                        '_ga_34JYJ0BCRN': 'GS1.1.1724479930.50.1.1724480134.0.0.0',
                        'imOrderAttribution': '{%22entryId%22:%22cake%22%2C%22entryName%22:%22instamartOpenSearch%22}',
                        '_ga_8N8XRG907L': 'GS1.1.1724479910.44.1.1724482869.0.0.0',
                    }

                    headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'en-US,en;q=0.9',
                        'cache-control': 'no-cache',
                        # 'cookie': '__SW=W9UCPh5ySrkx3z7LdbLfhfjPan0sU3nh; _device_id=75be40f9-a0c3-4e0e-1c86-d1f2ced0c907; _gcl_au=1.1.406511299.1718791436; _fbp=fb.1.1719233702143.931722654449798998; deviceId=s%3A75be40f9-a0c3-4e0e-1c86-d1f2ced0c907.Avin0k%2Fw1dkeC6Q2CDOF4DL6LvQ0cdWbPdzv0llDeCs; versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; isNative=false; openIMHP=false; addressId=s%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s; webBottomBarHeight=0; _ga_4BQKMMC7Y9=GS1.2.1723546342.9.1.1723546348.54.0.0; _gid=GA1.2.1530605234.1724130474; ally-on=false; strId=; LocSrc=s%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y; dadl=true; accessibility-enabled=false; tid=s%3Ac5c94a77-b0c9-4bfd-b5c5-b144727b79fc.%2Fk%2FtKgMA%2BOrHIospa7o0G9GT45vKy16pMOjzOjBS6MA; _guest_tid=a5c1ff9b-5847-45ff-8329-2cfc0da3ed51; _sid=fpn93f59-0168-4076-8823-067f124ee03a; fontsLoaded=1; _ga=GA1.1.11593828.1718791436; sid=s%3Afpn93f59-0168-4076-8823-067f124ee03a.wtSESWg%2FlHBsVZ5do1kNik0Tj%2FA7dr0soGpRg6%2FKezA; lat=s%3A28.5279118.PC7rKzpTQylqQw9CyVn8yO%2Bh9Xv3OOtlSkut%2FNSda2k; lng=s%3A77.20889869999999.1oT4Qa6G%2FxvpwUjLx%2FIV7YXW9Fh3qkLSCgfcqRBe%2FDk; address=s%3ANew%20Delhi%2C%20Delhi%20110017%2C%20India.oqwgnSjwL7vNf%2FPd6%2FBtqKF771PsolXMjg3HyUCzwCs; userLocation=%7B%22address%22%3A%22New%20Delhi%2C%20Delhi%20110017%2C%20India%22%2C%22lat%22%3A28.5279118%2C%22lng%22%3A77.20889869999999%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D; _ga_34JYJ0BCRN=GS1.1.1724479930.50.1.1724480134.0.0.0; imOrderAttribution={%22entryId%22:%22cake%22%2C%22entryName%22:%22instamartOpenSearch%22}; _ga_8N8XRG907L=GS1.1.1724479910.44.1.1724482869.0.0.0',
                        'pragma': 'no-cache',
                        'priority': 'u=0, i',
                        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'none',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    }

                    time.sleep(2)
                    yield scrapy.Request(url=f'https://www.swiggy.com/instamart/item/{product_id}?storeId={storeid}', cookies=cookies,
                                        headers=headers,callback=self.parse,meta={"page_loc": page_loc,
                          "pincode": pincode,
                          "city": city,
                          "rank": rank,
                          "sponsored": sponsored,
                          "product_id": product_id,
                          "storeid": storeid,
                          "platform": platform,
                          "Keyword": Keyword,
                          "prod_url": prod_url,
                          "id":id,
                          # "proxyy":True
                                                                                  })
                else:


                    if os.path.isfile(page_loc):

                        yield scrapy.Request(url="file://" + page_loc, callback=self.parse, dont_filter=True,
                                             # cookies=random.choice([cookies_1, cookies_2, cookies_3]),
                                             meta={"page_loc":page_loc,
                                                                                  "pincode":pincode,
                                                                                  "city":city,
                                                                                  "rank":rank,
                                                                                  "sponsored":sponsored,
                                                                                  "product_id":product_id,
                                                                                  "storeid":storeid,
                                                   "id": id,
                                                   "prod_url": prod_url,
                                                                     "platform": platform,
                                                                     "Keyword": Keyword,
                                                   # "proxyy": False
                                                                     })
                    else:
                    # print(page_loc,3)
                    # continue
                        yield scrapy.Request(url="file://" + page_loc.replace(f"{str(pincode)}/", f"{str(pincode)}/not_found_"),
                                             callback=self.parse, dont_filter=True,
                                             meta={"page_loc": page_loc,
                                                   "pincode": pincode,
                                                   "city": city,
                                                   "rank": rank,
                                                   "sponsored": sponsored,
                                                   "product_id": product_id,
                                                   "storeid": storeid,
                                                   "platform": platform,
                                                   "prod_url": prod_url,
                                                   "Keyword": Keyword,
                                                   "id": id,
                                                   # "proxyy": False
                                                   })




    def parse(self, response):
        # today_date = str(date.today())
        if response.xpath('//script[@type= "application/ld+json"]/text()').get() is not None:

            if not os.path.isfile(response.request.meta['page_loc']) and response.status == 200:
                with open(response.request.meta['page_loc'], 'wb') as file:
                    file.write(response.body)

            items=SwiggyInstamartBakeryfoodItem1()
            other_data = json.loads(
                response.xpath('//script[contains(text(), "window.___INITIAL_STATE__")]/text()').get().split(
                    ';  var App')[0].replace('  window.___INITIAL_STATE___ = ', ''))
            for each_variation in other_data['instamart']['cachedProductItemData']['lastItemState']['variations']:
                items['platform'] = response.meta['platform']
                items['pincode'] = response.meta['pincode']
                items['keyword'] = response.meta['Keyword']
                date = datetime.now()
                formatted_date = date.strftime("%d-%b-%y")
                items['dateOfScrap'] = formatted_date
                # items['scrapedTime'] = '08:00 PM'
                items['scrapedTime'] = '10:00 AM'
                # items['scrapedTime'] = '03:00 PM'
                items['productName'] = each_variation['display_name']
                items['productId'] = response.meta['product_id']
                items['rank'] = response.meta['rank']
                brand = other_data['instamart']['cachedProductItemData']['lastItemState']['brand']
                items['brand']=brand
                items['price'] = each_variation['price']['offer_price']
                items['mrp'] = each_variation['price']['mrp']
                if brand == "The Baker's Dozen":

                    items['isBrandProduct'] = 'True'
                else:
                    items['isBrandProduct'] = 'False'

                items['discount'] = each_variation['price']['offer_applied']['listing_description']
                items['unit'] = each_variation['quantity']
                items['quantity'] = each_variation['max_allowed_quantity']
                stock = each_variation['inventory']['in_stock']
                if stock == True:
                    items['stock'] = "True"
                else:
                    items['stock'] = "False"
                items['sponsored'] = response.meta['sponsored']
                items['rating'] = ''
                items['review_count'] = ''
                items['id'] = response.meta['id']
                items['city']=response.meta['city']
                items['storeid']=response.meta['storeid']
                items['url'] = response.meta['prod_url']
                yield items
                break

        else:
            page_loc = response.request.meta['page_loc']
            page_loc = page_loc.replace(f"{str(response.request.meta['pincode'])}/",f"{str(response.request.meta['pincode'])}/not_found_")
            if not os.path.isfile(page_loc) and response.status == 200:
                with open(page_loc, 'wb') as file:
                    file.write(response.body)
            items = SwiggyInstamartBakeryfoodItem1()
            items['platform'] = response.meta['platform']
            items['pincode'] = response.meta['pincode']
            items['keyword'] = response.meta['Keyword']
            date = datetime.now()
            formatted_date = date.strftime("%d-%b-%y")
            items['dateOfScrap'] = formatted_date
            # items['scrapedTime'] = '08:00 PM'
            items['scrapedTime'] = '10:00 AM'
            # items['scrapedTime'] = '03:00 PM'
            items['productName'] = ''
            items['productId'] = response.meta['product_id']
            items['rank'] = response.meta['rank']
            items['brand'] = ''
            items['price'] = ''
            items['mrp'] = ''
            items['isBrandProduct'] = ''

            items['discount'] = ''
            items['unit'] = ''
            items['quantity'] =''
            items['stock'] =''
            items['sponsored'] = response.meta['sponsored']
            items['rating'] = ''
            items['review_count'] = ''
            items['id'] = response.meta['id']
            items['city'] = response.meta['city']
            items['storeid'] = response.meta['storeid']
            items['url'] = response.meta['prod_url']
            yield items

# -a start=0 -a end=3000

if __name__ == '__main__':
    execute('scrapy crawl spider1 -a start=0 -a end=10000'.split())