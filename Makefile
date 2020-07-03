makemigrations:
	docker-compose run web bash -c "cd cashback_api && python manage.py makemigrations"

migrate:
	docker-compose run web bash -c "cd cashback_api && python manage.py migrate"

run-tests:
	docker-compose -f test.yml build
	docker-compose -f test.yml run test_api

runserver:
	docker-compose up
