import pixie as _pixie

class Field:
    TYPE="null"

    margin_x = 0
    margin_y = 0

    def __init__(self, margin_x: int=0, margin_y: int=0):
        self.margin_x = margin_x
        self.margin_y = margin_y

class Image(Field):
    TYPE="image"

    img = None
    scale = 1
    _path = ""
    _auto_scale_enabled = True

    def __init__(self, path: str, scale: float=None, margin_x: int=0, margin_y: int=0, auto_scale: bool=True):
        """
        :param str path: Path to an image or SVG
        :param float scale: Number to scale the image evenly (Default: 1)
        :param int margin_x: Additional margin for x (left and right) as a percentage of the field width (Default: 0)
        :param int margin_y: Additional margin for y (top and bottom) as a percentage of the field height (Default: 0)
        :param bool auto_scale: Whether to automatically scale the image if possible (Default: True)
        """
        super().__init__(margin_x, margin_y)
        self.path = path
        if scale:
            self.scale = scale
            self._auto_scale_enabled = False
        else:
            self.scale = 1
            self._auto_scale_enabled = auto_scale

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
        self.img = _pixie.read_image(path)
        self._path = path

    def auto_scale(self, max_width: int, max_height: int):
        """
        Provide a max width and height container for the image and automatically set the scale property to fit within the container
        """
        delta_width = abs(max_width - self.img.width)
        delta_height = abs(max_height - self.img.height)
        if delta_width > delta_height:
            self.scale = max_width / self.img.width
        else:
            self.scale = max_height / self.img.height

class TextField(Field):
    TYPE="text"
    
    font = None
    _text = ""
    _font_path = ""
    _font_color = ()
    _h_align = 0
    _v_align = 0
    _span = None

    def __init__(self, text: str, font_path: str, font_size: int=12, font_color: tuple=(0, 0, 0, 1), h_align: int=0, v_align: int=0, margin_x: int=0, margin_y: int=0):
        """
        :param str text: Text value for the field
        :param str font_path: Path to the font to load
        :param int font_size: Font size
        :param tuple font_color: 4-field tuple (R, G, B, A) to represent the font color
        :param int h_align: Enum for horizontal text alignment (see [pixie enums](https://github.com/treeform/pixie-python/blob/master/src/pixie/pixie.py#L87)) (Default: 0, left)
        :param int v_align: Enum for vertical text alignment (see [pixie enums](https://github.com/treeform/pixie-python/blob/master/src/pixie/pixie.py#L87)) (Default: 0, top)
        :param int margin_x: Additional margin for x (left and right) as a percentage of the field width (Default: 0)
        :param int margin_y: Additional margin for y (top and bottom) as a percentage of the field height (Default: 0)
        """
        super().__init__(margin_x, margin_y)
        self._span = _pixie.SeqSpan()        
        self._text = text
        self.font_path = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.h_align = h_align
        self.v_align = v_align

    def _update_span(self):
        self._span.clear()
        self._span.append(_pixie.Span(text=self.text, font=self.font))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        self._update_span()
        
    @property
    def font_path(self):
        return self._font_path

    @font_path.setter
    def font_path(self, font_path: str):
        # If this is already set, we need to preserve the size and paint to reload it when the new font face is loaded
        changing = bool(self.font)
        if changing:
            tmp_size = self.font.size
            tmp_paint = self.font.paint
        self.font = _pixie.read_font(font_path)
        if changing:
            self.font.size = tmp_size
            self.font.paint = tmp_paint
            
        self._update_span()
        self._font_path = font_path
    
    @property
    def font_size(self):
        """Font size"""
        return self.font.size

    @font_size.setter
    def font_size(self, size: int):
        self.font.size = size
        self._update_span()

    @property
    def font_color(self):
        """Text color"""
        return self._font_color

    @font_color.setter
    def font_color(self, color: tuple):
        self.font.paint.color = _pixie.Color(*color)
        self._font_color = color
        self._update_span()

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
