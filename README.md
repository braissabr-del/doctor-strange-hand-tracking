#  Doctor Strange — Hand Tracking

A real-time **Computer Vision** project inspired by the visual effects of the Doctor Strange universe.

This application uses hand tracking to position interactive visual effects over the webcam feed, creating an augmented reality experience.

##  Project Overview

The goal of this project is to explore computer vision concepts and human-computer interaction through real-time hand detection and tracking.

##  Technologies

- **Python** — Programming language.
- **OpenCV** — Image and video processing.
- **MediaPipe** — Hand detection and tracking.
- **CVZone** — Computer vision utilities.
- **NumPy** — Image manipulation and numerical operations.

##  Features

- Real-time webcam capture.
- Detection and tracking of up to two hands.
- Hand position tracking.
- Interactive visual effects.
- Green screen removal using Chroma Key.
- Image overlay with alpha transparency.

##  Project Structure

```text
doctor-strange-hand-tracking/
│
├── doctorstrange.py
├── testes_maos.py
├── verificar_video.py
├── hand_landmarker.task
├── requirements.txt
├── .gitignore
└── README.md
```

##  Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/braissabr-del/doctor-strange-hand-tracking.git
```

### 2. Navigate to the project folder

```bash
cd doctor-strange-hand-tracking
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Add the visual effects video

The effects video is not included in this repository. Place the video file in the project folder and make sure its filename matches the one specified in the source code.

### 7. Run the application

```bash
python doctorstrange.py
```

Press `Q` to close the application.

##  Key Learning Areas

- Computer Vision.
- Image and video processing.
- Hand tracking and gesture recognition.
- Alpha channel and image compositing.
- Real-time image processing with Python.

##  Future Improvements

- Improve processing performance and FPS stability.
- Enhance simultaneous two-hand interaction.
- Develop new gesture-based visual effects.
- Explore additional computer vision applications.

##  Author

**Brenda Raíssa Gonçalves Ferreira**

Systems Analysis and Development Student | Google Student Ambassador 2026

[GitHub Profile](https://github.com/braissabr-del)

---

*Educational project developed to explore computer vision and real-time visual interaction.*
