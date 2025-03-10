import requests, time
from bs4 import BeautifulSoup

from src import Solver

class Test:

    def __init__(self):
        self.solver = Solver()

    def get_captcha(self):
        response = requests.get("https://leak-lookup.com/account/login")
        soup = BeautifulSoup(response.text, "html.parser")
        captcha_element = soup.find(id="captcha-element")
        
        if captcha_element and captcha_element.pre:
            captcha_ascii = captcha_element.pre.text
            return captcha_ascii

    def task(self):
        captcha = self.get_captcha()
        print(captcha + "\n")

        start = time.time()
        result = self.solver.solve(captcha)
        end = time.time()
        print("Time:", end - start)
        print("Result:", result)

    def run(self):
        while True: self.task()

if __name__ == "__main__":
    test = Test()
    test.run()