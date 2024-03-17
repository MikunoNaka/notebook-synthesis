import click

MAX_WIDTH = 75

# works like pop but at the first index
def _pop(arr):
    x = arr[0]
    del arr[0]
    return x

# TODO: handle words longer than 75 chars
def split_line(line, max_width=MAX_WIDTH):
    if len(line) <= max_width:
        return [line]
    else:
        split = []
        
        s = ""
        for word in line.split():
            if len(s) == 0 and len(word) <= max_width:
                s = word
            elif (len(s) + len(word) + 1) <= max_width:
                s = s + " " + word
            else:
                split.append(s)
                s = word

        split.append(s)

        return split

def word_wrap(lines, max_width):
    if len(lines) > 1:
        return split_line(lines[0], max_width) + word_wrap(lines[1:], max_width)
    else:
        return split_line(lines[0], max_width)


@click.command()
@click.argument('input_file')
@click.option('--max-width', default=MAX_WIDTH)
@click.option('--stdout', is_flag=True, help="Print output to STDOUT instead of output file")
@click.argument('output_file', default=f"./formatted.txt")

def main(input_file, max_width, stdout, output_file):
    _input = open(input_file, "r")
    lines = _input.read().splitlines()

    if max_width > MAX_WIDTH:
        print(f"Error: max-width cannot be greater than {MAX_WIDTH}.")
        exit(1)

    wrapped = word_wrap(lines, max_width)
    if stdout:
        for i in wrapped:
            print(i)
    else:
        print(f"Writing to file {output_file}")
        _output = open(output_file, "w")
        _output.writelines(l + "\n" for l in wrapped)
        _output.close()

    _input.close()


if __name__ == "__main__":
    main()
