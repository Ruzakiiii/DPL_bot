import sqlite3

class BotDB:

    def __init__(self, DPL):
        self.conn = sqlite3.connect(DPL)
        self.cursor = self.conn.cursor()

    def check_user(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `id` = ?", (user_id,))
        return bool(len(result.fetchall()))
    def check_phone(self, user_id):
        """Получаем номер телефона юзера"""

        result = self.cursor.execute("SELECT phone_number FROM `users` WHERE `id` = ?", (user_id,))

        return result.fetchall()

    # def get_user_id(self, user_id):
    #     """Достаем id юзера в базе по его user_id"""
    #     result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
    #     return result.fetchone()[0]

    def add_order(self,user_id, imya, company_imya, phone_nomer, description_text):
        """Добавляем заказ в базу"""
        self.cursor.execute("INSERT INTO `orders` (`id`, `name`, `company_name`, `phone_number`, `description`) VALUES (?, ?, ?, ?, ?)", (user_id, imya, company_imya, phone_nomer, description_text,))
        return self.conn.commit()

    def add_user(self, user_id, first_name, username, number):
        """Добавляем пользователя в базу"""
        self.cursor.execute("INSERT INTO `users` (`id`, `name`, `user_name`, 'phone_number') VALUES (?, ?, ?, ?)", (user_id, first_name, username, number,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        """Создаем запись о доходах/расходах"""
        self.cursor.execute("INSERT INTO `records` (`users_id`, `operation`, `value`) VALUES (?, ?, ?)",
            (self.get_user_id(user_id),
            operation == "+",
            value))
        return self.conn.commit()

    def get_records(self, user_id, within = "all"):
        """Получаем историю о доходах/расходах"""

        if(within == "day"):
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        elif(within == "week"):
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        elif(within == "month"):
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        else:
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? ORDER BY `date`",
                (self.get_user_id(user_id),))

        return result.fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


# import sqlite3
#
# try:
#     conn = sqlite3.connect('dpl.db')
#     cursor = conn.cursor()
#
#     cursor.execute("INSERT OR IGNORE INTO 'users' ('id') VALUES (?)", (1000,))
#
#     users = cursor.execute("SELECT * FROM 'users'")
#     print(users.fetchall())
#     conn.commit()
#
# except sqlite3.Error as error:
#     print("Error", error)
#
# finally:
#     if(conn):
#         conn.close()
# import sqlite3
#
# conn = sqlite3.connect('DPL.db')
# sql = conn.cursor()
# sql.execute('CREATE TABLE orders (id INTEGER, name TEXT, company_name TEXT, phone_number TEXT, description TEXT);')
# sql.execute('CREATE TABLE users (id INTEGER, name TEXT, company_name TEXT, phone_number TEXT, description TEXT);')
# conn.commit()
# conn.close()
#
