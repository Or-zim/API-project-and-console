import yt_dlp
import sys

def progress_hook(d):
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str')
        if percentage:
            sys.stdout.write(f"\rСкачивание: {percentage}")
            sys.stdout.flush()

    if d['status'] == 'finished':
      print("\nСкачивание завершено.")

def download_audio_from_youtube(video_url, output_path="audio.webm", format='251'):
    ydl_opts = {
        'format': format,
        'outtmpl': output_path,
        'progress_hooks': [progress_hook],
        'socket_timeout': 30 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
        except Exception as e:
            print(f"Ошибка при скачивании: {e}")

if __name__ == "__main__":
    video_url = input("Введите URL видео на YouTube: ")
    output_path = input("Введите путь для сохранения аудио (например, audio.webm): ")
    download_audio_from_youtube(video_url, output_path)
