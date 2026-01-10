"""
Face Verification Service using DeepFace
Provides real face comparison functionality for identity verification.
"""

import base64
import io
import os
import tempfile
from dataclasses import dataclass
from typing import Optional, Tuple
from PIL import Image


@dataclass
class VerificationResult:
    """Result of face verification"""
    is_match: bool
    confidence: float
    distance: float
    message: str
    threshold: float


class FaceVerificationService:
    """
    Face verification service using DeepFace for identity checking.
    
    This service compares a captured image against a reference image
    to verify student identity during exam check-in.
    """
    
    def __init__(self, model_name: str = "Facenet512", threshold: float = 0.45):
        """
        Initialize the face verification service.
        
        Args:
            model_name: DeepFace model to use (Facenet512, VGG-Face, Facenet, etc.)
                       Facenet512 is more accurate and robust than VGG-Face
            threshold: Distance threshold for match (lower = stricter)
                      Facenet512 default threshold is around 0.30, we use 0.45 for some tolerance
        """
        self.model_name = model_name
        self.threshold = threshold
        self._deepface = None
        print(f"[FaceVerification] Initialized with model={model_name}, threshold={threshold}")
    
    def _get_deepface(self):
        """Lazy load DeepFace to avoid startup delay"""
        if self._deepface is None:
            from deepface import DeepFace
            self._deepface = DeepFace
            print("[FaceVerification] DeepFace loaded successfully")
        return self._deepface
    
    def _base64_to_temp_file(self, base64_data: str) -> str:
        """
        Convert base64 image data to a temporary file.
        
        Args:
            base64_data: Base64 encoded image (with or without data URI prefix)
            
        Returns:
            Path to temporary file
        """
        # Remove data URI prefix if present
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_data)
        
        # Create temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file.write(image_data)
        temp_file.close()
        
        return temp_file.name
    
    def verify_face(
        self, 
        captured_image_base64: str, 
        reference_image_base64: str
    ) -> VerificationResult:
        """
        Compare captured image with reference image using DeepFace.
        
        Args:
            captured_image_base64: Base64 encoded captured photo (from check-in camera)
            reference_image_base64: Base64 encoded reference photo (from registration)
            
        Returns:
            VerificationResult with match status and confidence
        """
        temp_captured = None
        temp_reference = None
        
        try:
            # Check if images are provided
            if not captured_image_base64 or not reference_image_base64:
                print("[FaceVerification] ERROR: Missing image data")
                return VerificationResult(
                    is_match=False,
                    confidence=0.0,
                    distance=1.0,
                    message="Eksik fotoğraf verisi",
                    threshold=self.threshold
                )
            
            print(f"[FaceVerification] Starting verification...")
            print(f"[FaceVerification] Captured image length: {len(captured_image_base64)}")
            print(f"[FaceVerification] Reference image length: {len(reference_image_base64)}")
            
            # Convert base64 to temp files
            temp_captured = self._base64_to_temp_file(captured_image_base64)
            temp_reference = self._base64_to_temp_file(reference_image_base64)
            
            print(f"[FaceVerification] Temp files created: {temp_captured}, {temp_reference}")
            
            # Get DeepFace
            DeepFace = self._get_deepface()
            
            # Perform verification
            print(f"[FaceVerification] Running verification with model={self.model_name}...")
            result = DeepFace.verify(
                img1_path=temp_captured,
                img2_path=temp_reference,
                model_name=self.model_name,
                enforce_detection=False,  # Don't fail if face detection is uncertain
                detector_backend='opencv'  # Use OpenCV for faster detection
            )
            
            # Extract results
            is_match = result.get("verified", False)
            distance = result.get("distance", 1.0)
            threshold = result.get("threshold", self.threshold)
            
            # Calculate confidence (inverse of distance, normalized)
            # For cosine distance: lower distance = better match
            confidence = max(0.0, min(1.0, 1.0 - distance))
            
            print(f"[FaceVerification] Result: verified={is_match}, distance={distance:.4f}, threshold={threshold:.4f}")
            print(f"[FaceVerification] Confidence: {confidence:.2%}")
            
            message = "Yüz doğrulama başarılı" if is_match else f"Yüz eşleşmedi (mesafe: {distance:.3f}, eşik: {threshold:.3f})"
            
            return VerificationResult(
                is_match=is_match,
                confidence=confidence,
                distance=distance,
                message=message,
                threshold=threshold
            )
            
        except Exception as e:
            import traceback
            print(f"[FaceVerification] ERROR: {str(e)}")
            print(f"[FaceVerification] Traceback: {traceback.format_exc()}")
            return VerificationResult(
                is_match=False,
                confidence=0.0,
                distance=1.0,
                message=f"Doğrulama hatası: {str(e)}",
                threshold=self.threshold
            )
        finally:
            # Clean up temp files
            if temp_captured and os.path.exists(temp_captured):
                try:
                    os.unlink(temp_captured)
                except:
                    pass
            if temp_reference and os.path.exists(temp_reference):
                try:
                    os.unlink(temp_reference)
                except:
                    pass
    
    def detect_face(self, image_base64: str) -> Tuple[bool, str]:
        """
        Check if a face is detected in the image.
        
        Args:
            image_base64: Base64 encoded image
            
        Returns:
            Tuple of (face_detected: bool, message: str)
        """
        temp_file = None
        try:
            temp_file = self._base64_to_temp_file(image_base64)
            DeepFace = self._get_deepface()
            
            # Try to extract face
            faces = DeepFace.extract_faces(
                img_path=temp_file,
                enforce_detection=False
            )
            
            if faces and len(faces) > 0:
                confidence = faces[0].get("confidence", 0)
                if confidence > 0.5:
                    return True, "Yüz tespit edildi"
            
            return False, "Yüz tespit edilemedi"
            
        except Exception as e:
            return False, f"Yüz tespit hatası: {str(e)}"
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass


# Singleton instance
_face_service: Optional[FaceVerificationService] = None


def get_face_service() -> FaceVerificationService:
    """Get the face verification service instance"""
    global _face_service
    if _face_service is None:
        _face_service = FaceVerificationService()
    return _face_service
