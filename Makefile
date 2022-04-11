
SERVICE_NAME=pickaper
MYPY_FLAGS=--namespace-packages \
	--ignore-missing-imports \
	--no-implicit-reexport \
	--python-version 3.10 \
	--warn-unreachable \
	--warn-redundant-casts \
	--warn-incomplete-stub \
	--no-warn-no-return \
	--no-implicit-optional \
	--disallow-untyped-defs \
	--disallow-untyped-calls \
	--check-untyped-defs \
	--strict-equality \
	--disallow-untyped-decorators \
	--disallow-incomplete-defs \
	--disallow-any-generics \
	--show-error-codes \
	--pretty \
	--follow-imports=skip \
	--allow-redefinition \
	--no-incremental


isort:
	isort ${SERVICE_NAME} -w 120  -m 7 -j 4

test: mypy pylint flake8 unittest
	echo "Tests passed!"

mypy: build_test
	docker run --env-file=cicd/test.env -t ${SERVICE_NAME}:test python -m mypy ${SERVICE_NAME} ${MYPY_FLAGS}

flake8: build_test
	docker run --env-file=cicd/test.env -t ${SERVICE_NAME}:test python -m flake8 ${SERVICE_NAME} --max-line-length 120

pylint: build_test
	docker run --env-file=cicd/test.env -t ${SERVICE_NAME}:test python -m pylint ${SERVICE_NAME} --rcfile=cicd/.pylint.cfg

unittest: build_test
	docker run --env-file=cicd/test.env -t ${SERVICE_NAME}:test cicd/run_unittests.sh

build_test:
	docker build -t ${SERVICE_NAME}:test -f cicd/Dockerfile --target=test .
	echo "Test image build complete"

build: build_test test
	docker build -t ${SERVICE_NAME}:prod -f cicd/Dockerfile --target=prod .
	echo "Prod image build complete"
