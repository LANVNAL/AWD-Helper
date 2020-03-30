#!/usr/bin/env python
#coding=utf-8

import sys
import os
import pwd
import hashlib
import datetime
import time
import getpass
import requests

CURRENT_UID = pwd.getpwnam(getpass.getuser()).pw_uid
CURRENT_GID = pwd.getpwnam(getpass.getuser()).pw_gid

def scan_files(directory, prefix=None, postfix=None):
	file_list = []
	dir_list  = []
	directory = os.path.normpath(directory)
	for parent, dirnames, filenames in os.walk(directory):
		for dirname in dirnames:
			dir_list.append(os.path.join(parent, dirname))
		
		for filename in filenames:
			if postfix:
				if filename.endswith(postfix):
					file_list.append(os.path.join(parent, filename))
			elif prefix:
				if filename.startswith(prefix):
					file_list.append(os.path.join(parent, filename))
			else:
				file_list.append(os.path.join(parent, filename))
				
	return {'file': file_list, 'dir': dir_list}

def md5sum(filename):
	md5 = ''
	if os.access(filename, os.F_OK) and os.access(filename, os.R_OK):
		fd = open(filename, 'rb')
		fcont = fd.read()
		fd.close()
		md5 = hashlib.md5(fcont).hexdigest()
	return md5

def diff(src_dir, dst_dir):
	modified_file  = []
	deleted_file   = []
	added_file     = []
	modified_dir   = []
	deleted_dir    = []
	added_dir      = []
	
	src_dir = os.path.normpath(src_dir)
	dst_dir = os.path.normpath(dst_dir)
	
	src_file_list  = scan_files(src_dir)['file']
	src_dir_list   = scan_files(src_dir)['dir']
	dst_file_list = scan_files(dst_dir)['file']
	dst_dir_list  = scan_files(dst_dir)['dir']
	
	short_dst_file_list = []
	short_dst_dir_list  = []
	
	for dfile in dst_file_list:
		short_dst_file_list.append(dfile[len(dst_dir):])
		found = False
		for sfile in src_file_list:
			if dfile[len(dst_dir):] == sfile[len(src_dir):]:
				found = True
				if md5sum(dfile) != '' and md5sum(dfile) != md5sum(sfile):
					modified_file.append(dfile[len(dst_dir):])
				elif os.stat(dfile).st_mode != os.stat(sfile).st_mode:
					modified_file.append(dfile[len(dst_dir):])
				break
		if found == False:
			added_file.append(dfile[len(dst_dir):])

	for sfile in src_file_list:
		if sfile[len(src_dir):] not in short_dst_file_list:
			deleted_file.append(sfile[len(src_dir):])
	
	for ddir in dst_dir_list:
		short_dst_dir_list.append(ddir[len(dst_dir):])
		found = False
		for sdir in src_dir_list:
			if ddir[len(dst_dir):] == sdir[len(src_dir):]:
				found = True
				if os.stat(ddir).st_mode != os.stat(sdir).st_mode:
					modified_dir.append(ddir[len(dst_dir):])
				break
		if found == False:
			added_dir.append(ddir[len(dst_dir):])

	for sdir in src_dir_list:
		if sdir[len(src_dir):] not in short_dst_dir_list:
			deleted_dir.append(sdir[len(src_dir):])
			
	return {'modified_file': modified_file, 'deleted_file': deleted_file, 'added_file': added_file, 'modified_dir': modified_dir, 'deleted_dir': deleted_dir, 'added_dir': added_dir}

def send_diff(msg,url):
	data = {'msg':msg}
	try:
		requests.post(url=url,data=data)
	except:
		return

def keep_it_same(src_dir, dst_dir, log_dir, receive_url):
	diff_files = diff(src_dir, dst_dir)
	dirname = ''
	for key,value in diff_files.items():
		if len(value) > 0:
			dirname = log_dir + '/' + datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')
			if not os.path.exists(dirname):  os.makedirs(dirname)
			break

	
	for modifiedfile in diff_files['modified_file']:
		srcfile = src_dir + modifiedfile
		dstfile = dst_dir + modifiedfile
		backupfile = dirname + '/modified' + modifiedfile
		if not os.path.exists(os.path.dirname(backupfile)): os.makedirs(os.path.dirname(backupfile))
		try:
			print 'Modified File: ' + dstfile
			msg = 'Modified File: ' + dstfile
			send_diff(msg, receive_url)
			os.system('cp -ap ' + dstfile + ' ' + backupfile + ' && cp -ap ' + srcfile + ' ' + dstfile)
		except:
			pass
	
	for deletedfile in diff_files['deleted_file']:
		srcfile = src_dir + deletedfile
		dstfile = dst_dir + deletedfile
		backupfile = dirname + '/deleted' + deletedfile
		if not os.path.exists(os.path.dirname(backupfile)): os.makedirs(os.path.dirname(backupfile))
		if not os.path.exists(os.path.dirname(dstfile)): os.makedirs(os.path.dirname(dstfile))
		try:
			print 'Deleted File: ' + dstfile
			msg = 'Deleted File: ' + dstfile
			send_diff(msg, receive_url)
			os.system('cp -ap ' + srcfile + ' ' + backupfile + ' && cp -ap ' + srcfile + ' ' + dstfile)
		except:
			pass
	
	for addedfile in diff_files['added_file']:
		dstfile = dst_dir + addedfile
		backupfile = dirname + '/added' + addedfile
		if not os.path.exists(os.path.dirname(backupfile)): os.makedirs(os.path.dirname(backupfile))
		try:
			print 'Added File: ' + dstfile
			msg = 'Added File: ' + dstfile
			send_diff(msg, receive_url)
			os.system('cp -ap ' + dstfile + ' ' + backupfile + ' && rm -rf ' + dstfile)
		except:
			pass
			
	for modifieddir in diff_files['modified_dir']:
		srcdir = src_dir + modifieddir
		dstdir = dst_dir + modifieddir
		backupfile = dirname + '/modified' + modifieddir
		if not os.path.exists(os.path.dirname(backupfile)): os.makedirs(os.path.dirname(backupfile))
		try:
			print 'Modified Dir: ' + dstdir
			msg = 'Modified Dir: ' + dstdir
			send_diff(msg, receive_url)
			os.system('cp -ap ' + dstdir + ' ' + backupfile + ' && rm -rf '+dstdir)
			os.system('cp -ap ' + srcdir + ' ' + dstdir)
		except:
			pass
			
	for deleteddir in diff_files['deleted_dir']:
		srcdir = src_dir + deleteddir
		dstdir = dst_dir + deleteddir
		backupfile = dirname + '/deleted' + deleteddir
		if not os.path.exists(os.path.dirname(backupfile)): os.makedirs(os.path.dirname(backupfile))
		if not os.path.exists(os.path.dirname(dstdir)): os.makedirs(os.path.dirname(dstdir))
		try:
			print 'Deleted Dir: ' + dstdir
			msg = 'Deleted Dir: ' + dstdir
			send_diff(msg, receive_url)
			os.system('cp -ap ' + srcdir + ' ' + backupfile + ' && cp -ap ' + srcdir + ' ' + dstdir)
		except:
			pass
			
	for addeddir in diff_files['added_dir']:
		dstdir = dst_dir + addeddir
		backupfile = dirname + '/added' + addeddir
		if not os.path.exists(os.path.dirname(backupfile)): os.makedirs(os.path.dirname(backupfile))
		try:
			print 'Added Dir: ' + dstdir
			msg = 'Added Dir: ' + dstdir
			send_diff(msg, receive_url)
			os.system('cp -ap ' + dstdir + ' ' + backupfile + ' && rm -rf ' + dstdir)
		except:
			pass
		
if __name__ == '__main__':
	if len(sys.argv) != 5:
		print 'Usage: ' + sys.argv[0] + ' srcdir dstdir logdir receive_url'
		exit()
	
	os.system('mkdir ' + sys.argv[3] + ' && chmod 755 ' + sys.argv[3])
	
	while True:
		print '# Keep It Same ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		keep_it_same(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
		time.sleep(1)
