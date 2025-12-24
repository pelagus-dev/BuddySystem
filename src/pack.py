def load(input_list):
    number_string = ''
    rid, lat, lon, loaded, heavy, convoy_size = input_list
    number_string += str(rid).zfill(3)
    quadrant = 0

    # i swear the order of these is not political, it's just numerical
    # don't need more Mercator projection kind of discourse
    if (lat > 0 and lon > 0):
        quadrant = 1
    elif (lat > 0 and lon < 0):
        quadrant = 2
    elif (lat < 0 and lon > 0):
        quadrant = 3
    elif (lat < 0 and lon < 0):
        quadrant = 4
    number_string += str(quadrant)

    # maul lat and lon into number strings so that we can, you guessed it...
    lat, lon = str(abs(lat)), str(abs(lon))
    lat = lat.replace('.','')
    lon = lon.replace('.','')
    lat.zfill(7)
    lon.zfill(8)

    # ... add 'em to the string
    number_string += (lat + lon)

    # again, this is subjective and based on the "bigness" of the vehicle
    veh_type = 0
    if (loaded == 1 and heavy == 1):
        veh_type = 4
    elif (loaded == 0 and heavy == 1):
        veh_type = 3
    elif (loaded == 1 and heavy == 0):
        veh_type = 2
    elif (loaded == 0 and heavy == 0):
        veh_type = 1
    
    number_string += str(veh_type)

    number_string += str(convoy_size)

    print(len(number_string))
    print(number_string)
    return number_string

def unload(number_string):
    rid = int(number_string[0:3].lstrip('0'))
    quadrant = int(number_string[3])

    lat = number_string[4:11]
    lon = number_string[11:18]
    lat = float(lat[0:2] + '.' + lat[2:])
    lon = float(lon[0:3] + '.' + lon[3:])

    if (quadrant > 2):
        lat = -lat
    if (quadrant == 2 or quadrant == 4):
        lon = -lon

    veh_type = int(number_string[18])
    if (veh_type == 4):
        loaded = 1
        heavy = 1
    elif (veh_type == 3):
        loaded = 0
        heavy = 1
    elif (veh_type == 2):
        loaded = 1
        heavy = 0
    elif (veh_type == 1):
        loaded = 0
        heavy = 0
    
    convoy_size = int(number_string[19])
    return [rid, lat, lon, loaded, heavy, convoy_size]

def compress(number_string):
    """Compress a string of decimal digits into ascii. Accepts only strings of digits 0-9. Returns cursed ASCII text."""
    ct = {
    "00": "d",
    "01": "e",
    "02": "f",
    "03": "g",
    "04": "h",
    "05": "i",
    "06": "j",
    "07": "k",
    "08": "l",
    "09": "m",

    "10": "n",
    "11": "o",
    "12": "p",
    "13": "q",
    "14": "r",
    "15": "s",
    "16": "t",
    "17": "u",
    "18": "v",
    "19": "w",

    "20": "x",
    "21": "y",
    "22": "z",
    "23": "{",
    "24": "|",
    "25": "}",
    "26": "~",
    "27": "]",
    "28": "^",
    "29": "_",

    "30": "`",
    "31": "a",
    "32": "b",

    "33": "!",
    "34": '"',
    "35": "#",
    "36": "$",
    "37": "%",
    "38": "&",
    "39": "'",

    "40": "(",
    "41": ")",
    "42": "*",
    "43": "+",
    "44": ",",
    "45": "-",
    "46": ".",
    "47": "/",
    "48": "0",
    "49": "1",

    "50": "2",
    "51": "3",
    "52": "4",
    "53": "5",
    "54": "6",
    "55": "7",
    "56": "8",
    "57": "9",
    "58": ":",
    "59": ";",

    "60": "<",
    "61": "=",
    "62": ">",
    "63": "?",
    "64": "@",
    "65": "A",
    "66": "B",
    "67": "C",
    "68": "D",
    "69": "E",

    "70": "F",
    "71": "G",
    "72": "H",
    "73": "I",
    "74": "J",
    "75": "K",
    "76": "L",
    "77": "M",
    "78": "N",
    "79": "O",

    "80": "P",
    "81": "Q",
    "82": "R",
    "83": "S",
    "84": "T",
    "85": "U",
    "86": "V",
    "87": "W",
    "88": "X",
    "89": "Y",

    "90": "Z",
    "91": "[",
    "92": "c",
    "93": "\x05",
    "94": "\x06",
    "95": "\x11",
    "96": "\x12",
    "97": "\x13",
    "98": "\x14",
    "99": "\x16",
    }
    compresso = ''
    for i in range(len(number_string)-1):
        if (i % 2 == 0):
            key = str(number_string[i]) + str(number_string[i+1])
            compresso += ct[key]

    return compresso

def extract(ascii_string):
    """Extracts the decimal digit string from compressed cursed ASCII."""
    et = {
    "d": "00",
    "e": "01",
    "f": "02",
    "g": "03",
    "h": "04",
    "i": "05",
    "j": "06",
    "k": "07",
    "l": "08",
    "m": "09",
    "n": "10",
    "o": "11",
    "p": "12",
    "q": "13",
    "r": "14",
    "s": "15",
    "t": "16",
    "u": "17",
    "v": "18",
    "w": "19",
    "x": "20",
    "y": "21",
    "z": "22",
    "{": "23",
    "|": "24",
    "}": "25",
    "~": "26",
    "]": "27",
    "^": "28",
    "_": "29",
    "`": "30",
    "a": "31",
    "b": "32",
    "!": "33",
    '"': "34",
    "#": "35",
    "$": "36",
    "%": "37",
    "&": "38",
    "'": "39",
    "(": "40",
    ")": "41",
    "*": "42",
    "+": "43",
    ",": "44",
    "-": "45",
    ".": "46",
    "/": "47",
    "0": "48",
    "1": "49",
    "2": "50",
    "3": "51",
    "4": "52",
    "5": "53",
    "6": "54",
    "7": "55",
    "8": "56",
    "9": "57",
    ":": "58",
    ";": "59",
    "<": "60",
    "=": "61",
    ">": "62",
    "?": "63",
    "@": "64",
    "A": "65",
    "B": "66",
    "C": "67",
    "D": "68",
    "E": "69",
    "F": "70",
    "G": "71",
    "H": "72",
    "I": "73",
    "J": "74",
    "K": "75",
    "L": "76",
    "M": "77",
    "N": "78",
    "O": "79",
    "P": "80",
    "Q": "81",
    "R": "82",
    "S": "83",
    "T": "84",
    "U": "85",
    "V": "86",
    "W": "87",
    "X": "88",
    "Y": "89",
    "Z": "90",
    "[": "91",
    "c": "92",
    "\x05": "93",
    "\x06": "94",
    "\x11": "95",
    "\x12": "96",
    "\x13": "97",
    "\x14": "98",
    "\x16": "99",
    }

    extracto = ''
    for i in ascii_string:
        extracto += et[i]
    
    return extracto

if __name__ == "__main__":
    test_input = [67,52.07478,-116.2746,1,0,1]
    print(f"\n{compress(load(test_input))}")