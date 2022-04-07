import serial as ser
import time as t
#import soundseq as sq
#from soundseq import *
import threading  
from threading import *  
import serial.tools.list_ports as lsports
"""
[15, 208, 64, 0, 0, 0, 72, 0, 13, 4, 0, 0, 0, 18, 162,
0, 3, 3, 0, 0, 0,
4, 7, 168, 10, 0, 0, 0, 0, 0, 
5, 6, 194, 6, 53, 8, 62,
6, 6, 2, 0, 0, 
13, 14, 170, 6, 172, 0, 155, 255, 179, 255, 182, 255, 
16, 16, 0, 0, 240, 15, 246, 15, 251, 15, 248, 15, 241, 15, 0, 0, 0, 0, 51, 15, 0, 0, 0, 0, 43, 15, 0, 0, 0, 0, 241, 241, 15, 255, 15, 255, 15, 240, 15, 0, 0, 0, 0, 19, 12, 51, 255, 218, 5, 77, 84, 57, 55, 65, 99, 25, 81, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 170, 85, 77, 1, 15, 152, 65, 0, 0, 0, 72, 0, 13, 4, 0, 0, 0, 18, 163, 0, 3, 3, 0, 0, 0, 4, 7, 168, 10, 0, 0, 0, 0, 0, 5, 6, 184, 6, 45, 8, 53, 6, 6, 2, 0, 0, 13, 14, 192, 6, 159, 0, 181, 255, 180, 255, 154, 0, 186, 255, 184, 255, 16]


"""


class Kobuki:
    __in_buff=[]
    __temp = bytearray() 
    button_0=False
    button_1=False
    button_2=False
    right_bumper=False
    left_bumper=False
    center_bumper=False
    right_wheel_dropped=False
    left_wheel_dropped=False
    both_wheel_dropped=False
    __basic_sensor=[1,2,3,45,6,7,8,9,10,11,12,13,14,15,16,17]
    __docking_IR=[]
    __inertial_sensor=[]
    __cliffsensor=[]
    __current=[]
    __gyro=[]
    __general_purpose_input=[]
    
    def __init__(self,port):
        self.seri = port#ser.Serial(port,115200)
        print(self.seri)
        try:
            print(5/0)
        except (ZeroDivisionError):
            print('z')
        th1 = threading.Thread(target=Kobuki.dum)  
        th1.start()
    def getKobukiPort():
        ports = lsports.comports()
        flag=0
        for kport, desc, hwid in sorted(ports):
            if(desc.find('Kobuki') != -1):
                print("kobuki is connected in the Following Port")
                print("{}: {} [{}]".format(kport, desc, hwid))
                comPort = ser.Serial(port='COM8',baudrate=115200)
                flag=1
                return comPort  
            if(flag==1):
                print("kobuki Not connected")
                return None
        

    def play_on_sound(port):
        barr=bytearray([170,85,3,4,1,0,6])#header 0,header 1,length,payload(header,length,data),checksum
        port.write(barr)
        return True
    def play_off_sound(port):
        barr=bytearray([170,85,3,4,1,1,7])
        port.write(barr)
        return True
    def play_recharge_sound(port):
        barr=bytearray([170,85,3,4,1,2,4])
        port.write(barr)
        return True
    def kokubihardwareinfo(port):
        barr=bytearray([170,85,4,9,2,0,1,14])
        port.write(barr)
        return True
    def play_button_sound(port):
        barr=bytearray([170,85,3,4,1,3,5])
        port.write(barr)
        return True
    def play_error_sound(port):
        barr=bytearray([170,85,3,4,1,4,2])
        port.write(barr)
        return True
    def play_clean_start_sound(port):
        barr=bytearray([170,85,3,4,1,5,3])
        port.write(barr)
        return True
    def play_clean_stop_sound(port):
        barr=bytearray([170,85,3,4,1,6,0])
        port.write(barr)
        return True
    def play_custom_sound(note,ms,port):
        cs=0
        freq={
            'CN4':'1389.88',#'523.25',
            'CS4':'1311.91',#'554.37',
            'DN4':'1238.29',#'587.33',
            'DS4':'1168.76',#'622.25',
            'EN4':'1103.16',#'659.25',
            'FN4':'1041.25',#'698.46',
            'FS4':'982.82',#'739.99',
            'GN4':'927.64',#'783.99',
            'GS4':'875.59',# 830.61'
            'AN4':'826.24',#440.0
            'AS4':'780.06',#466.16,
            'BN4':'737.35',#493.88,
            'CN5':'694.95',#'523.25',
            'CS5':'655.94',#'554.37',
            'DN5':'619.13',#'587.33',
            'DS5':'584.38',#'622.25',
            'EN5':'551.59',#'659.25',
            'FN5':'520.62',#'698.46',
            'FS5':'491.40',#'739.99',
            'GN5':'463.82',#'783.99',
            'GS5':'437.79',# 830.61'
            'AN5':'413.22',# 880.00
            'AS5':'390.02',# 932.33
            'BN5':'368.13',# 987.77
        }
        val = int(float(freq.get(note)))
        barr=bytearray([170,85,5,3,3])
        barr+=val.to_bytes(2,byteorder='little')
        barr+=ms.to_bytes(1,byteorder='big')
        cs=barr[len(barr)-1]
        for i in range(2,len(barr)-1):
            #print(barr[i])
            cs=cs^barr[i]
        barr+=cs.to_bytes(1,byteorder='little')
        port.write(barr)
        return True

    def set_led1_red_colour(port):
        barr=bytearray([170,85,4,12,2,0,1,11])
        port.write(barr)
        return True
    def set_led1_green_colour(port):
        barr=bytearray([170,85,4,12,2,0,2,8])
        port.write(barr)
        return True
    def clr_led1(port):
        barr=bytearray([170,85,4,12,2,0,0,10])
        port.write(barr)
        return True

    def set_led2_red_colour(port):
        barr=bytearray([170,85,4,12,2,0,4,14])
        port.write(barr)
        return True
    def set_led2_green_colour(port):
        barr=bytearray([170,85,4,12,2,0,8,2])
        port.write(barr)
        return True
    def clr_led2(port):
        barr=bytearray([170,85,4,12,2,0,0,10])
        port.write(barr)
        return True
    def power_on_3v3_supply(port):
        barr=bytearray([170,85,4,12,2,0,0,10])
        port.write(barr)
        return True
    def set_digital_output_pin_0(port):
        barr=bytearray([170,85,4,12,2,1,0,11])
        port.write(barr)
        return True
    def set_digital_output_pin_1(port):
        barr=bytearray([170,85,4,12,2,2,0,8])
        port.write(barr)
        return True
    def set_digital_output_pin_2(port):
        barr=bytearray([170,85,4,12,2,4,0,14])
        port.write(barr)
        return True
    def set_digital_output_pin_3(port):
        barr=bytearray([170,85,4,12,2,8,0,2])
        port.write(barr)
        return True
    def move(self,left_velocity, right_velocity,port,rotate):
        if(rotate==0):
            botspeed=(left_velocity+right_velocity)/2
            if(left_velocity==right_velocity):
                botradius=0
            else:
                botradius=(230*(left_velocity+right_velocity))/(2*(right_velocity-left_velocity))
            self.base_control(port,int(botspeed),int(botradius))
        elif(rotate==1):
            botspeed=(left_velocity+right_velocity)/2
            
            print("botspeed: ",botspeed)
            if(left_velocity==right_velocity):
                botradius=0
            else:
                botradius=(230*(left_velocity+right_velocity))/(2*(right_velocity-left_velocity))
            
            self.base_control(port,int(botspeed),int(botradius))

    def base_control(port,speed,radius):
        cs=0
        barr=bytearray([170,85,6,1,4])
        barr+=speed.to_bytes(2,byteorder='little',signed=True)

        barr+=radius.to_bytes(2,byteorder='little',signed=True)
        #print(len(barr))
        for i in range(2,len(barr)-1):
            #print(barr[i])
            cs=cs^barr[i]
        barr+=cs.to_bytes(1,byteorder='big')
        #print(cs)
        #print(barr)
        port.write(barr)
    
    #seri = ser.Serial(str(sq.getKobukiPort),sq.getBaud)
   
    def dum():
        while(1):
            print('i')

    def read_data(self):
            while(1):

                #print("VALUE: ",int.from_bytes(seri.read(2),byteorder='little'))
                if(int.from_bytes(Kobuki.seri.read(2),byteorder='little')==333): 
                    __temp=Kobuki.seri.read(200)
                    __in_buff=[x for x in __temp]
                    print(__in_buff)
                
                    Kobuki.__basic_sensor=__in_buff[0:14]
                    Kobuki.__docking_IR=__in_buff[15:21]
                    Kobuki.__inertial_sensor=__in_buff[21:30]
                    print('inertial sensor: ',Kobuki.__inertial_sensor)
                    Kobuki.__cliffsensor=__in_buff[30:38]
                    Kobuki.__current=__in_buff[38:42]
                    #general_purpose_input=in_buff=
                    #print(current)
                    
                    """if(in_buff[12]==1):
                        #print("Button 0 Pressed")
                        button_0=True
                        print(button_0)
                    else:
                        button_0=False
                        #print(button_0)
                    if(in_buff[12]==2):
                        button_1=True
                        print(button_1)
                        #print("Button 1 Pressed")
                    else:
                        button_1=False
                        #print(button_1)
                    if(in_buff[12]==4):
                        #print("Button 2 Pressed")
                        button_2=True
                        print(button_2)
                    else:
                        button_2=False
                        #print(button_2)
                    if(in_buff[3]==1):
                        right_bumper=True
                        print("Right Bumper Pressed")
                        print(right_bumper)
                    else:
                        right_bumper=False
                        #print("Right Bumper Pressed")
                        #print(right_bumper)
                    if(in_buff[3]==2):
                        center_bumper=True
                        print(center_bumper)
                        print("cb")
                        t.sleep(5)
                    else:
                        center_bumper=False
                        #print(center_bumper)
                        #print("Center Bumper Pressed")
                    if(in_buff[3]==4):
                        left_bumper=True
                        #print(left_bumper)ip
                        #print("Left Bumper Pressed")
                    else:
                        left_bumper=False
                        #print(left_bumper)
                    if(in_buff[4]==1):
                        left_wheel_dropped=True
                        print(left_wheel_dropped)
                        #print("Left Wheel Dropped")
                    else:
                        left_wheel_dropped=False
                        #print(left_wheel_dropped)                                     
                    if(in_buff[4]==2):
                        right_wheel_dropped=True
                        print(right_wheel_dropped)
                        #print("Right Wheel Dropped")
                    else:
                        right_wheel_dropped=False
                        #print(right_wheel_dropped)
                    if(in_buff[4]==3):
                        both_wheel_dropped=True
                        print(both_wheel_dropped)
                        print("Both Wheel Dropped")
                    else:
                        both_wheel_dropped=False
                        #print(both_wheel_dropped)  """
                    #print(in_buff)   
                    #print("------------")                                       
            

    def basic_sensor_data(self):
        
        sensor={}
        sensor.update({'bumper':Kobuki.__basic_sensor[3]})
        sensor.update({'wheeldrop':Kobuki.__basic_sensor[4]})
        sensor.update({'cliff':Kobuki.__basic_sensor[5]})
        sensor.update({'Left_encoder':Kobuki.__basic_sensor[6:8]})
        sensor.update({'Right_encoder':Kobuki.__basic_sensor[8:10]})
        sensor.update({'LeftPWM':Kobuki.__basic_sensor[10]})
        sensor.update({'RightPWM':Kobuki.__basic_sensor[11]})
        sensor.update({'Button':Kobuki.__basic_sensor[12]})
        if(Kobuki.__basic_sensor[13]==0):
            sensor.update({'Charger':'DISCHARGING'})
        elif(Kobuki.__basic_sensor[13]==2):
            sensor.update({'Charger':'DOCKING_CHARGED'}) 
        elif(Kobuki.__basic_sensor[13]==6):
            sensor.update({'Charger':'DOCKING_CHARGING'})  
        elif(Kobuki.__basic_sensor[13]==18):
            sensor.update({'Charger':'ADAPTER_CHARGED'}) 
        elif(Kobuki.__basic_sensor[13]==22):
            sensor.update({'Charger':'ADAPTER_CHARGING'})
        sensor.update({'Batteryvolt':Kobuki.__basic_sensor[14]})
        sensor.update({'Overcurrentflag':Kobuki.__basic_sensor[15]})
        if(Kobuki.__basic_sensor[15]==1):
            sensor.update({'Overcurrent':'Leftwheel'})
        elif(Kobuki.__basic_sensor[15]==2):
            sensor.update({'Overcurrent':'Rightwheel'})
        return sensor
    
    def  docking_IR_data():
        dockingdata={}
        dockingdata.update({'centralsignal':Kobuki.__docking_IR[4]})
        dockingdata.update({'leftsignal':Kobuki.__docking_IR[5]})
        if(Kobuki.__docking_IR[3]==1):
            dockingdata.update({'rightsignal':'NEAR_LEFT'})
        elif(Kobuki.__docking_IR[3]==2):
            dockingdata.update({'rightsignal':'NEAR_CENTER'})
        elif(Kobuki.__docking_IR[3]==4):
            dockingdata.update({'rightsignal':'NEAR_RIGHT'})
        elif(Kobuki.__docking_IR[3]==8):
            dockingdata.update({'rightsignal':'FAR_CENTER'})
        elif(Kobuki.__docking_IR[3]==16):
            dockingdata.update({'rightsignal':'FAR_LEFT'})
        elif(Kobuki.__docking_IR[3]==32):
            dockingdata.update({'rightsignal':'FAR_RIGHT'})
        return dockingdata
    def inertial_sensor_data():
        angle={}
        angle.update({'angle':Kobuki.__inertial_sensor[2:4]})
        angle.update({'anglerate':Kobuki.__inertial_sensor[4:6]})
        return angle
    def cliffsensor_data():
        cliff={}
        cliff.update({'right_cliff_sensor':Kobuki.__cliffsensor[0]})
        cliff.update({'central_cliff_sensor':Kobuki.__cliffsensor[0]})
        cliff.update({'left_cliff_sensor':Kobuki.__cliffsensor[0]})
        return cliff
    def current_data():
        curr={}
        curr.update({'Leftmotor':Kobuki.__current[0]})
        curr.update({'Rightmotor':Kobuki.__current[0]})
        return curr
    def obstracle_avoidance(left_velocity,right_velocity,port):
        #print("right-bumper: ",right_bumper)
        t.sleep(0.01)
        if(left_bumper==True):
            sq.move(int(left_velocity+30),int(right_velocity),seri,0)
        else:
            pass
        if(right_bumper==True):
            
            sq.move(int(left_velocity),int(right_velocity+30),seri,0)
            #print("moving")
        else:
            pass
        if(center_bumper==True):
            
            rev_left=-(int(left_velocity))
            rev_right=-(int(right_velocity))
            sq.move(rev_left,rev_right,seri,0)
            
            sq.move(int(left_velocity),int(right_velocity),seri,1)
        else:
            pass
            
    def kobukistart(start):       
        th2 = threading.Thread(target=start)
        th2.start()
        th2.join()
        th1.join()
    


  

                                                                                            