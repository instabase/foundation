test:
	./python_tests.sh

build-protos:
	protoc --proto_path=./proto/ --python_out=./py/ --mypy_out=./py ./proto/foundation/proto/*.proto

protos-to-dataclasses: build-protos
	PYTHONPATH=./py:./py/foundation/proto:$(PYTHONPATH) python3 scripts/protos_to_dataclasses.py

build: protos-to-dataclasses
