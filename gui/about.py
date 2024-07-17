import customtkinter as ctk
import webbrowser

githubKuziv = 'https://github.com/nazar-kuziv'
githubFranzyd = 'https://github.com/Franzyd'

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(fg_color='ghost white', *args, **kwargs)

        self.program = ctk.CTkLabel(self, text='MaritimeFlagMaster, ver. 0.2', fg_color='transparent')
        self.program.pack(anchor="w", padx=8)

        self.authors = ctk.CTkLabel(self, text='Autorzy:', fg_color='transparent', font=ctk.CTkFont(weight='bold'))
        self.authors.pack()

        self.textbox = ctk.CTkTextbox(self, width=300, height=400, activate_scrollbars=False, wrap="word", fg_color='transparent')
        self.textbox.pack()
        
        self.textbox.tag_config('name', foreground="green4")
        self.textbox.tag_config('link', foreground="blue")
        self.textbox.tag_bind('link', '<Enter>', lambda x: self.textbox.configure(cursor='hand2'))
        self.textbox.tag_bind('link', '<Leave>', lambda x: self.textbox.configure(cursor=''))
        self.textbox.tag_bind('gitKuziv', '<1>', lambda x: webbrowser.open_new(githubKuziv))
        self.textbox.tag_bind('gitFranzyd', '<1>', lambda x: webbrowser.open_new(githubFranzyd))

        self.textbox.insert('end', 'Nazar Kuziv', 'name')
        self.textbox.insert('end', '\nE-mail:  n.kuziv2005@gmail.com\nGitHub: ')
        self.textbox.insert('end', githubKuziv, ('link', 'gitKuziv'))
        self.textbox.insert('end', '\n\nFranciszek Firek', 'name')
        self.textbox.insert('end', '\nE-mail: firekfrank@gmail.com\nGitHub: ')
        self.textbox.insert('end', githubFranzyd, ('link', 'gitFranzyd'))

        self.textbox.insert('end',
                            '\n\nAplikacja MaritimeFlagMaster została stworzona przez pasjonatów programowania i edukacji, Nazara Kuziva i Franciszka Firka. Naszym celem jest umożliwienie użytkownikom efektywnego i przyjemnego przyswajania wiedzy na temat międzynarodowych flag sygnałowych. Jesteśmy otwarci na wszelkie sugestie i uwagi, które mogą pomóc w udoskonaleniu naszej aplikacji. Zachęcamy do kontaktu poprzez e-mail.')

        self.textbox.configure(state='disabled')
        self.resizable(False, False)