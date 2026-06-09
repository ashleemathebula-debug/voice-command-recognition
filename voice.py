import datetime
import os
import webbrowser

import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()
recognizer = sr.Recognizer()


def speak(text: str) -> None:
    """Speak a response using the system speech engine."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen_for_command() -> str:
    """Capture one spoken command from the default microphone."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak("Listening for your command...")
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("I could not understand that command.")
        return ""
    except sr.RequestError:
        speak("The speech recognition service is unavailable right now.")
        return ""


def handle_command(command: str) -> None:
    """Execute a known voice command."""
    if command in {"hello", "hi", "hey"}:
        speak("Hello! I am ready for your voice commands.")
        return

    if command in {"time", "what time is it"}:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
        return

    if command in {"date", "what date is it"}:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}.")
        return

    if command in {"open browser", "open google"}:
        webbrowser.open("https://www.google.com")
        speak("Opening your browser now.")
        return

    if command in {"open notepad", "launch notepad"}:
        os.startfile("notepad.exe")
        speak("Opening Notepad.")
        return

    if command in {"stop", "exit", "quit"}:
        speak("Goodbye.")
        raise SystemExit(0)

    speak("That command is not configured yet.")


def main() -> None:
    speak("Voice command recognition is ready.")

    while True:
        try:
            command = listen_for_command()
            if command:
                handle_command(command)
        except KeyboardInterrupt:
            speak("Stopped listening.")
            break


if __name__ == "__main__":
    main()
