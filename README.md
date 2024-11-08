# BannerPy

![BannerPy logo](logo.svg)

## Introduction

BannerPy is a library built on [pixie-python](https://github.com/treeform/pixie-python) for programatically generating "cards" that can be used for visual media (video, images, promotional material). BannerPy was built with on-screen assets for video production in mind. You can generate name cards, notes/sidebars, on-screen citations, and more.

## Examples

### Name card
![Name card](example/template_card.png)

<details><summary>Code</summary>

Python

```py
values = {
  "name": "Dr. Joe Garcia",
  "title": "Political science professor",
  "organization": "Harvard University, MA"
}

test_card = cards.TemplateCard(template='example/example_template.yml', filename='example/template_card.png', **values)

test_card.render()
```

Template (YAML)

```yaml
---
color_type:
fonts:
  dejavusans: /path/to/fonts/DejaVuSans.ttf
  silvertones: /path/to/fonts/Silvertones.ttf
bg_color: "#ffffff"
border_radius: 50
margin_x: 15
margin_y: 20
resolution:
  - 1920
  - 1080
auto_height: true
fields:
  name:
    type: text
    font: silvertones
    font_size: 200
    font_color: "#2b361b"
    h_align: center
    v_align: top # or middle or bottom
    margin_x: 0
    margin_y: 0
    variable: true
  divider:
    type: image
    value: /path/to/long-squiggle.png
    #scale: 1
    margin_x: 0
    margin_y: 15
    variable: false
  title:
    type: text
    font: dejavusans
    font_size: 100
    font_color: "#191515"
    h_align: center
    variable: true
  organization:
    type: text
    font: dejavusans
    font_size: 70
    font_color: "#191515"
    h_align: center
    variable: true
```

</details>

### On-screen citation
![citation](example/simple_with_underline.png)

<details><summary>Code</summary>

Python

```python
test_card = cards.Card('example/simple_with_underline.png', margin_x = 8, margin_y = 15, border_radius = 100)

title = fields.TextField('(Groth et al., 2011)', fonts['dejavusans'], 130, margin_y = 5, h_align=pixie.CENTER_ALIGN)
underline = fields.Image('example/short-squiggle.png', margin_x = 20, margin_y = 20)

test_card.fields = [title, underline]

test_card.render()
```

</details>

### Section heading
![heading](example/simple_heading.png)

<details><summary>Code</summary>

Python

```python
test_card = cards.Card('example/simple_heading.png', bg_color=(0.235, 0.549, 0.255, 0.9), border_radius = 125, margin_y = 25)

heading = fields.TextField('Part 1', '/path/to/fonts/GROBOLD.ttf', 150, font_color = (0, 0, 0, 0.7), h_align=pixie.CENTER_ALIGN)
subheading = fields.TextField('Introduction', '/path/to/fonts/DejaVuSans.ttf', 100, font_color = (0, 0, 0, 0.7), h_align=pixie.CENTER_ALIGN)

test_card.append(heading)
test_card.append(subheading)

test_card.render()
```

</details>

### Disclaimer
![disclaimer](example/simple.png)

<details><summary>Code</summary>

Python

```python
test_card = cards.Card('example/simple.png', margin_x=5, margin_y=35, border_radius=20, bg_color=(0.4, 0.1, 0.2, 0.8))
    
body = fields.TextField('These results are not definitive. Further research is necessary to determine definitive results.', '/path/to/fonts/DejaVuSans.ttf', 30, font_color=(0, 0, 0, 0.6))

test_card.fields = [body]

test_card.render()
```

</details>

## Technical overview

BannerPy has 4 main parts:
- [Card class](#Card-class)
- [TemplateCard class](#TemplateCard-class)
- `TextField` class
- `Image` class

### Card class

The `Card` class is the heart of BannerPy. It takes parameters, a list of `Field` objects, and then generates the card image with the `render()` method

#### Parameters

- `filename` (str): Path to the output file
- `bg_color` (tuple): Tuple (R, G, B, A) to represent the background color (Detault: `(1, 1, 1, 1)`)
- `border_radius` (int): Integer number for the radius (px) of the rounded corners of the card (Default: `0`)
- `margin` (int): Shorthand to set margin x and margin y to the same
- `margin_x` (int): Percentage for x margin for the content area (Default: `10`)
- `margin_y` (int): Percentage for y margin for the content area (Default: `20`)
- `resolution` (tuple): The resolution of the card (Default: `(1920, 1080)`)
- `fields` (list[Field]): A list of Fields to populate the card. (Default: `[]`)
- `auto_height` (bool): Whether to automatically determine the height of the card (Default: `True`)

#### Methods
Setter and getter methods are excluded, as well as internal methods

- `auto_height()`: Calculate the y resolution of the card based on the contents of `fields`. This is automatically run when `auto_height` is enabled at initialization
- `append(field: Field)`: Append a Field (TextField, Image) object to the card's `fields` property
- `render()`: Render the image

### TemplateCard class

The TemplateCard class is based on the Card class. It takes in a path to a yaml file and loads those settings. In addition to the template config, you also need to provide the `filename` and the values to fill in the template

#### Parameters

- `template` (str): Path to the YAML file to load
- `filename` (str): Path to the output file
- `**kwargs`: Arguments that match the variables in your template file. For example, if you have a `body_text` field in your template, kwargs would include `body_text = "text value"`

#### Methods

Same as `Card` class

#### Templates

Below is the outline of a YAML template, with notes

<details><summary>YAML template specification</summary>

Notes:
- For text fields, you *can* use the `font_path` argument instead of `font`. `font` is supported as a convenience for reusing fonts across different fields.
- All string fields are case insensitive
- Hex colors do not support transparency. They must be 6-digit hex codes.

```yml
---
color_type: "hex" #"hex" or "tuple"
# "hex" or "tuple". If "hex", the hex colors will be translated to the native pixie RGBA format

fonts:
  dejavusans: /run/current-system/sw/share/X11/fonts/DejaVuSans.ttf
  silvertones: /home/bean/.local/share/fonts/Silvertones.ttf
# A list of dicts for font paths. An example is given below.

bg_color: "#ffffff"
# bg_color: [1, 1, 1, 1]
# Hex color (str) or list of R, G, B, A values

border_radius: 50
# Border radius in pixels

margin_x: 15
# Margin x as a percentage for the content area

margin_y: 20
# Margin y as a percentage for the content area

resolution: [1920, 1080]
# List (x, y) of resolution values

auto_height: true
# Boolean whether or not auto_height is enabled on the card

fields:
# Dict of fields

  name:
  # Here, "name" is a KEY. This is the same key you will use to fill in the "value" field when you apply the template. Name this key whatever you like.

    type: text
    # "text" or "image". This designates this field as a TextField

    font: silvertones
    # Use the "silvertones" font from the fonts we declared at the beginning

    # font_path = /home/bean/.local/share/fonts/Silvertones.ttf
    # Path directly to a font

    font_size: 200
    # Font size of the TextField

    font_color: "#2b361b"
    # Font color of the TextField

    h_align: center
    # "center", "left", or "right". Text field justification

    v_align: top # or middle or bottom
    # "top", "middle", or "bottom". Text field vertical justification.

    margin_x: 0
    margin_y: 0
    # Margin (as a percentage) to be applied relative to the field.

    variable: true
    # Whether or not the value field is variable. When enabled, `value` will be filled by TemplateCard when it's rendered.
    # For example, you may want this set to false if you want a template that always has a title at the top saying your brand name or something.

  divider:
  # As before, this is a key
    type: image
    value: /home/bean/Nextcloud/beanstem/long-squiggle.png
    # Value for the `Field` object. In images fields, this is the image path, and in text fields this is the text value

    scale: 1
    # Manually set scale and disable auto scaling. Auto scaling is enabled if this argument is ommitted.

    margin_x: 0
    margin_y: 15
    variable: false
    # See? Here's an example where the field is totally static, so we set "variable" to false. Now we don't have to supply a value to this field when we render.

  title:
    type: text
    font: dejavusans
    font_size: 100
    font_color: "#191515"
    h_align: center
    variable: true

  organization:
    type: text
    font: dejavusans
    font_size: 70
    font_color: "#191515"
    h_align: center
    variable: true
```

</details>

TODO: Write more documentation on the Field objects. It's kiiinda self-explanatory though, you can figure it out.
