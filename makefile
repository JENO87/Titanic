.PHONY: install-uv sync install test lint format-check type-check scan-deps build export docker-build tag-docker pre-commit publish clean-docker editable-install clean

install-uv:
	pip install uv

sync:
	uv sync --extra build --extra dev --extra test

install:
	make install-uv
	make sync
	make editable-install
	uv run pre-commit install

test:
	uv run pytest --cov --junitxml=report.xml

lint:
	uv run ruff check . --fix
	uv run mypy .
	uv run pylint src/

   format-check:
       uv run pre-commit run ruff-format --all-files
       uv run ruff format --diff .

type-check:
	uv run mypy .

scan-deps:
	trivy fs --format json --output trivy-report.json requirements.txt

pre-commit:
	uv run pre-commit run --all-files

build-package:
	uv build

publish-package:
	uv publish --registry https://ghcr.io/api/v4/packages/pypi --token $(UV_PUBLISH_TOKEN)

export:
	uv pip compile pyproject.toml -o requirements.txt

build-docker-image:
	docker build -t titanic-classification:${DOCKER_TAG:-latest} .

tag-docker-image:
	docker tag titanic-classification:${DOCKER_TAG:-latest} ghcr.io/JensNorell/titanic-classification:${DOCKER_TAG:-latest}

push-docker-image:
	docker push ghcr.io/JensNorell/titanic-classification:${DOCKER_TAG:-latest}

clean-docker-image:
	docker rmi titanic-classification:${DOCKER_TAG:-latest} ghcr.io/JensNorell/titanic-classification:${DOCKER_TAG:-latest} || true

notify:
	gh issue comment 1 --body "Workflow ${STATUS} for commit ${GITHUB_SHA}. Check details at ${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

clean:
	rm -rf dist *.egg-info .pytest_cache .mypy_cache
