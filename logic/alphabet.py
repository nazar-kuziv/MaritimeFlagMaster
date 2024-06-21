import copy, re, random, requests

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
                             'Mam nurka pod wodą; trzymajcie się z dala i idźcie powoli', "Anioł bo biało niebieski",
                             "· ▬"),
                   'B': Flag('Bravo', 'flags/letters/Bravo.svg',
                             '"Ładuję" albo "wyładowuję" albo "mam na statku ładunki niebezpieczne"',
                             "Bolszewik bo czerwony",
                             "▬ · · ·"),
                   'C': Flag('Charlie', 'flags/letters/Charlie.svg',
                             '"Tak"(potwierdzenie) albo "znaczenie poprzedzającej grupy powinno być zrozumiane w trybie twierdzącym"',
                             'Ciastko tortowe', '▬ · ▬ ·'),
                   'D': Flag('Delta', 'flags/letters/Delta.svg',
                             'Trzymajcie się z dala ode mnie; manewruję z trudnością',
                             'Dunaj, rzeka a na brzegach plaże',
                             '▬ · ·'),
                   'E': Flag('Echo', 'flags/letters/Echo.svg', 'Zmieniam swój kurs w prawo',
                             'Ewa niebieskie oczy czerwone usta', '·'),
                   'F': Flag('Foxtrot', 'flags/letters/Foxtrot.svg',
                             'Jestem niezdolny do ruchu; nawiążcie łączność ze mną', 'Fikuśny kwadrat', '· · ▬ ·'),
                   'G': Flag('Golf', 'flags/letters/Golf.svg',
                             '"Potrzebuję pilota"; statki rybackie łowiące blisko siebie na łowiskach oznacza: "wybieram sieci"',
                             'Gówno za płotem', '▬ ▬ ·'),
                   'H': Flag('Hotel', 'flags/letters/Hotel.svg', 'Mam pilota na statku',
                             'Halina polska dziewczyna', '· · · ·'),
                   'I': Flag('India', 'flags/letters/India.svg',
                             'Zmieniam swój kurs w lewo', 'Igła lub Ippon(Japonia)', '· ·'),
                   'J': Flag('Juliett', 'flags/letters/Juliett.svg',
                             'Mam pożar i niebezpieczny ładunek na statku, trzymajcie sie z dala ode mnie',
                             'Jastarnia - półwysep a z obu stron woda', '· ▬ ▬ ▬'),
                   'K': Flag('Kilo', 'flags/letters/Kilo.svg',
                             'Pragne nawiązać z wami łączność', 'Kołobrzeg, plaża i morze', '▬ · ▬'),
                   'L': Flag('Lima', 'flags/letters/Lima.svg',
                             'Zatrzymajcie natychmiast wasz statek',
                             'Lotnik (szachownica, ale nie białoczerwona)', '· ▬ ▬ ▬'),
                   'M': Flag('Mike', 'flags/letters/Mike.svg',
                             'Zatrzymałem mój statek i nie posuwam się po wodzie', 'Miecze', '▬ ▬'),
                   'N': Flag('November', 'flags/letters/November.svg',
                             '"Nie"(zaprzeczenie) albo "znaczenie poprzedzającej grupy powinno być zrozumiane w trybie przeczącym"',
                             'Nie gram w szachy', '▬ ·'),
                   'O': Flag('Oscar', 'flags/letters/Oscar.svg',
                             'Człowiek za burtą', 'Ogień na dachu', '▬ ▬ ▬'),
                   'P': Flag('Papa', 'flags/letters/Papa.svg',
                             'W porcie: "zameldować się na statku (wychodzimy w morze)"; na morzu: "moje sieci zaczepiły się"',
                             'Port', '· ▬ ▬ ·'),
                   'Q': Flag('Quebec', 'flags/letters/Quebec.svg',
                             'Mój statek jest zdrowy i proszę o prawo zdolności ruchów', 'Qrczak cały żółty',
                             '▬ ▬ · ▬'),
                   'R': Flag('Romeo', 'flags/letters/Romeo.svg',
                             'Brak znaczenia pojedynczej litery', 'Rycerz(„Złoty Krzyżak”)', '· ▬ ·'),
                   'S': Flag('Sierra', 'flags/letters/Sierra.svg',
                             'Moje maszyny pracują wstecz', 'Sadzawka, Studnia', '· · ·'),
                   'T': Flag('Tango', 'flags/letters/Tango.svg',
                             'Trzymajcie się z dala ode mnie; jestem zajęty trałowaniem we dwójkę',
                             'Tuluza miasto we Francji', '▬'),
                   'U': Flag('Uniform', 'flags/letters/Uniform.svg',
                             'Kierujecie się ku niebezpieczeństwu', 'U lotnika', '· · ▬'),
                   'V': Flag('Victor', 'flags/letters/Victor.svg',
                             'Potrzebuję pomocy', 'V', '· · · ▬'),
                   'W': Flag('Whiskey', 'flags/letters/Whiskey.svg',
                             'Potrzebuje pomocy lekarskiej', 'Wojna w porcie', '· ▬ ▬'),
                   'X': Flag('X-ray', 'flags/letters/X-ray.svg',
                             'Wstrzymajcie się z wykonywaniem wszystkich zamierzeń i uważajcie na moje sygnały',
                             'Xsiądz',
                             '▬ · · ▬'),
                   'Y': Flag('Yankee', 'flags/letters/Yankee.svg',
                             '"Wlokę moją kotwicę" albo „Wiozę pocztę”', 'Yayecznica', '▬ · ▬ ▬'),
                   'Z': Flag('Zulu', 'flags/letters/Zulu.svg',
                             '"Potrzebuję holownika" lub "wydaję sieci" nadany przez statki rybackie na łowiskach',
                             'Zlepek kolorów', '▬ ▬ · ·'),
                   '0': Flag('Nadazero', 'flags/digits/0.svg', 'Zero',
                             'Zero w Yayecznicy (bo wpadło...)', '▬ ▬ ▬ ▬ ▬'),
                   '1': Flag('Unaone', 'flags/digits/1.svg', 'One', 'Jeden Japoniec',
                             '· ▬ ▬ ▬ ▬'),
                   '2': Flag('Bissotwo', 'flags/digits/2.svg', 'Two', 'Dwa (bo nie Japoniec?)',
                             '· · ▬ ▬ ▬'),
                   '3': Flag('Terrathree', 'flags/digits/3.svg', 'Three',
                             'Tróbarwna Francuska(Tuluza)', '· · · ▬ ▬'),
                   '4': Flag('Kartefour', 'flags/digits/4.svg', 'Four',
                             'Cztery białe ramiona (krzyża)', '· · · · ▬'),
                   '5': Flag('Pantafive', 'flags/digits/5.svg', 'Five', 'Piątka w Kołobrzegu',
                             '· · · · ·'),
                   '6': Flag('Soxisix', 'flags/digits/6.svg', 'Six',
                             'Sześciu Murzynów na sniegu', '▬ · · · ·'),
                   '7': Flag('Setteseven', 'flags/digits/7.svg', 'Seven', 'Siódemka Warszawska', '▬ ▬ · · ·'),
                   '8': Flag('Oktoeight', 'flags/digits/8.svg', 'Eight',
                             'Osiem czerwonych, bo podwójnie?', '▬ ▬ ▬ · ·'),
                   '9': Flag('Novenine', 'flags/digits/9.svg', 'Nine', 'Dziewięć 6+7 po barwach - 4 pola', '▬ ▬ ▬ ▬ ·')}
    _allFlags = [Flag('', 'flags/other/Answer.svg', 'Flaga wywoławcza pytania i odpowiedzi', '', ''),
                 Flag('', 'flags/other/Repeat_One.svg', 'Zastępcza 1', '', ''),
                 Flag('', 'flags/other/Repeat_Two.svg', 'Zastępcza 2', '', ''),
                 Flag('', 'flags/other/Repeat_Three.svg', 'Zastępcza 3', '', ''),
                 FlagMultiple([_characters['A'], _characters['C']], 'Opuszczam moje jednostkę pływającą'),
                 FlagMultiple([_characters['A'], _characters['D']],
                              'Opuszczam mój statek, który ucierpiał w wypadku nuklearnym i stanowi potencjalne źródło niebezpieczeństwa promieniowania'),
                 FlagMultiple([_characters['A'], _characters['N']], 'Potrzebuję lekarza'),
                 FlagMultiple([_characters['A'], _characters['N'], _characters['1']],
                              'Potrzebuję lekarza; mam poważne oparzenia'),
                 FlagMultiple([_characters['A'], _characters['N'], _characters['2']],
                              'Potrzebuję lekarza; mam ofiary promieniowania'),
                 FlagMultiple([_characters['E'], _characters['L']], 'Powtórz pozycję wzywania pomocy'),
                 FlagMultiple([_characters['E'], _characters['L'], _characters['1']],
                              'Jaką pozycję zajmuje statek w opałach?'),
                 FlagMultiple([_characters['G'], _characters['M']], 'Nie mogę uratować mojego statku'),
                 FlagMultiple([_characters['G'], _characters['N']], 'Powinieneś zabrać osoby z pokładu'),
                 FlagMultiple([_characters['G'], _characters['N'], _characters['1']],
                              'Życzę sobie, aby niektóre osoby zostały zabrane. Na pokładzie pozostanie załoga zredukowana do minimum'),
                 FlagMultiple([_characters['G'], _characters['N'], _characters['2']], 'Zabiorę ludzi z pokładu'),
                 FlagMultiple([_characters['G'], _characters['N'], _characters['3']],
                              'Czy możesz zabrać ludzi z pokładu?'),
                 FlagMultiple([_characters['I'], _characters['T']], 'Płonę'),
                 FlagMultiple([_characters['J'], _characters['A']], 'Potrzebuję urządzeń przeciwpożarowych'),
                 FlagMultiple([_characters['J'], _characters['A'], _characters['4']],
                              'Potrzebuję materiału do pianowych gaśnic'),
                 FlagMultiple([_characters['M'], _characters['A'], _characters['A']], 'Proszę o pilną poradę medyczną'),
                 FlagMultiple([_characters['M'], _characters['A'], _characters['B']],
                              'Proszę o zorganizowanie spotkania w wskazanej pozycji'),
                 FlagMultiple([_characters['M'], _characters['A'], _characters['C']],
                              'Proszę o zorganizowanie przyjęcia do szpitala'),
                 FlagMultiple([_characters['M'], _characters['A'], _characters['D']],
                              'Jestem oddalony o (wskazana liczba) godzin od najbliższego portu'),
                 FlagMultiple([_characters['M'], _characters['S'], _characters['1']],
                              'Mój statek stanowi niebezpieczne źródło promieniowania; możesz zbliżyć się od mojej prawej burty'),
                 FlagMultiple([_characters['V'], _characters['G']],
                              '„Zakrycie niskich chmur wynosi... (liczba ósemek lub óctantów nieba pokryta)'),
                 FlagMultiple([_characters['U'], _characters['S'], _characters['4']],
                              'Nic nie można zrobić, dopóki pogoda się nie poprawi'),
                 FlagMultiple([_characters['N'], _characters['C']],
                              'Jestem w sytuacji zagrożenia i potrzebuję natychmiastowej pomocy'),
                 FlagMultiple([_characters['R'], _characters['Y']], 'Trzymaj się z dala z wolną prędkością'),
                 FlagMultiple([_characters['A'], _characters['E']], 'Muszę opuścić mój statek'),
                 FlagMultiple([_characters['D'], _characters['X']], 'Tonę')] + list(_characters.values())

    @staticmethod
    def get_all_flags():
        """Returns a list of all posible flags. It is used for flashcards and meaning to flag mode.

        :rtype: List[Flag, FlagMultiple]
        """
        flags = copy.deepcopy(Alphabet._allFlags)
        random.shuffle(flags)
        return flags

    @staticmethod
    def get_flags_for_flag2letter_mode():
        """Returns a list of Flag objects for flag to letter mode.

        :rtype: List[Flag]
        """
        flags = list(Alphabet._characters.values())
        random.shuffle(flags)
        return flags

    @staticmethod
    def get_flag_sentence() -> FlagSentence:
        """Returns random sentence created from flags.

        :rtype: FlagSentence
        """
        sentence = Alphabet._get_random_quote()
        if not sentence:
            raise Exception('Failed to get a quote')
        cleaned_sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence).upper().strip()
        flags = Alphabet._translate_sentence_to_flags(cleaned_sentence)
        return FlagSentence(flags, sentence, cleaned_sentence)

    @staticmethod
    def _get_random_quote() -> str:
        """Returns a random quote from quotable.io.
        Function need internet connection to work.

        :rtype: str
        :return: Random quote
        """
        try:
            response = requests.get('https://api.quotable.io/random?maxLength=50')
            if response.status_code == 200:
                json_data = response.json()
                quote = json_data['content']
                return quote
            else:
                print('Failed to get a quote')
        except requests.exceptions.RequestException as e:
            print('Failed to get a quote:', e)

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
