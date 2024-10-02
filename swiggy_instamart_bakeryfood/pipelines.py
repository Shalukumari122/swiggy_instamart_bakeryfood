# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date, datetime, timedelta

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from swiggy_instamart_bakeryfood.items import SwiggyInstamartBakeryfoodItem, SwiggyInstamartBakeryfoodItem1


class SwiggyInstamartBakeryfoodPipeline:

    def __init__(self):
        # Connect to MySQL database
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='actowiz',
            database='swiggy_instamart_bakeryfood'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

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
                next_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

            # Format the time as requested
            formatted_time = next_time.strftime("%Y_%m_%d_%I_%p")

            return formatted_time

        today_date_time = adjust_time()

        if isinstance(item, SwiggyInstamartBakeryfoodItem):
            try:
                table_name = f"product_data{today_date_time}"

                # Create table if it doesn't exist
                query = f"""
                    CREATE TABLE IF NOT EXISTS `{table_name}` (
                        `Sr.No` INT AUTO_INCREMENT PRIMARY KEY
                    )
                """
                self.cursor.execute(query)

                # Check existing columns
                self.cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
                existing_columns = [column[0] for column in self.cursor.fetchall()]

                # Prepare columns for insertion
                item_columns = [column_name.replace(" ", "_") if " " in column_name else column_name for column_name in
                                item.keys()]
                for column_name in item_columns:
                    column_name_lower = column_name.lower()
                    if column_name_lower not in existing_columns:
                        try:
                            self.cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name_lower}` LONGTEXT")
                            existing_columns.append(column_name_lower)
                        except Exception as e:
                            print(e)

                # Prepare insert statement
                field_list = []
                value_list = []
                for field in item:
                    field_list.append(f"`{field}`")  # Enclose field names in backticks
                    value_list.append('%s')

                fields = ', '.join(field_list)
                values = ", ".join(value_list)

                insert_query = f"INSERT INTO `{table_name}` ({fields}) VALUES ({values})"

                self.cursor.execute(insert_query, tuple(item.values()))
                self.conn.commit()

            except Exception as e:
                print(e)

        if isinstance(item, SwiggyInstamartBakeryfoodItem1):
            try:
                data_table = f"data_table{today_date_time}"
                link_table=f"product_data{today_date_time}"
                # table_name='product_data2024_08_25_03_pm'
                # Create table if it doesn't exist
                query = f"""
                    CREATE TABLE IF NOT EXISTS `{data_table}` (
                        `Sr.No` INT AUTO_INCREMENT PRIMARY KEY
                    )
                """
                self.cursor.execute(query)

                # Check existing columns
                self.cursor.execute(f"SHOW COLUMNS FROM `{data_table}`")
                existing_columns = [column[0] for column in self.cursor.fetchall()]

                # Prepare columns for insertion
                item_columns = [column_name.replace(" ", "_") if " " in column_name else column_name for column_name
                                in
                                item.keys()]
                for column_name in item_columns:
                    column_name_lower = column_name.lower()
                    if column_name_lower not in existing_columns:
                        try:
                            self.cursor.execute(
                                f"ALTER TABLE `{data_table}` ADD COLUMN `{column_name_lower}` LONGTEXT")
                            existing_columns.append(column_name_lower)
                        except Exception as e:
                            print(e)

                # Prepare insert statement
                field_list = []
                value_list = []
                for field in item:
                    field_list.append(f"`{field}`")  # Enclose field names in backticks
                    value_list.append('%s')

                fields = ', '.join(field_list)
                values = ", ".join(value_list)

                insert_query = f"INSERT INTO `{data_table}` ({fields}) VALUES ({values})"

                self.cursor.execute(insert_query, tuple(item.values()))
                self.conn.commit()
                # if item['storeid']==None:
                try:
                    # Update the row where the id matches
                    update_query = f"UPDATE {link_table} SET status='Done' WHERE `id`=%s"
                    self.cursor.execute(update_query, (item['id'],))
                    self.conn.commit()
                    print("Update successful using id")
                except Exception as e:
                    print(f"Error updating status using id: {e}")
            except Exception as e:
                print(e)
        return item

