import cv2
import os
from time import time
from PIL import Image
from tkinter import messagebox
from typing import Tuple, Optional


class FaceRecognitionApp:
    """
    A face recognition application that uses OpenCV for real-time face detection
    and recognition with automatic timeout functionality.
    """
    
    def __init__(self, name: str, timeout: int = 5, confidence_threshold: int = 50):
        """
        Initialize the face recognition application.
        
        Args:
            name: Name of the person to recognize
            timeout: Timeout in seconds for the recognition process
            confidence_threshold: Minimum confidence level for positive recognition
        """
        self.name = name
        self.timeout = timeout
        self.confidence_threshold = confidence_threshold
        self.face_cascade_path = './data/haarcascade_frontalface_default.xml'
        self.classifier_path = f"./data/classifiers/{name}_classifier.xml"
        
        # Initialize components
        self.face_cascade = None
        self.recognizer = None
        self.cap = None
        
        # Recognition state
        self.is_recognized = False
        
    def _initialize_components(self) -> bool:
        """
        Initialize OpenCV components for face detection and recognition.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Load face cascade classifier
            if not os.path.exists(self.face_cascade_path):
                print(f"Error: Face cascade file not found at {self.face_cascade_path}")
                return False
                
            self.face_cascade = cv2.CascadeClassifier(self.face_cascade_path)
            
            # Load trained recognizer
            if not os.path.exists(self.classifier_path):
                print(f"Error: Classifier file not found at {self.classifier_path}")
                return False
                
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read(self.classifier_path)
            
            # Initialize camera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open camera")
                return False
                
            return True
            
        except Exception as e:
            print(f"Error initializing components: {e}")
            return False
    
    def _process_face_detection(self, frame, gray_frame):
        """
        Process face detection and recognition on the current frame.
        
        Args:
            frame: Original color frame
            gray_frame: Grayscale version of the frame
            
        Returns:
            Processed frame with annotations
        """
        faces = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        
        for (x, y, w, h) in faces:
            roi_gray = gray_frame[y:y+h, x:x+w]
            face_id, confidence = self.recognizer.predict(roi_gray)
            confidence_percentage = 100 - int(confidence)
            
            if confidence_percentage > self.confidence_threshold:
                self._draw_recognized_face(frame, x, y, w, h)
                self.is_recognized = True
            else:
                self._draw_unknown_face(frame, x, y, w, h)
                self.is_recognized = False
                
        return frame
    
    def _draw_recognized_face(self, frame, x: int, y: int, w: int, h: int):
        """Draw rectangle and text for recognized face."""
        text = f'Recognized: {self.name.upper()}'
        color = (0, 255, 0)  # Green
        font = cv2.FONT_HERSHEY_PLAIN
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, text, (x, y - 4), font, 1, color, 1, cv2.LINE_AA)
    
    def _draw_unknown_face(self, frame, x: int, y: int, w: int, h: int):
        """Draw rectangle and text for unknown face."""
        text = "Unknown Face"
        color = (0, 0, 255)  # Red
        font = cv2.FONT_HERSHEY_PLAIN
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, text, (x, y - 4), font, 1, color, 1, cv2.LINE_AA)
    
    def _show_result_message(self):
        """Show appropriate message based on recognition result."""
        if self.is_recognized:
            messagebox.showinfo('Success', 'You have successfully checked in!')
        else:
            messagebox.showerror('Failed', 'Recognition failed. Please try again.')
    
    def _cleanup(self):
        """Release resources and close windows."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def run(self) -> bool:
        """
        Run the face recognition application.
        
        Returns:
            bool: True if recognition was successful, False otherwise
        """
        # Initialize components
        if not self._initialize_components():
            return False
        
        print(f"Starting face recognition for {self.name}")
        print(f"Timeout: {self.timeout} seconds")
        print("Press 'q' to quit early")
        
        start_time = time()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame from camera")
                    break
                
                # Convert to grayscale for face detection
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Process face detection and recognition
                processed_frame = self._process_face_detection(frame, gray_frame)
                
                # Display the frame
                cv2.imshow("Face Recognition", processed_frame)
                
                # Check for quit key
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    print("Recognition stopped by user")
                    break
                
                # Check timeout
                elapsed_time = time() - start_time
                if elapsed_time >= self.timeout:
                    print(f"Timeout reached after {elapsed_time:.1f} seconds")
                    break
            
            # Show result message
            self._show_result_message()
            
        except KeyboardInterrupt:
            print("\nRecognition interrupted by user")
        except Exception as e:
            print(f"Error during recognition: {e}")
        finally:
            self._cleanup()
        
        return self.is_recognized


def main_app(name: str, timeout: int = 5) -> bool:
    """
    Main function to run face recognition application.
    
    Args:
        name: Name of the person to recognize
        timeout: Timeout in seconds (default: 5)
        
    Returns:
        bool: True if recognition was successful, False otherwise
    """
    app = FaceRecognitionApp(name, timeout)
    return app.run()


# Example usage
if __name__ == "__main__":
    # Replace 'john' with the actual name/identifier
    success = main_app("john", timeout=10)
    print(f"Recognition result: {'Success' if success else 'Failed'}")