import cv2
import os
import streamlit as st
from datetime import datetime
import time
from PIL import Image
#allowing the user to create a folder
def create_user_folder(user_name):
    folder_path = f"./{user_name}"
    if not os.path.exists(folder_path):
        os.makedirs(user_name)
    return folder_path

st.title("  VisionLock app  ")
st.write("### Welcome! Please follow the instructions below to capture your images.")
st.write("""
- **Step 1**: Enter your name in the input box below.
- **Step 2**: Click the button to start capturing your images.
- **Step 3**: After capturing, click "Show Images" to view your pictures.
- **Step 4**: Your images will be saved with your name in a folder created for you.
""")
user_name = st.text_input("Enter the user name ")
# loading the face cascade
# face_cascade = cv2.CascadeClassifier(cv2.data)
# handling the capture image
# Button to start capturing
if st.button('Start Capturing Images'):
    if user_name != "":
        folder_path = create_user_folder(user_name)  # Create a folder with the user's name
        st.write(f"Folder created: {folder_path}")

        # Open the webcam
        cap = cv2.VideoCapture(0)

        # List to store captured images
        captured_images = []

        st.write("### Capture Images!")
        st.write("Press 'q' to stop capturing images.")

        while True:
            ret, frame = cap.read()
            if not ret:
                st.write("Failed to grab frame. Check your webcam.")
                break

            # Convert frame to RGB for displaying in Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Show webcam feed on Streamlit interface
            st.image(frame_rgb, channels="RGB", use_column_width=True)

            # Capture the image when the user presses a key on the webcam
            key = cv2.waitKey(1)
            if key & 0xFF == ord('c'):  # 'c' for capturing images
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(folder_path, f"{user_name}_{timestamp}.jpg")
                cv2.imwrite(image_path, frame)
                captured_images.append(image_path)
                st.write(f"Captured Image: {image_path}")
                time.sleep(1)  # Delay between captures

            elif key & 0xFF == ord('q'):  # 'q' to quit capturing
                break

        # Release the webcam
        cap.release()

        # Button to show captured images
        if st.button('Show Captured Images'):
            if captured_images:
                st.write(f"### Images captured for {user_name}:")
                for img_path in captured_images:
                    img = Image.open(img_path)
                    st.image(img, caption=img_path, use_column_width=True)
            else:
                st.write("No images captured yet.")

        st.write("### All done!")
        st.write(f"Your images are saved in the folder: `{folder_path}`")

    else:
        st.write("Please enter your name before starting.")




