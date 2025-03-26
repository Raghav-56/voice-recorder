import simpleaudio as sa
import os


def play_audio(file_path):
    """
    Play an audio file using simpleaudio library

    Args:
        file_path (str): Path to the audio file to play
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    try:
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        return play_obj  # Return the play object if you want to wait later
    except Exception as e:
        print(f"Error playing audio: {e}")
        return None


def wait_for_playback(play_obj):
    """
    Wait for audio playback to complete

    Args:
        play_obj: The play object returned by play_audio
    """
    if play_obj:
        play_obj.wait_done()
