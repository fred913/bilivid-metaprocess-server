import ffmpeg


def convert_media_to_wav(media_path):
    audio_path = media_path + "_conv.wav"
    ffmpeg.FFmpeg().input(media_path).output(audio_path).execute()
    return audio_path
