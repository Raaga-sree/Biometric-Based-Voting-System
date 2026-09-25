from deepface import DeepFace
import os
import base64

FACE_DIR = "static/faces"


class BiometricAuth:

    def is_face_already_registered(self, temp_path):
        face_folder = FACE_DIR

        for file in os.listdir(face_folder):
            if file.startswith("temp_"):
                continue

            registered_face = os.path.join(face_folder, file)

            try:
                result = DeepFace.verify(
                    img1_path=temp_path,
                    img2_path=registered_face,
                    model_name="VGG-Face",
                    detector_backend="opencv",
                    enforce_detection=False
                )
                print(f"Checking against {file}")
                print("Distance =", result["distance"])

                if result["distance"] < 0.40:
                    print("Duplicate face found!")
                    return True

            except Exception as e:
                print(e)

        return False

    def __init__(self):
        os.makedirs(FACE_DIR, exist_ok=True)

    # ---------------- SAVE FACE ----------------

    def save_face(self, voter_id, face_data):
        if not face_data:
            return False, "Please capture face first"

        image_data = face_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        temp_path = os.path.join(
            FACE_DIR,
            f"temp_{voter_id}.jpg"
        )

        with open(temp_path, "wb") as f:
            f.write(image_bytes)

        #---------------Check Number of Faces -------------
        faces = DeepFace.extract_faces(
            img_path=temp_path,
            detector_backend="opencv",
            enforce_detection=False
        )

        print("Faces detected:", len(faces))

        if len(faces) == 0:
            os.remove(temp_path)
            return False, "No face detected. Please capture your face."

        if len(faces) >1:
            os.remove(temp_path)
            return False, "Multiple faces detected. Please capture only your face."
            

        # Check duplicate
        duplicate = self.is_face_already_registered(temp_path)
        print("Duplicate =", duplicate)

        if duplicate:
            print("Returning duplicate")

            if os.path.exists(temp_path):
                os.remove(temp_path)

            else:
                print("Temp file already deleted")

            return False, "This face is already registered."

        print("Saving new face....")

        #Save permanently
        final_path = os.path.join(
            FACE_DIR,
            f"{voter_id}.jpg"
        )

        os.rename(temp_path, final_path)
        return True, final_path


       

    # ---------------- VERIFY FACE ----------------

    def verify_face(self, voter_id, live_face_data):

        if not live_face_data:
            return False

        temp_path = os.path.join(
            FACE_DIR,
            f"temp_{voter_id}.jpg"
        )

        image_data = live_face_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        with open(temp_path, "wb") as f:
            f.write(image_bytes)

        stored_image = os.path.join(
            FACE_DIR,
            f"{voter_id}.jpg"
        )
        print("Comparing:")
        print("Stored = ", stored_image)
        print("Temp = ",temp_path)

        if not os.path.exists(stored_image):
            return False

        try:

            result = DeepFace.verify(
                img1_path=stored_image,
                img2_path=temp_path,
                enforce_detection=True
            )

            print("DeepFace Result:", result)
            print("Verified = ", result["verified"])
            print("Distance = ", result["distance"])

            os.remove(temp_path)

            if result["distance"] < 0.40:
                return True
            return False


        except Exception as e:
            print("FACE ERROR:", e)

            if os.path.exists(temp_path):
                os.remove(temp_path)

            return False

            