try:
    from tests import QuestionCreationTest
except ImportError:
    from .tests import QuestionCreationTest
    

browser = QuestionCreationTest(wait_time=25, anonymous_mode=True)

url_test = lambda state, process: f'http://localhost:8000/test/{state}?process={process}'


"""
Run the server and activate the test URLs to run the tests  
"""

# question creation test
browser.open(url_test('setUp', 'create_question'))
browser.create_base() # base for code
browser.login()
browser.send_question()
browser.open(url_test('result', 'create_question'))
browser.open(url_test('tearDown', 'create_question'))
browser.close()
