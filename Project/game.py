import pygame
import random

class TowerClimberGame:

    #Window properties
    FPS = 60
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 800
    BACKGROUND_COLOR = (0, 40, 90)

    #Game properties
    PLAYER_MOVE_STRENGTH = 6 #For one keystroke how much pixels will player move in horizontal plane
    PLAYER_VERTICAL_VELOCITY = 15 #Jumping velocity

    GRAVITY = 1 #For one game loop, how much will be reduce vertical velocity

    PLATFORM_GAP = 90 #Gap between platforms

    NUMBER_OF_LEVELS = 100

    GAME_TIME = 20 #Time of game is 20 seconds
    TOTAL_TIME_SCORE_DECREMENT = 100

    class Player:
        '''Model of a player in the game with possible actions and states it can be found in

        Static variables shared between all players
            PLAYER_HEIGHT :int - player height in pixels
            PLAYER_WIDTH :int - player width in pixels
            PLAYER_COLOR :tuple - color tuple (e.g. (255, 0, 255))

        Instance variables
            rect :pygame.Rect - rectangle representing a player
            vel_y :int - y (vertical) velocity of a player
            vertical_collision :bool - boolean representing if player is standing on something(used for jumping)

        Public methods
            __init__(self, x, y) -> None - constructor
            draw(self, offset_y :int) -> None - draws player on WINDOW
            jump(self) -> None - player jumps
            move_left(self) -> None - player moves left
            move_right(self) -> None - player moves right
        '''
        PLAYER_HEIGHT = 50
        PLAYER_WIDTH = 30
        PLAYER_COLOR = (27, 147, 168)

        MOVE_STRENGTH = 6 #For one keystroke how much pixels will player move in horizontal plane

        MAX_VERTICAL_VELOCITY = 15 #Jumping velocity

        def __init__(self, x :int, y :int) -> None:
            '''Constructor which takes x and y coordinate and creates player

            Keyword arguments:
                x :int - x (horizontal) coordinate
                y :int - y (vertical) coordinate
            '''
            self.rect = pygame.Rect(x, y, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

            self.vel_y = 0
            self.vertical_collision = False

        def draw(self, offset_y :int, window) -> None:
            '''Draws player on the WINDOW based on the given offset

            Keyword arguments:
                offset_y :int - y (vertical) offset'''
            pygame.draw.rect(window,
                             self.PLAYER_COLOR,
                             self.rect.move(0, offset_y))

        def jump(self) -> None:
            '''Changes player vertical velocity only if the player is touching ground
            '''
            #If we are not touching the ground, we can't jump
            if(not self.vertical_collision):
                return
            self.vel_y = -TowerClimberGame.PLAYER_VERTICAL_VELOCITY

        def move_left(self) -> None:
            '''Moves player left
            '''
            self.rect.move_ip(-TowerClimberGame.PLAYER_MOVE_STRENGTH, 0)

        def move_right(self) -> None:
            '''Moves player right
            '''
            self.rect.move_ip(TowerClimberGame.PLAYER_MOVE_STRENGTH, 0)

        def update(self) -> None:
            '''Updates player vertical position and updates player vertical velocity based on GRAVITY
            '''
            if(self.vertical_collision and self.vel_y >= 0):
                self.vel_y = 0
                return
            self.rect.move_ip(0, self.vel_y)
            self.vel_y += TowerClimberGame.GRAVITY
            if(self.vel_y > TowerClimberGame.PLAYER_VERTICAL_VELOCITY - 3):
                self.vel_y = TowerClimberGame.PLAYER_VERTICAL_VELOCITY - 3

    class Floor:
        '''Class for modeling floor

        Static variables shared between all players
            COLOR :tuple - color tuple (e.g. (255, 0, 255))
            THICKNESS :int - floor thicknes in pixels

        Instance variables
            rect :pygame.Rect - rectangle representing a floor

        Public methods
            __init__(self, x :int = 0, y :int = WINDOW_HEIGHT - THICKNESS, width :int = WINDOW_WIDTH) -> None - constructor
            draw(self, offset_y :int) -> None: - draws floor on the WINDOW based on the vertical offset
        '''
        COLOR = (255, 255, 255)
        THICKNESS = 4

        def __init__(self, x :int, y :int, width :int) -> None:
            '''Constructor which takes top left (x, y) coordinate and width (Floor() creates floor at the bottom of screen)

            Keyword arguments:
                x :int - x (horizontal) coordinate of top left corner of floor (default 0)
                y :int - y (vertical) coordinate of top left corner of floor default(WINDOW_HEIGHT - THICKNESS)
                width :int - width (length) of the floor (default WINDOW_WIDTH)'''
            self.rect = pygame.Rect(x, y, width, self.THICKNESS)

        def draw(self, offset_y :int, window) -> None:
            '''Draws floor on the WINDOW based on the given offset

            Keyword arguments:
                offset_y :int - y (vertical) offset'''
            pygame.draw.rect(window,
                             self.COLOR,
                             self.rect.move(0, offset_y))

    class Wall:
        '''Class for modeling wall

        Static variables shared between all players
            COLOR :tuple - color tuple (e.g. (255, 0, 255))
            THICKNESS :int - wall thicknes in pixels

        Instance variables
            rect :pygame.Rect - rectangle representing a wall
            left :bool - True if wall is on the left side of the window, False otherwise

        Public methods
            __init__(self) -> None - constructor
            draw(self) -> None: - draws wall on the WINDOW
        '''
        COLOR = (255, 255, 255)
        THICKNESS = 4

        def __init__(self, left :bool) -> None:
            '''Constructor which takes left as bool

            Keyword arguments:
                left :bool - if True wall will be on the left side of the window elsewise wall will be on the right
            '''
            if left:
                self.rect = pygame.Rect(0, 0, self.THICKNESS, TowerClimberGame.WINDOW_HEIGHT)
            else:
                self.rect = pygame.Rect(TowerClimberGame.WINDOW_WIDTH - self.THICKNESS, 0, self.THICKNESS, TowerClimberGame.WINDOW_HEIGHT)
            self.left = left

        def draw(self, window) -> None:
            '''Draws wall on the WINDOW
            '''
            pygame.draw.rect(window,
                             self.COLOR,
                             self.rect)




    def _draw(self) -> None:
        self.WINDOW.fill(self.BACKGROUND_COLOR)
        self._player.draw(self._offsetY, self.WINDOW)
        for floor in self._floors:
            floor.draw(self._offsetY, self.WINDOW)
        for wall in self._walls:
            wall.draw(self.WINDOW)
        self.WINDOW.blit(pygame.font.SysFont("comicsans",20, True , True).render("Score : "+str(int(self._current_score)),1,(255, 0, 0)), (10, 10))
        self.WINDOW.blit(pygame.font.SysFont("comicsans",20, True , True).render("Time : "+str(int(self._current_time)),1,(255, 0, 0)), (430, 10))
        
        pygame.display.update()

    def _handle_keys(self) -> None:
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self._player.move_left()
        if key[pygame.K_RIGHT]:
            self._player.move_right()
        if key[pygame.K_UP]:
            self._player.jump()

    def _handle_vertical_collision(self) -> None:
        #If I am going upwards, I do not want to check for vertical collision
        if self._player.vel_y < 0:
            self._player.vertical_collision = False
            return

        for floor in self._floors:
            if self._player.rect.colliderect(floor):
                self._player.vertical_collision = True

                # + 1 is added so that player will be one pixel in the floor, therefore constantly collinding, and there will be no small jumping up and down
                self._player.rect.bottom = floor.rect.top + 1
                return
        self._player.vertical_collision = False

    def _handle_horizontal_collision(self) -> None:
        for wall in self._walls:
            if self._player.rect.colliderect(wall.rect.move(0, -self._offsetY)):
                if wall.left:
                    self._player.rect.left = wall.rect.right
                else:
                    self._player.rect.right = wall.rect.left
                break

    def _handle_offset(self) -> None:
        if self._player.rect.top + self._offsetY < 400:
            self._offsetY -= (self._player.rect.top + self._offsetY - 400)

    def _generate_floors(self) -> list[Floor]:

        MAX_JUMP = 230 #Maximum possible jumpable distance between 2 Floor on the different levels

        max_distance = -68 #Max distance between 2 Floors on the different levels
        floor_width = 105

        mu, sigma = max_distance, 4 #Gaus distribution parameters

        last_floor_left_point, last_floor_right_point = 0 + 100, self.WINDOW_WIDTH - 100
        last_floor_height = self.WINDOW_HEIGHT

        floors = []

        for i in range(self.NUMBER_OF_LEVELS):

            direction = random.randint(0, 1)
            direction = 1 if direction == 1 else -1

            #update max_distance
            max_distance += 8
            max_distance = min(max_distance, MAX_JUMP - 10) #Added -10 so that levels do not be all exact the same

            #update floor_width
            floor_width -= 5
            floor_width = max(5, floor_width)

            #update mu and sigma
            mu = max_distance

            x_offset = round(random.normalvariate(mu, sigma))

            if direction == 1:

                if(last_floor_right_point + x_offset + floor_width/2 > self.WINDOW_WIDTH):
                    generated_floor = self.Floor(last_floor_left_point - x_offset - floor_width, last_floor_height - self.PLATFORM_GAP, floor_width)
                else:
                    generated_floor = self.Floor(last_floor_right_point + x_offset, last_floor_height - self.PLATFORM_GAP, floor_width if last_floor_right_point + x_offset + floor_width < self.WINDOW_WIDTH else self.WINDOW_WIDTH - last_floor_right_point - x_offset - 1)
            else:

                if(last_floor_left_point - x_offset - floor_width/2 < 0):
                    generated_floor = self.Floor(last_floor_right_point + x_offset, last_floor_height - self.PLATFORM_GAP, floor_width)
                else:
                    generated_floor = self.Floor(max(last_floor_left_point - x_offset - floor_width, 0), last_floor_height - self.PLATFORM_GAP, floor_width)

            last_floor_height -= self.PLATFORM_GAP
            last_floor_left_point = generated_floor.rect.left
            last_floor_right_point = generated_floor.rect.right

            floors.append(generated_floor)
        return floors


    def isEnd(self) -> bool:
        return self._player.rect.bottom + self._offsetY > self.WINDOW_HEIGHT + 4 \
                or self._current_time > self.GAME_TIME
    
    def timePassed(self) -> bool:
        return self._current_time > self.GAME_TIME

    def getPlayerPosition(self) -> list[int]:
        return [self._player.rect.centerx, self._player.rect.bottom, 1 if self._player.vertical_collision else 0]

    def getImportantFloors(self, numberOfFloors: int) -> list[int]:
        important = []
        playerXPosition = self._player.rect.bottom
        for floor in self._floors:
            if numberOfFloors <= 0: break
            if floor.rect.top - 2 * self.PLATFORM_GAP < playerXPosition:
                important.append(list(floor.rect.topleft))
                important.append(list(floor.rect.topright))
                numberOfFloors -= 1
        return important

    def getScore(self) -> int:
        floors_beneth = len([floor for floor in self._floors if floor.rect.top + 2 > self._player.rect.bottom])
        return floors_beneth*100 - self._current_time/self.GAME_TIME * self.TOTAL_TIME_SCORE_DECREMENT


    def __init__(self, render_mode: str | None) -> None:
        if(render_mode == "human"):
            pygame.init()
            self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            self.WINDOW.fill(self.BACKGROUND_COLOR)
            pygame.display.set_caption("Tower climber")

        self._player = self.Player(int(self.WINDOW_WIDTH/2), int(self.WINDOW_HEIGHT - self.Player.PLAYER_HEIGHT - self.Floor.THICKNESS - 10))
        self._walls = [self.Wall(left=True), self.Wall(left=False)]

        self._floors = [self.Floor(0, self.WINDOW_HEIGHT - self.Floor.THICKNESS, self.WINDOW_WIDTH)] #Create base floor
        self._floors += self._generate_floors()

        self._clock = pygame.time.Clock()

        self._offsetY = 0

        self._current_score = 0
        self._current_time = 0
    
    def playGame(self) -> None:
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self._handle_keys()
            self.takeAction(None)
            if self.isEnd():
                pygame.quit()
                quit()
            self.drawOnScreen()

        pygame.quit()
        quit()

    def drawOnScreen(self) -> None:
        self._clock.tick(self.FPS)
        self._draw()

    def reset(self) -> None:
        self._player = self.Player(int(self.WINDOW_WIDTH/2), int(self.WINDOW_HEIGHT - self.Player.PLAYER_HEIGHT - self.Floor.THICKNESS - 10))
        self._walls = [self.Wall(left=True), self.Wall(left=False)]

        self._floors = [self.Floor(0, self.WINDOW_HEIGHT - self.Floor.THICKNESS, self.WINDOW_WIDTH)] #Create base floor
        self._floors += self._generate_floors()

        self._offsetY = 0
        
        self._current_score = 0
        self._current_time = 0

    def takeAction(self, action :list[int]) -> None:
        if action is not None:
            if action[1] == 1:
                self._player.move_left()
            elif action[1] == 2:
                self._player.move_right()
            if action[0] == 1:
                self._player.jump()
        self._player.update()
        self._handle_horizontal_collision()
        self._handle_vertical_collision()
        self._handle_offset()

        self._current_time += 1/self.FPS
        self._current_score = self.getScore()

    def step(self) -> None:
        self._clock.tick(self.FPS)
        self._handle_horizontal_collision()
        self._handle_vertical_collision()
        self._handle_offset()
        self._player.update()

if __name__ == "__main__":
    game = TowerClimberGame(render_mode="human")
    game.playGame()