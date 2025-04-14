from __future__ import annotations

import copy
import os
import random
import re
import xml.etree.ElementTree as et
from svgpathtools import svg2paths2, Path
from datetime import datetime

import requests
from PIL import Image as PILImage
from customtkinter import filedialog

import logic.exceptions as exceptions
from logic.environment import Environment
from logic.flags import Flag, FlagMultiple, FlagSentence


class Alphabet:
    _characters = {'A': Flag('Alfa', 'static/graphics/flags/letters/Alfa.svg',
                             'A\nMam nurka pod wodą; trzymajcie się z dala i idźcie powoli',
                             "Anioł bo biało niebieski", "• ▬", "a-zot"),
                   'B': Flag('Bravo', 'static/graphics/flags/letters/Bravo.svg',
                             'B\nŁaduję, wyładowuję albo mam na statku ładunki niebezpieczne',
                             "Bolszewik bo czerwony", "▬ • • •", "bo-ta-ni-ka"),
                   'C': Flag('Charlie', 'static/graphics/flags/letters/Charlie.svg',
                             'C\nTak (potwierdzenie albo "znaczenie poprzedzającej grupy powinno być zrozumiane w trybie twierdzącym")',
                             'Ciastko tortowe', '▬ • ▬ •', "co-raz moc-niej"),
                   'D': Flag('Delta', 'static/graphics/flags/letters/Delta.svg',
                             'D\nTrzymajcie się z dala ode mnie; manewruję z trudnością',
                             'Dunaj, rzeka a na brzegach plaże', '▬ • •', "do-li-na"),
                   'E': Flag('Echo', 'static/graphics/flags/letters/Echo.svg',
                             'E\nZmieniam swój kurs w prawo (sterburta)',
                             'Ewa niebieskie oczy czerwone usta', '•', "Ełk"),
                   'F': Flag('Foxtrot', 'static/graphics/flags/letters/Foxtrot.svg',
                             'F\nJestem niezdolny do ruchu; nawiążcie łączność ze mną',
                             'Fikuśny kwadrat', '• • ▬ •', "fi-lan-tro-pia"),
                   'G': Flag('Golf', 'static/graphics/flags/letters/Golf.svg',
                             'G\nPotrzebuję pilota\n\nNadany przez statek rybacki: wybieram sieci.',
                             'Gówno za płotem', '▬ ▬ •', "go-spo-da"),
                   'H': Flag('Hotel', 'static/graphics/flags/letters/Hotel.svg',
                             'H\nMam pilota na statku',
                             'Halina polska dziewczyna', '• • • •', "ha-la-bar-da"),
                   'I': Flag('India', 'static/graphics/flags/letters/India.svg',
                             'I\nZmieniam swój kurs w lewo (bakburta)',
                             'Igła lub Ippon(Japonia)', '• •', "i-gła"),
                   'J': Flag('Juliett', 'static/graphics/flags/letters/Juliett.svg',
                             'J\nMam pożar i niebezpieczny ładunek na statku, trzymajcie sie z dala ode mnie',
                             'Jastarnia - półwysep a z obu stron woda', '• ▬ ▬ ▬', "je-dno-kon-no"),
                   'K': Flag('Kilo', 'static/graphics/flags/letters/Kilo.svg',
                             'K\nPragne nawiązać z wami łączność',
                             'Kołobrzeg, plaża i morze', '▬ • ▬', "ko-la-no"),
                   'L': Flag('Lima', 'static/graphics/flags/letters/Lima.svg',
                             'L\nZatrzymajcie natychmiast wasz statek',
                             'Lotnik (szachownica, ale nie białoczerwona)', '• ▬ ▬ ▬', "Le-o-ni-das"),
                   'M': Flag('Mike', 'static/graphics/flags/letters/Mike.svg',
                             'M\nZatrzymałem mój statek i nie posuwam się po wodzie',
                             'Miecze', '▬ ▬', "mo-tor"),
                   'N': Flag('November', 'static/graphics/flags/letters/November.svg',
                             'N\nNie (zaprzeczenie albo "znaczenie poprzedzającej grupy powinno być zrozumiane w trybie przeczącym")',
                             'Nie gram w szachy', '▬ •', "no-ga"),
                   'O': Flag('Oscar', 'static/graphics/flags/letters/Oscar.svg',
                             'O\nCzłowiek za burtą',
                             'Ogień na dachu', '▬ ▬ ▬', "O-po-czno"),
                   'P': Flag('Papa', 'static/graphics/flags/letters/Papa.svg',
                             'P\nW porcie: zameldować się na statku (wychodzimy w morze)\n\nNa morzu: moje sieci zaczepiły o przeszkodę',
                             'Port', '• ▬ ▬ •', "Pe-lo-po-nez"),
                   'Q': Flag('Quebec', 'static/graphics/flags/letters/Quebec.svg',
                             'Q\nMój statek jest zdrowy i proszę o prawo zdolności ruchów',
                             'Qrczak cały żółty', '▬ ▬ • ▬', "Qo-spo-dar-stwo"),
                   'R': Flag('Romeo', 'static/graphics/flags/letters/Romeo.svg',
                             'R\n(Brak znaczenia pojedynczej litery)',
                             'Rycerz(„Złoty Krzyżak”)', '• ▬ •', "re-for-ma"),
                   'S': Flag('Sierra', 'static/graphics/flags/letters/Sierra.svg',
                             'S\nMoje maszyny pracują wstecz',
                             'Sadzawka, Studnia', '• • •', "Sa-ha-ra"),
                   'T': Flag('Tango', 'static/graphics/flags/letters/Tango.svg',
                             'T\nTrzymajcie się z dala ode mnie; jestem zajęty trałowaniem we dwójkę',
                             'Tuluza miasto we Francji', '▬', "ton"),
                   'U': Flag('Uniform', 'static/graphics/flags/letters/Uniform.svg',
                             'U\nKierujecie się ku niebezpieczeństwu',
                             'U lotnika', '• • ▬', "Ur-bi-no"),
                   'V': Flag('Victor', 'static/graphics/flags/letters/Victor.svg',
                             'V\nPotrzebuję pomocy',
                             'V', '• • • ▬', "Vin-cent van Gogh"),
                   'W': Flag('Whiskey', 'static/graphics/flags/letters/Whiskey.svg',
                             'W\nPotrzebuję pomocy lekarskiej',
                             'Wojna w porcie', '• ▬ ▬', "wi-no-rośl"),
                   'X': Flag('X-ray', 'static/graphics/flags/letters/X-ray.svg',
                             'X\nWstrzymajcie się z wykonywaniem waszych zamierzeń i uważajcie na moje sygnały',
                             'Xsiądz', '▬ • • ▬', "Xo-chi-mil-co"),
                   'Y': Flag('Yankee', 'static/graphics/flags/letters/Yankee.svg',
                             'Y\nWlokę moją kotwicę',
                             'Yayecznica', '▬ • ▬ ▬', "York Hull, Oks-ford"),
                   'Z': Flag('Zulu', 'static/graphics/flags/letters/Zulu.svg',
                             'Z\nPotrzebuję holownika\n\nStatki rybackie: wydaję sieci',
                             'Zlepek kolorów', '▬ ▬ • •', "zło-to-list-na"),
                   '0': Flag('Nadazero', 'static/graphics/flags/digits/0.svg', 'Zero',
                             'Zero w Yayecznicy (bo wpadło...)', '▬ ▬ ▬ ▬ ▬', "5 kresek"),
                   '1': Flag('Unaone', 'static/graphics/flags/digits/1.svg', 'Jeden',
                             'Jeden Japoniec', '• ▬ ▬ ▬ ▬', "1 kropka i same kreski"),
                   '2': Flag('Bissotwo', 'static/graphics/flags/digits/2.svg', 'Dwa',
                             'Dwa (bo nie Japoniec?)', '• • ▬ ▬ ▬', "2 kropki i same kreski"),
                   '3': Flag('Terrathree', 'static/graphics/flags/digits/3.svg', 'Trzy',
                             'Tróbarwna Francuska(Tuluza)', '• • • ▬ ▬', "3 kropki i same kreski"),
                   '4': Flag('Kartefour', 'static/graphics/flags/digits/4.svg', 'Cztery',
                             'Cztery białe ramiona (krzyża)', '• • • • ▬', "4 kropki i kreska"),
                   '5': Flag('Pantafive', 'static/graphics/flags/digits/5.svg', 'Pięć',
                             'Piątka w Kołobrzegu', '• • • • •', "5 kropek"),
                   '6': Flag('Soxisix', 'static/graphics/flags/digits/6.svg', 'Sześć',
                             'Sześciu Murzynów na sniegu', '▬ • • • •', "1 kreska i same kropki"),
                   '7': Flag('Setteseven', 'static/graphics/flags/digits/7.svg', 'Siedem',
                             'Siódemka Warszawska', '▬ ▬ • • •', "2 kreski i same kropki"),
                   '8': Flag('Oktoeight', 'static/graphics/flags/digits/8.svg', 'Osiem',
                             'Osiem czerwonych, bo podwójnie?', '▬ ▬ ▬ • •', "3 kreski i same kropki"),
                   '9': Flag('Novenine', 'static/graphics/flags/digits/9.svg', 'Dziewięć',
                             'Dziewięć 6+7 po barwach - 4 pola', '▬ ▬ ▬ ▬ •', "4 kreski i kropka")}
    _additionalFlags = {
        '?': Flag('?', 'static/graphics/flags/other/Answer.svg', 'Flaga wywoławcza pytania i odpowiedzi', '', '', ''),
        '!': Flag('!', 'static/graphics/flags/other/Repeat_One.svg', 'Zastępcza 1', '', '', ''),
        '@"': Flag('@"', 'static/graphics/flags/other/Repeat_Two.svg', 'Zastępcza 2', '', '', ''),
        '#£': Flag('#£', 'static/graphics/flags/other/Repeat_Three.svg', 'Zastępcza 3', '', '', '')}
    _multipleFlags = [FlagMultiple([_characters['A'], _characters['C']], 'Opuszczam mój statek'),
                      FlagMultiple([_characters['A'], _characters['D']],
                                   'Opuszczam mój statek, który ucierpiał w wypadku nuklearnym i stanowi potencjalne źródło niebezpieczeństwa promieniowania'),
                      FlagMultiple([_characters['A'], _characters['N']], 'Potrzebuję lekarza'),
                      FlagMultiple([_characters['A'], _characters['N'], _characters['1']],
                                   'Potrzebuję lekarza; mam poważne oparzenia'),
                      FlagMultiple([_characters['A'], _characters['N'], _characters['2']],
                                   'Potrzebuję lekarza; mam ofiary promieniowania'),
                      FlagMultiple([_characters['E'], _characters['L']], 'Powtórz pozycję niebezpieczeństwa'),
                      FlagMultiple([_characters['E'], _characters['L'], _characters['1']],
                                   'Jaka jest pozycja statku w niebezpieczeństwie?'),
                      FlagMultiple([_characters['G'], _characters['M']], 'Nie mogę uratować mojego statku'),
                      FlagMultiple([_characters['G'], _characters['N']], 'Powinieneś zabrać osoby z pokładu'),
                      FlagMultiple([_characters['G'], _characters['N'], _characters['1']],
                                   'Życzę sobie zdjęcia niektórych osób. Na pokładzie pozostanie załoga zredukowana do minimum'),
                      FlagMultiple([_characters['G'], _characters['N'], _characters['2']], 'Zabiorę ludzi z pokładu'),
                      FlagMultiple([_characters['G'], _characters['N'], _characters['3']],
                                   'Czy możesz zabrać ludzi z pokładu?'),
                      FlagMultiple([_characters['I'], _characters['T']], 'Płonę'),
                      FlagMultiple([_characters['J'], _characters['A']], 'Potrzebuję urządzeń przeciwpożarowych'),
                      FlagMultiple([_characters['J'], _characters['A'], _characters['4']],
                                   'Potrzebuję materiału do gaśnic pianowych'),
                      FlagMultiple([_characters['M'], _characters['A'], _additionalFlags['@"']],
                                   'Proszę o pilną poradę medyczną'),
                      FlagMultiple([_characters['M'], _characters['A'], _characters['B']],
                                   'Proszę o spotkanie we wskazanej pozycji'),
                      FlagMultiple([_characters['M'], _characters['A'], _characters['C']],
                                   'Proszę o zorganizowanie przyjęcia do szpitala'),
                      FlagMultiple([_characters['M'], _characters['A'], _characters['D']],
                                   'Jestem oddalony o (wskazana liczba) godzin od najbliższego portu'),
                      FlagMultiple([_characters['M'], _characters['S'], _characters['1']],
                                   'Mój statek stanowi niebezpieczne źródło promieniowania; możesz zbliżyć się od sterburty'),
                      FlagMultiple([_characters['V'], _characters['G']],
                                   'Zakrycie niskich chmur wynosi... (liczba oktantów lub ósmych części nieba)'),
                      FlagMultiple([_characters['U'], _characters['S'], _characters['4']],
                                   'Nic nie można zrobić, dopóki pogoda się nie poprawi'),
                      FlagMultiple([_characters['N'], _characters['C']],
                                   'Jestem w niebezpieczeństwie i potrzebuję natychmiastowej pomocy'),
                      FlagMultiple([_characters['R'], _characters['Y']], 'Zachowaj odstęp przy niskiej prędkości'),
                      FlagMultiple([_characters['A'], _characters['E']], 'Muszę opuścić mój statek'),
                      FlagMultiple([_characters['D'], _characters['X']], 'Tonę')]
    _allFlags = list(_characters.values()) + list(_additionalFlags.values()) + _multipleFlags
    _sentences_from_user_file = []
    _default_sentences = []

    @staticmethod
    def get_all_flags(size: int = 0) -> list[Flag | FlagMultiple]:
        """Returns a list of a specified size of all possible flags. If size is not provided, returns all existing ones.
         If size is bigger than the number of flags (66) returns all flags.

        :param size: Size of the list to return
        :rtype: List[Flag, FlagMultiple]
        """
        flags = copy.deepcopy(Alphabet._allFlags)
        random.shuffle(flags)
        if 0 < size < len(flags):
            return flags[:size]
        return flags

    @staticmethod
    def get_all_flags_with_meaning(size: int = 0) -> list[Flag | FlagMultiple]:
        """Returns a list of a specified size of all possible flags which have meaning. If size is not provided, returns all existing ones.
         If size is bigger than the number of flags (65), returns all flags.

        :param size: Size of the list to return
        :rtype: List[Flag, FlagMultiple]
        """
        list_of_all_flags_with_meaning = copy.deepcopy(Alphabet._characters)
        list_of_all_flags_with_meaning.pop('R')
        list_of_all_flags_with_meaning = list(list_of_all_flags_with_meaning.values())
        list_of_all_flags_with_meaning.extend(Alphabet._additionalFlags.values())
        list_of_all_flags_with_meaning.extend(Alphabet._multipleFlags)
        random.shuffle(list_of_all_flags_with_meaning)
        if 0 < size < len(list_of_all_flags_with_meaning):
            return list_of_all_flags_with_meaning[:size]
        return list_of_all_flags_with_meaning

    @staticmethod
    def get_single_flags_shuffled() -> list[Flag]:
        """Returns a shuffled list of all single flags.

        :rtype: List[Flag]
        """
        flags = copy.deepcopy(list(Alphabet._characters.values()))
        flags.extend(list(Alphabet._additionalFlags.values()))
        random.shuffle(flags)
        return flags

    @staticmethod
    def get_single_flags() -> list[Flag]:
        """Returns a list of all single flags.

        :rtype: List[Flag]
        """
        flags = copy.deepcopy(list(Alphabet._characters.values()))
        flags.extend(list(Alphabet._additionalFlags.values()))
        return flags

    @staticmethod
    def get_characters_flags_shuffled(size: int = 0) -> list[Flag]:
        """Returns a shuffled list of a specified size of letter and numeral Flag objects.If size is not provided, returns all existing ones.
         If size is bigger than the number of flags (36), returns all flags.

        :param size: Size of the list to return
        :rtype: List[Flag]
        """
        flags = list(Alphabet._characters.values())
        random.shuffle(flags)
        if 0 < size < len(flags):
            return flags[:size]
        return flags

    @staticmethod
    def get_flag_using_character(character: str) -> Flag | None:
        """Returns a Flag object using a character.
        Returns None if space character is passed.

        :raise InputCharacterException if character is not found.
        :param character: Character to search for
        :rtype: Flag|None
        """
        if character in ['?', '!']:
            return Alphabet._additionalFlags[character]
        # Two characters represent 'Second substitute' flag
        elif character in ['"', '@']:
            return Alphabet._additionalFlags['@"']
        # Two characters represent 'Third substitute' flag
        elif character in ["#", "£"]:
            return Alphabet._additionalFlags['#£']
        elif character == ' ':
            return None
        else:
            flag = Alphabet._characters.get(character.upper())
            if flag:
                return flag
            raise exceptions.InputCharacterException()

    @staticmethod
    def get_default_sentence() -> FlagSentence | None:
        """Returns random sentence from default set created from flags, if everything is ok.
        Returs None if there is no file selected, or if there is no sentence.

        :rtype: FlagSentence | None
        """
        if len(Alphabet._default_sentences) > 0:
            sentence = random.choice(Alphabet._default_sentences)
            Alphabet._default_sentences.remove(sentence)
            return sentence
        return None

    @staticmethod
    def load_default_sentences():
        """Loads sentences from default set.

        :raise CantLoadDefaultSentencesException: If there is a problem with loading default sentences
        """
        filename = Environment.resource_path('static/files/default_sentences.txt')
        Alphabet._default_sentences = []
        try:
            with open(filename, 'r') as file:
                sentences_str = [line.strip() for line in file]
                print(sentences_str)
                for sentence_str in sentences_str:
                    cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence_str).upper().strip()[:50]
                    flags = Alphabet._translate_sentence_to_flags(cleaned_sentence)
                    Alphabet._default_sentences.append(FlagSentence(flags, sentence_str, cleaned_sentence))
        except Exception:
            raise exceptions.CantLoadDefaultSentencesException()

    @staticmethod
    def get_number_of_default_sentences() -> int:
        """Returns the number of default sentences.

        :rtype: int
        """
        return len(Alphabet._default_sentences)

    @staticmethod
    def get_flag_sentence_from_api() -> FlagSentence:
        """Returns random sentence created from flags, if everything is ok.

        :raise NoInternetConnectionException if there is no internet connection.
        :raise RequestLimitExceededException if requests limit has been exceeded.
        :rtype FlagSentence
        """
        sentence = Alphabet._get_random_sentence()
        print(sentence)
        cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence).upper().strip()
        flags = Alphabet._translate_sentence_to_flags(cleaned_sentence)
        return FlagSentence(flags, sentence, cleaned_sentence)

    @staticmethod
    def get_sentence_from_user_file() -> FlagSentence | None:
        """Returns random sentence from user's file created from flags, if everything is ok.
        Returs None if there is no file selected, or if there is no sentence.

        :rtype FlagSentence | None
        """
        if len(Alphabet._sentences_from_user_file) > 0:
            sentence = random.choice(Alphabet._sentences_from_user_file)
            Alphabet._sentences_from_user_file.remove(sentence)
            return sentence
        return None

    @staticmethod
    def load_sentences_from_user_file():
        """Loads sentences from user's file.

        :raise NoFileSelectedException: If there is no file selected
        :raise SmthWrongWithFileException: If there is a problem with loading sentences from user's file
        """
        Alphabet._sentences_from_user_file = []
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        try:
            if not filename:
                raise exceptions.NoFileSelectedException()
            with open(filename, 'r') as file:
                sentences_str = [line.strip() for line in file]
                print(sentences_str)
                for sentence_str in sentences_str:
                    cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence_str).upper().strip()[:50]
                    flags = Alphabet._translate_sentence_to_flags(cleaned_sentence)
                    Alphabet._sentences_from_user_file.append(FlagSentence(flags, sentence_str, cleaned_sentence))
        except Exception:
            raise exceptions.SmthWrongWithFileException()

    @staticmethod
    def get_number_of_sentences_from_user_file() -> int:
        """Returns the number of sentences from user's file.

        :rtype: int
        """
        return len(Alphabet._sentences_from_user_file)

    @staticmethod
    def get_flag_sentence_svg(sentence: str, background_color: str = 'gray') -> str:
        """Creates SVG file with flags from sentence.

        :param sentence: Sentence to save
        :param background_color: If 'gray', background will be gray, otherwise transparent
        :return Path to the created file
        :rtype: str
        """
        target_flag_dimension = 650
        new_img_width = (max(len(line) for line in sentence.split('\n')) * target_flag_dimension) - 50
        new_img_height = ((sentence.count("\n") + 1) * target_flag_dimension) - 50
        et.register_namespace("","http://www.w3.org/2000/svg")
        new_svg = et.Element("svg", {
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "width": str(new_img_width),
            "height": str(new_img_height),
            "viewBox": f"0 0 {new_img_width} {new_img_height}"
        })
        if background_color == 'gray':
            new_svg.append(et.Element("rect", {"width": str(new_img_width), "height": str(new_img_height),
                                               "fill": "rgb(128, 128, 128)"}))

        ns = {"svg": "http://www.w3.org/2000/svg"}
            
        def get_svg_bbox(paths: list[Path]):
            xmin, xmax, ymin, ymax = paths.pop(0).bbox()
            for path in paths:
                p_xmin, p_xmax, p_ymin, p_ymax = path.bbox()
                xmin = min(xmin, p_xmin)
                xmax = max(xmax, p_xmax)
                ymin = min(ymin, p_ymin)
                ymax = max(ymax, p_ymax)

            return xmin, xmax, ymin, ymax

        row, column = 0, 0
        for symbol in sentence:
            if symbol == '\n':
                row += 1
                column = 0
            elif symbol == ' ':
                column += 1
            else:
                current_flag = Alphabet.get_flag_using_character(symbol)
                if isinstance(current_flag, Flag):
                    paths, _, svg_attributes = svg2paths2(Environment.resource_path(current_flag.img_path))
                    svg_width = float(svg_attributes["width"])
                    svg_height = float(svg_attributes["height"])

                    bbox = get_svg_bbox(paths)
                    scale_x = new_img_width / (bbox[1] - bbox[0])
                    scale_y = new_img_height / (bbox[3] - bbox[2])

                    scale = min(scale_x, scale_y)

                    current_flag_group = et.Element("g", {"transform": f"translate({column * target_flag_dimension}, {row * target_flag_dimension}) scale({scale}, {scale})"})
                    svg = et.parse(Environment.resource_path(current_flag.img_path)).getroot()
                    for child in list(svg):
                        current_flag_group.append(child)

                    new_svg.append(current_flag_group)
                    column += 1
        tree = et.ElementTree(new_svg)
        file_name = f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.svg"
        os.makedirs(Environment.resource_path(f"static/tmp"), exist_ok=True)
        file_path = Environment.resource_path(f"static/tmp/{file_name}")
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        return file_path

    @staticmethod
    def save_flag_sentence_png(sentence: list[Flag | None], background: str = 'gray',
                               suggest_file_name: bool = True, max_row_characters: int = 0) -> bool:
        """Saves FlagSentence as PNG file.

        :param sentence: Sentence to save
        :param background: Background color, either 'gray' or 'transparent'
        :param suggest_file_name: If True, suggests file name based on sentence:
        :param max_row_characters: Maximum number of characters in a row
        :return True if everything is ok, False if user didn't select file
        :rtype: bool
        """
        file_name = ''

        if suggest_file_name:
            for flag in sentence:
                if flag is None or flag == '':
                    file_name += ' '
                elif isinstance(flag, Flag) and flag.code_word == 'Nadazero':
                    file_name += '0'
                elif isinstance(flag, Flag) and flag.code_word == 'Unaone':
                    file_name += '1'
                elif isinstance(flag, Flag) and flag.code_word == 'Bissotwo':
                    file_name += '2'
                elif isinstance(flag, Flag) and flag.code_word == 'Terrathree':
                    file_name += '3'
                elif isinstance(flag, Flag) and flag.code_word == 'Kartefour':
                    file_name += '4'
                elif isinstance(flag, Flag) and flag.code_word == 'Pantafive':
                    file_name += '5'
                elif isinstance(flag, Flag) and flag.code_word == 'Soxisix':
                    file_name += '6'
                elif isinstance(flag, Flag) and flag.code_word == 'Setteseven':
                    file_name += '7'
                elif isinstance(flag, Flag) and flag.code_word == 'Oktoeight':
                    file_name += '8'
                elif isinstance(flag, Flag) and flag.code_word == 'Novenine':
                    file_name += '9'
                elif isinstance(flag, Flag) and flag.code_word not in ('?', '!', '@"', '#£'):
                    file_name += flag.code_word[0].upper()
                else:
                    file_name += '_'

        cell_width = 200
        cell_height = 200
        x_padding = 10
        y_padding = 10

        if suggest_file_name:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile=file_name
            )
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )

        if file_path:
            png_files = []

            for flag in sentence:
                if flag is None or flag == '':
                    png_files.append(flag)
                else:
                    png_files.append(flag.png_img_path)

            max_rows = 0
            max_columns = 0

            current_columns = 0
            for png_file in png_files:
                if png_file is not None:
                    current_columns += 1
                    if current_columns > max_columns:
                        if max_row_characters == 0 or current_columns <= max_row_characters:
                            max_columns = current_columns
                        else:
                            max_rows += 1
                            current_columns = 1
                else:
                    current_columns = 0
                    max_rows += 1

            total_width = max_columns * cell_width + (max_columns - 1) * x_padding
            total_height = (max_rows + 1) * cell_height + max_rows * y_padding

            if background == 'gray':
                bg_color = (128, 128, 128, 255)
            else:
                bg_color = (255, 255, 255, 0)

            # Create empty image
            collage = PILImage.new('RGBA', (total_width, total_height), bg_color)

            x = 0
            y = 0
            for png_file in png_files:
                if png_file is None:
                    x = 0
                    y += cell_height + y_padding
                    continue
                if png_file == "":
                    x += cell_width + x_padding
                    continue

                Alphabet._embed_png(Environment.resource_path(png_file), x, y, cell_width, cell_height, collage,
                                    background)
                x += cell_width + x_padding

            collage.save(file_path, format='PNG')
            return True
        return False

    @staticmethod
    def _embed_png(png_file, x, y, cell_width, cell_height, output_image, background: str):
        """Embeds PNG image in another image.
        :param png_file: Path to PNG file
        :param x: X position to paste image
        :param y: Y position to paste image
        :param cell_width: Width of the cell
        :param cell_height: Height of the cell
        :param output_image: Image to embed PNG in
        :param background: Background color, either 'gray' or 'transparent'
        """
        with PILImage.open(png_file) as img:
            img = img.resize((cell_width, cell_height))
            if background == 'gray':
                background_img = PILImage.new('RGBA', (cell_width, cell_height), (128, 128, 128, 255))
                img = img.convert('RGBA')
                ready_flag = PILImage.alpha_composite(background_img, img)
                output_image.paste(ready_flag, (x, y))
            else:
                output_image.paste(img, (x, y))

    @staticmethod
    def _get_random_sentence() -> str:
        """Returns a random sentence from zenquotes.io if everything is ok.
        raise NoInternetConnectionException if there is no internet connection.
        raise RequestLimitExceededException if requests limit has been exceeded.

        Function need internet connection to work.

        :rtype: str
        :return: Random sentence
        """
        try:
            response = requests.get("https://zenquotes.io/api/quotes")
            if response.status_code == 200:
                sentences = response.json()
                for sentence in sentences:
                    try:
                        sentence_text = sentence['q']
                        if int(sentence['c']) <= 50:
                            return f"{sentence_text}"
                    except KeyError:
                        raise exceptions.RequestLimitExceededException()
                Alphabet._get_random_sentence()
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException:
            raise exceptions.NoInternetConnectionException()

    @staticmethod
    def _translate_sentence_to_flags(sentence: str) -> list[Flag | None]:
        """Translates sentence to flags.
        None is used for spaces.

        :param sentence: Sentence to translate
        :rtype: list[Flag | None]
        :return: Translated sentence in flag language
        """
        flags = []
        for letter in sentence:
            if letter in Alphabet._characters:
                flags.append(Alphabet._characters[letter])
            elif letter in Alphabet._additionalFlags:
                flags.append(Alphabet._additionalFlags[letter])
            else:
                flags.append(None)
        return flags
