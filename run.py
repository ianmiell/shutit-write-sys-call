import shutit

s = shutit.create_session(session_type='vagrant',
	                      vagrant_num_machines='1',
                          vagrant_session_name='systemcall',
                          vagrant_cpus='4',
                          vagrant_memory='4096',
                          vagrant_synced_folder={'hostfolder':'/space','guestfolder':'/space','owner':'503','group':'503'},
                          loglevel='debug')

s.login('vagrant ssh')
s.login('sudo su -')
s.send('useradd imiell')
s.send('rm -rf /space/linux-sys-call-tmp && mkdir -p /space/linux-sys-call-tmp && cd /space/linux-sys-call-tmp')
s.install('bc')
s.install('xz')
s.install('tar')
s.install('curl')
s.install('build-essential')
s.send('apt build-dep -y -q linux-image-$(uname -r)')
s.send('apt-get source -y -q linux')
# TODO: 
#The file containing the system call table for x86_64 is located in arch/x86/entry/syscalls/syscall_64.tbl. This table is read by scripts and used to generate some of the boilerplate code, which makes our lives a lot easier! Go to the bottom of the first group (it ends at syscall 328 in version 4.7.1), and add the following line:
#
#329	common	stephen	sys_stephen
#
#
#System call function
#
#You can implement system calls anywhere, but miscellaneous syscalls tend to go in the kernel/sys.c file. Put this somewhere in the file:
#
#SYSCALL_DEFINE1(stephen, char *, msg)
#{
#  char buf[256];
#  long copied = strncpy_from_user(buf, msg, sizeof(buf));
#  if (copied < 0 || copied == sizeof(buf))
#    return -EFAULT;
#  printk(KERN_INFO "stephen syscall called with \"%s\"\n", buf);
#  return 0;
#}
#SYSCALL_DEFINEN is a family of macros that make it easy to define a system call with N arguments. The first argument to the macro is the name of the system call (without sys_ prepended to it). The remaining arguments are pairs of type and name for the parameters. Since our system call has one argument, we use SYSCALL_DEFINE1, and our only parameter is a char * which we name msg.
#
#An interesting issue that we encounter immediately is that we cannot directly use the msg pointer provided to us. There are several reasons why this is the case, but none are very obvious!
#
#The process could try to trick us into printing out data from kernel memory by giving us a pointer that maps to kernel space. This should not be allowed.
#We also need to respect the read/write/execute permissions of memory.
#To handle these issues, we use a handy strncpy_from_user() function which behaves like normal strncpy, but checks the user-space memory address first. If the string was too long or if there was a problem copying, we return EFAULT (although returning EINVAL for a too-long string might be better).
#
#Finally, we use printk with the KERN_INFO log level. This is actually a macro that resolves to a string literal. The compiler concatenates that with the format string and printk() uses it to determine the log level. Finally, printk does formatting similar to printf(), which is where the %s comes in.
s.send('cd linux-4.4.0')
s.send('cp /boot/config-4.4.0-131-generic .config')
s.send('CONFIG_LOCALVERSION="-miell"')
s.send('make -j4')
s.send('make modules install')
s.send('cp arch/x86_64/boot/bzImage /boot/vmlinuz-linux-${CONFIG_LOCALVERSION}')
s.send('sed s/linux/linux${CONFIG_LOCALVERSION}/g </etc/mkinitcpio.d/linux.preset >/etc/mkinitcpio.d/linux${CONFIG_LOCALVERSION}.preset')
s.send('mkinitcpio -p linux${CONFIG_LOCALVERSION}')
s.send('grub-mkconfig -o /boot/grub/grub.cfg')
s.send('sleep 60 && reboot &')
s.logout()
s.logout()
s.send('sleep 120')
s.login('vagrant ssh')
s.login('sudo su -')
s.pause_point('ok?')

# TODO
# s.send('reboot
