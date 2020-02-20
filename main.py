import csv
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import time
import os


@dataclass
class MenuGame:
    _error: int = 3
    _path_file: str = './template/Questions.csv'

    def mainMenu(self):
        print('\t Правда или Ложь')
        print('1 - Начать игру!\n2 - Об игре\n3 - Настройки\n0 - Выход\n')

        selected_number_choice = int(input('Введите ваш выбор: '))

        if selected_number_choice == 1:
            self.startGame()
        elif selected_number_choice == 2:
            self.aboutGame()
        elif selected_number_choice == 3:
            self.cls()
            self.setting()
        elif selected_number_choice == 0:
            self.cls()
            self.exitGame()
        else:
            print('\nТакой цифры нету!\nВозвращение в главное меню')
            time.sleep(2)
            self.cls()
            self.mainMenu()

    def startGame(self):
        game = StartGame(self._error, self._path_file)
        game.startGame()

    def setting(self):
        setting_start = Setting(self._error, self._path_file)
        setting_start.openSetting()

    def aboutGame(self):
        self.cls()
        with open('./template/About.txt', 'r') as f:
            for text in f:
                print(text)

        print('\n\n9 - Главное меню\n0 - Выход\n')
        selected_number_choice = int(input('Введите ваш выбор: '))
        if selected_number_choice == 9:
            self.cls()
            self.mainMenu()
        elif selected_number_choice == 0:
            self.cls()
            os.system(exit())
        else:
            print('\nТакой цифры нету!\nПопробуйте ещё раз!')
            time.sleep(2)
            self.cls()
            self.aboutGame()

    def exitGame(self):
        self.cls()
        os.system(exit())

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')


@dataclass
class StartGame:
    _error: int = 3
    _path_file: str = './template/Questions.csv'
    _question: str = ''
    _answer: str = ''
    _explanation: str = ''
    _answered: int = 0
    _errors_allowed: int = 0
    _row_full_text: Dict[int, List[str]] = field(default_factory=dict)
    _row_question: Dict[int, Tuple[str, Tuple[str, str]]] = field(default_factory=dict)

    def startGame(self):
        menu = MenuGame()
        self.openCSV()
        question_search = 'Подбираем вопрос'
        print(question_search)
        for row_index in range(1, len(self._row_full_text)):
            question = self._row_full_text.get(row_index)
            answer = self._row_full_text.get(row_index)
            explanation = self._row_full_text.get(row_index)
            question = question.split(';')[0]
            answer = answer.split(';')[1]
            explanation = explanation.split(';')[2]
            self._row_question[row_index] = (question, (answer, explanation))
            question_search = question_search.replace('ос', 'ос.').replace('ос....', 'ос.')
            menu.cls()
            print(question_search)
            time.sleep(1)
        self.startGuessing(0)

    def startGuessing(self, flag):
        flag = flag
        menu = MenuGame()
        menu.cls()
        if self._error > 0:
            print(f'Ошибок: {self._error}')
            print(self._row_question)

            if self._row_question:
                try:
                    if flag == 0:
                        for index in list(self._row_question):
                            question_tuple = self._row_question.pop(index)
                            print(question_tuple)
                            self._question = question_tuple[0]
                            self._answer = question_tuple[1][0]
                            self._explanation = question_tuple[1][1]
                            break
                    print(self._question)
                except UnboundLocalError:
                    menu.cls()
                    print(f'Вы ответили на {self._answered} вопрос(а/ов)!\nОшибок допущено:{self._errors_allowed}')
                    print('\n9 - Главное меню\n0 - Выход\n')

                    selected_number_choice = int(input('Введите ваш выбор: '))
                    if selected_number_choice == 9:
                        menu = MenuGame(self._error, self._path_file)
                        menu.cls()
                        menu.mainMenu()
                    elif selected_number_choice == 0:
                        menu.cls()
                        os.system(exit())
                    else:
                        menu.cls()
                        menu.mainMenu()

                input_you_value = input('Введите значение(Yes or No, Y or N, Да или Нет): ')
                if input_you_value == 'Yes' or input_you_value == 'Y' or input_you_value == 'Да':
                    yes = 'Yes'
                    if yes == self._answer:
                        print('Правильно!')
                        self._answered += 1
                        time.sleep(2)
                        self.startGuessing(0)
                    else:
                        self._error -= 1
                        self._errors_allowed += 1
                        print(self._explanation)
                        time.sleep(len(self._explanation) // 10)
                        self.startGuessing(0)
                elif input_you_value == 'No' or input_you_value == 'N' or input_you_value == 'Нет':
                    no = 'No'
                    if no == self._answer:
                        print('Правильно!')
                        self._answered += 1
                        time.sleep(3)
                        self.startGuessing(0)
                    else:
                        self._error -= 1
                        self._errors_allowed += 1
                        print(self._explanation)
                        time.sleep(len(self._explanation) // 10)
                        self.startGuessing(0)
                else:
                    print('Wrong!')
                    time.sleep(3)
                    self.startGuessing(1)
            else:
                menu.cls()
                print(f'Вы ответили на {self._answered} вопрос(а/ов)!\nОшибок допущено:{self._errors_allowed}')
                print('\n9 - Главное меню\n0 - Выход\n')

                selected_number_choice = int(input('Введите ваш выбор: '))
                if selected_number_choice == 9:
                    menu = MenuGame()
                    menu.cls()
                    menu.mainMenu()
                elif selected_number_choice == 0:
                    menu.cls()
                    os.system(exit())
                else:
                    menu.cls()
                    menu.mainMenu()
        else:
            print(f'Вы допустили максимальное количество ошибок!')
            print('\n9 - Главное меню\n0 - Выход\n')

            selected_number_choice = int(input('Введите ваш выбор: '))
            if selected_number_choice == 9:
                menu = MenuGame()
                menu.cls()
                menu.mainMenu()
            elif selected_number_choice == 0:
                menu.cls()
                os.system(exit())
            else:
                menu.cls()
                menu.mainMenu()

    def openCSV(self):
        with open(self._path_file, 'r') as f:
            index = 1
            reader = csv.reader(f)
            for row in reader:
                full_data = ' '.join(row)
                self._row_full_text[index] = full_data
                index += 1


@dataclass
class Setting:
    _error: int = 3
    _path_file: str = './template/Questions.csv'

    def openSetting(self):
        menu = MenuGame()
        print(f'Ошибок: {self._error}\nПуть к файлу с вопросами: "{self._path_file}"\n')
        print('1 - Изменить кол-во ошибок\n2 - Изменить путь к вопросам\n3 - Сбросить настройки\n9 - Главное меню\n0 '
              '- Выход\n')
        selected_number_choice = int(input('Введите ваш выбор: '))
        if selected_number_choice == 1:
            menu.cls()
            input_error_number = int(input('Введите количество ошибок которое вы желаете для себя: '))
            if 0 <= input_error_number <= 100:
                self._error = input_error_number
                menu.cls()
                self.openSetting()
        elif selected_number_choice == 2:
            print('Посетите раздел "Об игре", чтобы узнать, какой файл с вопросами подходит для игры')
            input_path_file = input('Введите путь к файлу с вопросами: ').replace('\\', '/')
            menu.cls()
            self._path_file = input_path_file
            menu.cls()
            self.openSetting()
        elif selected_number_choice == 3:
            self._error = 3
            self._path_file = './template/Questions.csv'
        elif selected_number_choice == 9:
            menu = MenuGame(self._error, self._path_file)
            menu.cls()
            menu.mainMenu()
        elif selected_number_choice == 0:
            menu.cls()
            os.system(exit())
        else:
            print('\nТакой цифры нету!\nПопробуйте ещё раз!')
            time.sleep(2)
            menu.cls()
            self.openSetting()


if __name__ == '__main__':
    start = MenuGame()
    start.mainMenu()
