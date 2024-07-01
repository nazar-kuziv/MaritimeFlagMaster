import copy
import random
import re
import requests
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

from PIL import Image as PILImage

from logic import constants
from logic.environment import Environment
from logic.flags import Flag, FlagMultiple, FlagSentence


class AlphabetMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Alphabet(metaclass=AlphabetMeta):
    _characters = {'A': Flag('Alfa', 'flags/letters/Alfa.svg',
                             'Mam nurka pod wodą; trzymajcie się z dala i idźcie powoli',
                             "Anioł bo biało niebieski", "• ▬"),
                   'B': Flag('Bravo', 'flags/letters/Bravo.svg',
                             'Ładuję, wyładowuję albo mam na statku ładunki niebezpieczne',
                             "Bolszewik bo czerwony", "▬ • • •"),
                   'C': Flag('Charlie', 'flags/letters/Charlie.svg',
                             'Tak (potwierdzenie albo "znaczenie poprzedzającej grupy powinno być zrozumiane w trybie twierdzącym")',
                             'Ciastko tortowe', '▬ • ▬ •'),
                   'D': Flag('Delta', 'flags/letters/Delta.svg',
                             'Trzymajcie się z dala ode mnie; manewruję z trudnością',
                             'Dunaj, rzeka a na brzegach plaże', '▬ • •'),
                   'E': Flag('Echo', 'flags/letters/Echo.svg',
                             'Zmieniam swój kurs w prawo (sterburta)',
                             'Ewa niebieskie oczy czerwone usta', '•'),
                   'F': Flag('Foxtrot', 'flags/letters/Foxtrot.svg',
                             'Jestem niezdolny do ruchu; nawiążcie łączność ze mną',
                             'Fikuśny kwadrat', '• • ▬ •'),
                   'G': Flag('Golf', 'flags/letters/Golf.svg',
                             'Potrzebuję pilota\n\nNadany przez statek rybacki: wybieram sieci.',
                             'Gówno za płotem', '▬ ▬ •'),
                   'H': Flag('Hotel', 'flags/letters/Hotel.svg',
                             'Mam pilota na statku',
                             'Halina polska dziewczyna', '• • • •'),
                   'I': Flag('India', 'flags/letters/India.svg',
                             'Zmieniam swój kurs w lewo (bakburta)',
                             'Igła lub Ippon(Japonia)', '• •'),
                   'J': Flag('Juliett', 'flags/letters/Juliett.svg',
                             'Mam pożar i niebezpieczny ładunek na statku, trzymajcie sie z dala ode mnie',
                             'Jastarnia - półwysep a z obu stron woda', '• ▬ ▬ ▬'),
                   'K': Flag('Kilo', 'flags/letters/Kilo.svg',
                             'Pragne nawiązać z wami łączność',
                             'Kołobrzeg, plaża i morze', '▬ • ▬'),
                   'L': Flag('Lima', 'flags/letters/Lima.svg',
                             'Zatrzymajcie natychmiast wasz statek',
                             'Lotnik (szachownica, ale nie białoczerwona)', '• ▬ ▬ ▬'),
                   'M': Flag('Mike', 'flags/letters/Mike.svg',
                             'Zatrzymałem mój statek i nie posuwam się po wodzie',
                             'Miecze', '▬ ▬'),
                   'N': Flag('November', 'flags/letters/November.svg',
                             'Nie (zaprzeczenie albo "znaczenie poprzedzającej grupy powinno być zrozumiane w trybie przeczącym")',
                             'Nie gram w szachy', '▬ •'),
                   'O': Flag('Oscar', 'flags/letters/Oscar.svg',
                             'Człowiek za burtą',
                             'Ogień na dachu', '▬ ▬ ▬'),
                   'P': Flag('Papa', 'flags/letters/Papa.svg',
                             'W porcie: zameldować się na statku (wychodzimy w morze)\n\nNa morzu: moje sieci zaczepiły o przeszkodę',
                             'Port', '• ▬ ▬ •'),
                   'Q': Flag('Quebec', 'flags/letters/Quebec.svg',
                             'Mój statek jest zdrowy i proszę o prawo zdolności ruchów',
                             'Qrczak cały żółty', '▬ ▬ • ▬'),
                   'R': Flag('Romeo', 'flags/letters/Romeo.svg',
                             'Brak znaczenia pojedynczej litery',
                             'Rycerz(„Złoty Krzyżak”)', '• ▬ •'),
                   'S': Flag('Sierra', 'flags/letters/Sierra.svg',
                             'Moje maszyny pracują wstecz',
                             'Sadzawka, Studnia', '• • •'),
                   'T': Flag('Tango', 'flags/letters/Tango.svg',
                             'Trzymajcie się z dala ode mnie; jestem zajęty trałowaniem we dwójkę',
                             'Tuluza miasto we Francji', '▬'),
                   'U': Flag('Uniform', 'flags/letters/Uniform.svg',
                             'Kierujecie się ku niebezpieczeństwu',
                             'U lotnika', '• • ▬'),
                   'V': Flag('Victor', 'flags/letters/Victor.svg',
                             'Potrzebuję pomocy',
                             'V', '• • • ▬'),
                   'W': Flag('Whiskey', 'flags/letters/Whiskey.svg',
                             'Potrzebuję pomocy lekarskiej',
                             'Wojna w porcie', '• ▬ ▬'),
                   'X': Flag('X-ray', 'flags/letters/X-ray.svg',
                             'Wstrzymajcie się z wykonywaniem waszych zamierzeń i uważajcie na moje sygnały',
                             'Xsiądz', '▬ • • ▬'),
                   'Y': Flag('Yankee', 'flags/letters/Yankee.svg',
                             'Wlokę moją kotwicę',
                             'Yayecznica', '▬ • ▬ ▬'),
                   'Z': Flag('Zulu', 'flags/letters/Zulu.svg',
                             'Potrzebuję holownika\n\nStatki rybackie: wydaję sieci',
                             'Zlepek kolorów', '▬ ▬ • •'),
                   '0': Flag('Nadazero', 'flags/digits/0.svg', 'Zero',
                             'Zero w Yayecznicy (bo wpadło...)', '▬ ▬ ▬ ▬ ▬'),
                   '1': Flag('Unaone', 'flags/digits/1.svg', 'Jeden',
                             'Jeden Japoniec', '• ▬ ▬ ▬ ▬'),
                   '2': Flag('Bissotwo', 'flags/digits/2.svg', 'Dwa',
                             'Dwa (bo nie Japoniec?)', '• • ▬ ▬ ▬'),
                   '3': Flag('Terrathree', 'flags/digits/3.svg', 'Trzy',
                             'Tróbarwna Francuska(Tuluza)', '• • • ▬ ▬'),
                   '4': Flag('Kartefour', 'flags/digits/4.svg', 'Cztery',
                             'Cztery białe ramiona (krzyża)', '• • • • ▬'),
                   '5': Flag('Pantafive', 'flags/digits/5.svg', 'Pięć',
                             'Piątka w Kołobrzegu', '• • • • •'),
                   '6': Flag('Soxisix', 'flags/digits/6.svg', 'Sześć',
                             'Sześciu Murzynów na sniegu', '▬ • • • •'),
                   '7': Flag('Setteseven', 'flags/digits/7.svg', 'Siedem',
                             'Siódemka Warszawska', '▬ ▬ • • •'),
                   '8': Flag('Oktoeight', 'flags/digits/8.svg', 'Osiem',
                             'Osiem czerwonych, bo podwójnie?', '▬ ▬ ▬ • •'),
                   '9': Flag('Novenine', 'flags/digits/9.svg', 'Dziewięć',
                             'Dziewięć 6+7 po barwach - 4 pola', '▬ ▬ ▬ ▬ •')}
    _additionalFlags = [Flag('', 'flags/other/Answer.svg', 'Flaga wywoławcza pytania i odpowiedzi', '', ''),
                        Flag('', 'flags/other/Repeat_One.svg', 'Zastępcza 1', '', ''),
                        Flag('', 'flags/other/Repeat_Two.svg', 'Zastępcza 2', '', ''),
                        Flag('', 'flags/other/Repeat_Three.svg', 'Zastępcza 3', '', '')]
    _allFlags = [FlagMultiple([_characters['A'], _characters['C']], 'Opuszczam mój statek'),
                 FlagMultiple([_characters['A'], _characters['D']],
                              'Opuszczam mój statek, który ucierpiał w wypadku nuklearnym i stanowi potencjalne źródło niebezpieczeństwa promieniowania'),
                 FlagMultiple([_characters['A'], _characters['N']], 'Potrzebuję lekarza'),
                 FlagMultiple([_characters['A'], _characters['N'], _characters['1']],
                              'Potrzebuję lekarza; mam poważne oparzenia'),
                 FlagMultiple([_characters['A'], _characters['N'], _characters['2']],
                              'Potrzebuję lekarza; mam ofiary promieniowania'),
                 FlagMultiple([_characters['E'], _characters['L']], 'Powtórz pozycję niebezpieczeństwa'),
                 FlagMultiple([_characters['E'], _characters['L'], _characters['1']],
                              'Jaką jest pozycja statku w niebezpieczeństwie?'),
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
                 FlagMultiple([_characters['M'], _characters['A'], _additionalFlags[2]],
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
    + list(_characters.values()) + _additionalFlags

    _quotes = []

    @staticmethod
    def get_all_flags():
        """Returns a list of all posible flags.

        :rtype: List[Flag, FlagMultiple]
        """
        flags = copy.deepcopy(Alphabet._allFlags)
        random.shuffle(flags)
        return flags

    @staticmethod
    def get_single_flags_shuffled():
        """Returns a shuffled list of all single flags.

        :rtype: List[Flag]
        """
        flags = copy.deepcopy(list(Alphabet._characters.values()))
        flags.extend(Alphabet._additionalFlags)
        random.shuffle(flags)
        return flags

    @staticmethod
    def get_single_flags():
        """Returns a list of all single flags.

        :rtype: List[Flag]
        """
        flags = copy.deepcopy(list(Alphabet._characters.values()))
        flags.extend(Alphabet._additionalFlags)
        return flags

    @staticmethod
    def get_characters_flags_shuffled():
        """Returns a shuffled list of letter and numeral Flag objects.

        :rtype: List[Flag]
        """
        flags = list(Alphabet._characters.values())
        random.shuffle(flags)
        return flags

    @staticmethod
    def get_flag_sentence_from_api() -> FlagSentence | str:
        """Returns random sentence created from flags, if everything is ok.
        Returs NO_INTERNET_CONNECTION if there is no internet connection.
        Returs REQUEST_LIMIT_EXCEEDED if requests limit has been exceeded.

        :rtype: FlagSentence | str
        """
        sentence = Alphabet._get_random_quote()
        print(sentence)
        match sentence:
            case constants.REQUEST_LIMIT_EXCEEDED | constants.NO_INTERNET_CONNECTION:
                return sentence
            case _:
                cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence).upper().strip()
                flags = Alphabet._translate_sentence_to_flags(cleaned_sentence)
                return FlagSentence(flags, sentence, cleaned_sentence)

    @staticmethod
    def get_sentence_from_file():
        """Returns random sentence from file created from flags, if everything is ok.
        Returs None if there is no file selected, or if there is no sentence.

        :rtype: FlagSentence | None
        """
        if len(Alphabet._quotes) > 0:
            sentence = random.choice(Alphabet._quotes)
            Alphabet._quotes.remove(sentence)
            return sentence
        return None

    @staticmethod
    def load_sentences_from_file():
        """Loads sentences from file.

        :return: True if everything is ok, False if something went wrong, None if user not selected file
        :rtype: bool | Nonez
        """
        Alphabet._quotes = []
        filename = askopenfilename(filetypes=[("Text files", "*.txt")])
        try:
            if not filename:
                return None
            with open(filename, 'r') as file:
                sentences_str = [line.strip() for line in file]
                print(sentences_str)
                for sentence_str in sentences_str:
                    cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence_str).upper().strip()
                    flags = Alphabet._translate_sentence_to_flags(cleaned_sentence)
                    Alphabet._quotes.append(FlagSentence(flags, sentence_str, cleaned_sentence))
            return True
        except Exception:
            return False

    @staticmethod
    def saveFlagSentencePNG(sentence: list[Flag | None], background: str = 'grey'):
        """Saves FlagSentence as PNG file.

        :param sentence: Sentence to save
        :param background: Background color, either 'grey' or 'transparent'
        """

        file_name = ''

        for flag in sentence:
            if flag is None:
                file_name += ' '
            elif isinstance(flag, Flag) and flag.letter == 'Nadazero':
                file_name += '0'
            elif isinstance(flag, Flag) and flag.letter == 'Unaone':
                file_name += '1'
            elif isinstance(flag, Flag) and flag.letter == 'Bissotwo':
                file_name += '2'
            elif isinstance(flag, Flag) and flag.letter == 'Terrathree':
                file_name += '3'
            elif isinstance(flag, Flag) and flag.letter == 'Kartefour':
                file_name += '4'
            elif isinstance(flag, Flag) and flag.letter == 'Pantafive':
                file_name += '5'
            elif isinstance(flag, Flag) and flag.letter == 'Soxisix':
                file_name += '6'
            elif isinstance(flag, Flag) and flag.letter == 'Setteseven':
                file_name += '7'
            elif isinstance(flag, Flag) and flag.letter == 'Oktoeight':
                file_name += '8'
            elif isinstance(flag, Flag) and flag.letter == 'Novenine':
                file_name += '9'
            elif isinstance(flag, Flag) and flag.letter != '':
                file_name += flag.letter[0].upper()
            else:
                file_name += '_'

        cell_width = 200
        cell_height = 200
        x_padding = 10
        y_padding = 10

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=file_name
        )

        if file_path:
            png_files = []

            for flag in sentence:
                if flag is None:
                    png_files.append(None)
                else:
                    png_files.append('graphics/' + flag.png_img_path)

            max_rows = 0
            max_columns = 0

            current_columns = 0
            for png_file in png_files:
                if png_file is not None:
                    current_columns += 1
                    if current_columns > max_columns:
                        max_columns = current_columns
                else:
                    current_columns = 0
                    max_rows += 1

            total_width = max_columns * cell_width + (max_columns - 1) * x_padding
            total_height = (max_rows + 1) * cell_height + max_rows * y_padding

            if background == 'grey':
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

                Alphabet._embed_png(Environment.resource_path(png_file), x, y, cell_width, cell_height, collage,
                                    background)
                x += cell_width + x_padding

            collage.save(file_path, format='PNG')
            return True
        return False

    @staticmethod
    def _embed_png(png_file, x, y, cell_width, cell_height, output_image, background: str):
        """Embeds PNG image in another image."""
        with PILImage.open(png_file) as img:
            img = img.resize((cell_width, cell_height))
            if background == 'grey':
                background_img = PILImage.new('RGBA', (cell_width, cell_height), (128, 128, 128, 255))
                img = img.convert('RGBA')
                ready_flag = PILImage.alpha_composite(background_img, img)
                output_image.paste(ready_flag, (x, y))
            else:
                output_image.paste(img, (x, y))

    @staticmethod
    def _get_random_quote() -> str:
        """Returns a random quote from zenquotes.io if everything is ok.
        Returs NO_INTERNET_CONNECTION if there is no internet connection.
        Returs REQUEST_LIMIT_EXCEEDED if requests limit has been exceeded.

        Function need internet connection to work.

        :rtype: str
        :return: Random quote
        """
        try:
            response = requests.get("https://zenquotes.io/api/quotes")
            if response.status_code == 200:
                quotes = response.json()
                for quote in quotes:
                    try:
                        quote_text = quote['q']
                        if int(quote['c']) <= 50:
                            # return random.choice([x for x in quote_text.split(' ') if len(x) > 2])
                            return f"{quote_text}"
                    except KeyError:
                        return constants.REQUEST_LIMIT_EXCEEDED
                Alphabet._get_random_quote()
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException:
            return constants.NO_INTERNET_CONNECTION

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
            else:
                flags.append(None)
        return flags
