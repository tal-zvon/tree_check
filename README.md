tree_check
==========

I have had 2 NAS (Network Attached Storage) devices for quite a while now,
and despite them both running RAID 5, there's always a chance that a unit
will suffer a catastrophic failure one of these days, and all its data will
be gone. I figured it might be nice if I had something keeping track of what
files/folders were on them both, so that if one of them dies, I would know
exactly what I may have lost.

After failing to find a suitable solution online, I wrote this python program,
which uses the tree command to create easily grep-able output with a list
of every file and folder in a given directory. It also works with git to
track changes in those directories over time.

This program is meant to be run by cron to keep track of your files. The
output looks like this:

	/etc/ssh
	|-- [  87]  fingerprint_check.sh*
	|-- [133K]  moduli
	|-- [1.6K]  ssh_config
	|-- [2.4K]  sshd_config
	|-- [ 668]  ssh_host_dsa_key
	|-- [ 602]  ssh_host_dsa_key.pub
	|-- [ 227]  ssh_host_ecdsa_key
	|-- [ 174]  ssh_host_ecdsa_key.pub
	|-- [1.6K]  ssh_host_rsa_key
	`-- [ 394]  ssh_host_rsa_key.pub

	 145K used in 0 directories, 10 files

Examples:

Show only top level files and folders:

        $ grep '^.--' output.txt

Show only top level folders:

        $ grep '^.--' output.txt | grep '/'

Show only top level files:

        $ grep '^.--' output.txt | grep -v '/'

Show files and folders 2 levels in:

        $ grep '^.--\|^.   .--' output.txt

