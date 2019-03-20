CURDIR := $(shell pwd)
MUNKIPKG := /usr/local/bin/munkipkg
PKG_ROOT := $(CURDIR)/pkg/jamf-versioner/payload
PKG_BUILD := $(CURDIR)/pkg/jamf-versioner/build
PKG_VERSION := $(shell defaults read $(CURDIR)/pkg/jamf-versioner/build-info.plist version)

objects = "$(PKG_ROOT)/usr/local/munki/versioner"


default : "$(PKG_BUILD)/jamf-versioner-$(PKG_VERSION).pkg"


"$(PKG_BUILD)/jamf-versioner-$(PKG_VERSION).pkg": $(objects)
	cd $(CURDIR)/pkg && $(MUNKIPKG) jamf-versioner


"$(PKG_ROOT)/usr/local/munki/versioner":
	@echo "Copying versioner folder into munki folder"
	mkdir -p "$(PKG_ROOT)/usr/local/munki/versioner"
	cp "$(CURDIR)/code/jamf_versioner.py" "$(CURDIR)/code/write_version_to_json_file.py" "$(CURDIR)/code/__init__.py" "$(PKG_ROOT)/usr/local/munki/versioner"


.PHONY : clean
clean :
	@echo "Cleaning up package root"
	rm -rf $(PKG_ROOT)/usr/local/munki/versioner
	rm $(CURDIR)/pkg/jamf-versioner/build/*.pkg
