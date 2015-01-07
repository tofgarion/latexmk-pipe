INSTALL_DIR=/usr/local/bin

install:
	cp latexmk_pipe.py $(INSTALL_DIR)/
	chmod 755 $(INSTALL_DIR)/latexmk_pipe.py
	ln -sf $(INSTALL_DIR)/latexmk_pipe.py $(INSTALL_DIR)/latexmk_pipe
