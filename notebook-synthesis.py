import shutil
import subprocess
import string
import random
import os
import click

@click.command()
@click.argument('input_file')
@click.option('--bias', default=.75, help="The default is .75. That seems to work. Experiment with other numbers, I dunno.")
@click.option('--width', default=1, help="Default is 1. This is the width of the pen stroke.")
@click.option('--style', default=3, help="This is the various styles of writing. The options are 1 - 9")
@click.option('--pen-color', default="#005fd7", help="Pen color")
@click.argument('output_file', default=f"./generated.pdf")

# TODO: add pen color flag
def generate(input_file, bias, width, style, pen_color, output_file):
    # this keeps from generating useless logs when --help is used
    from handwriting_synthesis import Hand
    hand = Hand()

    if output_file[-4:] != ".pdf":
        output_file += ".pdf"

    # random string for the temporary directory name
    _dir = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    _input = open(input_file, "r")
    lines = _input.read().splitlines()

    # split lines into groups of at most 25
    pages = [lines[x:x+25] for x in range(0, len(lines), 25)]

    # create a directory to temporarily store SVGs
    print(f"Created directory ./{_dir}")
    os.mkdir(_dir)
    
    count = 0
    for page in pages:
        biases = [bias for i in page]
        styles = [style for i in page]
        stroke_colors = [pen_color for i in page]
        stroke_widths = [width for i in page]

        hand.write(
            filename=f"./{_dir}/page{count}.svg",
            lines=page,
            biases=biases,
            styles=styles,
            stroke_colors=stroke_colors,
            stroke_widths=stroke_widths
        )

        # add background and page rulings to svg using imagemagick
        subprocess.run(["magick", "convert", "canvas.png", "(" , f"./{_dir}/page{count}.svg", "-resize", "2133x3327", ")", "-geometry", "+309+172", "-composite", "(", "printings.png", ")", "-resize", "2480x3508", "-composite", f"./{_dir}/page{count}.png"])

        count += 1

    # generate pdf
    subprocess.run(["convert"] + [f"./{_dir}/page{i}.png" for i in range(count)] + [output_file])

    # remove directory containing SVGs
    shutil.rmtree(_dir)

if __name__ == "__main__":
    generate()
