from .flf import FLF

class Solver:

    def __init__(self):
        self.font = FLF("data/zend-framework.flf")
        self.char_patterns = self._create_character_patterns()

    def _create_character_patterns(self):
        patterns = {}

        # A-Z
        for code in range(65, 91):
            char = chr(code)
            char_art = self.font.get_char(code)
            patterns[char] = char_art
        
        # a-z
        for code in range(97, 123):
            char = chr(code)
            char_art = self.font.get_char(code)
            patterns[char] = char_art
        
        return patterns
    
    def solve(self, captcha):
        lines = captcha.strip().split('\n')
        result = ""
        
        char_height = len(next(iter(self.char_patterns.values())))
        
        max_width = max(len(line) for line in lines)
        lines = [line.ljust(max_width) for line in lines]
        
        current_pos = 0
        
        while current_pos < max_width:
            best_match = None
            best_match_score = 0
            best_width = 0
            
            for char, pattern in self.char_patterns.items():
                pattern_width = max(len(line) for line in pattern)
                if current_pos + pattern_width > max_width and current_pos > 0:
                    continue
                
                actual_width = min(pattern_width, max_width - current_pos)                
                match_score = 0
                total_chars = 0
                
                for i in range(min(char_height, len(lines))):
                    captcha_window = lines[i][current_pos:current_pos+actual_width]
                    pattern_line = pattern[i][:actual_width]
                    
                    for j in range(min(len(captcha_window), len(pattern_line))):
                        if captcha_window[j] != ' ' and pattern_line[j] != ' ':
                            total_chars += 1
                            if captcha_window[j] == pattern_line[j]:
                                match_score += 1
                
                normalized_score = match_score / max(1, total_chars) if total_chars > 0 else 0
                if normalized_score > best_match_score:
                    best_match_score = normalized_score
                    best_match = char
                    best_width = pattern_width
            
            if best_match and best_match_score > 0.6:
                result += best_match
                current_pos += best_width
            else:
                current_pos += 1
                
                if current_pos >= max_width - 5 and not result:
                    for char, pattern in self.char_patterns.items():
                        if any(line.endswith(pattern[i][:5]) for i, line in enumerate(lines)):
                            result += char
                            break
        
        return result