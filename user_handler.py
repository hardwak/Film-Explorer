import os
import json


class UserHandler:
    def __init__(self):
        self.filepath = 'resources/users/users.json'
        if not os.path.exists(self.filepath):
            self.users = []
            self.save_users()

        self.users = self.load_users()

    def load_users(self):
        with open(self.filepath, 'r') as file:
            return json.load(file)

    def save_users(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.users, file, indent=4)

    def exists(self, username: str):
        for user in self.users:
            if username == user['username']:
                return True

        return False

    def get_user_lists(self, username: str):
        if not self.exists(username):
            raise ValueError(f'User {username} does not exist')

        for user in self.users:
            if username == user['username']:
                return user['to_watch'], user['watched']

    @staticmethod
    def __is_valid_input(username: str, index: int):
        if len(username) <= 4:
            raise ValueError(f'Username is too short. Minimum 4 characters allowed')
        if index < 0:
            raise ValueError(f'Index can\'t be negative')

    def add_user(self, username: str):
        self.__is_valid_input(username, 0)

        if self.exists(username):
            raise ValueError(f'User {username} already exist')

        user_data = {'username': username,
                     'to_watch': [],
                     'watched': []}
        self.users.append(user_data)
        self.save_users()
        print(f'User {username} added to users')

    def remove_user(self, username: str):
        self.__is_valid_input(username, 0)

        for user in self.users:
            if user['username'] == username:
                self.users.remove(user)
                self.save_users()
                print(f'User {username} removed from users')
                return

        print(f'User {username} does not exist')

    def add_to_watch(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index not in user['to_watch']:
                    user['to_watch'].append(index)
                    self.save_users()
                else:
                    print(f'Film index {index} already added')
                return

        print(f'User {username} does not exist')

    def remove_to_watch(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index in user['to_watch']:
                    user['to_watch'].remove(index)
                    self.save_users()
                else:
                    print(f'Film index {index} not added')
                return

        print(f'User {username} does not exist')

    def add_watched(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index not in user['watched']:
                    user['watched'].append(index)
                    self.save_users()
                else:
                    print(f'Film index {index} already added')
                return

        print(f'User {username} does not exist')

    def remove_watched(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index in user['watched']:
                    user['watched'].remove(index)
                    self.save_users()
                else:
                    print(f'Film index {index} not added')
                return

        print(f'User {username} does not exist')


if __name__ == '__main__':
    user_handler = UserHandler()
    user_handler.add_user('user1')
    user_handler.add_user('user2')
    user_handler.add_user('user3')

    user_handler.add_to_watch('user1', 123)
    user_handler.add_to_watch('user1', 222)
    user_handler.add_to_watch('user1', 333)
    user_handler.remove_to_watch('user1', 222)
    user_handler.remove_to_watch('user1', 1)
    # user_handler.remove_user('user3')
