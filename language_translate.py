import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import speech_recognition as sr

class LanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")

        self.translator = Translator()
        self.recognizer = sr.Recognizer()

        self.create_widgets()

    def create_widgets(self):
        self.input_label = ttk.Label(self.root, text="Enter text:")
        self.input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.input_text = tk.Text(self.root, height=5, width=40)
        self.input_text.grid(row=1, column=0, padx=10, pady=5)

        self.voice_input_label = ttk.Label(self.root, text="Voice Input:")
        self.voice_input_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.voice_input_text = tk.Text(self.root, height=1, width=40, state="disabled")
        self.voice_input_text.grid(row=3, column=0, padx=10, pady=5)

        self.output_label = ttk.Label(self.root, text="Translated text:")
        self.output_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.output_text = tk.Text(self.root, height=5, width=40, state="disabled")
        self.output_text.grid(row=5, column=0, padx=10, pady=5)

        self.language_label = ttk.Label(self.root, text="Destination Language (ISO 639-1 code):")
        self.language_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.language_entry = ttk.Entry(self.root)
        self.language_entry.grid(row=7, column=0, padx=10, pady=5)

        self.translate_button = ttk.Button(self.root, text="Translate", command=self.translate_text)
        self.translate_button.grid(row=8, column=0, padx=10, pady=5)

        self.voice_start_button = ttk.Button(self.root, text="Start Voice Input", command=self.start_voice_input)
        self.voice_start_button.grid(row=9, column=0, padx=10, pady=5)

        self.voice_stop_button = ttk.Button(self.root, text="Stop Voice Input", command=self.stop_voice_input)
        self.voice_stop_button.grid(row=10, column=0, padx=10, pady=5)

        self.print_voice_button = ttk.Button(self.root, text="Print Voice Matter", command=self.print_voice_matter)
        self.print_voice_button.grid(row=11, column=0, padx=10, pady=5)

    def translate_text(self):
        input_text = self.input_text.get("1.0", "end-1c")
        destination_language = self.language_entry.get()
        
        if destination_language:
            translated_text = self.translator.translate(input_text, dest=destination_language).text
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translated_text)
            self.output_text.config(state="disabled")
        else:
            tk.messagebox.showerror("Error", "Please enter a destination language code.")

    def start_voice_input(self):
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                self.voice_input_text.config(state="normal")
                self.voice_input_text.delete("1.0", "end")
                self.voice_input_text.insert("1.0", text)
                self.voice_input_text.config(state="disabled")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error with the service; {0}".format(e))

    def stop_voice_input(self):
        self.recognizer.energy_threshold = 4000
        self.recognizer.pause_threshold = 0.8
        self.recognizer.stop_listening()

    def print_voice_matter(self):
        text = self.voice_input_text.get("1.0", "end-1c")
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", text)

def main():
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
