from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage
from unittest import skip


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
        self.addCleanup(lambda: quit_if_posible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')
        
        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')
        
        # Она замечает опцию "Поделится этим списком"
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
        
        # Она делится свои списком. 
        # Страница обновляется и сообщает, что
        # теперь страница используется совместно с Анцифером:
        list_page.share_list_with('oniciferous@example.com')

        # Анцифер переходит на страницу списков в своем браузере
        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        # Он видит на ней список Эдит!
        self.browser.find_element_by_link_text('Get help').click()

        # На странице, которую Анцифер видит, говорится, что это список Эдит
        self.wait_for(lambda: self.assertEqual(
            list_page.get_lists_owner(),
            'edith@example.com'
        ))

        # Он добовляет элемент в список
        list_page.add_list_item('Hi Edith')

        # Когда Эдит обновляет страницу, она видит добольнение Анцифера
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith', 2)