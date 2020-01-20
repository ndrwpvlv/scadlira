# -*- coding: utf-8 -*-

import re

from .helpers import NODES_PATTERN, ELEMENTS_PATTERN, DOFS_PATTERN, REPEATER_PATTERN, INT_PATTERNT, RANGE_PATTERN, \
    HEADER


class ScadModel:
    def __init__(self, filname: str):
        self.filname = filname
        self.txt = self.readtxt()  # Читаем текст и заменяем повторители
        self.model = {
            'nodes': self.parse_nodes(self.extract_data(NODES_PATTERN)),
            'elements': self.parse_elems(self.extract_data(ELEMENTS_PATTERN)),
            'dofs': self.parse_dofs(self.extract_data(DOFS_PATTERN)),
        }

    def readtxt(self):
        with open(self.filname, 'r') as file:
            txt = file.read().replace('\n', ' ').replace('  ', ' ')
        return self.replace_range(self.replace_repeaters(txt))

    def extract_data(self, pattern):
        search = re.findall(pattern, self.txt)[0]
        return search.replace('/', '/\n')

    def parse_nodes(self, data):
        try:
            return [self.check_list_size(line, 3) for line in self.split_by_whitespaces(data)]
        except:
            return None

    def parse_elems(self, data):
        try:
            return [[int(item) for item in line] for line in self.split_by_whitespaces(data)]
        except:
            return None

    @staticmethod
    def parse_dofs(data):
        try:
            lines = [string.split(':') for string in data.split('/\n') if string]
            dofs = {int(nds): line[0].replace('  ', ' ') for line in lines for nds in line[1].split(' ') if nds}
            return dict(sorted(dofs.items()))
        except IndexError:
            return None

    def write_liratxt(self):
        filname = self.filname.split('.')[0]
        with open('%s-converted.txt' % filname[:20], 'w') as file:
            file.write(HEADER.replace('scadlira', filname))  # заголовок
            if self.model['nodes']:
                file.write('(1/\n')  # узлы
                for line in self.model['elements']:
                    file.write(' '.join(str(item) for item in line) + '/\n')
                file.write(')\n')
            if self.model['elements']:
                file.write('(4/\n')  # элементы
                for line in self.model['nodes']:
                    file.write(' '.join(str(item) for item in line) + '/\n')
                file.write(')\n')
            if self.model['dofs']:
                file.write('(5/\n')  # закрепления
                for key in self.model['dofs']:
                    file.write('%s %s/\n' % (str(key), self.model['dofs'][key]))
                file.write(')\n')

    @staticmethod
    def split_by_whitespaces(data):
        return [[float(item) for item in line.split(' ') if item] for line in
                data.replace('/', '').replace('  ', ' ').split('\n') if line]

    @staticmethod
    def check_list_size(data: list, size: int) -> list:
        """
        Проверка размера list. Если размер list меньше требуемого,
        то добавляется "хвост" из нулей
        """
        while len(data) < size:
            data.append(0)
        return data

    def replace_repeaters(self, string: str) -> str:
        """
        Метод находит повторители и заменяет их на указанный диапазон
        чисел через пробел.
        На вход подается текстовый файл, импортированный из SCAD
        """
        match = re.findall(REPEATER_PATTERN, string)
        repeaters = [[int(item) for item in re.findall(INT_PATTERNT, line)] for line in match]
        match_list = [[str(x) for x in range(num[0], num[1] + num[2], num[2])] for num in repeaters]
        match_replace = [' '.join(line) for line in match_list]
        return self.translate(string, dict(zip(match, match_replace)))

    def replace_range(self, string: str) -> str:
        """
        Метод находит диапазоны целых чисел, к примеру, 100-1000 и заменяет их
        на указанный диапазон чисел через пробел.
        На вход подается текстовый файл, импортированный из SCAD
        """
        match = re.findall(RANGE_PATTERN, string)
        repeaters = [[int(item) for item in re.findall(INT_PATTERNT, line)] for line in match]
        match_list = [[str(x) for x in range(line[0], line[1] + 1)] for line in repeaters]
        match_replace = [' '.join(line) for line in match_list]
        return self.translate(string, dict(zip(match, match_replace)))

    @staticmethod
    def translate(string: str, replace: dict):
        pattern = re.compile("|".join([re.escape(k) for k in sorted(replace, key=len, reverse=True)]), flags=re.DOTALL)
        return pattern.sub(lambda x: replace[x.group(0)], string)
