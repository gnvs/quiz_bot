# questions.py
# Список вопросов квиза
QUIZ_DATA = [
    {
        'question': 'Что означает аббревиатура "Python"?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Название змеи'],
        'correct_option': 0,
        'explanation': 'Python - это язык программирования, названный в честь комедийного шоу "Летающий цирк Монти Пайтона"'
    },
    {
        'question': 'Какой оператор используется для возведения в степень в Python?',
        'options': ['^', '**', 'pow()', '^^'],
        'correct_option': 1,
        'explanation': 'Оператор ** используется для возведения в степень, например: 2**3 = 8'
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'bool'],
        'correct_option': 0,
        'explanation': 'int (integer) используется для хранения целых чисел, например: 42, -10, 0'
    },
    {
        'question': 'Что выведет print(type(10.5))?',
        'options': ['<class "int">', '<class "float">', '<class "str">', '<class "decimal">'],
        'correct_option': 1,
        'explanation': '10.5 - это число с плавающей точкой, поэтому тип будет float'
    },
    {
        'question': 'Как создать список в Python?',
        'options': ['{}', '()', '[]', '<>'],
        'correct_option': 2,
        'explanation': 'Список создается с помощью квадратных скобок: my_list = [1, 2, 3]'
    },
    {
        'question': 'Какая функция используется для вывода информации на экран?',
        'options': ['input()', 'print()', 'output()', 'display()'],
        'correct_option': 1,
        'explanation': 'print() - это встроенная функция для вывода текста в консоль'
    },
    {
        'question': 'Что такое PEP 8?',
        'options': [
            'Стиль кодирования в Python',
            'Версия Python',
            'Библиотека для графики',
            'Фреймворк для веба'
        ],
        'correct_option': 0,
        'explanation': 'PEP 8 - это руководство по написанию читаемого и понятного кода на Python'
    },
    {
        'question': 'Какой символ используется для комментариев в Python?',
        'options': ['//', '/*', '#', '<!--'],
        'correct_option': 2,
        'explanation': 'Знак # используется для однострочных комментариев в Python'
    },
    {
        'question': 'Что делает функция len()?',
        'options': [
            'Возвращает длину объекта',
            'Создает новый список',
            'Преобразует в строку',
            'Округляет число'
        ],
        'correct_option': 0,
        'explanation': 'len() возвращает количество элементов в объекте (списке, строке и т.д.)'
    },
    {
        'question': 'Какой цикл используется для перебора элементов?',
        'options': ['for', 'while', 'do-while', 'foreach'],
        'correct_option': 0,
        'explanation': 'Цикл for в Python используется для итерации по последовательностям'
    }
]

def get_question_count():
    """Возвращает количество вопросов"""
    return len(QUIZ_DATA)

def get_question(index):
    """Возвращает вопрос по индексу"""
    if 0 <= index < len(QUIZ_DATA):
        return QUIZ_DATA[index]
    return None