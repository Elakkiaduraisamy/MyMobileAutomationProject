from behave import given, then, when

from pages.product import ProductPage
from utils.appium_utilities import swipe_down
from utils.logger import logger
from webdriver.webdriver_setup import WebDriverSetup


@given(u'user selects any products from the list')
def step_impl(context):
    logger.info("Setting up WebDriver")
    context.webdriver_init = WebDriverSetup(context)
    logger.info("verifying the product page feature file and in step user select the product step")
    context.product_page = ProductPage(context.driver, context.input_platform_name)
    context.product_page.user_selects_products()


@then(u'user navigates to that product page')
def step_impl(context):
    logger.info("user navigates to selected product page")
    context.driver.implicitly_wait(40)
    context.product_page.user_navigate_products_page()


@then(u'Verify the selected product page is displayed')
def step_impl(context):
    logger.info("user is now verifying the product page")
    context.driver.implicitly_wait(40)
    context.product_page.verify_product_page()


@then(u'Get the price of the product')
def step_impl(context):
    logger.info("user is now verifying the product price")
    context.product_page.get_product_price()


@then(u'click the add to cart button')
def step_impl(context):
    logger.info("user is adding the product to the cart")
    context.product_page.add_to_cart()


@given(u'user scrolls down')
def step_impl(context):
    context.product_page = ProductPage(context.driver, context.input_platform_name)
    logger.info("user is scrolling the screen searching for copyrights and social media ")
    swipe_down(context.driver, 1000)


@then(u'user can see the social media links and copyrights')
def step_impl(context):
    logger.info("user is finding the copyrights in the page")
    context.product_page.social_media_copyright_links()
