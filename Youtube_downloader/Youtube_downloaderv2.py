import yt_dlp # type: ignore
import os

def download_video(url):
    downloads_path = os.path.join(os.path.expanduser("~"), "D:", "Video_Download.%(ext)s")
    ydl_opts = {
        'format': 'best',
        'outtmpl': downloads_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Finished downloading.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    link = input("Enter a link to download: ")
    download_video(link)