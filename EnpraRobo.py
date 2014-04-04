#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file EnpraRobo.py
 @brief Robot
 @date $Date$


"""
import sys, traceback
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import serial

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
enprarobo_spec = ["implementation_id", "EnpraRobo", 
		 "type_name",         "EnpraRobo", 
		 "description",       "Robot", 
		 "version",           "1.0.0", 
		 "vendor",            "OgataLab", 
		 "category",          "Tes", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.filename", "/dev/ttyACM0",
		 "conf.__widget__.filename", "text",
		 ""]
# </rtc-template>

##
# @class EnpraRobo
# @brief Robot
# 
# 
class EnpraRobo(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_leftMotor = RTC.TimedLong(RTC.Time(0,0),0)
		"""
		"""
		self._leftMotorIn = OpenRTM_aist.InPort("leftMotor", self._d_leftMotor)
		self._d_rightMotor = RTC.TimedLong(RTC.Time(0,0),0)
		"""
		"""
		self._rightMotorIn = OpenRTM_aist.InPort("rightMotor", self._d_rightMotor)
		self._d_servo = RTC.TimedLong(RTC.Time(0,0),0)
		"""
		"""
		self._servoIn = OpenRTM_aist.InPort("servo", self._d_servo)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  filename
		 - DefaultValue: /dev/ttyACM0
		"""
		self._filename = ['/dev/ttyACM0']
		
		# </rtc-template>

		self.rightMotor = 0
		self.leftMotor = 0
		self.servo = 90
		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("filename", self._filename, "/dev/ttyACM0")
		
		# Set InPort buffers
		self.addInPort("leftMotor",self._leftMotorIn)
		self.addInPort("rightMotor",self._rightMotorIn)
		self.addInPort("servo",self._servoIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
		print self._filename[0]
		try:
			self.serial = serial.Serial(self._filename[0])
		except:
			traceback.print_exc()
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
		self.serial.close()
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
		try:
			if self._leftMotorIn.isNew():
				self.leftMotor = self._leftMotorIn.read().data
			if self._rightMotorIn.isNew():
				self.rightMotor = self._rightMotorIn.read().data
			if self._servoIn.isNew():
				self.servo = self._servoIn.read().data - 90
			sys.stdout.write('%d,%d,%d=\n' % (self.leftMotor, self.rightMotor, self.servo))
			self.serial.write('%d,%d,%d=' % (self.leftMotor, self.rightMotor, self.servo))
		#print serial.readline()
		except:
			traceback.print_exc()
			return RTC.RTC_ERROR
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def EnpraRoboInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=enprarobo_spec)
    manager.registerFactory(profile,
                            EnpraRobo,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    EnpraRoboInit(manager)

    # Create a component
    comp = manager.createComponent("EnpraRobo")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

