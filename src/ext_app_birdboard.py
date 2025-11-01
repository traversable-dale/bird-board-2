class app_birdboard:

	def __init__(self,ownerComp):
		self.ownerComp = ownerComp
	
	def Reboot(self):
		print("REBOOTING")
		import os
		# Restart the system
		os.system("shutdown /r /t 0")
		return
		
	def Shutdown(self):
		print("SHUTTING DOWN")
		import os
		# Restart the system
		os.system("shutdown -s")
		return
		
	def Test(self):
		print("TESTING")
		return
		
	def Stop(self):
		op.birdboard_audio.op('Hotel_California').par.play = 0
		op.birdboard_audio.op('Hotel_California').par.cuepulse.pulse()
		op.birdboard_audio.op('Pretty_Girl_Rock').par.play = 0
		op.birdboard_audio.op('Pretty_Girl_Rock').par.cuepulse.pulse()
		op.birdboard_audio.op('Like_A_Virgin').par.play = 0
		op.birdboard_audio.op('Like_A_Virgin').par.cuepulse.pulse()
		print('STOP')
		return
		
	def Play(self):
		op.birdboard_audio.op('filein_ambi_day').par.play = 1
		op.birdboard_audio.op('filein_ambi_night').par.play = 1
		op.birdboard_audio.op('filein_nature_day').par.play = 1
		op.birdboard_audio.op('filein_nature_night').par.play = 1
		
		op.birdboard_audio.op('audio_par')['filter_high',1] = 0
		op.birdboard_audio.op('audio_par')['filter_low',1] = 0
		print('PLAY')
		return

	def Normal(self):
		op.birdboard_audio.op('special').par.const0value = 0
		op.birdboard_audio.op('special_nature').par.const0value = 0

	def Special(self):
		op.birdboard_audio.op('special').par.const0value = 1

	def SpecialNature(self):
		op.birdboard_audio.op('special_nature').par.const0value = 1
		
	def HotelCalifornia(self):
		op.birdboard_audio.op('Hotel_California').par.play = 1
		op.birdboard_audio.op('Hotel_California').par.cuepulse.pulse()
		return

	def LikeAVirgin(self):
		op.birdboard_audio.op('Like_A_Virgin').par.play = 1
		op.birdboard_audio.op('Like_A_Virgin').par.cuepulse.pulse()
		return

	def PrettyGirlRock(self):
		op.birdboard_audio.op('Pretty_Girl_Rock').par.play = 1
		op.birdboard_audio.op('Pretty_Girl_Rock').par.cuepulse.pulse()
		return
		
	def Idle(self):
		print('IDLE')
		op.birdboard_audio.op('audio_par')['filter_high',1] = 1
		op.birdboard_audio.op('audio_par')['filter_low',1] = 1
		return
		
		