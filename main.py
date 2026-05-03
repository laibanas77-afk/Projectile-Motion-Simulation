import pygame
import pygame_gui
import sys
import math

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Lab Simulator - Input Box Version")

manager = pygame_gui.UIManager((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ---------------- LABELS ----------------
label_speed = pygame_gui.elements.UILabel(
    pygame.Rect((50, 495), (200, 20)),
    "Speed (m/s)",
    manager
)

label_angle = pygame_gui.elements.UILabel(
    pygame.Rect((300, 495), (200, 20)),
    "Angle (degrees)",
    manager
)

label_gravity = pygame_gui.elements.UILabel(
    pygame.Rect((550, 495), (200, 20)),
    "Gravity (m/s²)",
    manager
)

# ---------------- INPUT BOXES ----------------
speed_input = pygame_gui.elements.UITextEntryLine(
    pygame.Rect((50, 520), (200, 40)),
    manager
)
speed_input.set_text("60")

angle_input = pygame_gui.elements.UITextEntryLine(
    pygame.Rect((300, 520), (200, 40)),
    manager
)
angle_input.set_text("45")

gravity_input = pygame_gui.elements.UITextEntryLine(
    pygame.Rect((550, 520), (200, 40)),
    manager
)
gravity_input.set_text("9.8")

# START BUTTON
start_button = pygame_gui.elements.UIButton(
    pygame.Rect((800, 520), (150, 40)),
    "START",
    manager
)

# ---------------- FONT ----------------
font = pygame.font.SysFont(None, 28)

# ---------------- PHYSICS ----------------
running = False

x0, y0 = 100, 450
x, y = x0, y0

time = 0
trajectory = []

vx = vy = 0
gravity = 9.8
scale = 5
camera_x = 0

# RESULTS
range_m = 0
max_height_m = 0
time_of_flight = 0

# ---------------- LOOP ----------------
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        manager.process_events(event)

        # START SIMULATION
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:

                try:
                    speed = float(speed_input.get_text())
                    angle = float(angle_input.get_text())
                    gravity = float(gravity_input.get_text())
                except:
                    speed, angle, gravity = 60, 45, 9.8

                angle_rad = math.radians(angle)

                vx = speed * math.cos(angle_rad)
                vy = speed * math.sin(angle_rad)

                x, y = x0, y0
                time = 0
                trajectory.clear()
                running = True

                # THEORY (meters)
                range_m = (speed**2 * math.sin(2 * angle_rad)) / gravity
                max_height_m = (speed**2 * math.sin(angle_rad)**2) / (2 * gravity)
                time_of_flight = (2 * speed * math.sin(angle_rad)) / gravity

    manager.update(dt)

    screen.fill((255, 255, 255))

    # ground
    pygame.draw.line(screen, (0, 0, 0), (0, y0), (WIDTH, y0), 3)

    # ---------------- PHYSICS ----------------
    if running:
        time += dt

        x_m = vx * time
        y_m = vy * time - 0.5 * gravity * time**2

        x = x0 + x_m * scale
        y = y0 - y_m * scale

        trajectory.append((x, y))

        if y_m <= 0:
            running = False

    # ---------------- CAMERA ----------------
    camera_x = x - 300

    # trajectory
    for p in trajectory:
        pygame.draw.circle(
            screen,
            (0, 120, 255),
            (int(p[0] - camera_x), int(p[1])),
            2
        )

    # ball
    pygame.draw.circle(screen, (255, 0, 0), (int(x - camera_x), int(y)), 10)

    # ---------------- OUTPUT ----------------
    result_text = font.render(
        f"Range: {range_m:.2f} m | Height: {max_height_m:.2f} m | Time: {time_of_flight:.2f} s",
        True,
        (0, 0, 0)
    )
    screen.blit(result_text, (50, 10))

    manager.draw_ui(screen)

    pygame.display.update()
