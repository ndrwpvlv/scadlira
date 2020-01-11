# scadlira

**scadlira** - конвертер текстового файла расчетной модели из программного комплекса SCAD в ЛИРА-САПР 

## Установка
Установка пакета для Python 3 через PIP:
```
pip3 install git+https://github.com/ndrwpvlv/code_syntax_analyser.git
```
Если есть проблемы с правами доступа при установке под LINUX, то возможен подобный вариант:
```
sudo -H pip3 install git+https://github.com/ndrwpvlv/code_syntax_analyser.git

```

## Дорожная карта
- [x] Перевод узлов
- [x] Перевод элементов
- [x] Перевод закреплений
- [ ] Конвертация нагрузок и загружений
- [ ] Конвертация РСУ 

## Использование пакета
Конвертер файлов работает только с текстовыми файлами SCAD, записанными __БЕЗ__ повторителей.

### Использование внутри макроса
```
from scadlira.converter import ScadModel

filename = 'example.txt'  # Название текстового файла с расчетной моделью SCAD
model = ScadModel(filename)  # Создаем объект, внутри которого
model.write_liratxt()
```

### Использование командной строки
Предварительно следует установить пакет в систему или виртуальное окружение через __PIP__

```buildoutcfg
python3 -m scadlira [-f FILENAME]
```

## Зависимости
```
Python 3.7+ (Возможно, что 3.5+, но пакет не проверялся под него)
```

## Contributors
Andrei S. Pavlov (https://github.com/ndrwpvlv/)