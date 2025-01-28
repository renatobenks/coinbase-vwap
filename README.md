# Coinbase Volume-Weight-Average-Price

This project has been built to the purpose of calculating,
in real-time, the VWAP to the following tradings-pairs.

## Getting started

Follow the bellow instructions to run up the project.

> There are built-in scripts to make those processes easier,
> to go through, but feel free to run it manually

### Requirements

#### 2. Python (>=v3.8)

> I strongly encourage and recommend you to use pyenv to alternate
> between python versions, it helps you to properly manage it without pain

#### 2. pipenv (>= v2018.11.26)

> I've been using it over `pip` because it's fully better constructed
> to manage python dependencies from applications, [see here](https://pypi.org/project/pipenv/)

### Setting it up

Even `pipenv` already automatically creates an entire own virtualenv to install the project
dependencies, I recommend create a local one to be used, in favor to keep things unhidden,
given the flexibility to don't have to use `pipenv` to run into virtualenv, especially in production.

So, to do that, it's basically to run the following command in your terminal:

> it creates a `venv/` directory on project's root, which it's ignored on git by default

```bash
$ pipenv run virtualenv venv
```

### Installing

```bash
$ pipenv install
```

### Running

```bash
$ pipenv run python .
```

Or, use the built-in script to run that:

```bash
$ ./scripts/run.sh
```

In watch mode, just run:

```bash
$ ./scripts/run_watch.sh
```

### Testing

```bash
$ pipenv run python -m pytest
```

Or, use the built-in script to run that:

```bash
$ ./scripts/test.sh
```

If you're in development mode, to help you out on changing tests or writing new ones, just
run the following script:

```bash
$ ./scripts/test_development.sh
```

### Linting

> default standards based on PEC-8.

The code have been statically checked by [pylint](https://pypi.org/project/pylint/) linter.

To go through this, just run in your terminal, the following command:

```bash
$ pipenv run pylint
```

Or, use the built-in script to run that:

```bash
$ ./scripts/lint.sh
```
