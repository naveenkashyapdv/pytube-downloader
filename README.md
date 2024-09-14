
# YouTube Video Downloader - Flask Application

This is a Flask web application that allows users to download YouTube videos by entering a YouTube URL and selecting the desired video format.

## Features

- Fetches available video formats from YouTube using `yt-dlp`.
- Allows users to select and download videos in different formats (resolution/size).
- Simple and intuitive interface for downloading videos.
- Deployed using **Heroku** with **Gunicorn** as the WSGI server.

## Requirements

Before running the app, you need to install the required dependencies. You can install them using `pip`:

```bash
pip install -r requirements.txt
```

The required packages include:

- **Flask**: Web framework for Python.
- **yt-dlp**: YouTube downloader library to fetch and download videos.
- **Gunicorn**: WSGI HTTP Server to serve the app in production environments.

## Installation and Setup

1. **Clone the Repository:**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. **Install the Dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the Application Locally:**

To run the application locally, execute the following command:

```bash
python app.py
```

The app will be running locally at `http://127.0.0.1:5000`.

## Deploying to Heroku

### Steps to Deploy

1. **Create a Heroku account** if you don't have one already: [Heroku Sign Up](https://signup.heroku.com/).
2. **Install the Heroku CLI**: [Heroku CLI Installation Guide](https://devcenter.heroku.com/articles/heroku-cli).
3. **Log in to Heroku** from your terminal:

   ```bash
   heroku login
   ```

4. **Create a new Heroku app**:

   ```bash
   heroku create your-app-name
   ```

5. **Push the code to Heroku**:

   ```bash
   git push heroku main
   ```

6. **Open the app in your browser**:

   ```bash
   heroku open
   ```

### Additional Configuration

You need the following files to successfully deploy the app on Heroku:

- **Procfile**: Specifies how to run the app using `gunicorn`.
- **runtime.txt**: (Optional) Specifies the Python version to use on Heroku.
- **requirements.txt**: Lists all the dependencies needed for the app.

### File Descriptions

- **`app.py`**: The main Flask application file.
- **`requirements.txt`**: Lists all Python dependencies.
- **`Procfile`**: Instructs Heroku to run the app using `gunicorn`.
- **`runtime.txt`**: (Optional) Specifies the Python version for the app.
- **`templates/index.html`**: The HTML template for the app interface.

## Technologies Used

- **Flask**: Lightweight Python web framework.
- **yt-dlp**: A YouTube downloader that fetches video formats and downloads videos.
- **Gunicorn**: WSGI server for deploying Python web apps in production.
- **Heroku**: Cloud platform for hosting web applications.

## Screenshots

### Main Page
![Main Page](screenshots/main-page.png)

### Format Selection
![Format Selection](screenshots/format-selection.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **yt-dlp Documentation**: [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Heroku Documentation**: [https://devcenter.heroku.com/](https://devcenter.heroku.com/)

---


