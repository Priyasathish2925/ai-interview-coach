import speech_recognition as sr

def transcribe_audio(file_path: str):
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True

    try:
        with sr.AudioFile(file_path) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source)

        text = r.recognize_google(audio, language="en-IN")
        print("TRANSCRIBED:", text)
        return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""

    except Exception as e:
        print("TRANSCRIBE ERROR:", e)
        return ""
