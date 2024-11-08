import pixie
from bannerpy import fields, cards

fonts = {
    "dejavusans": '/run/current-system/sw/share/X11/fonts/DejaVuSans.ttf',
    "grobold": '/home/bean/.local/share/fonts/GROBOLD.ttf',
    "silvertones": '/home/bean/.local/share/fonts/Silvertones.ttf'
}

def blank():
    """
    No text or images
    Background color reddish pink
    Resolution 200x100 px
    No auto-height (because no content)
    """
    test_card = cards.Card('test/blank.png', bg_color=(1, 0.5, 0.5, 1), resolution=(200, 100), auto_height=False)
    test_card.render()

def simple():
    """
    One line of text: translucent black, dejavu sans, size 30, default left-aligned
    Slightly rounded corners
    Baground color maroon-ish
    35% y margin
    """
    test_card = cards.Card('test/simple.png', margin_y=35, border_radius=40, bg_color=(0.4, 0.1, 0.2, 0.8))
    
    body = fields.TextField('This is a simple card', fonts['dejavusans'], 30, font_color=(0, 0, 0, 0.4))

    test_card.fields = [body]

    test_card.render()

def simple_with_underline():
    """
    One line of text: default black, dejavu sans, size 130, center-aligned
    One image: Loaded png, automatically scaled
    Background color default white
    Tweaked margins (all around)
    """
    test_card = cards.Card('test/simple_with_underline.png', margin_x = 8, margin_y = 15, border_radius = 100)

    title = fields.TextField('(Groth et al., 2011)', fonts['dejavusans'], 130, margin_y = 5, h_align=pixie.CENTER_ALIGN)
    underline = fields.Image('test/short-squiggle.png', margin_x = 20, margin_y = 20)

    test_card.fields = [title, underline]

    test_card.render()

def section_intro():
    """
    Heading: translucent black, grobold, size 150, center-aligned
    Subheading: translucent black, dejavu sans, size 100, center-aligned
    Background color a nice green, slightly ranslucent

    This also tests the Card.append() function
    This also tests changing a TextField font property, which tests the internal _update_span function
    """

    test_card = cards.Card('test/simple_heading.png', bg_color=(0.235, 0.549, 0.255, 0.9), border_radius = 125, margin_y = 25)

    heading = fields.TextField('Part 1', fonts['grobold'], 150, font_color = (0, 0, 0, 0.7), h_align=pixie.CENTER_ALIGN)
    subheading = fields.TextField('Introduction', fonts['grobold'], 100, font_color = (0, 0, 0, 0.7), h_align=pixie.CENTER_ALIGN)
    subheading.font_path = fonts['dejavusans']

    test_card.append(heading)
    test_card.append(subheading)

    test_card.render()

def heading_subheading_divider_body():
    """
    4 elements: heading, subheading, divider (image), body
    Heading: bright green, grobold, size 100, center-aligned
    Subheading: default black, dejavu sans, size 70, center-aligned
    Divider: Loaded png, per-element y margin set to 100%, scaled 75% manually
    Body: default black, dejavu sans, size 50, right-aligned
    Background color default white

    This also tests initializing a card with a list of fields
    """
    header = fields.TextField('Heading', fonts['grobold'], 100, margin_y=10, h_align=pixie.CENTER_ALIGN, font_color=(0.2, 1, 0.2, 1))
    subtitle = fields.TextField('Subtitle', fonts['dejavusans'], 70, h_align=pixie.CENTER_ALIGN)
    divider = fields.Image('/home/bean/Nextcloud/beanstem/short-squiggle.png', margin_y=100, scale=0.75)
    body = fields.TextField('Body text, this is a lot of text that will take up space and hopefully wrap around just so I can make extra sure that it does wrap', fonts['dejavusans'], 50, h_align=pixie.RIGHT_ALIGN)

    test_card = cards.Card('test/heading_subheading_divider_body.png', fields = [header, subtitle, divider, body])

    test_card.render()

if __name__ == "__main__":
    blank()
    simple()
    simple_with_underline()
    section_intro()
    heading_subheading_divider_body()

# NOTE: missing tests:
# fields.Image.auto_scale = False. Not directly tested, but it's disabled in heading_subheading_divider_body when scale is manually specified
# fields.Image.margin_x. Not tested here, but it should work
# fields.TextField.margin_x. Not tested here, but it should work
# fields.TextField.v_align. Not tested here. I did test it, it works, but it probably doesn't do what you want it to

# any setter functions. Not directly tested, but the setter functions are utilized by by __init__() functions, so they are tested
# any getter functions. Not directly tested, but I'm pretty sure every property/getter is used by one of the tool functions (render, auto_height, stuff like that)
# any errors or error handling. just don't break it, dingus.
