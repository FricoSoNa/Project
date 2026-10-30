from selenium.webdriver.common import keys
from selenium.webdriver.support.expected_conditions import element_to_be_selected

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.NAME, "code")
    taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    comfort_button = (By.XPATH, "//button[@data-for='tariff-card-4']/..")
    phone_button = (By.CLASS_NAME, "np-button")
    phone_field = (By.ID, 'phone')
    next_button = (By.XPATH, "//button[text()='Siguiente']")
    code_number = (By.ID, 'code')
    confirm_button = (By.XPATH, "//button[text()='Confirmar']")
    payment_button = (By.CSS_SELECTOR, ".pp-button.filled")
    add_button = (By.CSS_SELECTOR, ".pp-plus-container")
    add_card_button = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    comment_field = (By.ID, "comment")
    blanket_tissues_switch = (By.XPATH,
        "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div//span[@class='slider round']")
    close_card_button = (By.XPATH,
        "//div[contains(@class,'section')][.//div[@class='head' and text()='Método de pago']]//button[contains(@class,'close-button')]")
    payment_method_value = (By.XPATH,
        "//div[@class='pp-value']//div[@class='pp-value-text' and text()='Tarjeta']")
    ice_cream_button = (By.CLASS_NAME, "counter-plus")
    request_taxi_button = (By.CSS_SELECTOR, "button.smart-button")
    search_taxi_title = (By.CLASS_NAME,"order-header-title")
    driver_window_title = (By.CLASS_NAME,"order-header-title")

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

    def set_from(self, from_address):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        self.wait.until(
            EC.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        self.wait.until(
            EC.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def select_taxi_button(self):
        self.driver.find_element(*self.taxi_button).click()

    def select_comfort_button(self):
        self.driver.find_element(*self.comfort_button).click()

    def select_phone_button(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone_field(self, phone_value):
        self.driver.find_element(*self.phone_field).send_keys(phone_value)

    def get_phone_field(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_code_number(self):
        self.driver.find_element(*self.code_number).send_keys(retrieve_phone_code(self.driver))

    def get_code_number(self):
        return self.driver.find_element(*self.code_number).get_property('value')

    def select_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def select_payment_button(self):
        element = self.driver.find_element(*self.payment_button)
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)
        element.click()

    def select_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def set_card_number(self, number_value):
        self.driver.find_element(*self.card_number_input).send_keys(number_value)

    def set_card_code(self, code_value):
        self.driver.find_element(*self.card_code_input).send_keys(code_value)

    def get_card_number(self):
        return self.driver.find_element(*self.card_number_input).get_property('value')

    def get_card_code(self):
        return self.driver.find_element(*self.card_code_input).get_property('value')

    def set_card(self, card_number, card_code):
        number_field = self.wait.until(
            EC.element_to_be_clickable(self.card_number_input)
        )
        number_field.clear()
        number_field.send_keys(card_number)

        code_field = self.wait.until(
            EC.element_to_be_clickable(self.card_code_input)
        )
        code_field.clear()
        code_field.send_keys(card_code)
        code_field.send_keys(Keys.TAB)

    def select_add_card_button(self):
        self.wait.until(
            EC.element_to_be_clickable(self.add_card_button)
        ).click()

    def close_card_window(self):
        self.wait.until(EC.element_to_be_clickable(self.close_card_button)).click()

    def set_comment(self, message):
        comment = self.wait.until(
            EC.visibility_of_element_located(self.comment_field)
        )
        comment.clear()
        comment.send_keys(message)

    def select_blanket_tissues(self):
        element = self.driver.find_element(
            *self.blanket_tissues_switch
        )
        self.driver.execute_script(
            'arguments[0].scrollIntoView(true);',
            element
        )
        element.click()

    def add_ice_cream(self):
        element = self.driver.find_element(*self.ice_cream_button)
        self.driver.execute_script(
            'arguments[0].scrollIntoView(true);',
            element
        )
        element.click()
        element.click()

    def request_taxi(self):
        element = self.driver.find_element(*self.request_taxi_button)
        self.driver.execute_script(
            'arguments[0].scrollIntoView(true);',
            element
        )
        element.click()

    def get_search_taxi_title(self):
        return self.driver.find_element(*self.search_taxi_title).text

    def get_driver_window_title(self):
        return self.driver.find_element(*self.driver_window_title).text

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_method(self):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(options=options)


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_button(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.select_taxi_button()
        routes_page.select_comfort_button()


    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.select_taxi_button()
        routes_page.select_comfort_button()
        routes_page.select_phone_button()
        phone_number = data.phone_number
        routes_page.set_phone_field(phone_number)
        routes_page.click_next_button()
        routes_page.set_code_number()
        routes_page.select_confirm_button()


    def test_set_creditcard(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.select_taxi_button()
        routes_page.select_comfort_button()
        routes_page.select_payment_button()
        routes_page.select_add_button()
        routes_page.set_card(data.card_number, data.card_code)
        routes_page.select_add_card_button()
        routes_page.close_card_window()
        assert routes_page.wait.until(
            EC.visibility_of_element_located(
                routes_page.payment_method_value)).text == "Tarjeta"

    def test_set_comments(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.select_taxi_button()
        routes_page.select_comfort_button()
        routes_page.set_comment(data.message_for_driver)
        assert self.driver.find_element(
            *routes_page.comment_field
        ).get_property("value") == data.message_for_driver

    def test_set_blanket(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.select_taxi_button()
        routes_page.select_comfort_button()
        routes_page.select_blanket_tissues()
        assert self.driver.find_element(
            By.XPATH,
            "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div//input[@type='checkbox']"
        ).is_selected()

    def test_set_icecream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.select_taxi_button()
        routes_page.select_comfort_button()
        routes_page.add_ice_cream()

        assert routes_page.driver.find_element(
            *(By.CLASS_NAME, "counter-value")
        ).text == "2"

    def test_request_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.select_taxi_button()
        routes_page.select_comfort_button()
        routes_page.select_phone_button()
        phone_number = data.phone_number
        routes_page.set_phone_field(phone_number)
        routes_page.click_next_button()
        routes_page.set_code_number()
        routes_page.select_confirm_button()

        routes_page.select_payment_button()
        routes_page.select_add_button()
        routes_page.set_card(data.card_number, data.card_code)
        routes_page.select_add_card_button()
        routes_page.close_card_window()

        routes_page.set_comment(data.message_for_driver)

        routes_page.select_blanket_tissues()

        routes_page.add_ice_cream()

        routes_page.request_taxi()

        assert routes_page.wait.until(
            EC.visibility_of_element_located(
                routes_page.search_taxi_title
            )
        ).text == "Buscar automóvil"

        assert WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element(
                routes_page.driver_window_title,
                "El conductor llegará en"))

    @classmethod
    def teardown_method(self):
        self.driver.quit()