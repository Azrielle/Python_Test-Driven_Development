from selenium import webdriver
from .base import FunctionalTest

def quit_if_posible(browser):
    '''выход если возможен'''
    try: browser.quit()
    except:pass

class SharingTest(FunctionalTest):
    '''тест обмена данными'''

    def test_can_share_a_lists_with_another_user(self):
        '''тест: можно обмениватся списком с еще одним пользователем'''
        # Эдит является зарегистрированным пользователем
        self.create_pre_authenticated_session('edith@example.cjm')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_posible(edith_browser))

        # Ee друг Анцифер тоже зависает на сайте списков
        oni_browser = webdriver.Firefox()
        self.addCleanup = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')
        
        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')
        
        # Она замечает опцию "Поделится этим списком"
        share_box = self.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
        