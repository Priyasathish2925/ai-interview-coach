from pydub import AudioSegment

def get_audio_duration(file_path: str) -> int:
    audio = AudioSegment.from_file(file_path)
    duration_seconds = len(audio) / 1000
    return round(duration_seconds)
