from flask import Flask, render_template, request, send_from_directory, send_file
import os
import yt_dlp
import logging
import re

# Initialize Flask app
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Directory to save downloaded videos
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to clean up YouTube URL (removes query parameters)
def sanitize_youtube_url(url):
    clean_url = re.sub(r"&.*$", "", url)
    clean_url = re.sub(r"\?.*$", "", clean_url)
    logging.info(f"Sanitized URL: {clean_url}")
    return clean_url

@app.route('/')
def index():
    return render_template('index.html')

# Fetch available formats from YouTube
@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form['url']
    clean_url = sanitize_youtube_url(url)
    
    try:
        logging.info(f"Fetching formats for URL: {clean_url}")
        
        # Use yt-dlp to fetch available formats
        ydl_opts = {'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(clean_url, download=False)
            formats = info_dict.get('formats', [])
        
        # Extract the format options (quality and file sizes)
        format_options = [{'format_id': f['format_id'], 'ext': f['ext'], 'resolution': f['resolution'], 'size': f.get('filesize', 'Unknown')} for f in formats if 'resolution' in f]
        return render_template('index.html', formats=format_options, video_title=info_dict['title'], url=clean_url)
    
    except Exception as e:
        logging.error(f"Error fetching formats: {str(e)}")
        return render_template('index.html', error=str(e))

# Download the selected video format
@app.route('/download', methods=['POST'])
def download_video():
    try:
        url = request.form['url']
        format_id = request.form['format_id']
        clean_url = sanitize_youtube_url(url)

        logging.info(f"Downloading video from URL: {clean_url} with format {format_id}")

        # Configure yt-dlp options for downloading the selected format
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        }

        # Download the selected format using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(clean_url)
            video_title = info_dict['title']  # Capture the correct title

        # Construct the correct filename
        filename = f"{video_title}.mp4"
        logging.info(f"Downloaded video successfully: {filename}")
        return render_template('index.html', success=True, video_title=video_title, filename=filename)
    
    except KeyError:
        logging.error("Missing 'format_id' or 'url'. Make sure a format is selected.")
        return render_template('index.html', error="Please select a format before downloading.")
    
    except Exception as e:
        logging.error(f"Error downloading video: {str(e)}")
        return render_template('index.html', error=str(e))

# Serve file for download
@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        logging.info(f"Sending file for download: {filepath}")
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        logging.error(f"Error sending file: {str(e)}")
        return render_template('index.html', error="File not found or could not be downloaded.")

if __name__ == '__main__':
    # Bind Flask app to all network interfaces, making it accessible externally
    app.run(debug=True, host='0.0.0.0', port=2000)
