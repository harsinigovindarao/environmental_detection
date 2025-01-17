import cv2
import numpy as np
import flask
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from flask import Flask
import winsound





def fire_detection():
    # Initialize variables
    Fire_Reported = 0
    Email_Status = False

    def send_email(subject, body, to_email, app_password, frame):
        email = 'harsinigovindarao24@gmail.com'  # Your email address
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Convert frame to JPEG format for email attachment
        _, frame_encoded = cv2.imencode('.jpg', frame)
        frame_as_bytes = frame_encoded.tobytes()
        image = MIMEImage(frame_as_bytes)
        msg.attach(image)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()

            try:
                server.login(email, app_password)
                server.sendmail(email, to_email, msg.as_string())
                print(f"Email sent to {to_email} successfully.")
                return True
        
            except smtplib.SMTPException as e:
                print(f"SMTP Exception: {e}")
                return False

    video = cv2.VideoCapture(0)  # Index 0 for default webcam, you can change it if you have multiple cameras.

    while True:
        (grabbed, frame) = video.read()
        if not grabbed:
            break

        frame = cv2.resize(frame, (960, 540))

        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        lower = [18, 50, 50]
        upper = [35, 255, 255]
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(hsv, lower, upper)

        output = cv2.bitwise_and(frame, hsv, mask=mask)

        no_red = cv2.countNonZero(mask)

        if int(no_red) > 15000:
            Fire_Reported = Fire_Reported + 1
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Draw boxes around contours
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow("output", output)

        if Fire_Reported >= 1 and not Email_Status:
            # Email details
            subject = "Fire Detected!"
            body = "A fire has been detected. Please take necessary action."
            recipient_email = 'harsinisg.csbs2022@citchennai.net'
            app_password = "oalg cyed nxwl cmee"
            
            # Send email with frame as attachment
            success = send_email(subject, body, recipient_email, app_password, frame)
            if success:
                Email_Status = True
                frequency = 2500  # Set frequency (in Hz)
                duration = 1000  # Set duration (in milliseconds)
                winsound.Beep(frequency, duration)
                

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    video.release()

# Call the function to run fire detection
fire_detection()
# Create a Flask application instance
app = Flask(__name__)

# Define a route and associated function
@app.route('/')
def hello():
    return 'Hello, World!'
    

# Define your main content or functions
def main():
    # Your main content goes here
    print("This is the main content of your Python file.")

# Entry point of your application
if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
