const express = require('express');
const bodyParser = require('body-parser');
const ytDlp = require('yt-dlp-exec');
const app = express();

app.use(bodyParser.json());
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*'); // Enable CORS
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// Fetch available formats
app.post('/get_formats', async (req, res) => {
  const url = req.body.url;
  try {
    const info = await ytDlp(url, { dumpSingleJson: true });
    const formats = info.formats.map(f => ({
      format_id: f.format_id,
      ext: f.ext,
      resolution: f.height ? `${f.height}p` : 'audio only',
      size: f.filesize ? `${(f.filesize / (1024 * 1024)).toFixed(2)} MB` : 'Unknown',
    }));
    res.json({ formats, video_title: info.title });
  } catch (error) {
    res.json({ error: 'Failed to fetch formats.' });
  }
});

// Download video
app.post('/download', async (req, res) => {
  const url = req.body.url;
  const formatId = req.body.format_id;
  try {
    const output = `./downloads/%(title)s.%(ext)s`;
    await ytDlp(url, ['-f', formatId, '-o', output]);
    res.json({ success: 'Video download started!' });
  } catch (error) {
    res.json({ error: 'Failed to download video.' });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
