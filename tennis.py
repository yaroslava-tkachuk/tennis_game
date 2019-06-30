import pygame
import time


class Background(pygame.sprite.Sprite):

    '''Background class.'''

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


pygame.mixer.init()
class Ball(pygame.sprite.Sprite):

    '''Ball class.'''

    def __init__(self, image_file, location, speed, increment_x, increment_y, sound):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.speed = speed
        self.increment_x = increment_x
        self.increment_y = increment_y
        self.sound = sound
        self.speed = speed
    
    def reverse_increment_x(self):

        '''Reversing x increment.'''

        self.increment_x *= -1

    def move(self, increment_x, increment_y):

        '''Moving the ball.'''

        self.rect.move_ip(-1*self.increment_x*self.speed, 0)
        self.rect.move_ip(0, 1*self.increment_y*(self.speed//3))

    def collision_left(self, smth):

        '''Ball hitting racket of Player 1.'''

        if (self.rect.left  <= smth.rect.right) and (self.rect.top < smth.rect.bottom) and (self.rect.bottom > smth.rect.top):
            return True

    def collision_right(self, smth):

        '''Ball hitting racket of Palyer 2.'''

        if (self.rect.right  >= smth.rect.left) and (self.rect.top < smth.rect.bottom) and (self.rect.bottom > smth.rect.top):
            return True

    def change_angle(self, smth):

        '''Change the ball's angle depending on how far from the center it hits the racket.'''

        a = self.rect.center[1]  - smth.rect.top
        b = smth.rect.bottom - self.rect.center[1]
        angle = (smth.rect.center[1]-smth.rect.top)/(9000)*(b-a)
        self.increment_y = angle
    
    def hit_reaction(self, smth):

        '''Reaction of the ball for hitting the racket: hitting sound, reversing x increment and changing y increment depending on the hit.'''

        self.hit_sound()
        self.reverse_increment_x()
        self.change_angle(smth)

    def out_left(self, field):

        '''Check if the ball is out of the field and the point goes to player1.'''

        if ((self.rect.left > 1497) or (((self.rect.bottom < 156) or (self.rect.top > 700)) and (self.rect.left > field.rect.center[0]))):
            return True

    def out_right(self, field):

        '''Check if the ball is out of the field and the point goes to player2.'''

        if ((self.rect.right < 297) or (((self.rect.bottom < 156) or (self.rect.top > 700)) and (self.rect.right < field.rect.center[0]))):
            return True

    def reset_pos(self, new_loc):

        '''Reset the ball's position to center and increment y to 0.'''

        self.rect.center = new_loc
        self.increment_y = 0

    def hit_sound(self):

        '''Sound of hitting the ball with a racket.'''

        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play(0)


class Player(pygame.sprite.Sprite):

    '''Player class.'''

    def __init__(self, image_file, location, speed, up_key, down_key):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.speed = speed
        self.up_key = up_key
        self.down_key = down_key

    def handle_keys(self):

        '''Moving rackets when user presses the button.'''

        key = pygame.key.get_pressed()
        if key[self.up_key]:
            if self.rect.top >= 156:
                self.rect.move_ip(0, -1*self.speed)
        if key[self.down_key]:
            if self.rect.bottom <= 700:
                self.rect.move_ip(0, 1*self.speed)

    def reset_pos(self, loc_x, loc_y):

        '''Reset the racket's position to the initial one.'''

        self.rect.center = (loc_x, loc_y)


pygame.font.init()
class Score(pygame.sprite.Sprite):

    '''Score class.'''

    def __init__(self, points1=0, points2=0):
        pygame.sprite.Sprite.__init__(self)
        self.myfont = pygame.font.SysFont('Liberation Sans', 30)
        self.points1 = points1
        self.points2 = points2

        self.plus_point_msg = 'One point for Player {}.'
        self.won_msg = 'Congratualtions, Player {}! You won the game.'
        self.congrats_song = 'tina_turner_the_best_cut.wav'
        
    def refresh(self, screen):

        '''Refreshing the score with the Players' points.'''

        self.textsurface = self.myfont.render('Player 1 points: {}     Player 2 points: {}'.format(self.points1, self.points2), False, (255, 255, 255))
        screen.blit(self.textsurface, (20, 20))

    def plus_point1(self):

        '''Adding point to player 1.'''

        self.points1 += 1

    def plus_point2(self):

        '''Adding point to player 2.'''

        self.points2 += 1

    def play_congrats_song(self):

        '''Playing a congratulations song.'''

        pygame.mixer.music.load(self.congrats_song)
        pygame.mixer.music.play(0)


    def display_message(self, msg, screen, background, player_numb, waiting, dist):

        '''Displaying the add points and victory messages.'''
    
        msg_textsurface = self.myfont.render(msg.format(player_numb), False, (255, 255, 255))
    
        screen.blit(msg_textsurface, (background.rect.center[0]-dist, 50))
        self.refresh(screen)
        pygame.display.update()
        time.sleep(waiting)


class Game(object):

    '''Game class.'''

    def __init__(self):

        self.speed = 10
        self.background = Background('court.png', [0, 0])
        self.screen = pygame.display.set_mode(self.background.rect.size)
        self.ball = Ball('ball.png', self.background.rect.center, self.speed, 1, 0, 'ball_hit.wav')
        self.player1 = Player('racket1.png', [297, self.background.rect.center[1]], self.speed, pygame.K_w, pygame.K_s)
        self.player2 = Player('racket2.png', [1497, self.background.rect.center[1]], self.speed, pygame.K_UP, pygame.K_DOWN)
        self.score = Score()
        self.running = True

    def display_objects(self):

        '''Displaying all objects on the screen.'''

        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.ball.image, self.ball.rect)
        self.screen.blit(self.player1.image, self.player1.rect)
        self.screen.blit(self.player2.image, self.player2.rect)

    def reset_positions(self):

        '''Reset the positions of the rackets and the ball.'''

        self.ball.reset_pos(self.background.rect.center)
        self.player1.reset_pos(297, self.background.rect.center[1])
        self.player2.reset_pos(1497, self.background.rect.center[1])

    def add_points(self, player_numb):

        '''Adding one point to player 1 or 2 and ending the game if they have won.'''

        if player_numb == 1:
            self.score.plus_point1()
        else:
            self.score.plus_point2()

        if ((self.score.points1 == 6) or (self.score.points2 == 6)):
            self.score.play_congrats_song()
            self.score.display_message(self.score.won_msg, self.screen, self.background, player_numb, 20, 300)
            self.end_game()
        else:
            self.score.display_message(self.score.plus_point_msg, self.screen, self.background, player_numb, 4, 150)

    def end_game():

        '''Ending the game.'''

        self.running = False

    
    def play_game(self):

        '''Playing process.'''
        
        pygame.display.set_caption('Tennis Game')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.display_objects()

        self.player1.handle_keys()
        self.player2.handle_keys()

        if self.ball.collision_left(self.player1):
            self.ball.hit_reaction(self.player1)

        if self.ball.collision_right(self.player2):
            self.ball.hit_reaction(self.player2)

        self.ball.move(self.ball.increment_x, self.ball.increment_y)

        if self.ball.out_left(self.background):
            self.add_points(1)
            self.reset_positions()

        if self.ball.out_right(self.background):
            self.add_points(2)
            self.reset_positions()

        self.score.refresh(self.screen)
        pygame.display.update()


tennis_game = Game()
while tennis_game.running:
    tennis_game.play_game()
