import speech_recognition as sr
import webbrowser
import pyttsx3
import wikipedia
import musiclibrary  # Make sure this file has: music = {"songname": "url"}

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Function to handle commands
def processCommand(command):
    print("Command received:", command)
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif "wikipedia" in command:
        try:
            topic = command.replace("search for", "").replace("on wikipedia", "").replace("wikipedia", "").strip()
            speak(f"Searching Wikipedia for {topic}")
            result = wikipedia.summary(topic, sentences=2)
            print("Wikipedia says:", result)
            speak(result)
        except Exception as e:
            speak("Sorry, I couldn't find anything on Wikipedia.")
            print("Error:", e)

    elif command.startswith("play"):
        try:
            words = command.split()
            if len(words) > 1:
                song = words[1]
                if song in musiclibrary.music:
                    link = musiclibrary.music[song]
                    webbrowser.open(link)
                    speak(f"Playing {song}")
                else:
                    speak(f"I don't have {song} in the music list.")
            else:
                speak("Please specify which song to play.")
        except Exception as e:
            speak("Something went wrong while trying to play music.")
            print("Error:", e)

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I did not understand the command.")

# Main loop
if __name__ == "__main__":
    speak("Initializing Elsa...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=4)

                try:
                    word = recognizer.recognize_google(audio)
                    print("Heard:", word)
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                    continue

            if word.lower() == "elsa":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for your command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=7, phrase_time_limit=6)

                    try:
                        command = recognizer.recognize_google(audio)
                        print("You said:", command)
                        processCommand(command)
                    except sr.UnknownValueError:
                        speak("Sorry, I did not catch that.")
                    except sr.RequestError as e:
                        speak("Network error.")
                        print("Speech recognition error:", e)

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except Exception as e:
            print(f"An error occurred: {e}")
