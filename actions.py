#!/usr/bin/python


from pisi.actionsapi import shelltools, get, autotools, pisitools
import os
import shutil

IgnoreAutodep = True

def setup():
    libdir = "/usr/lib" if get.buildTYPE() != "emul32" else "/usr/lib32"
    confEx = "--disable-tests" if get.buildTYPE() == "emul32" else ""
    del os.environ['LD_AS_NEEDED']
    autotools.configure ("--prefix=/usr \
                          --sysconfdir=/etc \
                          --localstatedir=/var \
                          --libexecdir=/usr/lib/dbus-1.0 \
                          --with-console-auth-dir=/run/console/\
                          --with-systemdsystemunitdir=/usr/lib/systemd/system\
                          --with-system-pid-file=/run/dbus/pid \
                          --with-system-socket=/run/dbus/system_bus_socket \
                          --libdir=%s \
                          --enable-epoll \
                          --enable-user-session \
                          --disable-static %s" % (libdir, confEx))

def build():
    autotools.make ()

def install():
    idir = get.installDIR()
    if get.buildTYPE() == "emul32":
        idir += "/derpmcderp"

    autotools.rawInstall ("DESTDIR=%s" % idir)
    if get.buildTYPE() != "emul32":
        os.system("chmod o+x %s/usr/lib/dbus-1.0/dbus-daemon-launch-helper" % get.installDIR())
        pisitools.removeDir("/var/run")
    else:
        pisitools.dodir("/usr")
        shelltools.system("mv \"%s/usr/lib32\" \"%s/usr/.\"" % (idir, get.installDIR()))
        shutil.rmtree(idir)
