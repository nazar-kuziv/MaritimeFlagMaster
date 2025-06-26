import customtkinter as ctk
import webbrowser

githubKuziv = 'github.com/nazar-kuziv'
githubFranzyd = 'github.com/Franzyd'

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(fg_color=('ghost white', 'gray14'), *args, **kwargs)

        self.program = ctk.CTkLabel(self, text='MaritimeFlagMaster, ver. 0.2', fg_color='transparent')
        self.program.pack(anchor="w", padx=8)

        self.authors = ctk.CTkLabel(self, text='Autorzy:', fg_color='transparent', font=ctk.CTkFont(weight='bold'))
        self.authors.pack()

        self.description = ctk.CTkTextbox(self, width=370, height=280, activate_scrollbars=False, wrap="word", fg_color='transparent')
        self.description.pack()
        
        self.description.tag_config('name', foreground="green4")
        self.description.tag_config('link', foreground="blue")
        self.description.tag_bind('link', '<Enter>', lambda x: self.description.configure(cursor='hand2'))
        self.description.tag_bind('link', '<Leave>', lambda x: self.description.configure(cursor=''))
        self.description.tag_bind('gitKuziv', '<1>', lambda x: webbrowser.open_new(f'https://{githubKuziv}'))
        self.description.tag_bind('gitFranzyd', '<1>', lambda x: webbrowser.open_new(f'https://{githubFranzyd}'))

        self.description.insert('end', 'Nazar Kuziv', 'name')
        self.description.insert('end', '\nE-mail:  n.kuziv2005@gmail.com\nGitHub: ')
        self.description.insert('end', githubKuziv, ('link', 'gitKuziv'))
        self.description.insert('end', '\n\nFranciszek Firek', 'name')
        self.description.insert('end', '\nE-mail: firekfrank@gmail.com\nGitHub: ')
        self.description.insert('end', githubFranzyd, ('link', 'gitFranzyd'))

        self.description.insert('end',
                            '\n\nAplikacja MaritimeFlagMaster została stworzona przez pasjonatów programowania i edukacji, Nazara Kuziva i Franciszka Firka. Naszym celem jest umożliwienie użytkownikom efektywnego i przyjemnego przyswajania wiedzy na temat międzynarodowych flag sygnałowych. Jesteśmy otwarci na wszelkie sugestie i uwagi, które mogą pomóc w udoskonaleniu naszej aplikacji. Zachęcamy do kontaktu poprzez e-mail.')

        self.description.configure(state='disabled')

        links = ['www.scribd.com/document/689336702/MKS', 'www.scribd.com/user/708834842/tomczak-s2000',
                 'en.wikipedia.org/wiki/International_Code_of_Signals', r'pl.wikipedia.org/wiki/Kod_Morse%E2%80%99a']

        self.sources = ctk.CTkLabel(self, text='Źródła:', fg_color='transparent', font=ctk.CTkFont(weight='bold'))
        self.sources.pack()

        self.links = ctk.CTkTextbox(self, width=370, height=200, activate_scrollbars=False, wrap="word", fg_color='transparent')
        self.links.pack()

        self.links.tag_config('link', foreground="blue")
        self.links.tag_bind('link', '<Enter>', lambda x: self.links.configure(cursor='hand2'))
        self.links.tag_bind('link', '<Leave>', lambda x: self.links.configure(cursor=''))
        self.links.tag_bind('link0', '<1>', lambda x: webbrowser.open_new(f'https://{links[0]}'))
        for i, l in enumerate(links):
            self.links.tag_bind(f'link{i}', '<1>', lambda x, url=l: webbrowser.open_new(f'https://{url}'))
        
        self.links.insert('end', 'Większość skojarzeń mnemotechnicznych do flag i wszystkie znaczenia do jednoznakowych flag:\n')
        self.links.insert('end', links[0], ('link', 'link0'))
        self.links.insert('end', '\nWgrane przez ')
        self.links.insert('end', 'tomczak.s2000', ('link', 'link1'))
        self.links.insert('end', '\n\nZnaczenia do sygnałów wieloznakowych (przetłumaczone z angielskiego):\n')
        self.links.insert('end', links[2], ('link', 'link2'))
        self.links.insert('end', '\n\nSkojarzenia mnemotechniczne do kodu Morse\'a:\n')
        self.links.insert('end', links[3], ('link', 'link3'))

        self.links.configure(state='disabled')

        self.resizable(False, False)
        self.after(1, self.focus)