const express = require('express');
const bodyParser = require('body-parser');
const ytDlp = require('yt-dlp-exec');
const app = express();

app.use(bodyParser.json());

// CORS Setup to allow requests from frontend
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*'); // Allow all origins
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// Route to fetch available formats from YouTube
app.post('/get_formats', async (req, res) => {
  const url = req.body.url;
  try {
    console.log(`Fetching formats for URL: ${url}`);

    // Fetch video information using yt-dlp
    const info = await ytDlp(url, { dumpSingleJson: true });
    console.log(info); // Log the complete info object for debugging

    // Map formats for the response
    const formats = info.formats.map(f => ({
      format_id: f.format_id,
      ext: f.ext,
      resolution: f.height ? `${f.height}p` : 'audio only',
      size: f.filesize ? `${(f.filesize / (1024 * 1024)).toFixed(2)} MB` : 'Unknown',
    }));

    // Return formats and video title
    res.json({ formats, video_title: info.title });
  } catch (error) {
    console.error('Error fetching formats:', error); // Log the error for debugging
    res.json({ error: 'Failed to fetch formats.' });
  }
});

// Route to download video
app.post('/download', async (req, res) => {
  const url = req.body.url;
  const formatId = req.body.format_id;
  try {
    console.log(`Downloading video from URL: ${url} with format: ${formatId}`);

    // Download the selected format using yt-dlp
    const output = `./downloads/%(title)s.%(ext)s`;
    await ytDlp(url, ['-f', formatId, '-o', output]);

    console.log('Video download started successfully');
    res.json({ success: 'Video download started!' });
  } catch (error) {
    console.error('Error downloading video:', error); // Log the error for debugging
    res.json({ error: 'Failed to download video.' });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
