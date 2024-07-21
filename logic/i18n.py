import glob
import json
import os


class Translator:
    _supported_format = ['json']
    _data = {}
    _locale = 'pl'

    @staticmethod
    def initialize(file_format: str, locale: str = 'pl'):
        """
        Initialize the translator with the given file format and locale. Raise an exception if the locale is not supported.
        :param file_format: Currently, only JSON is supported.
        :param locale: pl or en
        """
        Translator._locale = locale
        if file_format in Translator._supported_format:
            files = glob.glob(os.path.join('static/locales', f'*.{file_format}'))
            for fil in files:
                file_name_without_extension = os.path.splitext(os.path.basename(fil))[0]
                with open(fil, 'r', encoding='utf8') as f:
                    Translator._data[file_name_without_extension] = json.load(f)
        if locale not in Translator._data:
            raise Exception('Invalid locale')

    @staticmethod
    def set_locale(loc: str):
        """
        Set the locale to the given locale. Raise an exception if the locale is not supported.
        :param loc: pl or en
        """
        if len(Translator._data) == 0:
            Translator.initialize('json', loc)
        else:
            if loc in Translator._data:
                Translator._locale = loc
            else:
                raise Exception('Invalid locale')

    @staticmethod
    def get_locale() -> str:
        """
        Get the current locale.
        :rtype: str
        """
        return Translator._locale

    @staticmethod
    def translate(key: str) -> str:
        """
        Get the translation of the given key.
        :param key: The key to translate
        :rtype: str
        """
        if len(Translator._data) == 0:
            Translator.initialize('json')
        text = Translator._data[Translator._locale].get(key, None)
        return text
