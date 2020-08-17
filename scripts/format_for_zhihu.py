import re
import argparse
import chardet


def formula_ops(_lines):
    _lines = re.sub(
        r"((.*?)\$\$)(\s*)?([\s\S]*?)(\$\$)\n",
        r'\n<img src="https://www.zhihu.com/equation?tex=\\4" alt="\\4" class="ee_img tr_noresize" eeimg="1">\n',
        _lines,
    )
    _lines = re.sub(
        r"(\$)(?!\$)(.*?)(\$)",
        r' <img src="https://www.zhihu.com/equation?tex=\\2" alt="\\2" class="ee_img tr_noresize" eeimg="1"> ',
        _lines,
    )
    return _lines


def main():
    parser = argparse.ArgumentParser("Input file path with --input=")
    parser.add_argument("--input", type=str)

    args = parser.parse_args()
    if args.input is None:
        exit()

    with open(str(args.input), "rb") as f:
        s = f.read()
        chatest = chardet.detect(s)
    print(chatest, chatest['encoding'])

    with open(str(args.input), "r", encoding=chatest['encoding']) as f:
        lines = f.read()
        lines = formula_ops(lines)
        with open(
            str(args.input) + ".zhihu.md", "w+", encoding=chatest['encoding']
        ) as fw:
            fw.write(lines)

    print("Success!")


if __name__ == "__main__":
    main()
