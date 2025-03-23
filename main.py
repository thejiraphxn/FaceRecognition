# import cv2
# import face_recognition
# import numpy as np
# import json
# import requests
#
#
#
# known_face_encodings = list()
# known_face_fisrtnames = list()
# known_face_lastnames = list()
# faces_request = requests.get('http://192.168.0.105:3000/execute')
# Alldata = json.loads(faces_request.content)
#
# for data in Alldata:
#     known_face_encodings.append(np.array(json.loads(data["member_face_verification"])['data']))
#     known_face_fisrtnames.append(data["member_firstname"])
#     known_face_lastnames.append(data["member_lastname"])
#
#
#
# # Initialize video capture from webcam
# video_capture = cv2.VideoCapture(0)
#
# while True:
#     # Capture frame-by-frame
#     ret, frame = video_capture.read()
#
#     # Resize frame to improve performance
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#
#     # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
#     rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
#
#     # Find all face locations and encodings in the current frame
#     face_locations = face_recognition.face_locations(rgb_small_frame)
#     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#
#     # Iterate through all faces found in the frame
#     for face_encoding in face_encodings:
#         # Compare face encodings to known faces
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#
#         # If match found, get the corresponding name
#         firstname = "Unknown"
#         lastname = " "
#         if True in matches:
#             first_match_index = matches.index(True)
#             firstname = known_face_fisrtnames[first_match_index]
#             lastname = known_face_lastnames[first_match_index]
#
#             # Draw a rectangle around the face
#             top, right, bottom, left = face_locations[0]
#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#
#             # Draw a label with the name below the face
#             if firstname is not None and lastname is not None:  # Check if name is not None
#                 firstname = str(firstname)  # Ensure name is a string
#                 lastname = str(lastname)
#                 name = str(firstname + " " + lastname)
#                 cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)
#         else:
#             top, right, bottom, left = face_locations[0]
#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4
#             cv2.rectangle(frame, (left, top), (right, bottom), ((0, 0, 255)), 2)
#             firstname = str(firstname)  # Ensure name is a string
#             lastname = str(lastname)
#             name = str(firstname + " " + lastname)
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), ((0, 0, 255)), cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)
#
#
#     # Display the resulting image
#     cv2.imshow('Video', frame)
#
#     # Press 'q' to quit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Release video capture
# video_capture.release()
# cv2.destroyAllWindows()
#
#
#



import cv2
import face_recognition
import tkinter as tk
import json
import requests
import numpy as np
from PIL import Image, ImageTk

class IPAddress:
    def __init__(self):
        self.IPAddress = 'http://192.168.0.105:3000'

    def get_ip(self):
        return self.IPAddress


class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceRecognition")

        self.image = Image.open('icon.png')
        self.max_width = 200
        self.max_height = 200

        if self.image.width > self.max_width or self.image.height > self.max_height:
            ratio = min(self.max_width / self.image.width, self.max_height / self.image.height)
            new_width = int(self.image.width * ratio)
            new_height = int(self.image.height * ratio)
            self.image = self.image.resize((new_width, new_height))

        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self.root, image=self.photo)
        self.label.pack()

        self.label = tk.Label(root, text="Select Program:")
        self.label.pack(pady=10)

        self.recognition_button = tk.Button(root, text="Face Recognition", command=self.open_recognition)
        self.recognition_button.pack(pady=5)

        self.capture_button = tk.Button(root, text="Face Registration", command=self.open_capture)
        self.capture_button.pack(pady=5)

    def open_recognition(self):
        self.root.destroy()
        recognition_root = tk.Tk()
        recognition_app = FaceRecognition(recognition_root)
        recognition_root.mainloop()

    def open_capture(self):
        self.root.destroy()
        capture_root = tk.Tk()
        capture_app = FaceCapture(capture_root)
        capture_root.mainloop()

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition")

        self.IPGET = IPAddress()
        self.GET_IPADRESS = self.IPGET.get_ip()
        print(self.IPGET.get_ip())

        # Initialize face recognition
        self.known_face_encodings = []
        self.known_face_fisrtnames = []
        self.known_face_lastnames = []
        self.load_known_faces()

        # Initialize video capture from webcam
        self.video_capture = cv2.VideoCapture(0)

        # Create GUI elements
        self.video_frame = tk.Label(root)
        self.video_frame.pack()

        self.quit_button = tk.Button(root, text="Back", command=self.back_to_home)
        self.quit_button.pack()

        # Start video processing loop
        self.update()

    def load_known_faces(self):
        faces_request = requests.get(self.GET_IPADRESS+'/execute')
        Alldata = json.loads(faces_request.content)

        for data in Alldata:
            self.known_face_encodings.append(np.array(json.loads(data["member_face_verification"])['data']))
            self.known_face_fisrtnames.append(data["member_firstname"])
            self.known_face_lastnames.append(data["member_lastname"])

    def back_to_home(self):
        self.root.destroy()
        home_root = tk.Tk()
        home_root.minsize(500, 500)
        home_app = HomePage(home_root)
        home_root.mainloop()

    def update(self):
        ret, frame = self.video_capture.read()

        if ret:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                firstname = "Unknown"
                lastname = " "

                if True in matches:
                    first_match_index = matches.index(True)
                    firstname = self.known_face_fisrtnames[first_match_index]
                    lastname = self.known_face_lastnames[first_match_index]

                    top, right, bottom, left = face_locations[0]
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    if firstname is not None and lastname is not None:
                        firstname = str(firstname)
                        lastname = str(lastname)
                        name = str(firstname + " " + lastname)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)
                else:
                    top, right, bottom, left = face_locations[0]
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), ((0, 0, 255)), 2)
                    firstname = str(firstname)
                    lastname = str(lastname)
                    name = str(firstname + " " + lastname)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), ((0, 0, 255)), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = img
            self.video_frame.configure(image=img)

        self.root.after(10, self.update)

class FaceCapture:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("Face Registration")

        self.IPGET = IPAddress()
        self.GET_IPADRESS = self.IPGET.get_ip()

        self.known_face_encodings = []
        self.known_face_fisrtnames = []
        self.known_face_lastnames = []
        # self.load_known_faces()

        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        self.capturing = True

        self.video_frame = tk.Label(root)
        self.video_frame.pack()

        self.capture_button = tk.Button(root, text="Capture", command=self.capture_and_print)
        self.capture_button.pack()

        self.quit_button = tk.Button(root, text="Back", command=self.back_to_home)
        self.quit_button.pack()

        self.update()

    def load_known_faces(self):
        faces_request = requests.get(self.GET_IPADRESS+'/execute')
        Alldata = json.loads(faces_request.content)

        for data in Alldata:
            self.known_face_encodings.append(np.array(json.loads(data["member_face_verification"])['data']))
            self.known_face_fisrtnames.append(data["member_firstname"])
            self.known_face_lastnames.append(data["member_lastname"])

    def capture_and_print(self):
        ret, frame = self.cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.load_known_faces()

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        encodings_dict = {f"data": list(enc) for i, enc in enumerate(face_encodings)}
        self.encodings_json = json.dumps(encodings_dict)
        print(self.encodings_json)

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            print(matches)

            if self.encodings_json != "{}" and (not matches or False in matches):

                # Create a Tkinter window for the input form
                self.input_window = tk.Toplevel(self.root)
                self.input_window.geometry("400x400")
                self.input_window.title("User information")

                # Create labels and entry widgets for each field
                tk.Label(self.input_window, text="First Name:").grid(row=0, column=0)
                self.entry_firstname = tk.Entry(self.input_window)
                self.entry_firstname.grid(row=0, column=1)

                tk.Label(self.input_window, text="Last Name:").grid(row=1, column=0)
                self.entry_lastname = tk.Entry(self.input_window)
                self.entry_lastname.grid(row=1, column=1)


                tk.Label(self.input_window, text="Email:").grid(row=2, column=0)
                self.entry_email = tk.Entry(self.input_window)
                self.entry_email.grid(row=2, column=1)

                tk.Label(self.input_window, text="Username:").grid(row=3, column=0)
                self.entry_username = tk.Entry(self.input_window)
                self.entry_username.grid(row=3, column=1)

                # Create a submit button
                submit_button = tk.Button(self.input_window, text="Submit", command=self.on_submit)
                submit_button.grid(row=5, column=0, columnspan=2)

                # Label to display error message
                self.error_label = tk.Label(self.input_window, text="", fg="red")
                self.error_label.grid(row=6, column=0, columnspan=2)

            elif True in matches:
                self.alert_window = tk.Toplevel(self.root)
                self.alert_window.title("Alert")

                # Create labels and entry widgets for each field
                tk.Label(self.alert_window, text="This face has archived !").grid(row=0, column=1)

    def back_to_home(self):
        self.root.destroy()
        home_root = tk.Tk()
        home_root.minsize(500, 500)
        home_app = HomePage(home_root)
        home_root.mainloop()

    def update(self):
        ret, frame = self.cap.read()

        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            img = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = img
            self.video_frame.configure(image=img)

        self.root.after(10, self.update)

    def on_submit(self):
        # Retrieve input values
        firstname = self.entry_firstname.get()
        lastname = self.entry_lastname.get()
        email = self.entry_email.get()
        username = self.entry_username.get()
        verify = self.encodings_json
        print("First Name:", firstname)
        print("Last Name:", lastname)
        print("Email:", email)
        print("Username:", username)
        print("Verify:", verify)
        # Check if any field is empty
        if not all([firstname, lastname, email, username, verify]):
            self.error_label.config(text="All fields are required", fg="red")
            return
        else:
            if(self.send_post_request(firstname, lastname, email, username, verify)):

                self.error_label.config(text="Success", fg="green")
                self.input_window.destroy()
                self.back_to_home()
            else:
                self.error_label.config(text="Try again", fg="red")

    def send_post_request(self, firstname, lastname, email, username, verify):
        # Define the URL endpoint for your API
        url = self.GET_IPADRESS+'/insert'

        # Define the parameters to be sent in the POST request
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'username': username,
            'verify': verify
        }

        # Send the POST request
        response = requests.post(url, data=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Data submitted successfully!")
            return True
        else:
            print("Failed to submit data. Status code:", response.status_code)
            return False

# class FaceCaptureApp:
#     def __init__(self, root, video_source=0):
#         self.root = root
#         self.root.title("Face Registration")
#
#         self.video_source = video_source
#         self.cap = cv2.VideoCapture(self.video_source)
#         self.capturing = True
#
#         self.video_frame = tk.Label(root)
#         self.video_frame.pack()
#
#         self.capture_button = tk.Button(root, text="Capture", command=self.capture_and_print)
#         self.capture_button.pack()
#
#         self.quit_button = tk.Button(root, text="Back to Home Page", command=self.back_to_home)
#         self.quit_button.pack()
#
#         self.update()
#
#     def capture_and_print(self):
#         ret, frame = self.cap.read()
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#         encodings_dict = {f"data": list(enc) for i, enc in enumerate(face_encodings)}
#         self.encodings_json = json.dumps(encodings_dict)
#         print(self.encodings_json)
#
#         if self.encodings_json != "{}":
#
#             # Create a Tkinter window for the input form
#             self.input_window = tk.Toplevel(self.root)
#             self.input_window.title("Input Form")
#
#             # Create labels and entry widgets for each field
#             tk.Label(self.input_window, text="First Name:").grid(row=0, column=0)
#             self.entry_firstname = tk.Entry(self.input_window)
#             self.entry_firstname.grid(row=0, column=1)
#
#             tk.Label(self.input_window, text="Last Name:").grid(row=1, column=0)
#             self.entry_lastname = tk.Entry(self.input_window)
#             self.entry_lastname.grid(row=1, column=1)
#
#             tk.Label(self.input_window, text="Email:").grid(row=2, column=0)
#             self.entry_email = tk.Entry(self.input_window)
#             self.entry_email.grid(row=2, column=1)
#
#             tk.Label(self.input_window, text="Username:").grid(row=3, column=0)
#             self.entry_username = tk.Entry(self.input_window)
#             self.entry_username.grid(row=3, column=1)
#
#             # Create a submit button
#             submit_button = tk.Button(self.input_window, text="Submit", command=self.on_submit)
#             submit_button.grid(row=5, column=0, columnspan=2)
#
#             # Label to display error message
#             self.error_label = tk.Label(self.input_window, text="", fg="red")
#             self.error_label.grid(row=6, column=0, columnspan=2)
#
#     def back_to_home(self):
#         self.root.destroy()
#         home_root = tk.Tk()
#         home_app = HomePage(home_root)
#         home_root.mainloop()
#
#     def update(self):
#         ret, frame = self.cap.read()
#
#         if ret:
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(rgb_frame)
#             img = ImageTk.PhotoImage(image=img)
#             self.video_frame.imgtk = img
#             self.video_frame.configure(image=img)
#
#         self.root.after(10, self.update)
#
#     def on_submit(self):
#         # Retrieve input values
#         firstname = self.entry_firstname.get()
#         lastname = self.entry_lastname.get()
#         email = self.entry_email.get()
#         username = self.entry_username.get()
#         verify = self.encodings_json
#         print("First Name:", firstname)
#         print("Last Name:", lastname)
#         print("Email:", email)
#         print("Username:", username)
#         print("Verify:", verify)
#         # Check if any field is empty
#         if not all([firstname, lastname, email, username, verify]):
#             self.error_label.config(text="All fields are required", fg="red")
#             return
#         else:
#             if(self.send_post_request(firstname, lastname, email, username, verify)):
#
#                 self.error_label.config(text="Success", fg="green")
#                 self.input_window.destroy()
#             else:
#                 self.error_label.config(text="Try again", fg="red")
#
#     def send_post_request(self, firstname, lastname, email, username, verify):
#         # Define the URL endpoint for your API
#         url = 'http://192.168.0.105:3000/insert'
#
#         # Define the parameters to be sent in the POST request
#         data = {
#             'firstname': firstname,
#             'lastname': lastname,
#             'email': email,
#             'username': username,
#             'verify': verify
#         }
#
#         # Send the POST request
#         response = requests.post(url, data=data)
#
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             print("Data submitted successfully!")
#             return True
#         else:
#             print("Failed to submit data. Status code:", response.status_code)
#             return False

# class HomePage:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Home Page")
#
#         self.label = tk.Label(root, text="Select Program:")
#         self.label.pack(pady=10)
#
#         self.recognition_button = tk.Button(root, text="Face Recognition", command=self.open_recognition)
#         self.recognition_button.pack(pady=5)
#
#         self.capture_button = tk.Button(root, text="Face Capture", command=self.open_capture)
#         self.capture_button.pack(pady=5)
#
#     def open_recognition(self):
#         self.root.destroy()
#         recognition_root = tk.Tk()
#         recognition_app = FaceRecognition(recognition_root)
#         recognition_root.mainloop()
#
#     def open_capture(self):
#         self.root.destroy()
#         capture_root = tk.Tk()
#         capture_app = FaceCapture(capture_root)
#         capture_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 500)
    app = HomePage(root)
    root.mainloop()
