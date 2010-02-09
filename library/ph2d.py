from library import core

class Ph2D:
	def __init__(self):
		self.veloc=[0, 0]
		self.velc_z = 0
		self.z = 0
		self.z2 = 0
		self.displacement = [0, 0]
		self.__displacement = [0, 0]
		self.gravity = -9.8
		
	def get_z(self):
		self.z2 = self.z
		self.z = max(0, 1./2 * self.gravity * (core.core.vdelay ** 2) + self.velc_z * core.core.vdelay + self.z  )		
		self.velc_z = self.gravity * core.core.vdelay + self.velc_z
		
		if self.z == 0:
			self.velc_z = 0
		return self.z - self.z2
		
	def update(self):
		self.displacement = self.veloc[:]
		self.displacement[0] = self.__displacement[0] + self.displacement[0] * 15 * core.core.vdelay
		self.displacement[1] = self.__displacement[1] + self.displacement[1] * 15 * core.core.vdelay - self.get_z()
		self.__displacement[0] = self.displacement[0] - int(self.displacement[0]) 
		self.__displacement[1] = self.displacement[1] - int(self.displacement[1])
		
	def go_down(self):  self.veloc[1]+=1
	def go_up(self):    self.veloc[1]-=1
	def go_right(self):  self.veloc[0]+=1
	def go_left(self):    self.veloc[0]-=1

	def not_go_down(self):  self.veloc[1]-=1
	def not_go_up(self):    self.veloc[1]+=1
	def not_go_right(self):  self.veloc[0]-=1
	def not_go_left(self):    self.veloc[0]+=1
	
	def jump(self):  self.velc_z = 35 if (self.velc_z == 0) else self.velc_z;