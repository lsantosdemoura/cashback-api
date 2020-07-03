from decimal import Decimal

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Purchase, User


@pytest.fixture
def reseller_fullname():
    name = 'Lucas Santos de Moura'
    return name


@pytest.fixture
def reseller_invalid_full_name():
    return ""


@pytest.fixture
def reseller_email():
    email = 'lucas@email.com'
    return email


@pytest.fixture
def reseller_invalid_email():
    return "lucas..invalid@email.com"


@pytest.fixture
def reseller_cpf():
    cpf = '12345678909'
    return cpf


@pytest.fixture
def reseller_invalid_cpf():
    cpf = '12345678909'
    return cpf


@pytest.fixture
def reseller_password():
    password = 'test_password'
    return password


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_reseller(
    reseller_fullname, reseller_email, reseller_cpf, reseller_password
):
    test_reseller = User.objects.create(
        fullname=reseller_fullname,
        email=reseller_email,
        cpf=reseller_cpf,
        password=reseller_password,
    )
    return test_reseller


@pytest.fixture
def purchase_code():
    purchase_code = "1"
    return purchase_code


@pytest.fixture
def purchase_value_900():
    purchase_value = Decimal("900")
    return purchase_value


@pytest.fixture
def purchase_value_1100():
    purchase_value = Decimal("1100")
    return purchase_value


@pytest.fixture
def purchase_value_1600():
    purchase_value = Decimal("1600")
    return purchase_value


@pytest.fixture
def purchase_date_june():
    purchase_date = "2020-06-23"
    return purchase_date


@pytest.fixture
def purchase_date_may():
    purchase_date = "2020-05-23"
    return purchase_date


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_purchase_june_900(
    purchase_date_june, purchase_code, test_reseller, purchase_value_900
):
    test_purchase = Purchase.objects.create(
        code=purchase_code,
        value=purchase_value_900,
        date=purchase_date_june,
        reseller=test_reseller,
    )
    return test_purchase


@pytest.fixture
def client_admin(test_reseller):
    token = RefreshToken.for_user(test_reseller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client
