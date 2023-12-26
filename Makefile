DJANGO_EXEC=docker compose exec django sh -c

env:
	cp .env.example .env

up:
	docker compose up -d --build

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d --build

shell:
	$(DJANGO_EXEC) "python manage.py shell"

shell-plus:
	$(DJANGO_EXEC) "python manage.py shell_plus --ipython"

create-superuser:
	$(DJANGO_EXEC) "python manage.py createsuperuser"

create-test-superuser:
	@$(DJANGO_EXEC) "DJANGO_SUPERUSER_USERNAME=kek \
	DJANGO_SUPERUSER_PASSWORD=kek \
	DJANGO_SUPERUSER_EMAIL=mail@mail.kek \
	python3 manage.py createsuperuser --noinput && \
	echo 'Test Django superuser login/pass: kek / kek' || true"

collectstatic:
	$(DJANGO_EXEC) "python manage.py collectstatic"

migrations:
	poetry run python3 manage.py migrate

requirements:
	poetry export --without-hashes -o requirements.txt

test:
	$(DJANGO_EXEC) "PYTHONPATH=. pytest ./drf_web3/tests.py"


.PHONY: \
	env \
	up \
	down \
	restart \
	shell \
	shell-plus \
	create-superuser \
	create-test-superuser \
	collectstatic \
	migrations \
	requirements \
	test
