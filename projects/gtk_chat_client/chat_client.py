```python
import os
import openai
from gi.repository import Gtk

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("Missing OpenAI API key")

class ChatBotHandler:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("your_glade_file.glade")
        self.builder.connect_signals(self)

        window = self.builder.get_object("main_window")
        window.show_all()

    def chat_gpt3(self, prompt):
        try:
            response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150)
            return response.choices[0].text.strip()
        except Exception as e:
            error_message = f"An error occurred: {e}"
            print(error_message)
            return error_message

    def on_send_button_clicked(self, button):
        input_field = self.builder.get_object("input_field")
        text = input_field.get_text()

        response = self.chat_gpt3(text)

        display_area = self.builder.get_object("display_area")
        display_area.set_text(response)

    def on_clear_button_clicked(self, button):
        input_field = self.builder.get_object("input_field")
        display_area = self.builder.get_object("display_area")
        
        input_field.set_text("")
        display_area.set_text("")

if __name__ == "__main__":
    handler = ChatBotHandler()
    Gtk.main()
```