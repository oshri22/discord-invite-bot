import sqlite3 as sql


class sql_mang:

    def __enter__(self):
        '''ro use the with comand kinda _init__'''
        self.conn = sql.connect("infoo.db")
        self.controler = self.conn.cursor()

        self.controler.execute(
            "CREATE TABLE IF NOT EXISTS USERS(id, name, inviteamount)")
        self.controler.execute(
            "CREATE TABLE IF NOT EXISTS USED(id, name, bywho)")
        self.controler.execute(
            "CREATE TABLE IF NOT EXISTS ALLUSERS(id, name)")

        self.conn.commit()

        return self

    def __exit__(self, *kargs):
        '''oart of the with'''
        self.conn.commit()
        self.conn.close()

    def add_user(self, user_name: str, user_id: int) -> None:
        '''add user to the counting table'''
        self.controler.execute(
            "INSERT INTO USERS VALUES(?,?,?)", (user_id, user_name, 0))
        print(f"add user {user_name}")
        self.conn.commit()

    def get_invite_ammount(self, user_id: int) -> int:
        '''geting how many invited the user have'''
        return list(self.controler.execute("SELECT inviteamount FROM USERS WHERE id = ?", (user_id,)))[0][0]

    def delete_user(self, user_id: int) -> None:
        '''deleting a user from the table when removed'''
        self.controler.execute("DELETE FROM USERS WHERE id = ?", (user_id,))
        self.conn.commit()
        print("deleted the user ")

    def update_invite_amount(self, user_id: int) -> None:
        '''updating the amount of invited a user have'''
        try:
            curr_amount = self.get_invite_ammount(user_id)
        except IndexError:
            print("no invitation")
        else:
            self.controler.execute(
                "UPDATE USERS SET inviteamount = ? WHERE id = ? ", (curr_amount + 1, user_id))
            self.conn.commit()
            print("updated the invite amount ")

    def print_table(self) -> None:
        '''print the table so it will be easy to track'''
        ans = self.controler.execute("SELECT * FROM USERS")
        for i in ans:
            print(f"user name - {i[1]} id - {i[0]} amount - {i[2]}")

    def add_to_already_used(self, name: str, id:int, by_who: str):
        '''add the user to the already used table'''
        self.controler.execute(
            "INSERT INTO USED VALUES(?,?,?)", (id, name, by_who))
        self.conn.commit()

    def delete_user_from_exist(self, user_id: int):
        '''remove the user in case he left\removed'''
        self.controler.execute("DELETE FROM USED WHERE id = ?", (user_id,))
        self.conn.commit()
        print("deleted the user ")

    def if_used(self, user_id: int):
        '''check if a user already used his invite'''
        some = list(self.controler.execute(
            "SELECT * FROM USED WHERE id = ?", (user_id, )))
        if some:
            return False
        return True

    def if_exist_at_all(self, id: int):
        '''cjeck if the user is in the server'''
        some = list(self.controler.execute(
            "SELECT * FROM ALLUSERS WHERE id = ?", (id, )))
        if some:
            return False
        return True

    def delete_user_from_server(self, user_id: int):
        '''in case the user is removed'''
        self.controler.execute("DELETE FROM ALLUSERS WHERE id = ?", (user_id,))
        self.conn.commit()
        print("deleted the user ")

    def add_to_all_users(self, id: int, name: str):
        '''add the user to '''
        if self.if_exist_at_all(id):
            self.controler.execute(
                "INSERT INTO ALLUSERS VALUES(?,?)", (id, name))
            self.conn.commit()

    def find_user_id(self, name: str) -> str:
        '''find the user id from the name'''
        try:
            return list(self.controler.execute("SELECT id FROM ALLUSERS WHERE name = ?", (name, )))[0][0]
        except IndexError:
            return list(self.controler.execute("SELECT id FROM ALLUSERS WHERE name = ?", (name, ))) 

    def find_user_name(self, id: int):
        '''find the user name from user name'''
        user_name = list(self.controler.execute(
            "SELECT name FROM ALLUSERS WHERE id = ?", (id, )))[0][0]
        return user_name

    def print_all_users(self):
        '''print the server user so it will be easy to track'''
        ans = self.controler.execute("SELECT * FROM ALLUSERS")
        for i in ans:
            print(f"user name - {i[1]} id - {i[0]}")

    def drop_tabels(self):
        '''if you like to delete all the tables'''
        self.controler.execute("DROP TABLE USERS")
        self.controler.execute("DROP TABLE ALLUSERS")
        self.controler.execute("DROP TABLE USED")
        self.conn.commit()
    
    def find_users(self):
        data = list(self.controler.execute("SELECT * FROM USERS"))
        print(data)
        return data[:3:]


def main():
    with sql_mang() as foo:
        print(foo.find_user_id("oshri22"))

if __name__ == "__main__":
    main()
