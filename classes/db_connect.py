import sqlite3
import datetime 


class db_connect(object):
    def __init__(self):
        self.base_connection = sqlite3.connect('database.db')
        self.cursor = self.base_connection.cursor()
        self.create_table()


    def create_table(self):
        # Создаём базу таблицу с объявлениями
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads
        (
            id integer primary key,
            ad_id bigint,
            town text DEFAULT "moskva",
            time_parse timestamp without time zone
        )
        ''')

        # Создаём базу таблицу с юзерами
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (
            id integer primary key,
            tg_id bigint,
            username text,
            is_admin boolean DEFAULT false,
            sub_start timestamp without time zone,
            sub_end timestamp without time zone,
            pay_money integer DEFAULT 0,
            town_search text DEFAULT 'moskva',
            referral_vote boolean DEFAULT true,
            cnt_referral_votes integer DEFAULT 0
        )           
        ''')

        # Сохраняем изменения
        self.base_connection.commit()
    

    # users
    def get_users(self, tg_id=None, username=None, town=None, sub_active=False):
        request = f'''SELECT * FROM users WHERE id '''
        if tg_id:
            request += f'''AND tg_id = {tg_id} '''
        if username:
            request += f'''AND username = '{username}' '''
        if town:
            request += f'''AND town_search = '{town}' '''
        if sub_active:
            request += f'''AND sub_end >= datetime('now') '''
        self.cursor.execute(request)
        return self.cursor.fetchall()

    
    def get_user_by_tg_id(self, tg_id):
        self.cursor.execute(f'SELECT * FROM users WHERE tg_id = {tg_id}')
        return self.cursor.fetchone()
    
    
    def get_user_by_username(self, username):
        self.cursor.execute(f'''SELECT * FROM users WHERE username = '{username}' ''')
        return self.cursor.fetchone()
    
    
    def add_user(self, tg_id, username):
        self.cursor.execute(f'''
            INSERT INTO users (tg_id, username, sub_start, sub_end)
            SELECT {tg_id}, '{username}', datetime('now'), datetime('now','+5 hour')
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE tg_id={tg_id});
        ''')
        self.base_connection.commit()
        return self.get_user_by_tg_id(tg_id=tg_id)
    
    
    def is_user_in_database(self, tg_id):
        return True if self.get_user_by_tg_id(tg_id) else False
    
    
    def user_renew_subscription(self, tg_id, amount):
        self.cursor.execute(f'''
            UPDATE users
            SET sub_start = datetime('now'),
                sub_end = datetime('now','+1 month'),
                pay_money = pay_money + {amount}
            WHERE tg_id = {tg_id};
        ''')
        self.base_connection.commit()
        return self.get_user_by_tg_id(tg_id=tg_id)
    
    
    def user_change_city(self, tg_id, town):
        self.cursor.execute(f'''
            UPDATE users
            SET town_search = '{town}'
            WHERE tg_id = {tg_id};
        ''')
        self.base_connection.commit()
        return self.get_user_by_tg_id(tg_id=tg_id)
    

    def user_set_admin(self, tg_id, is_admin=1):
        self.cursor.execute(f'''
            UPDATE users
            SET is_admin = {is_admin}
            WHERE tg_id = {tg_id};
        ''')
        self.base_connection.commit()
        return self.get_user_by_tg_id(tg_id=tg_id)    
    
        
    # ads
    def get_ad_by_id(self, ad_id):
        self.cursor.execute(f'SELECT * FROM ads WHERE ad_id = {ad_id}')
        return self.cursor.fetchone()
    
    def is_ad_in_database(self, ad_id):
        return True if self.get_ad_by_id(ad_id) else False
    
    def add_ad(self, ad_id, town):
        self.cursor.execute(f'''
            INSERT INTO ads (ad_id, town, time_parse)
            SELECT {ad_id}, '{town}', datetime('now')
            WHERE NOT EXISTS (SELECT 1 FROM ads WHERE ad_id={ad_id});
        ''')
        self.base_connection.commit()
        
        
    # database
    def delete_ads_with_time_more_12hours(self):
        self.cursor.execute(f'''
            DELETE FROM ads
            WHERE time_parse <= datetime('now','-12 hour')
        ''')
        self.base_connection.commit()
