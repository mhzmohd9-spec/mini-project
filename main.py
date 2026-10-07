from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Initialize OpenCV camera
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Mirror frame horizontally for natural user interaction
        frame = cv2.flip(frame, 1)

        # Encode frame to clean JPEG format (No overlays/mesh lines)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translator')
def translator():
    return render_template('translator.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)