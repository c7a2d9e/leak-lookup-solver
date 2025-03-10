class FLF:
    
    def __init__(self, file):
        with open(file, "r") as f:
            self.font_definition = f.read()
        
        if self.font_definition is None or not self.font_definition.startswith("flf2a"):
            raise ValueError("Invalid font definition, string must start with flf2a")
        
        self.font = None
        self.parse_font()

    def parse_font(self):
        lines = self.font_definition.split("\n")
        header = lines[0].split(" ")
        
        self.font = {
            "defn": lines[int(header[5]) + 1:],
            "hardblank": header[0][-1],
            "height": int(header[1]),
            "char": {}
        }

    def get_char(self, char_code):
        if char_code in self.font["char"]:
            return self.font["char"][char_code]
        
        height = self.font["height"]
        start = (char_code - 32) * height
        char_defn = []
        
        for i in range(height):
            if start + i < len(self.font["defn"]):
                line = self.font["defn"][start + i]
                line = line.replace("@", "").replace(self.font["hardblank"], " ").replace("#", "")
                char_defn.append(line)
        
        self.font["char"][char_code] = char_defn
        return char_defn

    def write(self, string):
        chars = []
        for i in range(len(string)):
            chars.append(self.get_char(ord(string[i])))

        result = ""
        for i in range(len(chars[0])):
            result += "\n"
            for j in range(len(string)):
                result += chars[j][i].replace("#", "")
        
        return result