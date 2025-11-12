import os
import arcade
import random
from engine import *

window = make_window(title="Sidecroller Maker")
window.set_mouse_visible(False)


class Mouse(arcade.Sprite):
    def __init__(
        self,
        textures: list[arcade.Texture],
    ):
        super().__init__(textures[0])
        self.textures = textures


class MakerView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.game = make_game(window)

        self.sprites = arcade.SpriteList()
        self.player = arcade.SpriteList()

        self.textures_indices = {
            0: "player",
            1: "platform",
            2: "enemy",
            3: "coin",
        }
        textures = [
            arcade.load_texture("assets/images/p1_stand.png"),
            arcade.make_soft_square_texture(
                size=40,
                color=arcade.color.YELLOW,
                center_alpha=255,
                outer_alpha=255,
            ),
            arcade.load_texture(":resources:/images/enemies/slimeBlock.png"),
            arcade.load_texture(":resources:/images/items/gold_1.png"),
        ]
        self.mouse = Mouse(textures)
        self.mouse.position = window.width // 2, window.height // 2
        self.sprites.append(self.mouse)

    def on_draw(self) -> None:
        self.clear()
        self.sprites.draw()
        self.player.draw()

    def on_update(self, delta_time) -> None:
        self.mouse.update(delta_time)

        self.mouse.center_x = arcade.math.clamp(
            self.mouse.center_x, 0, self.game.level_width
        )

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.position = x, y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.textures_indices[self.mouse.cur_texture_index] == "player":
                self.game.player.position = x, y
                self.game.player.start_x = x
                self.game.player.start_y = y
                if self.player:
                    self.player.remove(self.player[0])
                self.player.append(
                    arcade.Sprite(
                        arcade.load_texture("assets/images/p1_stand.png"),
                        center_x=x,
                        center_y=y,
                    )
                )
            elif self.textures_indices[self.mouse.cur_texture_index] == "platform":
                self.game.make_platform(x, y, 40, 40)
                self.sprites.append(
                    arcade.SpriteSolidColor(
                        width=40,
                        height=40,
                        center_x=x,
                        center_y=y,
                        color=arcade.color.YELLOW,
                    )
                )
            elif self.textures_indices[self.mouse.cur_texture_index] == "enemy":
                self.game.make_enemy(x, y)
                self.sprites.append(
                    arcade.Sprite(
                        arcade.load_texture(
                            ":resources:/images/enemies/slimeBlock.png"
                        ),
                        scale=0.5,
                        center_x=x,
                        center_y=y,
                    )
                )
            elif self.textures_indices[self.mouse.cur_texture_index] == "coin":
                self.game.make_coin(x, y)
                self.sprites.append(
                    arcade.Sprite(
                        arcade.load_texture(":resources:/images/items/gold_1.png"),
                        scale=0.7,
                        center_x=x,
                        center_y=y,
                    )
                )

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == arcade.key.ENTER:
            run(self.game)
        if symbol == arcade.key.LEFT:
            if self.mouse.cur_texture_index == 0:
                self.mouse.cur_texture_index = len(self.mouse.textures)
                self.mouse.set_texture(self.mouse.cur_texture_index)
            else:
                self.mouse.cur_texture_index -= 1
                self.mouse.set_texture(self.mouse.cur_texture_index)
        elif symbol == arcade.key.RIGHT:
            self.mouse.cur_texture_index = (self.mouse.cur_texture_index + 1) % len(
                self.mouse.textures
            )
            self.mouse.set_texture(self.mouse.cur_texture_index)

        if self.textures_indices[self.mouse.cur_texture_index] == "enemy":
            self.mouse.scale = 0.5
        elif self.textures_indices[self.mouse.cur_texture_index] == "coin":
            self.mouse.scale = 0.7
        else:
            self.mouse.scale = 1.0


game = MakerView()
window.show_view(game)
arcade.run()
