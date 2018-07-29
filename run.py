import shutit

s = shutit.create_session(session_type='vagrant',
	                      vagrant_num_machines='1',
                          vagrant_session_name='systemcall',
                          loglevel='debug')

s.login('vagrant ssh')
s.login('sudo su -')
s.install('bc')
s.install('xz')
s.install('tar')
s.install('curl')
s.install('build-essential')
s.send('apt build-dep -y linux-image-$(uname -r)')
s.send('apt-get source -y linux')
s.send('cd linux-4.4.0')
s.send('cp /boot/config-4.4.0-131-generic .config')
s.send('CONFIG_LOCALVERSION="-miell"')
s.send('make')
