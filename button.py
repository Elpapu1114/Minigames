import pygame

class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # "clicked" tracks whether the mouse button was down while over this button
        # so we only trigger an action on the transition from not-pressed -> pressed.
        self.clicked = False

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()

        mouse_pressed = pygame.mouse.get_pressed()[0]

        # If mouse is over button and pressed now, and wasn't pressed before -> fire action
        if self.rect.collidepoint(pos):
            if mouse_pressed and not self.clicked:
                self.clicked = True
                action = True

        # Reset clicked flag when mouse button is released so the button can be clicked again
        if not mouse_pressed:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action