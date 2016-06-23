#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import tkFileDialog
import ttk 
import tkMessageBox

class GUI :

	def __init__ (self) :
		self.masterTitle = 'Observer'
		self.slaveTitle = 'Config'
		self.aboutTitle = 'About'
		self.backupStat = ''
		self.operat = {
			'start': '',
			'stop': '',
			'saveConfig': ''
		}
		self.config = {'path':'', 'backup':''}
		self.tempConfig = {'path':'', 'backup':''}

	def __mainWindow (self) :
		self.master = Tkinter.Tk();

		self.master.title(self.masterTitle)
		self.master.resizable(width = 'false', height = 'false')

		self.__menu()
		self.__topBox()
		self.__showInfo()

	def __menu (self) :
		menubar = Tkinter.Menu(self.master)

		filemenu = Tkinter.Menu(menubar, tearoff = 0)
		filemenu.add_command(label = "Config", command = self.showConfig)
		filemenu.add_command(label = "Quit", command = self.master.quit)
		menubar.add_cascade(label = "File", menu = filemenu)

		about = Tkinter.Menu(menubar, tearoff = 0)
		about.add_command(label = "Info", command = self.__about)
		menubar.add_cascade(label = "About", menu = about)


		self.master.config(menu = menubar)

	def __topBox (self) :
		self.mainTop = Tkinter.Frame(self.master, bd = 10)
		self.mainTop.grid(row = 0, column = 0, sticky = '')

		self.startBtn()
		self.stopBtn()


	def __showInfo (self) :
		self.mainFoot = Tkinter.Frame(self.master, bd = 10)
		self.mainFoot.grid(row = 1, column = 0, sticky = '')

		self.dlStat = Tkinter.StringVar()
		self.dlZone = Tkinter.Label(self.mainFoot, textvariable = self.dlStat, width = 30, anchor = 'center')
		self.dlZone.grid(row = 0, column = 0, sticky = 'ew')

		self.__infoUpdate()

	def __infoUpdate (self) :
		self.dlStat.set(self.backupStat)

		self.timer = self.master.after(1000, self.__infoUpdate)

	def startBtn (self, stat = True) :
		if stat :
			self.sBtn = Tkinter.Button(self.mainTop, text = '启动', width = 10, command = self.operat['start'])
			self.sBtn.grid(row = 0, column = 0)
		else :
			self.sBtn = Tkinter.Button(self.mainTop, text = '监控中...', width = 10, command = '')
			self.sBtn.grid(row = 0, column = 0)

	def stopBtn (self) :
		self.sBtn = Tkinter.Button(self.mainTop, text = '停止', width = 10, command = self.operat['stop'])
		self.sBtn.grid(row = 0, column = 1)

	def showConfig (self) :
		self.slave = Tkinter.Toplevel();

		self.slave.title(self.slaveTitle)
		self.slave.resizable(width = 'false', height = 'false')

		self.inputFrame = Tkinter.Frame(self.slave, bd = 10)
		self.inputFrame.grid(row = 0, column = 0, sticky = '')

		self.pathVal = Tkinter.StringVar()
		fileLabel = Tkinter.Label(self.inputFrame, text = '目标目录')
		fileLabel.grid(row = 0)
		self.pathInput = Tkinter.Entry(self.inputFrame, textvariable = self.pathVal)
		self.pathVal.set(self.config['path'])
		self.pathInput.grid(row = 0, column = 1)		

		pathButton = Tkinter.Button(self.inputFrame, text = '选择', command = self.__chooseTarget)
		pathButton.grid(row = 0, column = 2)

		self.backVal = Tkinter.StringVar()
		fileLabel = Tkinter.Label(self.inputFrame, text = '备份目录')
		fileLabel.grid(row = 1)
		self.backInput = Tkinter.Entry(self.inputFrame, textvariable = self.backVal)
		self.backVal.set(self.config['backup'])
		self.backInput.grid(row = 1, column = 1)		

		pathButton = Tkinter.Button(self.inputFrame, text = '选择', command = self.__chooseBackup)
		pathButton.grid(row = 1, column = 2)

		btnFrame = Tkinter.Frame(self.slave, bd = 10)
		btnFrame.grid(row = 1, column = 0, sticky = '')

		funcButton = Tkinter.Button(btnFrame, text = 'Save', command = self.__saveConfig)
		funcButton.grid(row = 0, column = 1, sticky = 'e')
		quitButton = Tkinter.Button(btnFrame, text = 'Quit', command = self.slave.withdraw)
		quitButton.grid(row = 0, column = 2, sticky = 'e')

		# self.slave.mainloop()

	def __chooseTarget (self) :
		self.pathVal = Tkinter.StringVar()
		self.targetPath = tkFileDialog.askdirectory(initialdir="/",title='请选择目录')
		self.pathInput = Tkinter.Entry(self.inputFrame, textvariable = self.pathVal)
		self.pathVal.set(self.targetPath.strip())
		self.tempConfig['path'] = self.targetPath.strip()
		self.pathInput.grid(row = 0, column = 1)

	def __chooseBackup (self) :
		self.backVal = Tkinter.StringVar()
		self.backupPath = tkFileDialog.askdirectory(initialdir="/",title='请选择目录')
		self.backInput = Tkinter.Entry(self.inputFrame, textvariable = self.backVal)
		self.backVal.set(self.backupPath.strip())
		self.tempConfig['backup'] = self.backupPath.strip()
		self.backInput.grid(row = 1, column = 1)

	def __saveConfig (self) :
		self.config['path'] = (self.tempConfig['path'] != '') and self.tempConfig['path'] or self.config['path']
		self.config['backup'] = (self.tempConfig['backup'] != '') and self.tempConfig['backup'] or self.config['backup']
		self.slave.withdraw()
		self.operat['saveConfig']()

	def notice (self, msg) :
		tkMessageBox.showinfo('错误', msg)


	def __about(self):
		self.about = Tkinter.Toplevel();

		self.about.title(self.aboutTitle)
		self.about.resizable(width = 'false', height = 'false')

		label = Tkinter.Label(self.about, text="Observer", font = ("Helvetica", "16", 'bold'), anchor = 'center')
		label.grid(row = 0)

		info = [
			'Support: OS X',
			'Website: https://github.com/EvilCult/Observer',
		]

		information = Tkinter.Text(self.about, height = 10, width = 30, highlightthickness = 0)
		information.grid(row = 1, padx = 10, pady = 5)
		for n in info :
			information.insert('end', n.split(': ')[0] + '\n')
			information.insert('end', n.split(': ')[1] + '\r')

		label = Tkinter.Label(self.about, text="Version: Beta 1.0.0", font = ("Helvetica", "10"), anchor = 'center')
		label.grid(row = 2)
		label = Tkinter.Label(self.about, text="Author: EvilCult.", font = ("Helvetica", "10"), anchor = 'center')
		label.grid(row = 3)


	def run (self) :
		self.__mainWindow()
		self.master.mainloop()

# obj = GUI()
# obj.showConfig()