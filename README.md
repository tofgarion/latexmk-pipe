# latexmk-pipe
A simple python-script in the spirit of rubber_pipe.py to be able to use latexmk with pipes. The makefile should work on any Linux distribution (use INSTALL_DIR variable to specify directory in which install `latexmk-pipe`).

You can use it to pass options "on the fly" to an existing LaTeX file for instance:

```
echo "\PassOptionsToClass{answers,grades}{exam} \input{exam150128.tex} | latexmk-pipe > exam150128.sol.pdf
```

Temporary files are deleted if no errors are produced during the compilation process.
