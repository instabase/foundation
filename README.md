# Foundation

## Repo structure

There are Python and TypeScript versions of the Foundation types. Both the
Python and the TypeScript projects are rooted at this repo's root.

## Versioning

(Please talk to Andrey if this changes.)

To ship a new version of Foundation:
- Grep for `FOUNDATION_VERSION` and update the version strings.
- Make a commit that includes all the changes for your new version,
  including the version string bumps.
- Merge your commit into `instabase/foundation/main`.
- Make a new release in GitHub for your new Foundation version.
  This will also create a Git tag for the version.

## Installing

**(These instructions may be out-of-date. Please check with Aaron/Andrey/Erick.)**

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
