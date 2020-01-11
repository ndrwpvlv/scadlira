# -*- coding: utf-8 -*-

import re

from .helpers import NODES_PATTERNS, ELEMENTS_PATTERNS, DOFS_PATTERNS, REPEATER_PATTERN, INT_PATTERNT, RANGE_PATTERN, \
    HEADER


class ScadModel:
    def __init__(self, filname: str):
        self.filname = filname
        self.txt = self.readtxt()  # Читаем текст и заменяем повторители
        self.model = {
            'nodes': self.parse_nodes(self.extract_data(*NODES_PATTERNS)),
            'elements': self.parse_elems(
                self.extract_data(*ELEMENTS_PATTERNS)
            ),
            'dofs': self.parse_dofs(self.extract_data(*DOFS_PATTERNS)),
        }

    def readtxt(self):
        with open(self.filname, 'r') as file:
            txt = file.read().replace('\n', '')
        return self.replace_range(self.replace_repeaters(txt))

    def extract_data(self, pattern, clean_suffix):
        search = re.findall(pattern, self.txt)[0]
        return search.replace(clean_suffix, '').replace('/', '/\n')

    def parse_nodes(self, data):
        return [self.check_list_size(line, 3) for line in self.split_by_whitespaces(data)]

    def parse_elems(self, data):
        return [[int(item) for item in line] for line in self.split_by_whitespaces(data)]

    @staticmethod
    def parse_dofs(data):
        lines = [string.split(':') for string in data.split('/\n') if string]
        dofs = {int(nds): line[0].replace('  ', ' ') for line in lines for nds in line[1].split(' ') if nds}
        return dict(sorted(dofs.items()))

    def write_liratxt(self):
        filname = self.filname.split('.')[0]
        with open('%s-converted.txt' % filname[:20], 'w') as file:
            file.write(HEADER.replace('scadlira', filname))  # заголовок
            file.write('(1/\n')  # узлы
            for line in self.model['elements']:
                file.write(' '.join(str(item) for item in line) + '/\n')
            file.write(')\n')
            file.write('(4/\n')  # элементы
            for line in self.model['nodes']:
                file.write(' '.join(str(item) for item in line) + '/\n')
            file.write(')\n')
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

    @staticmethod
    def replace_repeaters(string: str) -> str:
        """
        Метод находит повторители и заменяет их на указанный диапазон
        чисел через пробел.
        На вход подается текстовый файл, импортированный из SCAD
        """
        match = re.findall(REPEATER_PATTERN, string)
        repeaters = [[int(item) for item in re.findall(INT_PATTERNT, line)] for line in match]
        match_replace = [[str(x) for x in range(num[0], num[1] + num[2], num[2])] for num in repeaters]
        for ii in range(len(match)):
            string = string.replace(match[ii], ' '.join(match_replace[ii]))
        return string

    @staticmethod
    def replace_range(string: str) -> str:
        """
        Метод находит диапазоны целых чисел, к примеру, 100-1000 и заменяет их
        на указанный диапазон чисел через пробел.
        На вход подается текстовый файл, импортированный из SCAD
        """
        match = re.findall(RANGE_PATTERN, string)
        repeaters = [[int(item) for item in re.findall(INT_PATTERNT, line)] for line in match]
        match_replace = [[str(x) for x in range(line[0], line[1] + 1)] for line in repeaters]
        for ii in range(len(match)):
            string = string.replace(match[ii], ' '.join(match_replace[ii]))
        return string
