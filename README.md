# Foundation
A library for defining types and interfaces to be used across Instabase apps and libraries.

## Installing

If installing from source, run the following commands in this projects root directory

```
make generate-proto
pip install .
```

To use this within a service, add the following lines to your Dockerfile (this assumes your build machine has access to the Instabase GitHub org):

```docker
RUN git clone git@github.com:instabase/foundation.git && \ # preferably at some version
    cd foundation && \
    make generate-proto && \
    pip install . && \
    cd .. && \
    rm -rf foundation
```

## Generate Typings

The following command can be used to generate mypy stubs, which can be copied into a codebase

```
make generate-stubs
```

The stubs will be written to a `stubs` folder in the root project directory.