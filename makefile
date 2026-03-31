# =============================================================================
# Makefile for Dental CDSS Project
# =============================================================================

SHELL := /bin/bash

# -----------------------------------------------------------------------------
# Core Configuration
# -----------------------------------------------------------------------------
PROJECT_NAME        := config
SETTINGS            := config.settings
SETTINGS_TEST       := config.settings_test
MANAGE              := python manage.py
APPS                := $(shell ls -d apps/*/ | xargs -n1 basename)

# -----------------------------------------------------------------------------
# Dev Database (Docker)
# -----------------------------------------------------------------------------
DB_CONTAINER        := dental_cdss-dev-db
DB_USER             := postgres
DB_NAME             := dental_cdss_db

# -----------------------------------------------------------------------------
# Staging Configuration
# -----------------------------------------------------------------------------
STAGING_COMPOSE_FILE := docker-compose-staging.yml
STAGING_ENV_FILE     := envs/.env.staging
STAGING_CONTAINER    := dental_cdss-staging-api
STAGING_DB           := dental_cdss-staging-db
STAGING_CELERY       := dental_cdss-staging-celery
STAGING_BEAT         := dental_cdss-staging-beat

# -----------------------------------------------------------------------------
# Reusable Macros
# -----------------------------------------------------------------------------
# Run a command inside the dev app container (if used in future)
# Run a command inside the staging API container
define STAGING_EXEC
	docker exec -it $(STAGING_CONTAINER) python manage.py $(1)
endef

# Run a command inside the staging DB container via psql
define STAGING_DB_EXEC
	docker exec -it $(STAGING_DB) psql -U $(DB_USER) -d template1 -c $(1)
endef

# Run a command inside the dev DB container via psql
define DEV_DB_EXEC
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d template1 -c $(1)
endef

# -----------------------------------------------------------------------------
# 1. SETUP & INSTALL
# -----------------------------------------------------------------------------
install:
	pip install -r requirements.txt
	pre-commit install
	pre-commit install --hook-type commit-msg

setup:
	@echo "🔧 Setting up virtual environment..."
	@if ! python3 -c "import venv" >/dev/null 2>&1; then \
		echo "venv not found — installing..."; \
		apt-get update && apt-get install -y python3-venv; \
	fi
	@python3 -m venv venv
	@source venv/bin/activate && make install
	@echo "✅ Setup complete."


# =============================================================================
# 2. DJANGO COMMANDS (Local)
# =============================================================================
run:
	$(MANAGE) runserver --settings=$(SETTINGS)

shell:
	$(MANAGE) shell --settings=$(SETTINGS)

createsuperuser:
	$(MANAGE) createsuperuser --settings=$(SETTINGS)

collectstatic:
	$(MANAGE) collectstatic --noinput --settings=$(SETTINGS)

migrate:
	$(MANAGE) migrate --settings=$(SETTINGS)

makemigrations:
	$(MANAGE) makemigrations --settings=$(SETTINGS)

makemigrations-force:
	$(MANAGE) makemigrations --settings=$(SETTINGS)

showmigrations:
	$(MANAGE) showmigrations --settings=$(SETTINGS)

checkmigrationsconflicts:
	$(MANAGE) makemigrations --check --dry-run --settings=$(SETTINGS)

role:
	$(MANAGE) seed_roles --settings=$(SETTINGS)


# =============================================================================
# 3. CODE QUALITY
# =============================================================================
check:
	pre-commit run --all-files

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +


# =============================================================================
# 5. DOCKER (Dev)
# =============================================================================
up:
	docker compose up -d

down:
	docker compose down

rescelery:
	docker restart dental_cdss-dev-celery


# =============================================================================
# 6. DATABASE & MIGRATIONS (Dev)
# =============================================================================
reset-migrations:
	find ./apps -path "*/migrations/*.py" ! -name "__init__.py" -delete

reset-db:
	$(CONFIRM)
	$(call RESET_POSTGRES, docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d template1 -c)
	@echo "🔄 Rebuilding migrations..."
	$(call REBUILD_MIGRATIONS, $(MANAGE) --settings=$(SETTINGS))
	@echo "✅ Database reset complete."


# =============================================================================
# 7. FIXTURES
# =============================================================================
FIXTURES_DIR := fixtures-minimal

FIXTURE_FILES := \
	01_prescriptions.json \
	02_treatment_plans.json \
	03_patients.json \
	04_consultations.json \
	05_audit_logs.json

load-fixtures:
	@for f in $(FIXTURE_FILES); do \
		echo "📦 Loading $$f..."; \
		$(MANAGE) loaddata $(FIXTURES_DIR)/$$f --settings=$(SETTINGS); \
	done
	@echo "✅ All fixtures loaded."

dump-fixtures:
	@mkdir -p $(FIXTURES_DIR)
	$(MANAGE) dumpdata prescriptions.Prescription --indent 2 --settings=$(SETTINGS) > $(FIXTURES_DIR)/01_prescriptions.json
	$(MANAGE) dumpdata treatment_plans.TreatmentPlan --indent 2 --settings=$(SETTINGS) > $(FIXTURES_DIR)/02_treatment_plans.json
	$(MANAGE) dumpdata patients.Patient --indent 2 --settings=$(SETTINGS) > $(FIXTURES_DIR)/03_patients.json
	$(MANAGE) dumpdata consultations.Consultation --indent 2 --settings=$(SETTINGS) > $(FIXTURES_DIR)/04_consultations.json
	$(MANAGE) dumpdata audit_logs.AuditLog --indent 2 --settings=$(SETTINGS) > $(FIXTURES_DIR)/05_audit_logs.json
	@echo "✅ Fixtures dumped to $(FIXTURES_DIR)/"


# =============================================================================
# 8. CLIENT DATA LOADING (Local)
# =============================================================================
load-client-data:
	@echo "📥 Loading client data..."
	$(MANAGE) load_client_data --settings=$(SETTINGS)
	@echo "✅ Client data loaded."


# =============================================================================
# 9. DUMMY DATA (Local)
# =============================================================================
generate-dummy-data:
	$(MANAGE) generate-dummy-data --settings=$(SETTINGS)

generate-dummy-data-preserve:
	$(MANAGE) generate_dummy_data --preserve --settings=$(SETTINGS)

reset-dummy-data:
	$(MANAGE) generate_dummy_data --clear-existing --settings=$(SETTINGS)

check-data-status:
	@python check_data_status.py

clear-all-data:
	$(CONFIRM)
	$(MANAGE) flush --noinput --settings=$(SETTINGS)
	@echo "✅ All data cleared."


# =============================================================================
# 10. APP SCAFFOLDING
# =============================================================================
APP_SUBDIRS := models migrations views serializers services permissions tasks

# Usage: make app name=my_app
app:
	@if [ -z "$(name)" ]; then \
		echo "❌ Usage: make app name=your_app_name"; exit 1; \
	fi
	@echo "🚀 Creating app '$(name)'..."
	@mkdir -p apps/$(name)
	@django-admin startapp $(name) apps/$(name)
	@for d in $(APP_SUBDIRS); do \
		mkdir -p apps/$(name)/$$d; \
		touch apps/$(name)/$$d/__init__.py; \
	done
	@printf 'from django.urls import path\n\napp_name = "$(name)"\n\nurlpatterns = [\n    # Add your URL patterns here\n]\n' > apps/$(name)/urls.py
	@echo "✅ App '$(name)' created."


# =============================================================================
# 11. STAGING — Docker Compose
# =============================================================================
STAGING_COMPOSE := docker compose -f $(STAGING_COMPOSE_FILE) --env-file $(STAGING_ENV_FILE)

staging-up:
	$(STAGING_COMPOSE) up -d --build

staging-run:
	$(STAGING_COMPOSE) up --build

staging-down:
	$(STAGING_COMPOSE) down

staging-makemigrations:
	$(call STAGING_EXEC, makemigrations)

staging-migrate:
	$(call STAGING_EXEC, migrate)

staging-createsuperuser:
	$(call STAGING_EXEC, createsuperuser)

staging-shell:
	$(call STAGING_EXEC, shell)

staging-restart-backend:
	docker restart $(STAGING_CONTAINER)


# =============================================================================
# 12. DEPLOYMENT
# =============================================================================

# Usage: make deploy ENV=staging | make deploy ENV=prod
deploy:
	@if [ -z "$(ENV)" ]; then echo "❌ Usage: make deploy ENV=staging|prod"; exit 1; fi
	git reset --hard
	git checkout master
	git pull origin master --no-edit
	docker compose -f docker-compose-$(ENV).yml up --build -d
	docker compose -f docker-compose-$(ENV).yml exec dental_cdss-$(ENV)-api python manage.py collectstatic --clear --no-input
	docker compose -f docker-compose-$(ENV).yml exec dental_cdss-$(ENV)-api python manage.py showmigrations
	docker compose -f docker-compose-$(ENV).yml exec dental_cdss-$(ENV)-api python manage.py migrate
	@echo "🎉 Deployed to $(ENV). Have a nice day!"

deployall:
	@make deploy ENV=$(ENV)
	@make -C ../dental_cdss_front deploy ENV=$(ENV)

upall:
	sudo docker compose -f docker-compose-$(ENV).yml up -d
	cd ../dental_cdss_front && sudo docker compose -f docker-compose-$(ENV).yml up -d

downall:
	sudo docker compose -f docker-compose-$(ENV).yml down
	cd ../dental_cdss_front && sudo docker compose -f docker-compose-$(ENV).yml down


# =============================================================================
# 13. SSL
# =============================================================================

sslrenew:
	certbot certonly -d dental_cdss.com -d staging.dental_cdss.com -d www.dental_cdss.com \
		--cert-name dental_cdss \
		--pre-hook "service nginx stop" \
		--post-hook "service nginx start"


# =============================================================================
# 14. HELP
# =============================================================================

help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════╗"
	@echo "║        Dental CDSS — Makefile Commands                   ║"
	@echo "╠══════════════════════════════════════════════════════════╣"
	@echo "║  SETUP        make install / setup                       ║"
	@echo "║  DEV          make run / shell / migrate / makemigrations ║"
	@echo "║  QUALITY      make check / clean                         ║"
	@echo "║  TESTS        make test [module=X] / test-ci / test-quick ║"
	@echo "║  DOCKER       make up / down / rescelery                 ║"
	@echo "║  DB RESET     make reset-db / reset-migrations           ║"
	@echo "║  FIXTURES     make load-fixtures / dump-fixtures         ║"
	@echo "║  DUMMY DATA   make generate-dummy-data / reset-dummy-data ║"
	@echo "║  STAGING      make staging-up / staging-reset-db / ...   ║"
	@echo "║  DEPLOY       make deploy ENV=staging|prod               ║"
	@echo "║  SSL          make sslrenew                              ║"
	@echo "╚══════════════════════════════════════════════════════════╝"
	@echo ""

.PHONY: install setup run shell createsuperuser collectstatic migrate makemigrations \
	makemigrations-force showmigrations checkmigrationsconflicts check clean \
	test test-ci test-quick test-help \
	up down rescelery reset-migrations reset-db \
	load-fixtures dump-fixtures \
	generate-dummy-data generate-dummy-data-preserve\
	app \
	staging-up staging-run staging-down staging-makemigrations staging-migrate \
	staging-createsuperuser staging-shell staging-restart-backend \
	staging-reset-db staging-reset-migrations \
	deploy deployall upall downall sslrenew help