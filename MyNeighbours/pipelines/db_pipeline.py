import psycopg2
import configparser


class DB_Pipeline(object):
    conn = None
    cursor = None

    def open_spider(self, spider):
        config = configparser.ConfigParser()
        config.read('/etc/opt/spider/config.ini')
        connect_str = config['database']['ConnectStr']
        self.conn = psycopg2.connect(connect_str)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into address (address, town, state, zipcode) values (%s, %s, %s, %s)',
                            (item['address'], item['town'], item['state'], item['zipcode']))
        self.conn.commit()
        return item
