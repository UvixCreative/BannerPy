import pixie as _pixie
from .fields import Field as _Field
from .fields import TextField as _TextField
from .fields import Image as _Image

class Card:
    _res_x = 10
    _res_y = 10
    _filename = ""
    _bg_color = ()
    _rounded_corners = 0
    _margin_x = 10
    _margin_y = 20
    _content_width = 10
    _content_height = 10

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


    def _update_content_res(self):
        self._content_width = self._res_x - 2 * (self._res_x * (self._margin_x/100))
        self._content_height = self._res_y - 2 * (self._res_y * (self._margin_y/100))        
        
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
        self._update_content_res()

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color: tuple):
        self._bg_color = _pixie.Color(*color)

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
        self._update_content_res()        

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
        self._update_content_res()

    def _init_image(self):
        """
        Render the background, return the image and the context
        """
        image = _pixie.Image(self._res_x, self._res_y)
        ctx = image.new_context()

        paint = _pixie.Paint(_pixie.SOLID_PAINT)
        paint.color = self.bg_color
        ctx.fill_style = paint

        ctx.rounded_rect(0, 0, *self.resolution, self.rounded_corners, self.rounded_corners, self.rounded_corners, self.rounded_corners)
        ctx.fill()

        return image, ctx
        
    def render(self):
        image, context = self._init_image()
        image.write_file(self.filename)

class ComplexCard(Card):
    _fields = ()
    _auto_height_enabled = True

    def __init__(self, filename: str, bg_color: tuple=(1, 1, 1, 1), rounded_corners: int=0, margin: int=None, margin_x: int=10, margin_y: int=20, resolution: tuple=(1920, 1080), fields: list=[], auto_height: bool=True):
        """
        Provide any number of Field objects to the card in a list and generate a card. Currently only supports vertical alignment. 
        
        :param str filename: Path to the output file
        :param tuple bg_color: Tuple (R, G, B, A) to represent the background color (Detault: (1, 1, 1, 1)
        :param int rounded_corners: Integer number for the radius (px) of the rounded corners of the card (Default: 0)
        :param int margin: Shorthand to set margin x and margin y to the same
        :param int margin_x: Percentage for x margin for the content area (Default: 10)
        :param int margin_y: Percentage for y margin for the content area (Default: 20)
        :param tuple resolution: The resolution of the card (Default: (1920, 1080))
        :param list fields: A list of Fields to populate the card.
        :param bool auto_height: Whether to automatically determine the height of the card
        """

        super().__init__(filename, bg_color, rounded_corners, margin, margin_x, margin_y, resolution)
        self.fields = fields
        self._auto_height_enabled = auto_height

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields: list[_Field]):
        self._fields = fields
        if self._auto_height_enabled:
            self.auto_height()
        
    def append(self, field: _Field):
        self.fields.append(field)
        if self._auto_height_enabled:
            self.auto_height()

    def auto_height(self):
        content_height = 0
        for field in self.fields:
            field_height = 0
            if field.TYPE == "text":
                arrangement = field._span.typeset(bounds=_pixie.Vector2(self._content_width, 1))
                field_height = arrangement.layout_bounds().y
            elif field.TYPE == "image":
                if field._auto_scale_enabled:
                    field.auto_scale(self._content_width, field.img.height) # This isn't perfect. Obviously. It's intended to support scaling to fit x, not y.
                field_height = field.img.height * field.scale
            else:
                raise Exception('Unknown field type! Panicking!!!')

            content_height += field_height
            # Add the per-field margin!
            content_height += field_height * (2 * field.margin_y / 100)

        # We're trying to find real height based on the content height and margin percentage.
        # If we want a 10% margin, then we want the content height to be 80% of the real height (because 10% on both top and bottom)
        # So, to work backwards, we can't multiply "real height * content percentage", so we divide "content height / 2 * margin percentage"
        self._res_y = round(content_height / (1 - (2 * self.margin_y / 100))) + 1
        self._content_height = content_height

    def render(self):
        image, context = self._init_image()

        margin_offset = (self._res_x * self.margin_x / 100, self._res_y * self.margin_y / 100)
        bounds = (self._content_width, self._content_height)

        y_offset = margin_offset[1]
        for field in self.fields:
            if field.TYPE == "text":
                arrangement = field._span.typeset(
                        bounds = _pixie.Vector2(*bounds),
                        h_align = field.h_align,
                        v_align = field.v_align
                )
                text_height = arrangement.layout_bounds().y
                y_offset += text_height * (field.margin_y / 100) # add top margin before filling text
                
                image.arrangement_fill_text(
                    arrangement,
                    transform = _pixie.translate(margin_offset[0], y_offset)
                )

                y_offset += text_height + (text_height * field.margin_y / 100) # Offset for real height + bottom margin
            elif field.TYPE == "image":
                if field._auto_scale_enabled:
                    field.auto_scale(self._content_width, field.img.height) # Again, not perfect.

                #resize
                resize_x = int(field.img.width * field.scale)
                resize_y = int(field.img.height * field.scale)
                tmp_img = field.img.resize(resize_x, resize_y)

                y_offset += tmp_img.height * (field.margin_y / 100) # add top margin before printing image

                #move
                translate_x = (self._res_x - tmp_img.width) / 2 # center, doesn't support other justification types right now. TODO?
                translate_y = y_offset # TODO: See if I need to add "half the image height" or something to center it properly
                image.draw(
                    tmp_img,
                    transform=_pixie.translate(translate_x, translate_y)
                )
                y_offset += tmp_img.height + (tmp_img.height * (field.margin_y / 100)) # Offset for real height + bottom margin
            else:
                raise Exception('Unknown field type! Panicking!!!')

        image.write_file(self.filename)
    
                         

class SimpleCard(Card):
    _divider = None
    _divider_scale_factor = None
    
    def __init__(self, filename: str, text: str, font_path: str, font_size: int=50, font_color: tuple=(0, 0, 0, 1), h_align: int=0, v_align: int=0, bg_color: tuple=(1, 1, 1, 1), rounded_corners: int=0, margin: int=None, margin_x: int=10, margin_y: int=20, resolution: tuple=(1920, 1080), divider=None, divider_scale=None, auto_height: bool=True):
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
        :param float divider_scale: Scale factor for the divider
        :param bool auto_height: Whether to automatically determine the height of the card
        """
        super().__init__(filename, bg_color, rounded_corners, margin, margin_x, margin_y, resolution)
        self.body_text = _TextField(text, font_path, font_size, font_color, h_align, v_align)
        if divider:
            self.divider = divider
        if divider_scale:
            self.divider_scale = divider_scale            
        if auto_height:
            self.auto_height()

    @property
    def body_text(self):
        return self._body_text

    @body_text.setter
    def body_text(self, txt: _TextField):
        self._body_text = txt
        self._real_body = _pixie.SeqSpan()
        self._real_body.append(_pixie.Span(text=txt.text, font=txt.font))

    @property
    def divider(self):
        return self._divider

    @divider.setter
    def divider(self, path: str):
        self._divider = _pixie.read_image(path)
        if not self._divider_scale_factor:
            self._divider_scale_factor = self._content_width / self._divider.width

    @property
    def divider_scale(self):
        return self._divider_scale_factor

    @divider_scale.setter
    def divider_scale(self, scale: float):
        self._divider_scale_factor = scale

    def auto_height(self):
        arrangement = self._real_body.typeset(bounds=_pixie.Vector2(self._content_width, 1))
        text_height = arrangement.layout_bounds().y
        content_height = text_height
        
        # If divider, add divider + its margins to content_height
        # NOTE: margins is 2x margin percentage times content height (not total height)
        if self._divider:
            divider_height = self.divider.height * self.divider_scale
            content_height += (content_height * 2 * (self._margin_y/100)) + divider_height

        # We're trying to find real height based on the content height and margin percentage.
        # If we want a 10% margin, then we want the content height to be 80% of the real height (because 10% on both top and bottom)
        # So, to work backwards, we can't multiply "real height * content percentage", so we divide "content height / 2 * margin percentage"
        self._res_y = round(content_height / (1 - (2 * self.margin[1] / 100)))
        self._content_height = content_height

    def render(self):
        image, context = self._init_image()

        real_margins = (self.resolution[0] * self.margin[0] / 100, self.resolution[1] * self.margin[1] / 100)
        real_bounds = (self.resolution[0] - (real_margins[0] * 2), self.resolution[1] - (real_margins[1] * 2))

        image.arrangement_fill_text(
            self._real_body.typeset(
                bounds = _pixie.Vector2(*real_bounds),
                h_align = self.body_text.h_align,
                v_align = self.body_text.v_align
            ),
            transform = _pixie.translate(*real_margins)
        )

        if self.divider:
            #resize
            resize_x = int(self.divider.width * self.divider_scale)
            resize_y = int(self.divider.height * self.divider_scale)
            self._divider = self.divider.resize(resize_x, resize_y)

            #move
            translate_x = (self.resolution[0] - self.divider.width) / 2
            translate_y = real_margins[1] + self._content_height - self.divider.height
            image.draw(
                self.divider,
                transform=_pixie.translate(translate_x, translate_y)
            )

        image.write_file(self.filename)
