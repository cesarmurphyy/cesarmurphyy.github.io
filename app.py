import cv2
import numpy as np
from flask import Flask, render_template, flash, request, send_from_directory

# Once you have built your image in Docker you can import OpenCV to use throughout the project.
# import cv2

app = Flask(__name__)
# Change this otherwise the other team might modify your cookies.
app.secret_key = b'COOKIE_MONSTER'


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

# WORKING EXAMPLE
# image = cv2.imread('cards.jpg')
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# highlight = (255, 255, 0)

# min_orange = np.array([16, 100, 100], np.uint8)
# max_orange = np.array([30, 255, 255], np.uint8)

# mask = cv2.inRange(hsv, min_orange, max_orange)

# res = cv2.bitwise_and(image, image, mask=mask)

# contours, hierarchy = cv2.findContours(
#     mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(image, contours, -1, highlight, 10)

# cv2.imwrite('contours.jpg', image)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():

    # Flash messages can be useful say when the user successfuly uploads an image or an error occurs.
    # You can change the type of alert box displayed by changing the second argument according to Bootsrap's alert types:
    # https://getbootstrap.com/docs/4.3/components/alerts/
    flash('Welcome! Please upload the image of your physical board below!', 'success')

    return render_template('upload.html')


@app.route('/send', methods=['POST'])
def send():
    image = request.form['image']
    file_name = find_cards(image)
    return render_template('display.html', filename=file_name)


@app.route('/send/<filename>')
def send_image(filename):
    return send_from_directory('./', filename)


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
