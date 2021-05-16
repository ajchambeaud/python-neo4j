from neo import Singleton, NeoDB, exit_handler

def test_singleton():
    print("[Singleton] should return always the same instance.")

    class TestSingleton(Singleton):
        count=0

        def increment(self, num):
            self.count += num

    instance1 = TestSingleton()
    instance1.increment(10)

    instance2 = TestSingleton()
    instance2.increment(10)

    assert(instance2.count == 20)


def test_NeoDB_getDriver_cache(mocker):
    print("[NeoDB_getDriver] should return cached instance if available.")

    cached_instance = "cached_instance"
    driver_returned_instance = "driver_returned_instance"

    mocker.patch('neo4j.GraphDatabase.driver', return_value=driver_returned_instance)

    neoDB = NeoDB()
    neoDB.driver = cached_instance

    assert neoDB.getDriver() == cached_instance

    neoDB.driver = None


def test_NeoDB_getDriver_non_cache(mocker):
    print("[NeoDB_getDriver] should get an instance from driver when cache is None.")

    driver_returned_instance = "driver_returned_instance"

    mocker.patch('neo4j.GraphDatabase.driver', return_value=driver_returned_instance)

    neoDB = NeoDB()
    neoDB.driver = None

    assert neoDB.getDriver() == driver_returned_instance

    neoDB.driver = None


def test_NeoDB_getDriver_envars(mocker):
    print("[NeoDB_getDriver] should pass envars to the driver.")

    env = {
        'DATABASE_USERNAME': 'username',
        'DATABASE_PASSWORD': 'password',
        'DATABASE_URL': 'url'
    }

    def getenv(value):
        return env[value]

    def driverMock(url, auth):
        return url + "-" + auth[0] + "-" + auth[1]

    mocker.patch('neo4j.GraphDatabase.driver', driverMock)
    mocker.patch('os.getenv', getenv)

    neoDB = NeoDB()
    neoDB.driver = None

    expected = 'url-username-password'

    assert neoDB.getDriver() == expected

    neoDB.driver = None


def test_NeoDB_getSession(mocker):
    print("[NeoDB_getSession] should return the driver session.")

    driver_session = 'driver_session'

    class DriverMock:
        def session(self):
            return driver_session

    neoDB = NeoDB()
    neoDB.driver = DriverMock()

    assert neoDB.getSession() == driver_session

    neoDB.driver = None


def test_NeoDB_close(mocker):
    print("[NeoDB_close] should call driver.close when there is a driver instance cached.")

    neoDB = NeoDB()
    neoDB.driver = mocker.Mock()
    neoDB.close()

    neoDB.driver.close.assert_called_once()

    neoDB.driver = None


def test_NeoDB_close(mocker):
    print("[NeoDB_close] should not rise an exception when driver is None.")

    neoDB = NeoDB()
    neoDB.driver = None
    neoDB.close()


def test_NeoDB_exit_handler(mocker):
    print("[NeoDB_exit_handler] should close the database.")

    instanceMock = mocker.Mock()

    def neoMock():
        return instanceMock

    mocker.patch('neo.NeoDB', neoMock)
    exit_handler()
    instanceMock.close.assert_called_once()