test:
	./python_tests.sh

build-protos:
	protoc --proto_path=./proto/ --python_out=./py/foundation/proto/ --mypy_out=./py/foundation/proto ./proto/*.proto