from tkinter import *
from tkinter import ttk
import webbrowser

class Translit(Frame):
    """Main Frame widget containing all other widgets"""
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky='nswe')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self['borderwidth'] = 2
        self['relief'] = 'sunken'
        self['bg'] = '#ffde57' #python yellow
        self['pady'] = 20
        self['padx'] = 20

        self.ru_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.ru_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        self.en_lower = ['a', 'b', 'v', 'g', 'd', 'e', 'yo', 'zh', 'z', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'x', 'ts',
            'ch', 'sh', 'shh', '\\', 'y', '\'', 'eh', 'yu', 'ya']
        self.en_upper = ['A', 'B', 'V', 'G', 'D', 'E', 'YO', 'ZH', 'Z', 'I',
                         'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T',
                         'U', 'F', 'X', 'TS', 'CH', 'SH', 'SHH', '|', 'Y',
                         '"', 'EH', 'YU', 'YA']

        #labels inside a frame
        self.ru_labels = []
        self.labelframe = self.create_labelframe()

        #text widget
        self.text = Text(self)
        self.text['wrap'] = 'word'
        self.text.grid(row=3, column=0, pady=24, sticky='n')
        self.text.rowconfigure(3, weight=1)
        self.text.columnconfigure(0, weight=1)
        self.text.focus()
        self.text.bind('<Key>', self.transliterate_letter)
        
        #button widget
        self.google_button = ttk.Button(self)
        self.google_button.grid(row=4, column=0)
        self.google_button['text'] = 'Загуглить'
        self.google_button['width'] = 20
        self.google_button.bind('<ButtonPress>', self.googleit)

    def googleit(self, event):
        """Open default browser. Perform google search on text contents"""
        
        query = '+'.join(self.text.get('1.0', 'end').split())
        google = 'https://www.google.com/'
        webbrowser.open(google+'search?q='+query)
        
   
    def transliterate_letter(self, event):
        """Return an English letter's corresponding Russian letter.
        For the majority of Russian letters there's a single English key.
        Some Russian letters' require a two-key English combination.
        For the latter look back at the previous letter to decide how to
        transliterate it.
        """
        
        single_letters = {'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д',
                          'e': 'е', 'z': 'з', 'i': 'и', 'j': 'й', 'k': 'к',
                          'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
                          'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф',
                          'x': 'х', '\\': 'ъ', 'y': 'ы', "'": 'ь', 'A': 'А',
                          'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е',
                          'Z': 'З', 'I': 'И', 'J': 'Й', 'K': 'К', 'L': 'Л',
                          'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р',
                          'S': 'С', 'T': 'Т', 'U': 'У', 'F': 'Ф', 'X': 'Х',
                          '|': 'Ъ', 'Y': 'Ы', '"': 'Ь'}
        repl = {'h': {'з': 'ж', 'с': 'ш', 'ш': 'щ', 'c': 'ч', 'е': 'э',
                      'З': 'Ж', 'С': 'Ш', 'Ш': 'Щ', 'C': 'Ч', 'Е': 'Э'},
                'H': {'З': 'Ж', 'С': 'Ш', 'Ш': 'Щ', 'C': 'Ч', 'Е': 'Э'},
                'o': {'ы': 'ё', 'Ы': 'Ё'},
                'O': {'Ы': 'Ё'},
                'a': {'ы': 'я', 'Ы': 'Я'},
                'A': {'Ы': 'Я'},
                'u': {'ы': 'ю', 'Ы': 'Ю'},
                'U': {'Ы': 'Ю'},
                's': {'т': 'ц', 'Т': 'Ц'},
                'S': {'Т': 'Ц'}}

        c = event.char
        
        if c in repl:
            start = 'end - 2 chars'
            end = 'end - 1 chars'
            prev = self.text.get(start, end)
            if prev in repl[c]:
                self.text.replace(start, end, repl[c][prev])
                return 'break' #return if replacement occurs

        if c in single_letters: 
            self.text.insert('end', single_letters[c])
            return 'break' #return if replacement occurs

        return c
    

    def create_label(self, master, **kwargs):
        """Create a Label widget under master with specified config options"""
        label = ttk.Label(master)
        for arg in kwargs:
            label[arg] = kwargs[arg]
        return label

    def create_labelframe(self):
        """Create a Frame widget to contain letter Label widgets"""
        font = 'Helvetica 16'
        py_yellow = '#ffde57'
        py_gray = '#646464'
        py_blue = '#4584b6'
        
        labelframe = Frame(self)
        labelframe.grid(row=0, column=0, sticky='n')
        labelframe.rowconfigure(0, weight=1)
        labelframe.columnconfigure(0, weight=1)
        
        options = {'font': font, 'background': py_yellow, 'foreground': py_gray,
                   'padding': '8 0 8 0', 'anchor': 'center'}
        letter_count = len(self.ru_lower)
        
        for i in range(letter_count):
            #1st row: russian letters
            options['text'] = self.ru_lower[i]
            label = self.create_label(labelframe, **options)
            label.grid(row=0, column=i, sticky='ew')
            self.ru_labels.append(label)

            #2nd row: down arrows
            options['text'] = '↓'
            label = self.create_label(labelframe, **options)
            label.grid(row=1, column=i, sticky='ew')
            self.ru_labels.append(label)

            #3rd row: english letters
            options['text'] = self.en_lower[i]
            label = self.create_label(labelframe, **options)
            label.grid(row=2, column=i, sticky='ew')
            self.ru_labels.append(label)

        return labelframe
        
if __name__ == '__main__':
    root = Tk()
    root.resizable(0, 0)
    root.title('Translit → Транслит')
    root.iconbitmap('icon.ico')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    tlit = Translit(root)
    root.mainloop()
