# Foundation
A library for defining types and interfaces to be used across Instabase apps and libraries.

## Installing

If installing from source, run the following commands in this projects root directory

```
pip install .
```

To use this within a service, add the following lines to your Dockerfile (this assumes your build machine has access to the Instabase GitHub org):

```docker
RUN git clone git@github.com:instabase/foundation.git && \ # preferably at some version
    cd foundation && \
    pip install . && \
    cd .. && \
    rm -rf foundation
```

## Changelog

### v0.0.2
- Change some type definitions to be more flexible
- Additional types

### v0.0.1
- Basic types and serialization/deserialization
