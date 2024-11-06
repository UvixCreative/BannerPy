import pixie

def determine_size():
    return

def namecard():
    return

def citation():
    return

class TextField:
    _font = None
    _text = ""
    _font_color = ()
    _h_align = 0
    _v_align = 0

    def __init__(self, text: str, font_path: str, font_color: tuple=(0, 0, 0, 1), font_size: int=12, h_align: int=0, v_align: int=0):
        self.text = text
        self.font = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.h_align = h_align
        self.v_align = v_align

    @property
    def text(self):
        """Text value"""
        return self._text

    @text.setter
    def text(self, in_text: str):
        if not type(in_text) == str:
            raise TypeError('Text must be a string')

        self._text = in_text

    @property
    def font(self):
        """Font for the text field"""
        return self._font

    @font.setter
    def font(self, font_path: str):
        self._font = pixie.read_font(font_path)
    
    @property
    def font_size(self):
        """Font size"""
        return self._font.size

    @font_size.setter
    def font_size(self, size: int):
        self._font.size = size

    @property
    def font_color(self):
        """Text color"""
        return self._font_color

    @font_color.setter
    def font_color(self, color: tuple):
        self._font.paint.color = pixie.Color(*color)

    @property
    def h_align(self):
        return self._h_align

    @h_align.setter
    def h_align(self, align: int):
        if not type(align) == int:
            raise TypeError('h_align must be an integer between 0-2')
        if align < 0 or align > 2:
            raise ValueError('h_align must be an integer between 0-2')

        self._h_align = align

    @property
    def v_align(self):
        return self._v_align

    @v_align.setter
    def v_align(self, align: int):
        if not type(align) == int:
            raise TypeError('v_align must be an integer between 0-2')
        if align < 0 or align > 2:
            raise ValueError('v_align must be an integer between 0-2')

        self._v_align = align

class Card:
    _res_x = 10
    _res_y = 10
    _filename = ""
    _bg_color = ()
    _body_text = None # TextField
    _rounded_corners = 0
    _margin = 10

    def __init__(self, filename: str, text: str, font_path: str, font_size: int=12, bg_color: tuple=(1, 1, 1, 1), font_color: tuple=(0, 0, 0, 1), rounded_corners: int=0, margin: int=10, divider=None):
        """
        :param str filename: Path to the output file
        :param str text: The body text
        :param path font_path: Path to the font to use for the body text
        :param int font_size: The size of the font for the body text
        :param tuple bg_color: Tuple (R, G, B, A) to represent the background color
        :param tuple font_color: Tuple (R, G, B, A) to represent the color of the body text
        :param int rounded_corners: Integer number for the radius of the rounded corners of the card
        :param int margin: The margin (as a percentage) between the text and the edge of the background shape
        :param path divider: Path to an image or SVG for the divider to accent/underline the text
        """
        self._body_text = TextField(text, font_path, font_color, font_size)
        self.filename = filename

        self.bg_color = bg_color
        self.rounded_corners = rounded_corners

        self.margin = margin
        
        self._determine_resolution()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if not type(filename) == str:
            raise TypeError('Filename must be a path')

        self._filename = filename
    
    @property
    def resolution(self):
        """Resolution of the card image file to be generated"""
        return (self._res_x, self._res_y)

    @resolution.setter
    def resolution(self, res: tuple):
        for i in res:
            if i < 1:
                raise ValueError('x and y must be positive integers')
            
        self._res_x = res[0]
        self._res_y = res[1]

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color: tuple):
        self._bg_color = pixie.Color(*color)

    @property
    def rounded_corners(self):
        return self._rounded_corners

    @rounded_corners.setter
    def rounded_corners(self, rounded: int):
        if not type(rounded) == int:
            raise TypeError('rounded_corners must be a positive integer')
        if rounded < 0:
            raise ValueError('rounded_corners must be a positive integer')

        self._rounded_corners = rounded

    def _determine_resolution(self):
        return

    @property
    def body_text(self):
        return self._body_text

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, margin: int):
        if not type(margin) == int:
            raise TypeError('margin must be an integer between 0-100')
        if margin < 0 or margin > 100:
            raise ValueError('margin must be an integer between 0-100')

        self._margin = margin

    def render(self):
        image = pixie.Image(self._res_x, self._res_y)
        ctx = image.new_context()

        paint = pixie.Paint(pixie.SOLID_PAINT)
        paint.color = self.bg_color
        ctx.fill_style = paint

        ctx.rounded_rect(0, 0, *self.resolution, self.rounded_corners, self.rounded_corners, self.rounded_corners, self.rounded_corners)
        ctx.fill()

        real_margins = tuple(x * self.margin / 100 for x in self.resolution)
        real_bounds = (self.resolution[0] - (real_margins[0] * 2), self.resolution[1] - (real_margins[1] * 2))

        real_body = pixie.SeqSpan()
        real_body.append(pixie.Span(text=self.body_text.text, font=self.body_text.font))
        image.arrangement_fill_text(
            real_body.typeset(
                bounds = pixie.Vector2(*real_bounds),
                h_align = self.body_text.h_align,
                v_align = self.body_text.v_align
            ),
            transform = pixie.translate(*real_margins)
        )

        image.write_file(self.filename)

test = Card('test.png', 'example text', '/home/bean/.local/share/fonts/Silvertones.ttf', 24, bg_color=(1, 0.5, 0.5, 1), font_color=(0.3, 0.3, 0.3, 1), rounded_corners = 30)
test.resolution = (1920, 1080)
test.render()
