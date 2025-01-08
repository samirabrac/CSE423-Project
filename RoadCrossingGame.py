from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Game state
game_state = {
    "player": {"x": 5, "y": 200, "lives": 3, "score": 0},
    "cars": [],
    "level": 1,
    "game_over": False,
}

def draw_point(x, y):
    """Draw a single point."""
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

class MidpointAlgorithms:
    @staticmethod
    def draw_line(x0, y0, x1, y1):
        """Midpoint line algorithm."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            draw_point(x0, y0)
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    @staticmethod
    def draw_circle(cx, cy, radius):
        """Midpoint circle algorithm."""
        x = 0
        y = radius
        d = 1 - radius
        MidpointAlgorithms._draw_circle_points(cx, cy, x, y)

        while x < y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            MidpointAlgorithms._draw_circle_points(cx, cy, x, y)

    @staticmethod
    def _draw_circle_points(cx, cy, x, y):
        draw_point(cx + x, cy + y)
        draw_point(cx - x, cy + y)
        draw_point(cx + x, cy - y)
        draw_point(cx - x, cy - y)
        draw_point(cx + y, cy + x)
        draw_point(cx - y, cy + x)
        draw_point(cx + y, cy - x)
        draw_point(cx - y, cy - x)

    @staticmethod
    def draw_rectangle(x0, y0, x1, y1):
        """Draw a rectangle using lines."""
        MidpointAlgorithms.draw_line(x0, y0, x1, y0)
        MidpointAlgorithms.draw_line(x1, y0, x1, y1)
        MidpointAlgorithms.draw_line(x1, y1, x0, y1)
        MidpointAlgorithms.draw_line(x0, y1, x0, y0)

    @staticmethod
    def draw_square(x0, y0, side_length):
        """Draw a square using lines."""
        MidpointAlgorithms.draw_rectangle(x0, y0, x0 + side_length, y0 + side_length)

# Define constants for screen width and number of paths
SCREEN_WIDTH = 500
NUM_PATHS = 10
PATH_WIDTH = (450 - 50) // NUM_PATHS  # Calculate the width of each path

def generate_cars(level):
    """Generate cars for the current level."""
    cars = []
    # Generate cars for each path
    for i in range(NUM_PATHS):
        # Calculate the starting x position for each path
        x = 50 + i * PATH_WIDTH + PATH_WIDTH // 2  # Place cars in the middle of each path
        # Generate a random y position for the car to start from off-screen
        y = random.randint(-500, 0)
        # Add the car to the list with its x, y, speed, and length
        cars.append({
            "x": x,
            "y": y,
            "length": 40,
            "speed": random.randint(2, 4 + level) + 2  # Increase speed by 5
        })
    return cars

def check_collision():
    """Check for collisions between the player and cars."""
    global game_state
    player = game_state["player"]
    for car in game_state["cars"]:
        if car["x"] - 20 <= player["x"] <= car["x"] + 20:
            if car["y"] <= player["y"] <= car["y"] + car["length"]:
                print("Collision Detected!")
                player["lives"] -= 1
                player["y"] = 240  # Reset player Y position to 200 after collision
                player["x"] = 5    # Reset player X position to 5 after collision
                return True
    return False

def show_final_score():
    """Print the final score."""
    print(f"Game Over! Final Score: {game_state['player']['score']}")

def special_key_listener(key, x, y):
    """Handle player movement."""
    global game_state
    player = game_state["player"]

    if not game_state["game_over"]:
        if key == GLUT_KEY_RIGHT:
            player["x"] += 25
            if player["x"] >= SCREEN_WIDTH:  # Player reaches the end
                player["x"] = 50
                player["score"] += 10
                game_state["level"] += 1
                game_state["cars"] = generate_cars(game_state["level"])

        if key == GLUT_KEY_LEFT and player["x"] > 10:
            player["x"] -= 25

        if key == GLUT_KEY_UP and player["y"] < SCREEN_HEIGHT - 10:
            player["y"] += 25

        if key == GLUT_KEY_DOWN and player["y"] > 10:
            player["y"] -= 25

    glutPostRedisplay()

def update():
    """Update the position of cars and check for collisions."""
    global game_state
    if not game_state["game_over"]:
        for car in game_state["cars"]:
            car["y"] += car["speed"]
            if car["y"] > SCREEN_HEIGHT:  # Reset car position when it goes off-screen
                car["y"] = -40

        if check_collision() and game_state["player"]["lives"] == 0:
            game_state["game_over"] = True
            show_final_score()

    glutPostRedisplay()

def draw_path_lines():
    """Draw the vertical lines separating the paths."""
    for i in range(1, NUM_PATHS):
        x = 50 + i * PATH_WIDTH
        MidpointAlgorithms.draw_line(x, 0, x, SCREEN_HEIGHT)  # Drawing vertical lines
    
    # Draw lines at X=50 and X=450 (left and right boundaries)
    MidpointAlgorithms.draw_line(50, 0, 50, SCREEN_HEIGHT)  # Left boundary
    MidpointAlgorithms.draw_line(450, 0, 450, SCREEN_HEIGHT)  # Right boundary

def draw_player():
    """Draw the player as a smaller solid-colored square."""
    player = game_state["player"]
    x, y = player["x"], player["y"]

    # Draw the player as a solid yellow square (25x25)
    glColor3f(1.0, 0.0, 0.0)  # Yellow
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + 25, y)
    glVertex2f(x + 25, y + 25)
    glVertex2f(x, y + 25)
    glEnd()

def draw_screen_boundaries():
    """Fill the left and right parts of the screen with solid white."""
    glColor3f(0.0, 1.0, 1.0)  # White color
    # Left solid white area (x = 0 to x = 50)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(50, 0)
    glVertex2f(50, 470)
    glVertex2f(0, 470)
    glEnd()

    # Right solid white area (x = 450 to x = 500)
    glColor3f(1.0, 0.0, 1.0)  # White color
    glBegin(GL_QUADS)
    glVertex2f(450, 0)
    glVertex2f(500, 0)
    glVertex2f(500, 500)
    glVertex2f(450, 500)
    glEnd()

def draw_replay_button():
    """Draw a replay button as a left arrow in the top-right corner."""
    glColor3f(0.0, 1.0, 0.0)  # Green
    glBegin(GL_TRIANGLES)
    glVertex2f(480, 490)
    glVertex2f(480, 470)
    glVertex2f(460, 480)
    glEnd()

def mouse_listener(button, state, x, y):
    """Handle mouse input for the replay button."""
    global game_state
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert mouse coordinates to OpenGL coordinates
        opengl_x = x
        opengl_y = SCREEN_HEIGHT - y
        
        # Check if the click is within the replay button bounds
        if 460 <= opengl_x <= 480 and 470 <= opengl_y <= 490:
            print("Replay button clicked!")
            # Reset game state
            game_state["player"] = {"x": 5, "y": 200, "lives": 3, "score": 0}
            game_state["level"] = 1
            game_state["game_over"] = False
            game_state["cars"] = generate_cars(game_state["level"])

    glutPostRedisplay()

def draw_scene():
    """Draw the entire game scene."""
    global game_state
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw solid white boundaries
    draw_screen_boundaries()

    # Draw path separator lines
    glColor3f(1.0, 1.0, 1.0)  # White
    draw_path_lines()

    # Draw player
    draw_player()

    # Draw cars
    for car in game_state["cars"]:
        # Draw car body
        glColor3f(0.9, 0.9, 0.8)  # Solid red color
        glBegin(GL_QUADS)
        glVertex2f(car["x"] - 15, car["y"])
        glVertex2f(car["x"] + 15, car["y"])
        glVertex2f(car["x"] + 15, car["y"] + car["length"])
        glVertex2f(car["x"] - 15, car["y"] + car["length"])
        glEnd()

    # Draw replay button
    draw_replay_button()

    # Display score and lives
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10, SCREEN_HEIGHT - 20)
    score_text = f"Score: {game_state['player']['score']} Lives: {game_state['player']['lives']}"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    glutSwapBuffers()

def setup_viewport():
    """Set up the OpenGL viewport."""
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, SCREEN_WIDTH, 0.0, SCREEN_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Initialize game
game_state["cars"] = generate_cars(game_state["level"])

# Initialize OpenGL
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT+50)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow(b"Road Crossing Game")

glutDisplayFunc(draw_scene)
glutIdleFunc(update)
glutSpecialFunc(special_key_listener)
glutMouseFunc(mouse_listener)
setup_viewport()
glutMainLoop()


