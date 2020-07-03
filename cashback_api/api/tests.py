import json

from django.urls import reverse
import pytest
import vcr

from core.models import Purchase, User


@pytest.mark.django_db(transaction=True)
def test_create_reseller(client, reseller_payload_request):
    response = client.post('/resellers/', reseller_payload_request)
    assert response.status_code == 201
    assert User.objects.filter(email=reseller_payload_request["email"]).exists()


@pytest.mark.django_db(transaction=True)
def test_create_invalid_reseller(client, reseller_invalid_payload_request):
    response = client.post('/resellers/', reseller_invalid_payload_request)
    assert response.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_create_approved_purchase(
    approved_client_admin, purchase_approved_payload_request
):
    response = approved_client_admin.post(
        '/purchases/', purchase_approved_payload_request
    )
    assert response.status_code == 201
    assert response.data['status'] == 'Aprovado'


@pytest.mark.django_db(transaction=True)
def test_create_approved_purchase(
    validating_client_admin, purchase_validating_payload_request
):
    response = validating_client_admin.post(
        '/purchases/', purchase_validating_payload_request
    )
    assert response.status_code == 201
    assert response.data['status'] == 'Em validação'


@pytest.mark.django_db(transaction=True)
def test_get_approved_purchase(
    approved_client_admin, test_purchase_june_900
):
    params = {'start_date': '2020-06-03'}
    response = approved_client_admin.get('/purchases/', params)
    assert response.status_code == 200
    assert response.data['results'][0]['cashback_value'] == '90.00'


@pytest.mark.django_db(transaction=True)
def test_get_approved_purchase_2500_total_value(
    approved_client_admin, test_purchase_june_900, test_purchase_june_1600
):
    params = {'start_date': '2020-06-03', 'end_date': '2020-07-03'}
    response = approved_client_admin.get('/purchases/', params)
    assert response.status_code == 200
    assert response.data['results'][0]['cashback_value'] == '500.00'
    assert response.data['results'][0]['cashback_percentage'] == '20%'


@pytest.mark.django_db(transaction=True)
def test_get_approved_purchase_2500_june_1100_may(
    approved_client_admin,
    test_purchase_june_900,
    test_purchase_june_1600,
    test_purchase_may_1100,
):
    params = {'end_date': '2020-06-24'}
    response = approved_client_admin.get('/purchases/', params)
    assert response.status_code == 200

    for result in response.data['results']:
        if result['code'] == '3':
            assert result['cashback_value'] == '165.00'
            assert result['cashback_percentage'] == '15%'
        else:
            assert result['cashback_value'] == '500.00'
            assert result['cashback_percentage'] == '20%'


@vcr.use_cassette('fixtures/vcr_cassettes/gathered-cashback.yml')
@pytest.mark.django_db(transaction=True)
def test_gathered_cashback(approved_client_admin):
    response = approved_client_admin.get('/gathered-cashback/')
    assert response.status_code == 200
    assert response.data['credit'] == 1651
