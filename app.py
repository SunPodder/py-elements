from flask import Flask, Response
import json, re


app = Flask(__name__)
table = json.loads(open("table.json", "r").read())["elements"]


def getElement(arg):
    if type(arg) == int:
        el = table[arg]
    else:
        el = [x for x in table if x["name"] == arg][0]
    return el


def hexToRGB(hex) -> tuple[int, int, int]:
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def superscript_electron_config(config):
    pattern = r"(?<=s|p|d|f)\d+"  
    def sup(match):
        return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[int(i)] for i in match.group(0)])
    return re.sub(pattern, sup, config)


def prettyPrint(el: dict[str, str]):
    name_color = "\x1b[38;2;255;203;5m"  # yellow
    number_color = "\x1b[38;2;51;153;255m"  # blue
    mass_color = "\x1b[38;2;255;102;204m"  # magenta
    phase_color = "\x1b[38;2;102;255;102m"  # green
    category_color = "\x1b[38;2;255;102;0m"  # red
    appearance_color = "\x1b[38;2;102;255;102m"  # greenish
    density_color = "\x1b[38;2;255;153;51m"  # orange
    boiling_color = "\x1b[38;2;255;0;127m"  # pink
    config_color = "\x1b[38;2;200;150;255m"  # purple
    summary_color = "\x1b[38;2;255;255;255m"  # white
    link_color = "\x1b[38;2;255;200;0m"  # yellowish
    ENDC = "\x1b[0m"  # reset color

    # the data contains different colors for each element
    # however, sticking to one color scheme is better for readability
    # colorize for true color terminals
    # R, G, B = hexToRGB(el["cpk-hex"])
    # print(R, G, B)

    config = el["electron_configuration_semantic"]
    config = superscript_electron_config(config)

    return f"""
{name_color}Name: {el["name"]} ({el["symbol"]}){ENDC}
{number_color}Atomic number: {el["number"]}{ENDC}
{mass_color}Atomic mass: {el["atomic_mass"]}{ENDC}
{phase_color}Phase: {el["phase"]}
{category_color}Category: {el["category"]}
{appearance_color}Appearance: {el.get("appearance", "N/A")}
{density_color}Density: {el.get("density", "N/A")}
{boiling_color}Boiling point: {el.get("boil", "N/A")}
{config_color}Electron configuration: {config}{ENDC}
{summary_color}Summary: {el.get("summary", "N/A")}
{link_color}More info: {el["source"]}
"""
    

@app.route('/')
def index():
    return "Usage: curl <url>/<element name or number>\nGithub: https://github.com/SunPodder/py-elements"


@app.route("/<string:name>")
def fromName(name):
    el = getElement(name)
    if el is None:
        return "Invalid element name"
    r = prettyPrint(el)
    res = Response(r)
    res.headers["Content-Type"] = "text/plain; charset=utf-8"
    return res


@app.route("/<int:number>")
def fromNumber(number):
    el = getElement(number)
    if el is None:
        return "Invalid element number"
    r = prettyPrint(el)
    res = Response(r)
    res.headers["Content-Type"] = "text/plain; charset=utf-8"
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
