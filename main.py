import speech_recognition as sr
import pyttsx3
from commands import texts, recommend_commands, hello_commands


def play_speech(text_to_speech):
    """
    Проигрывание ответов
    """
    engine.say(str(text_to_speech))
    engine.runAndWait()


def recognize_audio(*args: tuple):
    """
    Распознавание аудио
    """
    with microphone:
        recognizer.adjust_for_ambient_noise(microphone, duration=0.5)

        try:
            print("Говорите")
            audio = recognizer.listen(microphone)

        except sr.WaitTimeoutError:
            print("Проверьте что микрофон включен")
            return ""

        try:
            print("Идет распознавание...")
            recognized_data = recognizer.recognize_google(
                audio, language="ru"
            ).lower()

        except sr.UnknownValueError:
            return ""

        except sr.RequestError:
            print("Проверьте соединение с интернетом")

        return recognized_data


def hello(hello_text):
    play_speech(hello_text)
    voice_input = recognize_audio()
    print(voice_input)
    execute_hello(voice_input)


def recommend(recommend_text):
    play_speech(recommend_text)
    voice_input = recognize_audio()
    print(voice_input)
    execute_recommend(voice_input)


def hangup(hangup_text):
    play_speech(hangup_text)
    engine.stop()
    quit()


def execute_recommend(command_name):

    for key in recommend_commands.keys():
        if command_name in key:
            command = str(recommend_commands[key]).split("_")
            if command[0] == "recommend":
                recommend(texts[recommend_commands[key]])
            else:
                hangup(texts[recommend_commands[key]])
        else:
            pass


def execute_hello(command_name):

    for key in hello_commands.keys():
        if command_name in key:
            command = str(hello_commands[key]).split("_")
            if command[0] == "hello":
                hello(texts[hello_commands[key]])
            elif command[0] == "recommend":
                recommend(texts[hello_commands[key]])
            else:
                hangup(texts[hello_commands[key]])
        else:
            pass


if __name__ == "__main__":

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    hello_text = ("Добрый день! Вас беспокоит компания X, мы проводим "
                  "опрос удовлетворенности нашими услугами. Подскажите, "
                  "вам удобно сейчас говорить?")

    play_speech(hello_text)

    while True:
        voice_input = recognize_audio()
        print(voice_input)
        execute_hello(voice_input)
