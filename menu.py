import pygame
import assets

SLOT_COUNT = 3

class MainMenu:
    def __init__(self, screen, font) -> None:
        self.screen = screen
        self.font = font
        self.selected_slot = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_LEFT):
                self.selected_slot = self.selected_slot - 1
                if self.selected_slot < 1: self.selected_slot = SLOT_COUNT

            elif event.key in (pygame.K_UP, pygame.K_RIGHT):
                self.selected_slot = self.selected_slot + 1
                if self.selected_slot > SLOT_COUNT: self.selected_slot = 1

            elif event.key == pygame.K_RETURN:
                return "start_slot", self.selected_slot

        return None

    def draw(self) -> None:
        if assets.SLOT_IMG:
            slot_rect = assets.SLOT_IMG.get_rect()
            self.screen.blit(assets.SLOT_IMG, slot_rect)

        if assets.NUM_IMGS:
            num_img = assets.NUM_IMGS[self.selected_slot - 1]
            num_rect = num_img.get_rect()
            self.screen.blit(num_img, num_rect)
