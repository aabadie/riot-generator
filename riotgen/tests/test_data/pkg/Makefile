PKG_NAME=test
PKG_URL=http://test.com/pkg/src
PKG_VERSION=03176e844c79e6d134331855862a88056842f7f7
PKG_LICENSE=BSD

include $(RIOTBASE)/pkg/pkg.mk

all:
	$(QQ)"$(MAKE)" -C $(PKG_SOURCE_DIR) -f $(CURDIR)/$(PKG_NAME).mk
