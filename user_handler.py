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
    def __is_valid_input(username: str, index: int, password=None):
        if len(username) < 4:
            raise ValueError(f'Username is too short. Minimum 4 characters allowed')
        if len(username) > 32:
            raise ValueError(f'Username is too long. Maximum 32 characters allowed')
        if index < 0:
            raise ValueError(f'Index can\'t be negative')
        if password and len(password) < 4:
            raise ValueError(f'Password is too short. Minimum 4 characters allowed')
        if password and len(password) > 32:
            raise ValueError(f'Password is too long. Maximum 32 characters allowed')

    def is_correct_password(self, username: str, password: str):
        self.__is_valid_input(username, 0, password)

        if not self.exists(username):
            raise ValueError(f'User {username} does not exist')

        for user in self.users:
            if username == user['username']:
                return password == user['password']

    def add_user(self, username: str, password: str):
        self.__is_valid_input(username, 0, password)

        if self.exists(username):
            raise ValueError(f'User {username} already exist')

        user_data = {'username': username,
                     'password': password,
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

        raise ValueError(f'User {username} does not exist')

    def add_to_watch(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index not in user['to_watch'] and index not in user['watched']:
                    user['to_watch'].append(index)
                    self.save_users()
                elif index in user['to_watch']:
                    raise ValueError(f'Film already added to \'To Watch\'')
                else:
                    raise ValueError(f'Film already added to \'Watched\'')
                return

        raise ValueError(f'User {username} does not exist')

    def remove_to_watch(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index in user['to_watch']:
                    user['to_watch'].remove(index)
                    self.save_users()
                else:
                    raise ValueError(f'Film index {index} not added to list')
                return

        raise ValueError(f'User {username} does not exist')

    def add_watched(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index not in user['watched'] and index not in user['to_watch']:
                    user['watched'].append(index)
                    self.save_users()
                elif index in user['watched']:
                    raise ValueError(f'Film already added to \'Watched\'')
                else:
                    raise ValueError(f'Film already added to \'To Watch\'')
                return

        raise ValueError(f'User {username} does not exist')

    def remove_watched(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index in user['watched']:
                    user['watched'].remove(index)
                    self.save_users()
                else:
                    raise ValueError(f'Film index {index} not added to list')
                return

        raise ValueError(f'User {username} does not exist')

    def move_to_watched(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index in user['to_watch'] and index not in user['watched']:
                    user['to_watch'].remove(index)
                    user['watched'].append(index)
                    self.save_users()
                elif index not in user['to_watch']:
                    raise ValueError(f'Film index {index} not added to list')
                elif index in user['watched']:
                    raise ValueError(f'Film index {index} already added to \"Watched\"')
                return

        raise ValueError(f'User {username} does not exist')

    def move_to_towatch(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index in user['watched'] and index not in user['to_watch']:
                    user['watched'].remove(index)
                    user['to_watch'].append(index)
                    self.save_users()
                elif index not in user['to_watch']:
                    raise ValueError(f'Film index {index} not added to list')
                elif index in user['watched']:
                    raise ValueError(f'Film index {index} already added to \"Watched\"')
                return

        raise ValueError(f'User {username} does not exist')
