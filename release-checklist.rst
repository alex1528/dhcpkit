What not to forget
------------------

- Check that all previous changes have been committed
- Update version number in dhcpkit/__init__.py
- Check setup.py for correct release status (alpha, beta, stable)
- Update CHANGELOG.rst for release
- Update debian/changelog for release
- Update rpm/dhcpkit.spec for release
- Update README.rst if necessary
- generate-docs
- Commit all of the above
- git tag -s x.y.z
- git push --tags
- pypi-upload
- Create Ubuntu packages: ppa-upload
- Create CentOS packages: on each builder host:
  - python3 setup.py sdist
  - rpmbuild -ta dist/dhcpkit-x.y.x.tar.gz
  - rpm --addsign ~/rpmbuild/SRPMS/dhcpkit-*.rpm ~/rpmbuild/RPMS/noarch/dhcpkit-*.rpm
  - cp ~/rpmbuild/SRPMS/dhcpkit-*.rpm /mnt/repo/Source/Packages
  - cp ~/rpmbuild/RPMS/noarch/dhcpkit-*.rpm /mnt/repo/i386/Packages
  - cp ~/rpmbuild/RPMS/noarch/dhcpkit-*.rpm /mnt/repo/x86_64/Packages
  - createrepo --update --deltas /mnt/repo/Source
  - createrepo --update --deltas /mnt/repo/i386
  - createrepo --update --deltas /mnt/repo/x86_64
- Create new section for next release in CHANGELOG.rst
- Update version number in dhcpkit/__init__.py for development version
