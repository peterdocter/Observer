#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import shutil
import threading
from Module import DataBase
from Gui import GUI

class TimeMachine :

	def __init__ (self) :
		self.db = DataBase()
		self.gui = GUI()
		self.jobStat = False
		self.backupTime = 60 * 30
		self.job = ''
		self.config = {}

	def main (self) :
		path, backup = self.getConfig()

		self.config = {
			'path': path,
			'backup': backup
		}

		self.gui.operat = {
			'start': self.listen,
			'stop': self.stop,
			'saveConfig': self.saveConfig
		}
		self.gui.config = self.config

		self.gui.run()

	def listen (self) :
		self.jobStat = True
		
		path = self.config['path']
		backup = self.config['backup']

		if not os.path.exists(path) :
			self.err(1)
		elif backup == '' :
			self.err(3)
		else :
			self.chkPath(backup)
			self.gui.backupStat = '备份开始'
			self.gui.startBtn(False)
			self.job = threading.Thread(target = self.sync, args = (path, backup))
			self.job.setDaemon(True)
			self.job.start()

	def sync (self, path, backup) :
		while self.jobStat == True:
			self.chkBackupList(backup)

			folderName = str(time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time())))
			backupPath = os.path.join(backup, folderName)

			try:
				shutil.copytree(path, backupPath)
				self.gui.backupStat = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + ' - 备份成功'
				time.sleep(self.backupTime)
			except Exception, e:
				self.stop()
				self.err(2)

		self.gui.backupStat = '备份结束'

	def stop (self) :
		self.jobStat = False
		self.gui.backupStat = '备份结束'
		self.gui.startBtn()

	def getFileList (self, path) :
		fileList = []
		for item in os.listdir(path) :
			itemPath = os.path.join(path, item)
			if os.path.isdir(itemPath) :
				fileList.extend(self.getFileList(itemPath))
			else :
				fileList.append({'file':item, 'path':path})

		return fileList

	def chkBackupList (self, path) :
		temp = []
		for item in os.listdir(path) :
			if item[0:1] != '.' :
				temp.append(item)

		if len(temp) > 5 :
			temp.sort(reverse = True)
			for x in temp[9:] :
				shutil.rmtree(os.path.join(path, x))

	def saveConfig (self) :
		self.config = self.gui.config
		self.setConfig(self.config['path'], self.config['backup'])

	def getConfig (self) :
		result = self.db.getLast()
		if len(result) > 0:
			return result[1], result[2]
		else :
			return '', ''

	def setConfig (self, targetPath, backupPath) :
		data = {
			'path': targetPath,
			'backup': backupPath
		}
		self.db.insert(data)

	def chkPath (self, path) :
		if not os.path.exists(path) :
			os.makedirs(path)

	def err (self, errNum) :
		if errNum == 1 :
			self.gui.notice('目标文件夹不存在！')
		elif errNum == 2 :
			self.gui.notice('文件夹内部分文件锁定，本程序无法复制！')
		elif errNum == 3 :
			self.gui.notice('请选择备份保存目录！')
		else :
			self.gui.notice('未知错误！')


obj = TimeMachine()
obj.main()







