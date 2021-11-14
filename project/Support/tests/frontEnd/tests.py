try:
    from .web import SeleniumBrowser
except ImportError:
    from web import SeleniumBrowser
from selenium.webdriver.common.keys import Keys
from time import sleep




class QuestionCreationTest(SeleniumBrowser):
    
    def create_base(self):
        self.code = 123456 # equal room.views.TEST_CODE
        self.url_base = 'http://localhost:8000'  
        self.b = f'{self.url_base}/{self.code}'
        self.window_size(1500, 1000)
    
    def login(self):
        self.open(f'{self.b}')
        self.driver.implicitly_wait(self.wait_time)
        input_username = self.find('input#id_username')
        submit_btn = self.find('button.button-white-blue.button-blue-white.enter')
        input_username.click()
        input_username.send_keys('teste')
        submit_btn.click()
        
        
    def send_question(self):
        sleep(5)
        self.driver.implicitly_wait(self.wait_time)
        textarea = self.find('textarea#id_question')
        select_theme = self.find('select#question-theme')
        submit_btn = self.find('button.send')
        
        textarea.send_keys('test_question')
        select_theme.click()
        select_theme.send_keys(Keys.ARROW_DOWN)
        select_theme.send_keys(Keys.ENTER)
        submit_btn.click()        

