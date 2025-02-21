from flask import Flask, render_template, request, send_file, jsonify
from pytubefix import YouTube, Playlist
import os
import zipfile
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    # Check if the URL is a playlist
    if 'playlist' in url:
        playlist = Playlist(url)
        zip_file_path = 'downloads/playlist.zip'

        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # Create a zip file to store all videos
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for video in playlist.videos:
                stream = video.streams.filter(res="720p").first()
                file_path = stream.download(output_path='downloads')
                zipf.write(file_path, os.path.basename(file_path))

        # Return the zip file for download
        response = send_file(zip_file_path, as_attachment=True)

        # Delete the downloads folder after sending the file
        shutil.rmtree('downloads')

        return response

    else:
        # Handle single video download
        yt = YouTube(url)
        stream = yt.streams.filter(res="720p").first()

        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        file_path = stream.download(output_path='downloads')

        response = send_file(file_path, as_attachment=True)

        # Delete the downloads folder after sending the file
        shutil.rmtree('downloads')

        return response

if __name__ == '__main__':
    app.run(debug=True, port=8000)