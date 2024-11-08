import pixie
from bannerpy import fields, cards

test_card = cards.Card('test/card.png', bg_color=(1, 0.5, 0.5, 1),  rounded_corners = 90, margin=20, resolution=(200,100))
test_card.render()

test_simple = cards.SimpleCard('test/simplecard.png', 'more, longer example text that hopefully will wrap around', '/home/bean/.local/share/fonts/Silvertones.ttf', 100, font_color=(0.2, 0.2, 0.2, 1), bg_color=(0.5, 1, 0.5, 1), margin_y = 40, rounded_corners = 40)
test_simple.render()

test_simple_with_divider = cards.SimpleCard('test/simplecard_divider.png', '(Finucci et al., 2024)', '/run/current-system/sw/share/X11/fonts/DejaVuSans.ttf', 130, margin_x = 8, margin_y = 15, rounded_corners = 100, divider = 'test/short-squiggle.png', divider_scale=None, h_align=pixie.CENTER_ALIGN)
test_simple_with_divider.render()

dejavusans_path = '/run/current-system/sw/share/X11/fonts/DejaVuSans.ttf'
test_cc = cards.ComplexCard('test/complex.png')
header = fields.TextField('Heading', '/home/bean/.local/share/fonts/GROBOLD.ttf', 100, margin_y=10, h_align=pixie.CENTER_ALIGN, font_color=(0.2, 1, 0.2, 1))
subtitle = fields.TextField('Subtitle', dejavusans_path, 70, h_align=pixie.CENTER_ALIGN)
divider = fields.Image('/home/bean/Nextcloud/beanstem/short-squiggle.png', margin_y=100, scale=0.75,)
body = fields.TextField('Body text, this is a lot of text that will take up space and hopefully wrap around just so I can make extra sure that it does wrap', dejavusans_path, 50, h_align=pixie.RIGHT_ALIGN)
test_cc.fields = [header, subtitle, divider, body]
test_cc.render()
