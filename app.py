from flask import Flask, render_template, request, send_from_directory
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import yt_dlp
import logging
import os

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_FOLDER = BASE_DIR / "downloads"
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def sanitize_youtube_url(url: str) -> str:
    if not url:
        raise ValueError("URL is required.")

    url = url.strip()
    parsed = urlparse(url if urlparse(url).scheme else f"https://{url}")
    hostname = (parsed.hostname or "").lower()

    if hostname == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0]
        if not video_id:
            raise ValueError("Invalid YouTube short URL.")
        return f"https://www.youtube.com/watch?v={video_id}"

    if hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if not video_id:
                raise ValueError("Invalid YouTube watch URL.")
            return f"https://www.youtube.com/watch?v={video_id}"
        if parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
            if not video_id:
                raise ValueError("Invalid YouTube shorts URL.")
            return f"https://www.youtube.com/watch?v={video_id}"

    raise ValueError("Please provide a valid YouTube URL.")


def human_size(size_bytes):
    if not isinstance(size_bytes, (int, float)) or size_bytes <= 0:
        return "Unknown"
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024


def get_video_info(url: str):
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
        return ydl.extract_info(url, download=False)


def build_format_options(info_dict: dict):
    options = []
    seen = set()
    for fmt in info_dict.get("formats", []):
        format_id = fmt.get("format_id")
        if not format_id or fmt.get("vcodec") == "none":
            continue
        ext = fmt.get("ext")
        resolution = fmt.get("resolution") or fmt.get("format_note") or "Unknown"
        size = human_size(fmt.get("filesize") or fmt.get("filesize_approx"))
        key = (format_id, resolution, ext, size)
        if key in seen:
            continue
        seen.add(key)
        options.append({"format_id": format_id, "ext": ext, "resolution": resolution, "size": size})
    return options


def download_selected_format(url: str, format_id: str):
    ydl_opts = {
        "format": format_id,
        "outtmpl": str(app.config["DOWNLOAD_FOLDER"] / "%(title)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return Path(filename).name, info


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get_formats", methods=["POST"])
def get_formats():
    url = request.form.get("url", "").strip()
    if not url:
        return render_template("index.html", error="Please enter a YouTube URL."), 400
    try:
        clean_url = sanitize_youtube_url(url)
        info = get_video_info(clean_url)
        formats = build_format_options(info)
        if not formats:
            return render_template("index.html", error="No downloadable video formats were found.", url=clean_url), 400
        return render_template("index.html", formats=formats, video_title=info.get("title", "Unknown Title"), url=clean_url)
    except Exception as exc:
        logger.exception("Error fetching formats")
        return render_template("index.html", error=f"Error fetching formats: {exc}"), 500


@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url", "").strip()
    format_id = request.form.get("format_id", "").strip()
    if not url or not format_id:
        return render_template("index.html", error="A YouTube URL and format are required."), 400
    try:
        clean_url = sanitize_youtube_url(url)
        filename, info = download_selected_format(clean_url, format_id)
        return render_template("index.html", success=True, video_title=info.get("title", "Unknown Title"), filename=filename, url=clean_url)
    except Exception as exc:
        logger.exception("Error downloading video")
        return render_template("index.html", error=f"Error downloading video: {exc}"), 500


@app.route("/download_file/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "2000")), debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
