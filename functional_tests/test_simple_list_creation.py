# functional tests

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Otis has heard about a cool new online to-do app. He goes
        # to check out its homepagetest_can_start_a_list_for_one_user
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Save souls" into a text box (Otis' hobby
        # is converting people to Christianity)
        inputbox.send_keys('Save souls')

        # When he hits enter, the page updates, and now the page lists
        # "1: Save souls" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Save souls')

        # There is still a text box inviting him to add another item. He
        # enters "Dig rifle pits" (You can never have too many rifle pits)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Dig rifle pits')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Save souls')
        self.wait_for_row_in_list_table('2: Dig rifle pits')

        # Satisfied, he goes back to reading his Bible

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Otis starts a new to-do list
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Save souls')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Save souls')

        # He notices that his list has a unique URL
        otis_list_url = self.browser.current_url
        self.assertRegex(otis_list_url, '/lists/.+')

        # Now a new user, Lizzie, comes along to the site

        ## We use a new browser session to make sure that no information
        ## of Otis' is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Lizzie visits the home page. There is no sign of Otis'
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Save souls', page_text)
        self.assertNotIn('Dig rifle pits', page_text)

        # Lizzie starts a new list by entering a new item. She
        # is more practical than Otis...
        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Pay Otis\' bills')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Pay Otis\' bills')

        # Lizzie gets her own unique URL
        lizzie_list_url = self.browser.current_url
        self.assertRegex(lizzie_list_url, '/lists/.+')
        self.assertNotEqual(lizzie_list_url, otis_list_url)

        # Again, there is no trace of Otis' list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Save souls', page_text)
        self.assertNotIn('Dig rifle pits', page_text)

        # Satisfied, they both go back to reading the Bible

