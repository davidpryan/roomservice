const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.use(express.static('public'));

app.get('/images', (req, res) => {
  const imageDir = path.join(__dirname, 'images');

  fs.readdir(imageDir, (err, files) => {
    if (err) {
      console.error('Error reading images directory:', err);
      res.status(500).send('Internal Server Error');
      return;
    }

    const imageFiles = files.filter(file => {
      const extname = path.extname(file).toLowerCase();
      return extname === '.jpg' || extname === '.png' || extname === '.jpeg';
    });

    const imageUrls = imageFiles.map(file => `/images/${file}`);

    res.json(imageUrls);
  });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
