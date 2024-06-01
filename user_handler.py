import os
import json


class UserHandler:
    def __init__(self):
        if not os.path.exists('resources/users/users.json'):
            users = []
            with open('resources/users/users.json', 'w') as file:
                json.dump(users, file)

        with open('resources/users/users.json', 'r') as file:
            self.users = json.load(file)

    def exists(self, username: str):
        for user in self.users:
            if username == user['username']:
                return True

        return False

    @staticmethod
    def __is_valid_input(username: str, index: int):
        if len(username) <= 4:
            raise ValueError(f'Username is too short. Minimum 4 characters allowed')
        if index < 0:
            raise ValueError(f'Index can\'t be negative')

    def add_user(self, username: str):
        self.__is_valid_input(username, 0)

        for user in self.users:
            if username in user['username']:
                print(f'User {username} already exist')
                return

        user_data = {'username': username,
                     'to_watch': [],
                     'watched': []}
        self.users.append(user_data)
        with open('resources/users/users.json', 'w') as file:
            json.dump(self.users, file)
        print(f'User {username} added to users')

    def remove_user(self, username: str):
        self.__is_valid_input(username, 0)

        for user in self.users:
            if user['username'] == username:
                self.users.remove(user)
                with open('resources/users/users.json', 'w') as file:
                    json.dump(self.users, file)
                print(f'User {username} removed from users')
                return

        print(f'User {username} does not exist')

    def add_to_watch(self, username: str, index: int):
        self.__is_valid_input(username, index)

        for user in self.users:
            if user['username'] == username:
                if index not in user['to_watch']:
                    user['to_watch'].append(index)
                    with open('resources/users/users.json', 'w') as file:
                        json.dump(self.users, file)
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
                    with open('resources/users/users.json', 'w') as file:
                        json.dump(self.users, file)
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
                    with open('resources/users/users.json', 'w') as file:
                        json.dump(self.users, file)
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
                    with open('resources/users/users.json', 'w') as file:
                        json.dump(self.users, file)
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
