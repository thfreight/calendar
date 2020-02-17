#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  layout.py
#  
#  Copyright 2020 Sun Min <sun@sun-mint>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from tkinter import *
from tkinter import ttk

class layout:
	
	################################################################
	##### 建立主窗口
	################################################################	
	def __init__(self):
		self.main_window = Tk()
		self.main_window.geometry('1024x600')
		self.main_window.title('Morning Sun Calendar')
		self.main_window.configure(background="#1c1c1c")
		self.main_window.overrideredirect(True) # 隐藏窗口的标题行

	################################################################	
	#####    定义使用的色彩
	################################################################
		self.fg_grey    = "#c0c0c0"
		self.fg_gold    = "#ffd700"
		self.bg_blue    = "#064676"
		self.bg_black   = "#1c1c1c"
		self.bg_green   = "#2f4f4f"

	################################################################
	#####    定义使用的有关样式
	################################################################
		# 设置Frame的Style
		myStyle = ttk.Style()
		myStyle.theme_use("classic")
		
		# 设置Frame的样式
		myStyle.configure("TFrame",
						  background    = self.bg_black,     
						  foreground    = self.fg_grey, )

		# 设置Label的样式
		myStyle.configure("TLabel", 
						  background    = self.bg_black, 
						  foreground    = self.fg_grey,)
		
		# 设置一般按钮样式
		myStyle.configure("TButton",
						  foreground    = self.fg_grey,
						  background    = self.bg_black, 
						  relief        = "flat",
						  font          = 'helvetica 12',)
		myStyle.map("TButton",
					foreground=[('pressed',     self.fg_grey), 
								('active',      self.fg_grey)],
					background=[('pressed',     self.bg_black), 
								('disabled',    self.bg_black), 
								('active',      self.bg_black)]
					)

		myStyle.configure("red.TFrame", background="red")
		
		###########################################################
		###  用Frame设置界面布局
		###########################################################
		# 设置布局的frame, 左边的Frame
		self.left_frame = ttk.Frame(self.main_window, 
								width   = 375, 
								height  = 600)
		self.left_frame.grid_propagate(0) 				#####	设置尺寸不可调正
		self.left_frame.grid(row = 0, column = 0)
	
		# 设置布局的frame, 右边的Frame
		self.right_frame = ttk.Frame(self.main_window, 
								width   = 649, 
								height  = 600)
		self.right_frame.grid_propagate(0) 				#####	设置尺寸不可调正
		self.right_frame.grid(row = 0, column = 1)

		# 在左边Frame中，设置时钟Frame
		self.clock_frame = ttk.Frame(self.left_frame, 
								width   = 375, 
								height  = 200, 
								padding = (20, 20, 20, 20))
		self.clock_frame.grid_propagate(0)
		self.clock_frame.grid(row = 0, column = 0)

		# 在左边Frame中，设置显示当天细节Frame
		self.remind_frame = ttk.Frame(self.left_frame,
								width   = 375,
								height  = 400,
								padding = (20, 20, 20, 20))
		self.remind_frame.grid(row = 1, column = 0)
	
		# 设置右边Frame中的日历抬头Frame
		self.calendar_head_frame = ttk.Frame(self.right_frame, 
										width   = 649,
										height  = 100,
										padding = (20, 20, 20, 0),)
		self.calendar_head_frame.grid_propagate(0)
		self.calendar_head_frame.grid_columnconfigure(0, weight=1)
		self.calendar_head_frame.grid_columnconfigure(2, weight=1)
		self.calendar_head_frame.grid(row = 0, column = 0,)
		
		# 设置右边Frame中的日历Fram
		self.calendar_content_frame = ttk.Frame(self.right_frame,
										   width    = 649,
										   height   = 500,
										   padding  = (20, 0, 20, 5),)
		self.calendar_content_frame.grid(row = 1, column = 0)
		###################################################
		### 布局完成
		###################################################
