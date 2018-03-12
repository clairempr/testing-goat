# functional tests

from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

        def test_cannot_add_empty_list_items(self):
            # Otis goes to the home page and accidentally tries to submit
            # an empty list item. He hits Enter on the empty input box
            self.browser.get(self.live_server_url)
            self.get_item_input_box().send_keys(Keys.ENTER)

            # The browser intercepts the request, and does not load the
            # list page
            self.wait_for(lambda: self.browser.find_elements_by_css_selector(
                '#id_text:invalid'
            ))

            # He starts typing some text for the new item and the error disappears
            self.get_item_input_box().send_keys('Quit smoking')
            self.wait_for(lambda: self.browser.find_elements_by_css_selector(
                '#id_text:valid'
            ))

            # And he can submit it successfully
            self.get_item_input_box().send_keys(Keys.ENTER)
            self.wait_for_row_in_list_table('1: Quit smoking')

            # Perversely, he now decides to submit a second blank list item
            self.get_item_input_box().send_keys(Keys.ENTER)

            # Again, the browser will not comply
            self.wait_for_row_in_list_table('1: Quit smoking')
            self.wait_for(lambda: self.browser.find_elements_by_css_selector(
                '#id_text:invalid'
            ))

            # And he can correct it by filling some text in
            self.get_item_input_box().send_keys('Buy opium')
            self.wait_for(lambda: self.browser.find_elements_by_css_selector(
                '#id_text:valid'
            ))
            self.get_item_input_box().send_keys(Keys.ENTER)
            self.wait_for_row_in_list_table('1: Quit smoking')
            self.wait_for_row_in_list_table('2: Buy opium')
