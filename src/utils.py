def ensure_recordings_directory_exists(directory="recordings"):
    import os

    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_filename(base_name="recording", extension=".wav"):
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"


def list_recordings(directory="recordings"):
    import os

    return [f for f in os.listdir(directory) if f.endswith(".wav")]
