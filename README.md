# Spritter CLI

Command line interface for fetching fuel prices via the spritter library.

## Install

Get the repo and included submodules, then install the CLI package:

```bash
git clone --recursive https://github.com/spritter-org/spritter-cli
pip install -e spritter-cli
```

To force-update the associated [spritter](https://github.com/spritter-org/spritter) library, use:

```bash
pip install --force-reinstall -e spritter-cli
```

## Usage

> Get supported providers and station IDs can be found in the [spritter library repository](https://github.com/spritter-org/spritter/?tab=readme-ov-file#providers)

```bash
spritter --provider JET --id 2640f98f48
```
