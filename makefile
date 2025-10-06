.PHONY: install-uv sync install test lint format-check type-check scan-deps build-package publish-package export build-docker-image tag-docker-image push-docker-image clean-docker-image pre-commit clean editable-install ci

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
	docker build -t titanic-classification:${DOCKER_TAG} .

tag-docker-image:
	docker tag titanic-classification:${DOCKER_TAG} ghcr.io/JensNorell/titanic-classification:${DOCKER_TAG}

push-docker-image:
	docker push ghcr.io/JensNorell/titanic-classification:${DOCKER_TAG}

clean-docker-image:
	docker rmi titanic-classification:${DOCKER_TAG} ghcr.io/JensNorell/titanic-classification:${DOCKER_TAG} || true

notify:
	gh issue comment 1 --body "Workflow ${STATUS} for commit ${GITHUB_SHA}. Check details at ${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

clean:
	rm -rf dist *.egg-info .pytest_cache .mypy_cache

ci:
	gh workflow run ci.yml --field branch=$$(git rev-parse --abbrev-ref HEAD)

pr-quality:
	@powershell -Command "if ((git rev-parse --abbrev-ref HEAD) -ne 'development') { Write-Output 'Error: Must be on development branch'; exit 1 }; .\\gh.exe pr create --base quality --title 'Test in quality' --body 'Pull request to quality'"

pr-main:
	@powershell -Command "if ((git rev-parse --abbrev-ref HEAD) -ne 'quality') { Write-Output 'Error: Must be on quality branch'; exit 1 }; .\\gh.exe pr create --base main --title 'Deploy to main' --body 'Pull request to main'"

install-gh:
	powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cli/cli/releases/download/v2.81.0/gh_2.81.0_windows_amd64.zip' -OutFile 'gh.zip'; Expand-Archive -Path 'gh.zip' -DestinationPath '.' -Force; if (Test-Path 'gh_2.81.0_windows_amd64\gh.exe') { Move-Item -Path 'gh_2.81.0_windows_amd64\gh.exe' -Destination '.\gh.exe' -Force }; Remove-Item -Path 'gh.zip' -Force; if (Test-Path 'gh_2.81.0_windows_amd64') { Remove-Item -Path 'gh_2.81.0_windows_amd64' -Recurse -Force }"
