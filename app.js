const express = require('express');
const nunjucks = require('nunjucks');
const app = express();
const port = 5000;

// Once you are in the Docker container you can import opencv with the following line
const cv2 = require('opencv4nodejs');
const blue = new cv2.Vec(255, 0, 0);

let img = cv2.imread('blurred-squares.jpg', cv2.IMREAD_GRAYSCALE);
let threshold = img.threshold(240, 255, cv2.THRESH_BINARY);
let contours = threshold.findContours(cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
const result = img.drawContours(contours, cv2.Vec(0, 0, 0), { thickness: 5 });
cv2.imwrite('threshold.jpg', threshold);
cv2.imwrite('contours.jpg', result);

// Template engine
nunjucks.configure('templates', {
  autoescape: true,
  express: app
});

// Static files
app.use(express.static('.'));

// Routes
app.get('/', (req, res) => {
  res.render('index.html');
});

app.get('/upload', (req, res) => {
  res.render('upload.html');
});

app.get('/check_cv', (req, res) => {
  try {
    // const opencv = require('opencv4nodejs');
    res.render('detail.html', {
      heading: 'OpenCV is installed!',
      content: 'try something else'
    });
  } catch (ex) {
    res.render('detail.html', {
      heading: 'OpenCV is NOT installed!',
      content:
        'If you are seeing this message it means you have not correctly spun up your Docker container.<br>Refer to the instructions in the <a href="https://github.com/blakelockley/pace-2019-s1" target="_blank">README</a> file for more details.'
    });
  }
});

// Start app
app.listen(port, () => console.log(`Listening on port ${port}!`));
