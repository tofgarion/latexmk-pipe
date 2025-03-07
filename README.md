# latexmk-pipe

A simple Python script in the spirit of `rubber_pipe.py` to be able to
use latexmk with pipes.

## Install

To install `latexmk-pipe`, simply use `pip` with

```shell
pip install [--user] .
```

Use the `--user` option to install `latexmk-pipe` locally.

## Usage

You can use the `latexmk-pipe` executable to pass options "on the fly"
to an existing LaTeX file. For instance:

```shell
echo "\PassOptionsToClass{answers,grades}{exam} \input{exam150128.tex} | latexmk-pipe > exam150128.sol.pdf
```

Temporary files are deleted if no errors are produced during the
compilation process. The `-outdir` option can now be used.
