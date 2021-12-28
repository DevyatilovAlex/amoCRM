import os
import re
import time
import goslate
import pymorphy2

DIRECTORY = 'text'


def walk(directory: str) -> dict:
    for root, dirs, files in os.walk(directory):
        cnt_words = {}
        for name in files:
            file = os.path.join(root, name)
            with open(file, 'r', encoding='utf-8') as f:
                new_cnt_words = analysis(f)
                for word in new_cnt_words:
                    cnt = cnt_words.get(word, 0)
                    cnt_words[word] = cnt + new_cnt_words[word]

    return cnt_words


def analysis(iterable: iter) -> dict:
    morph = pymorphy2.MorphAnalyzer()
    word_pattern = re.compile(r'\b[а-я]+\b', re.IGNORECASE)

    cnt_words = {}
    for line in iterable:
        words = word_pattern.findall(line)
        words = map(str.lower, words)
        words = [morph.parse(word)[0].normal_form for word in words]
        for word in words:
            cnt = cnt_words.get(word, 0)
            cnt_words[word] = cnt + 1

    return cnt_words


def sorted_dict(dictionary: dict, reverse: bool = True) -> dict:
    sorted_dictionary = {}
    sorting_word_by_frequency = sorted(dictionary.keys(), key=dictionary.get, reverse=reverse)
    for word in sorting_word_by_frequency:
        sorted_dictionary[word] = dictionary[word]

    return sorted_dictionary


def show_words(words_dict: dict):
    max_len_word = len(max(words_dict.keys(), key=len))
    for key, cnt_item in words_dict.items():
        print(f'{key.ljust(max_len_word)}: {cnt_item}')


def translator(words_to_translate: iter, target_language: str = 'en', **kargs) -> dict:
    gs = goslate.Goslate(**kargs)
    translate = gs.translate
    for word, translation in zip(words_to_translate, gs.translate(words_to_translate, target_language)):
        print(word, translation)
        time.sleep(2)


if __name__ == '__main__':
    cnt_words = walk(DIRECTORY)
    sorted_cnt_words = sorted_dict(cnt_words)
    show_words(sorted_cnt_words)
    translator(cnt_words.keys())
