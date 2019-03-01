from flask import Flask, render_template, flash

# Once you have built your image in Docker you can import OpenCV to use throughout the project.
# import cv2

app = Flask(__name__)
app.secret_key = b'COOKIE_MONSTER' # Change this otherwise the other team might modify your cookies.


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():

    # Flash messages can be useful say when the user successfuly uploads an image or an error occurs.
    # You can change the type of alert box displayed by changing the second argument according to Bootsrap's alert types:
    # https://getbootstrap.com/docs/4.3/components/alerts/
    flash('Flashing messages are always useful!', 'success')

    return render_template('upload.html')


@app.route('/check_cv')
def check_cv():
    try: 
        import cv2  
    except ModuleNotFoundError:
        return render_template('detail.html', heading="OpenCV is NOT installed!", content=
            """
                If you are seeing this message it means you have not correctly spun up your Docker container.
                <br>Refer to the instructions in the <a href="https://github.com/blakelockley/pace-2019-s1" target="_blank">README</a> file for more details.
            """)

    return render_template('detail.html', heading="OpenCV is installed!", content=
        """
            You can use 'import cv2' in your flask app to access OpenCV.
        """)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)