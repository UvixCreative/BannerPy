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

    def __init__(self, text: str, font_path: str, font_size: int=12, font_color: tuple=(0, 0, 0, 1), h_align: int=0, v_align: int=0):
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
    _rounded_corners = 0
    _margin_x = 10
    _margin_y = 20

    def __init__(self, filename: str, bg_color: tuple=(1, 1, 1, 1), rounded_corners: int=0, margin: int=None, margin_x: int=10, margin_y: int=20, resolution: tuple=(1920, 1080)):
        """
        :param str filename: Path to the output file
        :param tuple bg_color: Tuple (R, G, B, A) to represent the background color (Default: (1, 1, 1, 1))
        :param int rounded_corners: Integer number for the radius of the rounded corners of the card (Default: 0)
        :param int margin: Shorthand to set margin x and margin y to the same
        :param int margin_x: Percentage for x margin (Default: 10)
        :param int margin_y: Percentage for y margin (Default: 20)
        :param tuple resolution: The resolution of the card (Default: (1920, 1080))
        """
        self.filename = filename

        self.resolution = resolution
        self.bg_color = bg_color
        self.rounded_corners = rounded_corners

        if margin:
            self.margin = margin
        else:
            self.margin_x = margin_x
            self.margin_y = margin_y

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

    def auto_height(self):
        print('Card is a base class that is not intended to be instantiated. auto_height() does nothing')
        return

    @property
    def margin(self):
        return self._margin_x, self._margin_y

    @margin.setter
    def margin(self, margin: int):
        if not type(margin) == int:
            raise TypeError('margin must be an integer between 0-100')
        if margin < 0 or margin > 100:
            raise ValueError('margin must be an integer between 0-100')

        self._margin_x = self._margin_y = margin

    @property
    def margin_x(self):
        return self._margin_x

    @margin_x.setter
    def margin_x(self, margin: int):
        if not type(margin) == int:
            raise TypeError('margin must be an integer between 0-100')
        if margin < 0 or margin > 100:
            raise ValueError('margin must be an integer between 0-100')        
        self._margin_x = margin

    @property
    def margin_y(self):
        return self._margin_y

    @margin_y.setter
    def margin_y(self, margin: int):
        if not type(margin) == int:
            raise TypeError('margin must be an integer between 0-100')
        if margin < 0 or margin > 100:
            raise ValueError('margin must be an integer between 0-100')        
        self._margin_y = margin        

    def _init_image(self):
        """
        Render the background, return the image and the context
        """
        image = pixie.Image(self._res_x, self._res_y)
        ctx = image.new_context()

        paint = pixie.Paint(pixie.SOLID_PAINT)
        paint.color = self.bg_color
        ctx.fill_style = paint

        ctx.rounded_rect(0, 0, *self.resolution, self.rounded_corners, self.rounded_corners, self.rounded_corners, self.rounded_corners)
        ctx.fill()

        return image, ctx
        
    def render(self):
        image, context = self._init_image()
        image.write_file(self.filename)

class SimpleCard(Card):
    _divider = None
    
    def __init__(self, filename: str, text: str, font_path: str, font_size: int=50, font_color: tuple=(0, 0, 0, 1), h_align: int=0, v_align: int=0, bg_color: tuple=(1, 1, 1, 1), rounded_corners: int=0, margin: int=None, margin_x: int=10, margin_y: int=20, resolution: tuple=(1920, 1080), divider=None, auto_height: bool=True):
        """
        A card with just one field of body text. Supports an optional underline/accent item.
        
        :param str filename: Path to the output file
        :param str text: Value of the text in the body
        :param path font_path: Path to the font for the body text
        :param int font_size: Size of the font (Default: 50)
        :param tuple font_color: Tuple (R, G, B, A) to represent the color of the body text (Default: (0, 0, 0, 1))
        :param int h_align: How elements should be aligned horizontally (left, center, right) (Default: left)
        :param int v_align: How elements should be aligned verticall (top, middle, bottom) (Default: top)
        :param tuple bg_color: Tuple (R, G, B, A) to represent the background color (Detault: (1, 1, 1, 1)
        :param int rounded_corners: Integer number for the radius (px) of the rounded corners of the card (Default: 0)
        :param int margin: Shorthand to set margin x and margin y to the same
        :param int margin_x: Percentage for x margin (Default: 10)
        :param int margin_y: Percentage for y margin (Default: 20)        
        :param tuple resolution: The resolution of the card (Default: (1920, 1080))
        :param path divider: Path to an image or SVG
        :param bool auto_height: Whether to automatically determine the height of the card
        """
        super().__init__(filename, bg_color, rounded_corners, margin, margin_x, margin_y, resolution)
        self.body_text = TextField(text, font_path, font_size, font_color, h_align, v_align)
        if auto_height:
            self.auto_height()
        #TODO Divider

    @property
    def body_text(self):
        return self._body_text

    @body_text.setter
    def body_text(self, txt: TextField):
        self._body_text = txt
        self._real_body = pixie.SeqSpan()
        self._real_body.append(pixie.Span(text=txt.text, font=txt.font))

    def auto_height(self):
        content_width = self.resolution[0] - 2 * (self.resolution[0] * (self.margin[0] / 100))
        arrangement = self._real_body.typeset(bounds=pixie.Vector2(content_width, 1))
        text_height = arrangement.layout_bounds().y
        content_height = text_height
        #TODO Divider
        # If divider, add divider + its margin to content_height
        if self._divider:
            pass


        # We're trying to find real height based on the content height and margin percentage.
        # If we want a 10% margin, then we want the content height to be 80% of the real height (because 10% on both top and bottom)
        # So, to work backwards, we can't multiply "real height * content percentage", so we divide "content height / 2 * margin percentage"

        self._res_y = round(content_height / (1 - (2 * self.margin[1] / 100)))

    def render(self):
        image, context = self._init_image()

        real_margins = (self.resolution[0] * self.margin[0] / 100, self.resolution[1] * self.margin[1] / 100)
        real_bounds = (self.resolution[0] - (real_margins[0] * 2), self.resolution[1] - (real_margins[1] * 2))

        image.arrangement_fill_text(
            self._real_body.typeset(
                bounds = pixie.Vector2(*real_bounds),
                h_align = self.body_text.h_align,
                v_align = self.body_text.v_align
            ),
            transform = pixie.translate(*real_margins)
        )

        image.write_file(self.filename)
