# 🛩️ Mechflight — 2D Side-Scrolling Action Game

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?style=for-the-badge&logo=mysql&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)

**Mechflight** is a full-featured, 2D side-scrolling action-runner game built in Python. It combines real-time sprite animation physics, adaptive Chrome-Dino style difficulty scaling, dual-layer user authentication, and high-score database persistence.

---

## 🌟 Key Features

- **🎮 Smooth Full-Screen Gameplay:** Dynamically adapts to your monitor resolution with responsive UI scaling.
- **⚡ Adaptive Difficulty Scaling:** Gradually accelerates obstacle speed and world scrolling as your score rises, while maintaining true parallax depth proportions.
- **🔐 Dual-Layer Authentication & Persistence:** Single-window Tkinter GUI interface backing local binary storage (pickle) and MySQL database persistence for user scores.
- **💥 Collision Physics & Animations:** Custom AABB hitbox detection with sprite animation state switching (ground walking vs. airborne jetpack flight and explosion VFX).
- **🏗️ Non-Recursive State Machine:** Engineered with an O(1) space complexity state loop that prevents call stack recursion and memory leaks.
- **🚀 Decoupled Render Loop & I/O:** Decouples heavy database network calls from the 60 FPS Pygame render pipeline to eliminate stutters.

---

## 🛠️ Tech Stack

| Component | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.8+ |
| **Engine / Graphics** | Pygame 2.x (pygame.display, pygame.font, pygame.image, pygame.event) |
| **GUI Framework** | Tkinter (Tk, Frame, Label, Button, Entry, messagebox) |
| **Image Processing** | Pillow (PIL.Image, PIL.ImageTk) |
| **Database** | MySQL Server 8.0+ (mysql.connector) |
| **Local Serialization** | Python pickle (binary file LG.dat) |

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.8+** installed
- **MySQL Server** installed and running on localhost (default port 3306)

### 1. Clone Repository
`ash
git clone https://github.com/vishtodev/mechflight.git
cd mechflight
`

### 2. Install Dependencies
`ash
pip install -r requirements.txt
`

### 3. Database Setup (Automatic / Manual)
* The game automatically attempts to connect to MySQL on localhost with user 
oot and password 987654321.
* If the database mechflight does not exist, the game auto-creates the schema and scores table.
* *Note:* If MySQL is unreachable, Mechflight will continue running seamlessly in standalone offline mode.

---

## 🕹️ Controls & How to Play

| Action | Control Key / Mouse |
| :--- | :--- |
| **Fly Upward (Jetpack)** | Hold SPACE |
| **Descend (Gravity)** | Release SPACE |
| **Menu Navigation** | Mouse Click |
| **Return to Home / Quit** | ESC Key |

---

## 📂 Project Structure

`	ext
mechflight/
│
├── main.py                  # Main game engine, auth flow & state machine
├── Script.txt               # Dialogue storyteller script
├── LG.dat                   # Local user credentials (binary)
├── requirements.txt         # Project dependency manifest
├── README.md                # Comprehensive project documentation
├── .gitignore               # Git untracked files specification
│
├── ARCADE.TTF               # Arcade font asset
├── ARCADE_N.TTF             # Arcade digital font asset
├── perfect-dark-brk/        # Perfect Dark font asset package
│
├── back1.jpeg               # Back button icon
├── back6.jpg                # Sky parallax background surface
├── ground.jpg               # Ground surface
├── lgbg.jpg                 # Authentication background surface
├── obstacles.png            # Obstacle sprite
├── profile photo1.png       # User profile avatar asset
├── explosion1.png - 2.png   # Explosion VFX sprite frames
└── sprite1.png - 8.png      # Mech character animation sprite frames
`

---

## 💡 Engineering Highlights & Problem Solving

- **Non-Recursive Scene Controller:** Solved potential call-stack recursion by replacing nested function calls with a top-level procedural state loop that processes scene tokens in O(1) memory.
- **Parallax Ratio Protection:** Developed an algorithm (sky_speed = current_speed * 0.4) that maintains exact visual depth ratios while world velocity dynamically speeds up.
- **Single-Window Tkinter Frame Switching:** Replaced window destruction with frame swapping (place / place_forget) to keep event-loops responsive during login navigation.
- **Hitbox Padding:** Applied 10-pixel inset bounding box calculation ((x+10, y+10, w-20, h-20)) to decouple collision logic from transparent PNG sprite padding.

---

## 📜 License

Distributed under the MIT License. See LICENSE for more information.
