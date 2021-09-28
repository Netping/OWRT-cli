SECTION="NetPing modules"
CATEGORY="Base"
TITLE="EPIC9 OWRT_CLI"

PKG_NAME="OWRT_CLI"
PKG_VERSION="Epic9.V1.S1"
PKG_RELEASE=4

MODULE_FILES=netpingcli.py
MODULE_FILES_DIR=/usr/lib/python3.7/

ETC_FILES=cli.py confparser.py
ETC_FILES_DIR=/etc/netping_cli/

CLI_LINK=netping

EBNF_DIR="frontend/model/ebnf/"
COMPILED_EBNF_DIR="grammars"


.PHONY: all install

all: install
	
install:
	mkdir $(ETC_FILES_DIR)
	#mkdir $(MODULE_FILES_DIR)
	for f in $(MODULE_FILES); do cp $${f} $(MODULE_FILES_DIR); done
	for f in $(ETC_FILES); do cp $${f} $(ETC_FILES_DIR); done

	#compile ebnf grammars for cli
	#mkdir $(ETC_FILES_DIR)$(COMPILED_EBNF_DIR)
	#for f in $(shell ls ${EBNF_DIR}); do fname=`echo $${f} | sed 's/\(.*\)\..*/\1/'`; python3 -m lark.tools.nearley $(EBNF_DIR)/$${f} main ./nearley > $(ETC_FILES_DIR)$(COMPILED_EBNF_DIR)/$${fname}.py; done

	ln -s $(ETC_FILES_DIR)cli.py /usr/bin/$(CLI_LINK)

clean:
	rm /usr/bin/$(CLI_LINK)
	rm -rf $(ETC_FILES_DIR)

	for f in $(MODULE_FILES); do rm -f $(MODULE_FILES_DIR)$${f}; done