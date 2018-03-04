PKG_NAME={name}
PKG_URL={url}
PKG_VERSION={hash}
PKG_LICENSE={license}

.PHONY: all

all: git-download
	@cp Makefile.${{PKG_NAME}} $(PKG_BUILDDIR)/Makefile
	"$(MAKE)" -C $(PKG_BUILDDIR)

include $(RIOTBASE)/pkg/pkg.mk
