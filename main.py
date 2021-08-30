import pygame
import sys

from pygame.draw import lines

pygame.init()

screen = pygame.display.set_mode((800, 600))

info_bar = pygame.Rect(0, 500, 800, 600)
pygame.draw.rect(screen, (255,255,255), info_bar, 0)



border_lines = [([150,0], [151,500]), ([150,2], [649,2]), ([649,0], [650,500]), ([150,167], [649,167]), 
                ([150,336], [649,336]), ([316,0], [317,500]), ([482,0], [483,500])]

for line in border_lines:
    pygame.draw.aaline(screen, (255,255,255), line[0],line[1])


actions_XY_fields = [
    [range(151,316), range(3,168)],
    [range(151,316), range(169,334)],
    [range(151,316), range(335,500)],
    [range(317,482), range(3,168)],
    [range(483,648), range(3,168)],
    [range(317,482), range(169,334)],
    [range(483,648), range(169,334)],
    [range(317,482), range(335,500)],
    [range(483,648), range(335,500)]
]

X_filled_action_fields = []
O_filled_action_fields = []

endgame_variants = [
    [[range(151, 316), range(3, 168)], [range(151, 316), range(169, 334)], [range(151, 316), range(335, 500)]],
    [[range(317, 482), range(3, 168)], [range(317, 482), range(169, 334)], [range(317, 482), range(335, 500)]],
    [[range(483, 648), range(3, 168)], [range(483, 648), range(169, 334)], [range(483, 648), range(335, 500)]],
    [[range(151, 316), range(3, 168)], [range(317, 482), range(3, 168)], [range(483, 648), range(3, 168)]],
    [[range(151, 316), range(169, 334)], [range(317, 482), range(169, 334)], [range(483, 648), range(169, 334)]],
    [[range(151, 316), range(335, 500)], [range(317, 482), range(335, 500)], [range(483, 648), range(335, 500)]],
    [[range(151, 316), range(3, 168)], [range(317, 482), range(169, 334)], [range(483, 648), range(335, 500)]],
    [[range(151, 316), range(335, 500)], [range(317, 482), range(169, 334)], [range(483, 648), range(3, 168)]]
]

def winner_check(player_filled_fields):
    for endgame_variant in endgame_variants:
        intersection_check = [x for x in endgame_variant if x in player_filled_fields]
        if len(intersection_check) == 3:
            return True
    return False

def draw_check(X_filled_fileds,O_filled_fileds):
    if len(X_filled_fileds) + len(O_filled_fileds) == 9:
        return True
    return False

def filled_fields_check(interacted_field):
    for filled_fields in X_filled_action_fields:
        if interacted_field[0] in filled_fields and \
            interacted_field[1] in filled_fields:
            return True
                                
    for filled_fields in O_filled_action_fields:
        if interacted_field[0] in filled_fields and \
            interacted_field[1] in filled_fields:
            return True
    return False

FONT_SIZE = 200
font = pygame.font.Font(None, FONT_SIZE)
X = font.render('X', True, (255,255,255))
O = font.render('O', True, (255,255,255))

restart_button_area = pygame.Rect(25,515,130,555)
pygame.draw.rect(screen, (0,0,0), restart_button_area, 0)
text_font = pygame.font.Font(None, int(FONT_SIZE/4))
restart_text = text_font.render('Restart', True, (255,255,255))
screen.blit(restart_text, (30, 540))

what_player_turn = 1
is_game_ended = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            for action_field in actions_XY_fields:
                if x in action_field[0] and y in action_field[1]:
                    coordsX_for_text = action_field[0][round(len(action_field[0])/2)] - FONT_SIZE/4
                    coordsY_for_text = action_field[1][round(len(action_field[1])/2)] - FONT_SIZE/4

                    if what_player_turn == 1 and not is_game_ended:
                        
                        if filled_fields_check(action_field):
                            break 

                        screen.blit(X, (coordsX_for_text, coordsY_for_text))
                        X_filled_action_fields.append([action_field[0], action_field[1]])
                        if winner_check(X_filled_action_fields):
                            winning_title = text_font.render('Player one wins!', True, (98,56,255))
                            screen.blit(winning_title, (160, 540))
                            is_game_ended = True
                            break

                        if draw_check(X_filled_action_fields, O_filled_action_fields):
                            draw_title = text_font.render('Draw!', True, (98,56,255))
                            screen.blit(draw_title, (160,540))

                        what_player_turn = 2

                    elif what_player_turn == 2 and not is_game_ended:
                        
                        if filled_fields_check(action_field):
                            break

                        screen.blit(O, (coordsX_for_text, coordsY_for_text))
                        O_filled_action_fields.append([action_field[0], action_field[1]])
                        if winner_check(O_filled_action_fields):
                            winning_title = text_font.render('Player two wins!', True, (98,56,255))
                            screen.blit(winning_title, (160, 540))
                            is_game_ended = True
                            break
                        
                        if draw_check(X_filled_action_fields, O_filled_action_fields):
                            draw_title = text_font.render('Draw!', True, (98,56,255))
                            screen.blit(draw_title, (160,540))

                        what_player_turn = 1

            if x in range(25,130) and y in range(515,600):
                screen.fill((0,0,0))
                is_game_ended = False

                pygame.draw.rect(screen, (255,255,255), info_bar, 0)
                for line in border_lines:
                    pygame.draw.aaline(screen, (255,255,255), line[0],line[1])
                pygame.draw.rect(screen, (0,0,0), restart_button_area, 0)
                screen.blit(restart_text, (30, 540))

                X_filled_action_fields.clear()
                O_filled_action_fields.clear()
    pygame.display.flip()