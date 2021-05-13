test:
	./python_tests.sh

build-protos:
	protoc --proto_path=./proto/ --python_out=./py/foundation/proto/ --mypy_out=./py/foundation/proto ./proto/*.proto

protos-to-dataclasses:
	
	PYTHONPATH=./py:./py/foundation/proto:$(PYTHONPATH) python3 scripts/protos_to_dataclasses.py