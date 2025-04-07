import os
import openai
import logging
from gi.repository import Gtk

openai.api_key = os.getenv('OPENAI_API_KEY')
engine = os.getenv('OPENAI_ENGINE', "text-davinci-002")

if not openai.api_key:
    raise ValueError("Missing OpenAI API key")

class ChatBotHandler:
    def __init__(self, glade_file, main_window, input_field, display_area):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(self)

        window = self.builder.get_object(main_window)
        window.show_all()

        self.input_field = self.builder.get_object(input_field)
        self.display_area = self.builder.get_object(display_area)

    def chat_gpt3(self, prompt):
        try:
            response = openai.Completion.create(engine=engine, prompt=prompt, max_tokens=150)
            return response.choices[0].text.strip()
        except Exception as e:
            error_message = f"An error occurred: {e}"
            logging.error(error_message)
            return error_message

    def on_send_button_clicked(self, button):
        text = self.input_field.get_text()
        response = self.chat_gpt3(text)
        self.display_area.set_text(response)

    def on_clear_button_clicked(self, button):
        self.input_field.set_text("")
        self.display_area.set_text("")

if __name__ == "__main__":
    handler = ChatBotHandler("your_glade_file.glade", "main_window", "input_field", "display_area")
    Gtk.main()
