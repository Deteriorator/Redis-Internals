# coding = utf8
import os
import re


def replace_func(match):
    full_text = match.group(0)
    if "127.0.0.1" in full_text:
        lang = "shell script"
    else:
        lang = "c"
    if full_text[-2] != "\n":
        full_text += "\n"
    middle = full_text[1:-2]
    final_middle = ""
    for line in middle.split("\n"):
        if line:
            if line[0] == "\t":
                skip_index = 1
            else:
                skip_index = 4
            final_middle += line[skip_index:] + "\n"
        else:
            final_middle += "\n"
    full_text = full_text[0] + "\n```" + lang + final_middle + "\n```" + full_text[-2:]
    return full_text


def replace(text):
    r = re.sub("\n\n((((?:\t|    ).+?\n)|\n)+)(?:\n(?!\t|    )|$)", replace_func, text, flags=re.DOTALL)
    return r


def replace_all():
    for each in os.walk("./"):
        if each[2]:
            for each_file in each[2]:
                suffix = each_file.split(".")[-1]
                if suffix == "md":
                    full_file = each[0] + os.path.sep + each_file
                    with open(full_file, "r") as f:
                        text = f.read()
                    replaced_text = replace(text)
                    with open(full_file, "w") as f:
                        f.write(replaced_text)
                    print("replaced: %s" % (full_file, ))


if __name__ == "__main__":
    replace_all()
