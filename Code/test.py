import pygame as pyg
import random

pyg.init()
screen_width = 800
screen_height = 800
cell_size = 40

screen = pyg.display.set_mode((screen_width, screen_height))
pyg.display.set_caption("Grid learning example")

clock = pyg.time.Clock()

columns = screen_width // cell_size
rows = screen_height // cell_size
print(f"Grid size: {columns} columns x {rows} rows")
cell_size = min(screen_width // columns, screen_height // rows)

grid = [[0 for _ in range(columns)] for _ in range(rows)]


playerPos = [0, 0]  # Player's position in grid coordinates
playerSize = cell_size // 2  # Player size in pixels
def drawPlayer():
    pyg.draw.rect(screen, (175, 0, 150), 
                 (playerPos[0] * cell_size + (cell_size - playerSize) // 2,
                  playerPos[1] * cell_size + (cell_size - playerSize) // 2,
                  playerSize, playerSize))

# render the grid with a white border around each cell
def renderGrid():
    for y in range(rows):
        for x in range(columns):
            color = (0, 0, 0) if grid[y][x] == 0 else (0, 255, 0)
            rect = (x * cell_size, y * cell_size, cell_size, cell_size)
            pyg.draw.rect(screen, color, rect)
            # Draw white border
            pyg.draw.rect(screen, (255, 255, 255), rect, 2)

def inputHandler():
    global playerPos
    keys = pyg.key.get_pressed()
    if keys[pyg.K_LEFT] and playerPos[0] > 0:
        next_pos = [playerPos[0] - 1, playerPos[1]]
        if (next_pos[0], next_pos[1]) not in obstacles:
            playerPos[0] -= 1

    if keys[pyg.K_UP] and playerPos[1] > 0:
        next_pos = [playerPos[0], playerPos[1] - 1]
        if (next_pos[0], next_pos[1]) not in obstacles:
            if not hasattr(inputHandler, "up_pressed") or not inputHandler.up_pressed:
                playerPos[1] -= 1
                inputHandler.up_pressed = True
            else:
                inputHandler.up_pressed = False

    if keys[pyg.K_RIGHT] and playerPos[0] < columns - 1:
        next_pos = [playerPos[0] + 1, playerPos[1]]
        if (next_pos[0], next_pos[1]) not in obstacles:
            if not hasattr(inputHandler, "right_pressed") or not inputHandler.right_pressed:
                playerPos[0] += 1
                inputHandler.right_pressed = True
            else:
                inputHandler.right_pressed = False

    if keys[pyg.K_DOWN] and playerPos[1] < rows - 1:
        next_pos = [playerPos[0], playerPos[1] + 1]
        if (next_pos[0], next_pos[1]) not in obstacles:
            if not hasattr(inputHandler, "down_pressed") or not inputHandler.down_pressed:
                playerPos[1] += 1
                inputHandler.down_pressed = True
            else:
                inputHandler.down_pressed = False


num_obstacles = columns + 10  # You can adjust the number of obstacles
obstacles = set()
random.seed(42)  # For reproducibility
#random number between 0.5 and 2
random.random = random.uniform(0.25, 2.0)  # Random number between 0.5 and 2.0
num_rewards = columns / random.random # Number of rewards to place
rewards = set()
num_penalties = columns / random.random  # Number of penalties to place
penalties = set()
score = 0  # Initialize score

def check_points():
    global score
    pos = tuple(playerPos)
    if pos in rewards:
        rewards.remove(pos)
        score += 1
    elif pos in penalties:
        penalties.remove(pos)
        score -= 1
    

# Place rewards randomly in the grid
while len(penalties) < num_penalties:
    px, py = random.randint(0, columns - 1), random.randint(0, rows - 1)
    if (px, py) != tuple(playerPos) and (px, py) not in obstacles:
        penalties.add((px, py))

while len(rewards) < num_rewards:
    rx, ry = random.randint(0, columns - 1), random.randint(0, rows - 1)
    if (rx, ry) != tuple(playerPos) and (rx, ry) not in obstacles:
        rewards.add((rx, ry))

while len(obstacles) < num_obstacles:
    ox, oy = random.randint(0, columns - 1), random.randint(0, rows - 1)
    if (ox, oy) != tuple(playerPos):
        obstacles.add((ox, oy))

def renderGrid():
    for y in range(rows):
        for x in range(columns):
            color = (0, 0, 0) if grid[y][x] == 0 else (0, 255, 0)
            rect = (x * cell_size, y * cell_size, cell_size, cell_size)
            pyg.draw.rect(screen, color, rect)
            # Draw obstacles
            if (x, y) in penalties:
                pyg.draw.circle(screen, (215, 0, 0), 
                               (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 4)
            elif (x, y) in obstacles:
                pyg.draw.rect(screen, (255, 255, 255), rect)
            # Draw rewards
            elif (x, y) in rewards:
                pyg.draw.circle(screen, (0, 215, 0), 
                               (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 4)
            
            else:
                pyg.draw.rect(screen, color, rect)
            
            #draw the goal in the bottom right corner
            if (x, y) == (columns - 1, rows - 1):
                pyg.draw.rect(screen, (0, 0, 255), rect)
            # Draw white border
            pyg.draw.rect(screen, (255, 255, 255), rect, 1)

def getGridSize():
    font = pyg.font.SysFont(None, 48)
    input_box = pyg.Rect(screen_width // 2 - 100, screen_height // 2 - 32, 200, 64)
    color_inactive = pyg.Color('lightskyblue3')
    color_active = pyg.Color('dodgerblue2')
    color = color_inactive
    active = False
    user_text = ''
    done = False
    while not done:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pyg.KEYDOWN:
                if active:
                    if event.key == pyg.K_RETURN:
                        if user_text.isdigit() and int(user_text) > 1:
                            columns = int(user_text)
                            rows = columns
                            cell_size = min(screen_width // columns, screen_height // rows)
                            grid[:] = [[0 for _ in range(columns)] for _ in range(rows)]
                            pyg.grid_size_selected = True
                            done = True
                        user_text = ''
                    elif event.key == pyg.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        if len(user_text) < 3 and event.unicode.isdigit():
                            user_text += event.unicode
        screen.fill((30, 30, 30))
        txt_surface = font.render(f"Grid size: {user_text}", True, color)
        prompt_surface = font.render("Enter grid size:", True, (255, 255, 255))
        screen.blit(prompt_surface, (screen_width // 2 - prompt_surface.get_width() // 2, screen_height // 2 - 100))
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pyg.draw.rect(screen, color, input_box, 2)
        pyg.display.flip()
        clock.tick(30)

while True:
    # Ask for grid size in the game window before starting the game loop
    if not hasattr(pyg, "grid_size_selected"):
        getGridSize()
        continue  # Skip the rest of the loop until grid size is set

    inputHandler()
    screen.fill((0, 0, 0))
    renderGrid()
    # Add a delay to slow down player movement
    drawPlayer()
    pyg.time.delay(100)  # Delay in milliseconds (adjust as needed)
    check_points()
    pyg.display.set_caption(f"Grid learning example - Score: {score}")
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()
    # Check if player reached the goal (bottom right corner)
    if tuple(playerPos) == (columns - 1, rows - 1):
        font = pyg.font.SysFont(None, 72)
        win_text = font.render(f"You Win! Score: {score}", True, (0, 255, 0))
        screen.fill((0, 0, 0))
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - win_text.get_height() // 2))
        pyg.display.flip()
        pyg.time.wait(3000)  # Show win screen for 3 seconds
        pyg.quit()
        exit()
    pyg.display.flip()
    clock.tick(60)
