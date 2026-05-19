import abc
import time
import pprint
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


MAX_RETRIES = 2


class TestBase(abc.ABC):
    url: str
    description: str
    version: str

    def __init_subclass__(cls, **kwargs):
        for key in ('url', 'description', 'version'):
            if not hasattr(cls, key):
                raise NotImplementedError(f'`{key}` not implemented')
            if not isinstance(getattr(cls, key), str):
                raise NotImplementedError(f'`{key}` must be type str')
        return super().__init_subclass__(**kwargs)

    @classmethod
    def run(cls, name: str | None = None,
            driver: webdriver.Remote | None = None):
        '''
        Used to run the test

        Arguments:
         - `name`: the unique name for the test
         - `driver`: can be used to specify a (local) webdriver
        '''
        if driver is None:
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                options=options,
                command_executor="http://localhost:4444")

        t0 = time.time()
        retries = MAX_RETRIES

        try:
            while True:
                try:
                    driver.get(cls.url)
                    cls.test(driver)

                    success = True
                    error = None
                    break
                except WebDriverException as e:
                    if retries:
                        retries -= 1
                        time.sleep(1.0)
                        try:
                            # reset browser to restart clean
                            driver.delete_all_cookies()
                            driver.get("about:blank")
                        except Exception:
                            pass
                        continue
                    success = False
                    error = e.msg or type(e).__name__
                    break
                except Exception as e:
                    success = False
                    error = str(e) or type(e).__name__
                    break

            return {
                'name': name or cls.__name__,  # str
                'test': cls.__name__,  # str
                'url': cls.url,  # str
                'success': success,  # int
                'error': error,  # str?
                'duration': time.time() - t0,  # float
                'description': cls.description,  # str
                'version': cls.version,  # str
                'retries': MAX_RETRIES-retries,  # int
            }
        finally:
            driver.quit()

    @classmethod
    def print_run(cls, name: str | None = None,
                  driver: webdriver.Remote | None = None):
        res = cls.run(name=name, driver=driver)
        pprint.pprint(res)

    @classmethod
    def test(cls, driver: webdriver.Remote):
        ...
