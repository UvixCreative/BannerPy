import pixie
from main import Card, SimpleCard

test_card = Card('test/card.png', bg_color=(1, 0.5, 0.5, 1),  rounded_corners = 90, margin=20, resolution=(100,200))
test_card.render()

test_simple = SimpleCard('test/simplecard.png', 'more, longer example text that hopefully will wrap around', '/home/bean/.local/share/fonts/Silvertones.ttf', 100, font_color=(0.2, 0.2, 0.2, 1), bg_color=(0.5, 1, 0.5, 1), margin_y = 40, rounded_corners = 40)
test_simple.render()

test_simple_with_divider = SimpleCard('test/simplecard_divider.png', '(Didier et al., 2024)', '/run/current-system/sw/share/X11/fonts/DejaVuSans.ttf', 100, margin_x = 5, margin_y = 10, rounded_corners = 40, divider = '/home/bean/Nextcloud/beanstem/medium-squiggle.png')
test_simple_with_divider.render()
