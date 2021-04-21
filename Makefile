test:
	./python_tests.sh

avro:
	PYTHONPATH=$(PYTHONPATH):./py/ python scripts/generate_avro.py