# Retro-Snake-python 🐍

A classic, polished Snake game built with **Python** and the **Pygame** library. This project features custom graphics, immersive sound effects, and a persistent high-score system.

## 🕹️ Game Features
* **Classic Gameplay:** Smooth grid-based movement to collect fruits and grow.
* **Progressive Difficulty:** The game gets faster as you eat more fruits (speed increases every 3 fruits).
* **High Score System:** Automatically saves your best score to `highscore.txt` and displays it on the main menu.
* **Dynamic Graphics:** Features rotatable textures for the snake's head and body based on the direction of movement.
* **Audio Experience:** Includes background music, eating sound effects, and special alerts for achieving a new high score or hitting game over.
* **Pause/Resume:** Use the `ENTER` key to pause the action at any time.
* **Verbose Logging:** Built-in console logging for real-time debugging and event tracking.

## 📂 Project Structure
Based on the repository assets, the project is organized as follows:

| File / Folder | Description |
| :--- | :--- |
| `main.py` | The main executable containing the game loop and logic classes. |
| `Map_bg.png` | Background texture for the game arena. |
| `Main_Menu.png` | Visual asset for the starting screen. |
| `Game_Over.png` | Visual asset for the game over screen. |
| `head1.png` / `body1.png` | Graphic assets for the snake's anatomy. |
| `apple.png` / `orange.png` / `cherry.png` | Variety of fruit textures for random spawning. |
| `border.png` | Texture for the arena boundaries. |
| `pause.png` / `play.png` | UI icons for game state feedback. |
| `sound.mp3` | Looping background soundtrack. |
| `eat.mp3` / `high.mp3` / `game_over.mp3` | Context-specific sound effects. |
| `highscore.txt` | Data file for persistent high score storage. |

## 🚀 Installation & Setup

### Prerequisites
Ensure you have Python installed. You can install the required **Pygame** library via pip:

```bash
pip install pygame
```
---
## Running the Game

### 1.Clone the repository:
```Bash
git clone [https://github.com/Sotos007/Retro-Snake-python.git](https://github.co
```
### 2.Navigate to the directory:
```Bash
cd Retro-Snake-python
```
### 3.Launch:
```Bash
python main.py
```
---
## 🎮 Controls
    * **Arrow Keys**: Navigate the Snake.
    * **SPACE**: Start Game / Restart after Game Over.
    * **ENTER**: Pause or Resume the game.
    * **ESC**: Exit the application (available on the Game Over screen).
---
## 🛠️ Technical Overview
The project follows an Object-Oriented Programming (OOP) structure:
    * **Snake Class**: Handles coordinate math, body segment growth, and self-collision.
    * **Fruit Class**: Manages randomized placement and texture selection logic.
    * **Background Class**: Controls UI state transitions and background rendering.
    * **Performance**: Implements pre-loading and surface conversion (.convert_alpha()) for optimal frame rates.






