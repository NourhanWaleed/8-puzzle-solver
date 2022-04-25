import pygame
import pygame_gui
import algorithm as alg

window_width = 1000
window_height = 800
tile_area_width = 600
tile_area_height = 600
tile_width = tile_area_width/3
tile_height = tile_area_height/3
button_area_width = window_width - tile_area_width
button_width = 200
button_height = 200
button_margin = (button_area_width - button_width) // 2
wait_time = 500
horizontal_center = 300
vertical_center = 300
background_colour = (102, 0, 102)  # purple
tile_colour = (160, 160, 160)      # gray
numbers_colour = (0, 0, 0)         # black
spacing_colour = (255, 255, 255)   # white
font_size = 60

pygame.init()
window = pygame.display.set_mode((window_width, window_height))
font = pygame.font.SysFont('arial', font_size)
button_font = pygame.font.SysFont('arial', font_size // 2)

manager = pygame_gui.UIManager((window_width, window_height))             # can't import pygame_gui
pygame.display.set_caption("8-puzzle solver")
alert_label_event = pygame.USEREVENT + 2


class Tile:

    def __init__(self, number, width, height, index_x, index_y):
        self.number = number
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.index_x = index_x
        self.index_y = index_y

    def tile_stats(self):
        return self.x, self.y, self.width, self.height


# a rect object to store the information for Rects used to create buttons
# with pygame_gui
class ButtonRect:

    def __init__(self, id, ):
        self.Rect = pygame.Rect(
            (window_width - button_area_width + button_margin, id * button_height + 10),  # top,left
            (button_width, button_height))
        self.id = id


def alert_label(message):
    alertLabel.set_text(message)              #error due to not importing pygame_gui
    pygame.time.set_timer(alert_label_event, wait_time)


def newState(state):
    # some random test state
    # state = m.GameState(None, None, m.random_game_state(), 0)
    gameState = alg.Node(None, None, state, 0)
    stateStr = str(gameState)

    # for now for the purpose of initialization, this list will contain some tiles to draw
    initial_tiles_list = []

    # the tile that will be left blank - represented by 0
    # initialized to silence warning
    blankTileLocal = Tile("0", tile_width - 2, tile_height - 2, 0, 0)

    # num is a string
    for i, num in enumerate(stateStr):

        index_x = (i // 3)
        index_y = (i % 3)

        # We need a reference to the blank tile at all times for purpose of swapping
        # and drawing a blank rectangle
        if num != '0':
            # Margins are left around tiles to give the appearance of
            tile = Tile(num, tile_width - 2, tile_height - 2, index_x, index_y)
            tile.x = index_y * tile_width + 1
            tile.y = index_x * tile_height + 1

            initial_tiles_list.append(tile)
        else:
            blankTileLocal.x = index_y * tile_width + 1
            blankTileLocal.y = index_x * tile_height + 1
            blankTileLocal.index_x = index_x
            blankTileLocal.index_y = index_y
            initial_tiles_list.append(blankTileLocal)

    return gameState, initial_tiles_list, blankTileLocal


def validate(state):
    if state.__len__() != 9 or not state.__contains__("0") or not state.__contains__("1") or not state.__contains__(
            "2") or not state.__contains__("3") or not state.__contains__("4") or not state.__contains__(
            "5") or not state.__contains__("6") or not state.__contains__("7") or not state.__contains__("8"):
        alert_label("Invalid Input")
        return
    return state


def updateBoard(direction):
    # saving the indices of blankTile for ease of use in calculating
    # index of tile in the tile list
    i, j = blankTile.index_x, blankTile.index_y
    list_index = 0

    # the tile required in list is different depending on swap direction
    if direction == 'Left':
        list_index = i * 3 + (j - 1)
    elif direction == 'Up':
        list_index = (i - 1) * 3 + j
    elif direction == 'Down':
        list_index = (i + 1) * 3 + j
    elif direction == 'Right':
        list_index = i * 3 + (j + 1)

    target_tile = numbered_tiles_list[list_index]
    blankTile_list_index = i * 3 + j

    # swapping location on board and index. Need to know where the blank tile is
    # at all times
    target_tile.x, blankTile.x = blankTile.x, target_tile.x
    target_tile.y, blankTile.y = blankTile.y, target_tile.y
    target_tile.index_x, blankTile.index_x = blankTile.index_x, target_tile.index_x
    target_tile.index_y, blankTile.index_y = blankTile.index_y, target_tile.index_y

    # swap the blank tile and target tile in the tile list. Not doing so will mess
    # with later swaps as indices are no longer accurate
    numbered_tiles_list[list_index], numbered_tiles_list[blankTile_list_index] \
        = numbered_tiles_list[blankTile_list_index], numbered_tiles_list[list_index]


def swapTiles(mousePosition):
    x, y = mousePosition
    index_y = x // tile_width
    index_x = y // tile_height

    # distance between blank tile and target tile in terms of x and y axis
    distance = abs(blankTile.index_x - index_x) + abs(blankTile.index_y - index_y)

    # there is a valid swap move
    if distance == 1:
        if blankTile.index_y < index_y:  # blank tile will move right
            updateBoard("Right")
        elif blankTile.index_y > index_y:  # blank tile will move left
            updateBoard("Left")
        elif blankTile.index_x < index_x:
            updateBoard("Down")
        elif blankTile.index_x > index_x:
            updateBoard("Up")


randomStateButtonRect = ButtonRect(1)
randomStateButton = pygame_gui.elements.UIButton(
    relative_rect=randomStateButtonRect.Rect, text="Random Start", manager=manager
)

# Clicking this button should go through the steps required to solve the puzzle
solveButtonRect = ButtonRect(3)
solveButton = pygame_gui.elements.UIButton(
    relative_rect=solveButtonRect.Rect, text="Solve", manager=manager
)

# slider to control speed of animation
speedSliderRect = ButtonRect(4)
speedSlider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=speedSliderRect.Rect, start_value=1, value_range=(1, 100),
    manager=manager
)

alertLabelRect = ButtonRect(5)
alertLabel = pygame_gui.elements.UILabel(
    relative_rect=alertLabelRect.Rect, manager=manager, text="Click Solve to solve!"
)

# Option box to select which searching algorithm to visualize
solveChoiceRect = ButtonRect(2)
solveChoice = pygame_gui.elements.UIDropDownMenu(
    ["BFS", "DFS", "A* Manhattan", "A* Euclid"], "BFS",
    relative_rect=solveChoiceRect.Rect, manager=manager)

inputTextFieldRect = pygame.Rect(
    (window_width - button_area_width + button_margin + 1, 0 * button_height + 10),
    (button_width, button_height / 2))
inputTextField = pygame_gui.elements.UITextEntryLine(
    relative_rect=inputTextFieldRect, manager=manager)
inputTextField.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8"])
inputTextField.set_text_length_limit(9)

confirmButtonRect = pygame.Rect(
    (window_width - button_area_width + button_margin + 1, 0.4 * button_height + 10),
    (button_width, button_height / 2))
confirmButton = pygame_gui.elements.UIButton(
    relative_rect=confirmButtonRect, text="Confirm", manager=manager)


statusTextFieldRect = pygame.Rect(
    (button_margin, window_height - 100),
    (button_height * 3.5, button_width * 20))
statusTextField = pygame_gui.elements.UITextEntryLine(
    relative_rect=statusTextFieldRect, manager=manager)
statusTextField.disable()

initialState, numbered_tiles_list, blankTile = newState(12345678)

solutionExists = False

# will be populated when a solution is returned
solutionStepsList = []
solutionIndex = 0

clock = pygame.time.Clock()

time_counter = 0
running = True
while running:

    time_delta = clock.tick(60) / 1000
    time_counter += time_delta * 1000

    if time_counter > 500 / speedSlider.get_current_value() and solutionExists:
        updateBoard(solutionStepsList[solutionIndex].move)
        time_counter = 0
        solutionIndex += 1
        if solutionIndex == len(solutionStepsList):
            solutionExists = False

            # I added this to stop it from crashing when trying to solve
            # a shadow state: state on board an state actually stored are
            # not the same, so it attempts to do wrong moves
            initialState, numbered_tiles_list, blankTile = newState(12345678)
            solutionStepsList = []

        # check the event queue for events, such as quit or click
        # I noticed while learning pygame that if the program doesn't process the event queue,
        # the OS considers the app frozen and it crashes
    events = pygame.event.get()

    # Check all events in even queue
    for event in events:

        # specific to the UI library. all events related to pygame_gui go here
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == randomStateButton:
                    state = alg.generate_random_puzzle()
                    initialState, numbered_tiles_list, blankTile = newState(state)
                    solveButton.enable()
                    solutionExists = False
                elif event.ui_element == solveButton:
                    if initialState.state != alg.goal_state:
                        type_of_search = solveChoice.selected_option
                        answer = alg.choose_algorithm(initialState, type_of_search)
                        path_to_goal = alg.path(answer)
                        status = alg.printing(answer, type_of_search)
                        solveButton.disable()
                        if path_to_goal:
                            solutionExists = True
                            solutionIndex = 0
                            solutionStepsList = path_to_goal[1:]
                            alert_label("Solving...")
                        else:
                            alert_label("No solution!")
                            solveButton.enable()

                        # print status in text field
                        statusTextField.text = status
                        statusTextField.focus()
                    else:
                        alert_label("Already solved")

                elif event.ui_element == confirmButton:
                    state = validate(inputTextField.text)
                    if state:
                        initialState, numbered_tiles_list, blankTile = newState(state)
                        solutionExists = False
                        solveButton.enable()
                    else:
                        pass

        if event.type == alert_label_event:
            alertLabel.set_text("")
            pygame.time.set_timer(alert_label_event, 0)

        # Checking for a mouseclick on a tile
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Check If the position of mouse click is within border of Tile Area
            # No need to do any swapping otherwise
            if x < tile_area_width and y < tile_area_height:
                pass
                # swapTiles(event.pos)

        if event.type == pygame.QUIT:
            running = False
            break

        manager.process_events(event)

    # specific to pygame_gui, must be called every loop to update UI
    manager.update(time_delta)

    # fill the screen with the background color before drawing anything else
    window.fill(background_colour)

    # Draw rectangles representing the tiles of the 8-puzzle except blank
    for tile in numbered_tiles_list:
        pygame.draw.rect(window, tile_colour, tile.tile_stats())

        # display the tile number on the tile as text
        textSurf = font.render(tile.number, True, numbers_colour, tile_colour)
        textRect = textSurf.get_rect()
        textRect.center = tile.x + tile_width // 2, tile.y + tile_height // 2
        window.blit(textSurf, textRect)

    # the blank tile is drawn as a black rectangle
    pygame.draw.rect(window, background_colour, blankTile.tile_stats())

    # called every loop to update visuals
    manager.draw_ui(window)
    pygame.display.update()

# quit application if somehow loop is escaped
pygame.quit()