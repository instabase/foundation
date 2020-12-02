generate-proto:
	cd protos && ./gen.sh

generate-stubs:
	rm -rf stubs && \
	make generate-proto && \
	stubgen py/foundation -o stubs