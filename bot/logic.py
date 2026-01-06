from collections import defaultdict
from translate import Translator


class TextAnalysis:
    # Задание №1
    # memory: owner -> list of TextAnalysis objects
    memory = defaultdict(list)

    # Задание №5
    # подготовленные ответы
    qwestions = {
        "как тебя зовут": "Я супер-крутой бот 🤖 и мое предназначение — помогать тебе!",
        "сколько тебе лет": "Это слишком философский вопрос 🤔",
        "что ты умеешь": "Я умею переводить сообщения и немного думать 🧠",
        "привет": "Привет! Рад тебя видеть 👋"
    }

    def __init__(self, text, owner):
        self.text = text
        self.owner = owner

        self.translation = None
        self.response = None

        # Задание №2
        TextAnalysis.memory[owner].append(self)

    def get_translation(self):
        if self.translation is None:
            self.translation = self.__translate(self.text, "ru", "en")
        return self.translation

    def get_answer(self):
        # Задание №6
        text_lower = self.text.lower()

        if text_lower in TextAnalysis.qwestions.keys():
            self.response = TextAnalysis.qwestions[text_lower]
        else:
            self.response = self.__translate(
                "I don't know how to help", "en", "ru"
            )

        return self.response

    def __translate(self, text, from_lang, to_lang):
        try:
            translator = Translator(from_lang=from_lang, to_lang=to_lang)
            return translator.translate(text)
        except Exception:
            return "Перевод не удался"
