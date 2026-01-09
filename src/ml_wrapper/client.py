class FaceRecognitionClient:
    def __init__(self, model_path="models/face_net.h5"):
        self.model_path = model_path
        # self.model = load_model(model_path)
        pass

    def verify_face(self, captured_img, reference_img):
        """
        Compares two images and returns a match boolean and confidence score.
        This is a mock implementation.
        """
        print("ML Model: Comparing faces...")
        
        # Mock logic
        confidence = 0.95
        threshold = 0.85
        
        return {
            "match": confidence > threshold,
            "confidence": confidence
        }

    def detect_liveness(self, captured_img):
        """
        Checks for liveness (not a photo of a photo).
        """
        return True
