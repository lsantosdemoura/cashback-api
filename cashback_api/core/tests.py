import pytest

from core.models import Purchase, User


@pytest.mark.django_db(transaction=True)
def test_user_instance(test_approved_reseller):
    assert isinstance(test_approved_reseller, User)


@pytest.mark.django_db(transaction=True)
def test_user_get_name(test_approved_reseller, reseller_fullname):
    assert test_approved_reseller.fullname == reseller_fullname


@pytest.mark.django_db(transaction=True)
def test_user_get_email(test_approved_reseller, reseller_approved_email):
    assert test_approved_reseller.email == reseller_approved_email


@pytest.mark.django_db(transaction=True)
def test_user_str(test_approved_reseller, reseller_approved_email):
    assert test_approved_reseller.__str__() == reseller_approved_email


@pytest.mark.django_db(transaction=True)
def test_purchase_instance(test_purchase_june_900):
    assert isinstance(test_purchase_june_900, Purchase)


@pytest.mark.django_db(transaction=True)
def test_purchase_get_name(test_purchase_june_900, purchase_code):
    assert test_purchase_june_900.code == purchase_code


@pytest.mark.django_db(transaction=True)
def test_purchase_get_email(test_purchase_june_900, purchase_value_900):
    assert test_purchase_june_900.value == purchase_value_900


@pytest.mark.django_db(transaction=True)
def test_purchase_str(test_purchase_june_900, purchase_code):
    assert test_purchase_june_900.__str__() == purchase_code
