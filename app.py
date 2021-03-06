import cv2
import numpy as np
import os
import requests
from flask import Flask, render_template, flash, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Change this otherwise the other team might modify your cookies.
app.secret_key = b'COOKIE_MONSTER'

# Keys for Trello API
api_key = '6c273a0a3217b9ef9dfab75ad52be718'
api_token = 'db500f0ec127c8035e415d8ef69efca62b9512e37c5a89e960c4c7feed65d07a'
api_secret = '559cdd086e4499cb9005b4a14b0be857f3772546301b3dd46571e088abf6124e'

# Identifiers for EY Sync board
board_id = '5cb3766abef1af32d1d419e7'

# Identifiers for the columns of the board
to_do = '5cb3767871b6b10a8a22f3c5'
in_progress = '5cb3767ca0a82f1361d0c87d'
done = '5cb3767e25a4056a46c12683'

# Identifiers for the cards on the board
test = '5cb3768ebb644455d2494410'
test_two = '5cb4740d12d2f18dd650076c'
test_three = '5cb4743965183c7875c07560'

# API calls to move cards 2 and 3
url = 'https://api.trello.com/1/cards/'+test_two + \
    '/idList?value='+in_progress+'&key='+api_key+'&token='+api_token
url2 = 'https://api.trello.com/1/cards/'+test_three + \
    '/idList?value='+done+'&key='+api_key+'&token='+api_token
# response = requests.request('PUT', url)
# response2 = requests.request('PUT', url2)


# Find orange cards
def find_cards(image):
    image = cv2.imread(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    highlight = (255, 255, 0)

    min_orange = np.array([16, 100, 100], np.uint8)
    max_orange = np.array([30, 255, 255], np.uint8)

    mask = cv2.inRange(hsv, min_orange, max_orange)

    res = cv2.bitwise_and(image, image, mask=mask)

    contours, hierarchy = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(image, contours, -1, highlight, 10)

    cv2.imwrite('contours.jpg', image)

    return 'contours.jpg'


def find_column(image):
    highlight = (255, 255, 0)
    img = cv2.imread(image, 0)
    ret, threshold = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], -1, highlight, 10)

        if len(approx) == 3:
            call = 'https://api.trello.com/1/cards/'+test + \
                '/idList?value='+to_do+'&key='+api_key+'&token='+api_token
            response = requests.request('PUT', call)
        elif len(approx) == 5:
            call = 'https://api.trello.com/1/cards/'+test + \
                '/idList?value='+in_progress+'&key='+api_key+'&token='+api_token
            response = requests.request('PUT', call)
        elif len(approx) == 6:
            call = 'https://api.trello.com/1/cards/'+test + \
                '/idList?value='+done+'&key='+api_key+'&token='+api_token
            response = requests.request('PUT', call)

    # cv2.imwrite('grayscale.jpg', img)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():

    # Flash messages can be useful say when the user successfuly uploads an image or an error occurs.
    # You can change the type of alert box displayed by changing the second argument according to Bootsrap's alert types:
    # https://getbootstrap.com/docs/4.3/components/alerts/

    return render_template('upload.html')

# Handle form submit
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        file = request.files['file']
        name = secure_filename(file.filename)
        file.save(os.path.join('./uploads', name))
        target = os.path.join('./uploads', name)
        find_column(target)
        # image = find_cards(target)
        return render_template('display.html', filename=name)


@app.route('/send/<filename>')
def send_image(filename):
    return send_from_directory('./uploads', filename)


@app.route('/check_cv')
def check_cv():
    try:
        import cv2
    except ModuleNotFoundError:
        return render_template('detail.html', heading="OpenCV is NOT installed!", content="""
                If you are seeing this message it means you have not correctly spun up your Docker container.
                <br>Refer to the instructions in the <a href="https://github.com/blakelockley/pace-2019-s1" target="_blank">README</a> file for more details.
            """)

    return render_template('detail.html', heading="OpenCV is installed!", content="""
            You can use 'import cv2' in your flask app to access OpenCV.
        """)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
