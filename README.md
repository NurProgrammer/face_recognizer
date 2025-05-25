# Face Recognition GUI Application

A modern desktop application that provides facial recognition capabilities with an intuitive graphical user interface. The application offers features like face detection, emotion recognition, and age/gender prediction using advanced computer vision techniques.

## Developer Information

- **Name:** Nurtas Kadirbergenuly
- **Email:** s1153458@s.eduhk.hk

## Project Description

This application combines powerful facial recognition technology with a user-friendly interface, making advanced computer vision capabilities accessible to everyday users. Key features include:

- User registration and authentication through facial recognition
- Real-time face detection and recognition
- Emotion detection capabilities
- Age and gender prediction
- Modern, dark-themed UI with purple and yellow accents

## Installation Instructions

### Prerequisites

- Python 3.10 or higher
- Webcam access
- Operating system: Windows/macOS/Linux

### Setup Steps

1. Create a Python virtual environment:

```bash
python -m venv venv_py310
source venv_py310/bin/activate  # On Unix/macOS
# or
.\venv_py310\Scripts\activate  # On Windows
```

2. Install required dependencies:

```bash
pip install opencv-python
pip install tensorflow
pip install numpy
pip install Pillow
```

3. Additional system-specific requirements:

- For macOS users: Camera permissions must be granted to the application
- For Linux users: Ensure OpenCV dependencies are installed

## Running the Application

1. Activate the virtual environment (if not already activated)
2. Run the main application:

```bash
python app-gui.py
```

## Design and Development Process

### UI/UX Design

The application features a modern, dark-themed interface designed for optimal user experience:

- Window size: 800x600 pixels for comfortable viewing
- Color scheme:
  - Primary: Purple (#8E44AD)
  - Secondary: Yellow (#FFC300)
  - Background: Dark (#1A1A1A)
  - Text: Light Gray (#ECF0F1)
- Consistent button styling with hover effects
- Clear typography and spacing for better readability

### Development Methodology

The project follows a modular architecture with separate components for:

- Face detection and recognition
- User interface management
- Data capture and processing
- Model training and classification

### Technical Implementation

- **GUI Framework**: Tkinter for native look and feel
- **Face Recognition**: OpenCV for efficient image processing
- **Deep Learning**: TensorFlow for facial analysis
- **Data Management**: Local storage for user data and trained models

## Technology Stack and Rationale

### Core Technologies

1. **Python**

   - Extensive machine learning and computer vision libraries
   - Cross-platform compatibility
   - Rapid development capabilities

2. **OpenCV**

   - Industry-standard computer vision library
   - Efficient real-time image processing
   - Robust face detection algorithms

3. **TensorFlow**

   - Advanced deep learning capabilities
   - Pre-trained models for facial analysis
   - Efficient model training and inference

4. **Tkinter**
   - Native GUI toolkit
   - Lightweight and fast
   - Built-in Python support

### Unique Approaches

1. **Modular Architecture**

   - Separate modules for different functionalities
   - Easy maintenance and updates
   - Scalable design for future enhancements

2. **Real-time Processing**

   - Efficient frame processing
   - Optimized resource usage
   - Smooth user experience

3. **User-Centric Design**
   - Intuitive interface
   - Clear feedback mechanisms
   - Accessible features

## Future Enhancements

- Multi-face recognition capabilities
- Enhanced emotion detection accuracy
- Additional biometric features
- Cloud storage integration
- Performance optimizations for larger datasets

# Live Demo

```html
https://www.youtube.com/embed/3EBdT-0gvu8
```
