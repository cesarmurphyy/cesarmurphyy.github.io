const express = require('express')
const nunjucks = require('nunjucks')
const app = express()
const port = 5000

// Once you are in the Docker container you can import opencv with the following line
// const opencv = require('opencv4nodejs');

// Template engine
nunjucks.configure('templates', {
    autoescape: true,
    express: app
});

// Static files
app.use(express.static('.'))

// Routes
app.get('/', (req, res) => {
    res.render('index.html');
});

app.get('/upload', (req, res) => {
    res.render('upload.html');
});

app.get('/check_cv', (req, res) => {
    try {
        const opencv = require('opencv4nodejs');
        res.render('detail.html', {
            'heading': 'OpenCV is installed!',
            'content': "You can use 'const opencv = require('opencv4nodejs');' in your flask app to access OpenCV."
        });
    } catch (ex) {
        res.render('detail.html', {
            'heading': 'OpenCV is NOT installed!',
            'content': 'If you are seeing this message it means you have not correctly spun up your Docker container.<br>Refer to the instructions in the <a href="https://github.com/blakelockley/pace-2019-s1" target="_blank">README</a> file for more details.'
        });
    }
});

app.get('/', (req, res) => {
    res.render('index.html');
});

// Start app
app.listen(port, () => console.log(`Listening on port ${port}!`))