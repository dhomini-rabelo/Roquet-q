"""
Módulo que otimiza o uso do selenium para automações web e raspagem de dados com bs4, funciona muito bem como classe pai para projetos maiores com selenium
"""
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from selenium.webdriver.support.expected_conditions import presence_of_element_located as presence
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class SeleniumBrowser:
    """
    Classe que trata um webdriver do selenium
    """
    def __init__(self, wait_time=10, not_show_browser=False, fullscreen=False, anonymous_mode=False):
        """
        Faz as configurações de inicialização
        Args:
            wait_time (int, optional): Tempo de insistência usado no WebDriverWait, que otimiza a espera por aparição de elementos web. Defaults to 10.
            not_show_browser (bool, optional): Se deve funcionar com a api sendo executada. Defaults to False.
            fullscreen (bool, optional): Tela do browser em modo fullscreen. Defaults to False.
            anonymous_mode (bool, optional): Tela do browser em modo anônimo. Defaults to False.
        Variáveis:
            driver : utiliza o webdriver do selenium para o Chrome
            search_engine : otimiza o uso do bs4
            wdw : WebDriverWait, que otimiza a espera por aparição de elementos web.

        """
        options = Options()
        if anonymous_mode:
            options.add_argument("--incognito")
        if fullscreen:
            options.add_argument("--kiosk")
        if not_show_browser:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
        self.search_engine = None
        self.wdw = WebDriverWait(self.driver, timeout=wait_time)
        self.wait_time = wait_time

    def open(self, url: str):
        """
        Abre uma página, otimiza bs4, além de ter uma semântica melhor
        """
        self.driver.get(url)
        self.bs4_update()
        
    def find(self, query):
        """
        Procura elemento por css selector
        """
        return self.driver.find_element_by_css_selector(query)

    def finds(self, query):
        """
        Procura elementos por css selector
        """
        return self.driver.find_elements_by_css_selector(query)

    def get_window_size(self, wait_time: float):
        """
        Espera um tempo para para usuário colocar o tamanho da tela do browser a seu gosto, depois retorna esse tamanho que pode ser configurado em window_size ()
        """
        sleep(wait_time)
        size = self.driver.get_window_size()
        return size["width"], size["height"]

    def change_wdw_time(self, new_time):
        """
        Muda o tempo de insitência do WebDriverWait
        """
        self.wdw = WebDriverWait(self.driver, timeout=new_time)

    def window_maximize(self):
        """
        Maximixa o tamanho da tela
        """
        self.driver.maximize_window()

    def window_size(self, width: int, height: int):
        """
        Muda o tamanho da tela para um tamanho desejado
        """
        self.driver.set_window_size(width, height)

    def bs4_update(self):
        """
        Atualiza BeautifulSoup para extração de dados
        """
        self.search_engine = bs(self.driver.page_source, 'html.parser')

    def url_analysis(self):
        """
        Retorna o scheme, netlock, path, params, query e fragment de uma url
        """
        url_parser = urlparse(self.driver.current_url)
        return url_parser

    def window_close(self):
        """
        Fecha janela atual do navegador
        """
        self.driver.close()

    def close_disposable_windows_for_page_id(self, id: str):
        """
        Fecha janelas inúteis do navegador, como propagandas, 
        a única janela que permanece é a de id  informado
        """
        sleep(1)
        windows = self.driver.window_handles
        for window in windows:
            self.driver.switch_to.window(window)
            if self.driver.current_window_handle != id:
                self.window_close()

    def close_disposable_windows_for_url(self, url: str):
        """
        Fecha janelas inúteis do navegador, como propagandas, 
        a única janela que permanece é a de url informado
        """
        windows = self.driver.window_handles
        sleep(1)
        for window in windows:
            self.driver.switch_to.window(window)
            if self.driver.current_url != url:
                self.window_close()

    def close_disposable_windows_for_url_netloc(self, url: str):
        """
        Fecha janelas inúteis do navegador, como propagandas, 
        as janelas que permanecem são as que tem o mesmo netloc
        da url de entrada
        """
        netloc_off_url = urlparse(url).netloc
        sleep(1)
        windows = self.driver.window_handles
        for window in windows:
            self.driver.switch_to.window(window)
            if self.url_analysis().netloc !=  netloc_off_url:
                self.window_close()

    def close(self):
        """
        Fecha todas as janelas do navegador
        """
        self.driver.quit()
