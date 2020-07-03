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
def reseller_invalid_fullname():
    return ""


@pytest.fixture
def reseller_approved_email():
    email = 'lucas@email.com'
    return email


@pytest.fixture
def reseller_validating_email():
    email = 'lucas2@email.com'
    return email


@pytest.fixture
def reseller_invalid_email():
    return "lucas..invalid@email.com"


@pytest.fixture
def reseller_validating_cpf():
    cpf = '12345678909'
    return cpf


@pytest.fixture
def reseller_approved_cpf():
    cpf = '15350946056'
    return cpf


@pytest.fixture
def reseller_invalid_cpf():
    cpf = '12312312312'
    return cpf


@pytest.fixture
def reseller_password():
    password = 'test_password'
    return password


@pytest.fixture
def reseller_invalid_password():
    return "1234"


@pytest.fixture
def reseller_payload_request(
    reseller_approved_email,
    reseller_approved_cpf,
    reseller_password,
    reseller_fullname,
):
    return {
        "cpf": reseller_approved_cpf,
        "email": reseller_approved_email,
        "password": reseller_password,
        "fullname": reseller_fullname,
    }


@pytest.fixture
def reseller_invalid_payload_request(
    reseller_approved_email,
    reseller_invalid_cpf,
    reseller_password,
    reseller_fullname,
):
    return {
        "cpf": reseller_invalid_cpf,
        "email": reseller_approved_email,
        "password": reseller_password,
        "fullname": reseller_fullname,
    }


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_approved_reseller(
    reseller_fullname,
    reseller_approved_email,
    reseller_approved_cpf,
    reseller_password,
):
    test_reseller = User.objects.create(
        fullname=reseller_fullname,
        email=reseller_approved_email,
        cpf=reseller_approved_cpf,
        password=reseller_password,
    )
    return test_reseller


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_validating_reseller(
    reseller_fullname,
    reseller_validating_email,
    reseller_validating_cpf,
    reseller_password,
):
    test_reseller = User.objects.create(
        fullname=reseller_fullname,
        email=reseller_validating_email,
        cpf=reseller_validating_cpf,
        password=reseller_password,
    )
    return test_reseller


@pytest.fixture
def purchase_code():
    purchase_code = "1"
    return purchase_code


@pytest.fixture
def purchase_value_900():
    purchase_value = Decimal("900.0")
    return purchase_value


@pytest.fixture
def purchase_value_1100():
    purchase_value = Decimal("1100.0")
    return purchase_value


@pytest.fixture
def purchase_value_1600():
    purchase_value = Decimal("1600.0")
    return purchase_value


@pytest.fixture
def purchase_date_june():
    purchase_date = "2020-06-23"
    return purchase_date


@pytest.fixture
def purchase_date_may():
    purchase_date = "2020-05-26"
    return purchase_date


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_purchase_june_900(
    purchase_date_june, test_approved_reseller, purchase_value_900
):
    test_purchase = Purchase.objects.create(
        code="1",
        value=purchase_value_900,
        date=purchase_date_june,
        reseller=test_approved_reseller,
        status="Aprovado",
    )
    return test_purchase


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_purchase_june_1600(
    purchase_date_june, test_approved_reseller, purchase_value_1600
):
    test_purchase = Purchase.objects.create(
        code="2",
        value=purchase_value_1600,
        date=purchase_date_june,
        reseller=test_approved_reseller,
        status="Aprovado",
    )
    return test_purchase


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def test_purchase_may_1100(
    purchase_date_may, test_approved_reseller, purchase_value_1100
):
    test_purchase = Purchase.objects.create(
        code="3",
        value=purchase_value_1100,
        date=purchase_date_may,
        reseller=test_approved_reseller,
        status="Aprovado",
    )
    return test_purchase


@pytest.fixture
def purchase_approved_payload_request(
    purchase_code, purchase_date_june, reseller_approved_cpf
):
    return {
        'code': purchase_code,
        'value': Decimal("1500.0"),
        'date': purchase_date_june,
        'reseller': reseller_approved_cpf,
    }


@pytest.fixture
def purchase_validating_payload_request(
    purchase_code, purchase_date_june, reseller_validating_cpf
):
    return {
        'code': purchase_code,
        'value': Decimal("1500.0"),
        'date': purchase_date_june,
        'reseller': reseller_validating_cpf,
    }


@pytest.fixture
def approved_client_admin(test_approved_reseller):
    token = RefreshToken.for_user(test_approved_reseller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client


@pytest.fixture
def validating_client_admin(test_validating_reseller):
    token = RefreshToken.for_user(test_validating_reseller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")
    return client
