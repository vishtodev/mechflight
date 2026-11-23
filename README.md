# Mechflight

A 2D side-scrolling arcade runner built with **Python**, **Pygame**, and **Tkinter**. Pilot a mech through an obstacle-filled course, use the jetpack to stay airborne, and try to beat your high score.

<p align="center">
  <strong>Python · Pygame · Tkinter · MySQL (optional score storage)</strong>
</p>

## Features

- Full-screen, side-scrolling gameplay
- Jetpack-style flight with gravity
- Animated mech sprites and explosion effects
- Increasing difficulty as the run progresses
- Login and registration screens
- Local player data and high-score tracking
- Optional MySQL-backed score persistence; the game can run without a reachable database

## Gameplay

| Action | Control |
| --- | --- |
| Fly upward | Hold <kbd>Space</kbd> |
| Descend | Release <kbd>Space</kbd> |
| Navigate menus | Mouse |
| Exit / return | <kbd>Esc</kbd> |

## Getting started

### Requirements

- Python 3.8 or newer
- pip
- MySQL Server only if you want to use the database score feature

### 1. Clone the project

```bash
git clone https://github.com/vishtodev/mechflight.git
cd mechflight
```

### 2. Create an environment

Windows:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run

```bash
python main.py
```

Run the game from the repository root so that its image, font, and data assets can be found.

## Project layout

```text
mechflight/
├── main.py                 # Game loop, menus, authentication and score logic
├── requirements.txt         # Python dependencies
├── README.md
├── .gitignore
├── Script.txt              # Game text / script
├── ARCADE.TTF              # Arcade font
├── ARCADE_N.TTF            # Alternate arcade font
├── perfect-dark-brk/       # Additional font assets
├── sprite*.png             # Mech animation frames
├── explosion*.png           # Explosion animation frames
├── obstacles.png           # Obstacle artwork
├── back*.jpg / back*.jpeg  # Background and UI artwork
├── ground.jpg              # Ground artwork
└── lgbg.jpg                # Login screen background
```

The game also creates or uses local player data at runtime. Keep personal data and local save files out of version control.

## Dependencies

The project uses:

- [Pygame](https://www.pygame.org/) for rendering, input, and the game loop
- [Pillow](https://python-pillow.org/) for image handling in the Tkinter UI
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) for optional database access
- Tkinter, included with many standard Python installations

## Security note

This repository has historically contained database credentials in source code and uses local pickle-based user data. **Do not use the current authentication or database implementation with real accounts or sensitive information.** Before deploying or sharing a production build:

1. Rotate any database password that has been committed.
2. Move database configuration to environment variables or a local, ignored configuration file.
3. Use a dedicated database account with limited permissions—never a MySQL root account.
4. Replace plaintext password storage with a suitable password-hashing function.
5. Do not load pickle files from untrusted sources.

The project is a learning/demo game and its authentication should not be considered production-secure.

## Contributing

Bug reports and improvements are welcome. Please include clear steps to reproduce gameplay bugs and mention your operating system and Python/Pygame versions.

## License

No license file is currently included. Until a license is added, all rights are reserved by the copyright holder; please do not assume the project is available for reuse.
