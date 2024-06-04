import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Camera App")

        self.camera = cv2.VideoCapture(0)  # 0 represents the default camera

        # Check if the camera is opened successfully
        if not self.camera.isOpened():
            print("Failed to open camera")
            return

        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        self.capture_button = tk.Button(window, text="Capture Image", command=self.capture_image)
        self.capture_button.pack(pady=10)

        self.retake_button = tk.Button(window, text="Retake Image", command=self.retake_image, state=tk.DISABLED)
        self.retake_button.pack(pady=10)

        self.image_taken = False

        self.video_loop()

    def video_loop(self):
        ret, frame = self.camera.read()

        if ret:
            # Convert the frame from BGR to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create PIL ImageTk object
            image = Image.fromarray(frame_rgb)
            image_tk = ImageTk.PhotoImage(image)

            # Update the canvas with the new image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            self.canvas.image = image_tk  # Store a reference to prevent image object from being garbage collected

        # Repeat the video loop after 15 milliseconds
        self.window.after(15, self.video_loop)

    def capture_image(self):
        ret, frame = self.camera.read()

        if ret:
            # Get the path to the user's "Downloads" directory
            downloads_dir = os.path.expanduser("~/Pictures/Screenshots")

            # Save the captured frame to a file in the "Downloads" directory
            image_path = os.path.join(downloads_dir, "captured_image.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image saved as {image_path}")
            self.image_taken = True

            # Disable the capture button and enable the retake button
            self.capture_button.config(state=tk.DISABLED)
            self.retake_button.config(state=tk.NORMAL)
        else:
            print("Failed to capture image")

    def retake_image(self):
        # Delete the previously captured image file
        image_path = os.path.expanduser("~/Pictures/Screenshots/captured_image.jpg")
        os.remove(image_path)
        print(f"Previous image deleted: {image_path}")

        # Enable the capture button and disable the retake button
        self.capture_button.config(state=tk.NORMAL)
        self.retake_button.config(state=tk.DISABLED)
        self.image_taken = False


# Create the main window
window = tk.Tk()

# Create an instance of the CameraApp
app = CameraApp(window)

# Run the main event loop
window.mainloop()