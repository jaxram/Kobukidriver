
import serial as ser
import time as t
import threading  

import serial.tools.list_ports as lsports



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
    __basic_sensor=[]
    __docking_IR=[]
    __inertial_sensor=[]
    __cliffsensor=[]
    __current=[]
    __gyro=[]
    __general_purpose_input=[]
    global __th1
    def __getKobukiPort():
        
        ports = lsports.comports()
        flag=0
        print(
            ports
        )
        for kport, desc, hwid in sorted(ports):
            
            if( desc.find('USB Serial Port')!=-1):
                print("kobuki is connected in the Following Port")
                print("{} {} [{}]".format(kport, desc, hwid))
                print(kport[0:4])
                Kobuki.seri = ser.Serial(port=kport[0:4],baudrate=115200)
                return Kobuki.seri
            elif(desc.find('Kobuki') != -1):
                #print(kport,desc)
                print("kobuki is connected in the Following Port")
                print("{} {} [{}]".format(kport, desc, hwid))
                #print(kport)
                Kobuki.seri = ser.Serial(port=kport,baudrate=115200)
                return Kobuki.seri
            else:
                raise Exception("Kobuki is not connected")
        
        

    def __init__(self):
        Kobuki.__getKobukiPort()
        __th1 = threading.Thread(target=Kobuki.read_data)  
        __th1.start()
       
    
    def play_on_sound():
        barr=bytearray([170,85,3,4,1,0,6])
        #header 0,header 1,length,payload(header,length,data),checksum
        Kobuki.seri.write(barr)
        return True
    def play_off_sound():
        barr=bytearray([170,85,3,4,1,1,7])
        Kobuki.seri.write(barr)
        return True
    def play_recharge_sound():
        barr=bytearray([170,85,3,4,1,2,4])
        Kobuki.seri.write(barr)
        return True
    def kokubihardwareinfo():
        barr=bytearray([170,85,4,9,2,0,1,14])
        Kobuki.seri.write(barr)
        return True
    def play_button_sound():
        barr=bytearray([170,85,3,4,1,3,5])
        Kobuki.seri.write(barr)
        return True
    def play_error_sound():
        barr=bytearray([170,85,3,4,1,4,2])
        Kobuki.seri.write(barr)
        return True
    def play_clean_start_sound():
        barr=bytearray([170,85,3,4,1,5,3])
        Kobuki.seri.write(barr)
        return True
    def play_clean_stop_sound():
        barr=bytearray([170,85,3,4,1,6,0])
        Kobuki.seri.write(barr)
        return True
    def play_custom_sound(note,ms):
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
        Kobuki.seri.write(barr)
        return True

    def set_led1_red_colour():
        barr=bytearray([170,85,4,12,2,0,1,11])
        Kobuki.seri.write(barr)
        return True
    def set_led1_green_colour():
        barr=bytearray([170,85,4,12,2,0,2,8])
        Kobuki.seri.write(barr)
        return True
    def clr_led1():
        barr=bytearray([170,85,4,12,2,0,0,10])
        Kobuki.seri.write(barr)
        return True

    def set_led2_red_colour():
        barr=bytearray([170,85,4,12,2,0,4,14])
        Kobuki.seri.write(barr)
        return True
    def set_led2_green_colour():
        barr=bytearray([170,85,4,12,2,0,8,2])
        Kobuki.seri.write(barr)
        return True
    def clr_led2():
        barr=bytearray([170,85,4,12,2,0,0,10])
        Kobuki.seri.write(barr)
        return True
    def power_on_3v3_supply():
        barr=bytearray([170,85,4,12,2,0,0,10])
        Kobuki.seri.write(barr)
        return True
    def set_digital_output_pin_0():
        barr=bytearray([170,85,4,12,2,1,0,11])
        Kobuki.seri.write(barr)
        return True
    def set_digital_output_pin_1():
        barr=bytearray([170,85,4,12,2,2,0,8])
        Kobuki.seri.write(barr)
        return True
    def set_digital_output_pin_2():
        barr=bytearray([170,85,4,12,2,4,0,14])
        Kobuki.seri.write(barr)
        return True
    def set_digital_output_pin_3():
        barr=bytearray([170,85,4,12,2,8,0,2])
        Kobuki.seri.write(barr)
        return True
    def move(self,left_velocity, right_velocity,rotate):
        if(rotate==0):
            botspeed=(left_velocity+right_velocity)/2
            if(left_velocity==right_velocity):
                botradius=0
            else:
                botradius=(230*(left_velocity+right_velocity))/(2*(right_velocity-left_velocity))
            self.base_control(int(botspeed),int(botradius))
        elif(rotate==1):
            botspeed=(left_velocity+right_velocity)/2
            
            print("botspeed: ",botspeed)
            if(left_velocity==right_velocity):
                botradius=0
            else:
                botradius=(230*(left_velocity+right_velocity))/(2*(right_velocity-left_velocity))
            
            self.base_control(int(botspeed),int(botradius))

    def base_control(speed,radius):
        cs=0
        barr=bytearray([170,85,6,1,4])
        barr+=speed.to_bytes(2,byteorder='little',signed=True)

        barr+=radius.to_bytes(2,byteorder='little',signed=True)
        for i in range(2,len(barr)-1):
        
            cs=cs^barr[i]
        barr+=cs.to_bytes(1,byteorder='big')
        Kobuki.seri.write(barr)
    

  

    def read_data():
            while(1):
                if(int.from_bytes(Kobuki.seri.read(2),byteorder='little')==333): 
                    __temp=Kobuki.seri.read(200)
                    __in_buff=[x for x in __temp]
                    
                    for data in range(0,len(__in_buff)-1):
                        if(__in_buff[data]==170 and __in_buff[data+1]==85):
                            Kobuki. __general_purpose_input=__in_buff[data-19:]
                
                    Kobuki.__basic_sensor=__in_buff[1:16]
                    Kobuki.__docking_IR=__in_buff[15:21]
                    Kobuki.__inertial_sensor=__in_buff[21:30]
                    Kobuki.__cliffsensor=__in_buff[30:38]
                    Kobuki.__current=__in_buff[38:42]
                    Kobuki.__gyro=__in_buff[42:44+__in_buff[43]]
                                                  
            

    def basic_sensor_data(self):
        
        sensor={}
        sensor.update({'bumper':Kobuki.__basic_sensor[2]})
        sensor.update({'wheeldrop':Kobuki.__basic_sensor[3]})
        sensor.update({'cliff':Kobuki.__basic_sensor[4]})
        sensor.update({'Left_encoder':Kobuki.__basic_sensor[5:7]})
        sensor.update({'Right_encoder':Kobuki.__basic_sensor[7:9]})
        sensor.update({'LeftPWM':Kobuki.__basic_sensor[9]})
        sensor.update({'RightPWM':Kobuki.__basic_sensor[10]})
        sensor.update({'Button':Kobuki.__basic_sensor[11]})
        if(Kobuki.__basic_sensor[12]==0):
            sensor.update({'Charger':'DISCHARGING'})
        elif(Kobuki.__basic_sensor[12]==2):
            sensor.update({'Charger':'DOCKING_CHARGED'}) 
        elif(Kobuki.__basic_sensor[12]==6):
            sensor.update({'Charger':'DOCKING_CHARGING'})  
        elif(Kobuki.__basic_sensor[12]==18):
            sensor.update({'Charger':'ADAPTER_CHARGED'}) 
        elif(Kobuki.__basic_sensor[12]==22):
            sensor.update({'Charger':'ADAPTER_CHARGING'})
        sensor.update({'Batteryvolt':Kobuki.__basic_sensor[13]})
        sensor.update({'Overcurrentflag':Kobuki.__basic_sensor[14]})
        if(Kobuki.__basic_sensor[14]==1):
            sensor.update({'Overcurrent':'Leftwheel'})
        elif(Kobuki.__basic_sensor[14]==2):
            sensor.update({'Overcurrent':'Rightwheel'})
        return sensor
    
    def  docking_IR_data(self):
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
    def inertial_sensor_data(self):
        angle={}
        angle.update({'angle':Kobuki.__inertial_sensor[2:4]})
        angle.update({'anglerate':Kobuki.__inertial_sensor[4:6]})
        return angle
    def cliffsensor_data(self):
        cliff={}
        cliff.update({'right_cliff_sensor':Kobuki.__cliffsensor[0]})
        cliff.update({'central_cliff_sensor':Kobuki.__cliffsensor[0]})
        cliff.update({'left_cliff_sensor':Kobuki.__cliffsensor[0]})
        return cliff
    def current_data(self):
        curr={}
        curr.update({'Leftmotor':Kobuki.__current[0]})
        curr.update({'Rightmotor':Kobuki.__current[0]})
        return curr
    def general_purpose_input_data(self):
        gpi={}
        
        gpi.update({'Digital input':Kobuki. __general_purpose_input[3]})
        if(Kobuki. __general_purpose_input[3]==1):
            gpi.update({'Digital input status':'High voltage is applied for digital input channel 0'})
        elif(Kobuki. __general_purpose_input[3]==2):
            gpi.update({'Digital input status':'High voltage is applied for digital input channel 1'})
        elif(Kobuki. __general_purpose_input[3]==4):
            gpi.update({'Digital input status':'High voltage is applied for digital input channel 2'})
        elif(Kobuki. __general_purpose_input[3]==8):
            gpi.update({'Digital input status':'High voltage is applied for input output channel 3'})
        elif(Kobuki. __general_purpose_input[3]==0):
            gpi.update({'Digital input status':'No voltage'})
        gpi.update({'Analog input channel 0 output':Kobuki.__general_purpose_input[4:6]})
        gpi.update({'Analog input channel 1 output':Kobuki.__general_purpose_input[6:8]})
        gpi.update({'Analog input channel 2 output':Kobuki.__general_purpose_input[8:10]})
        gpi.update({'Analog input channel 3 output':Kobuki.__general_purpose_input[10:12]})
        gpi.update({'Unused':Kobuki.__general_purpose_input[12:18]})
        return gpi
    def gyro_intconverted_data(self):
        
        x_axis=[]
        y_axis=[]
        z_axis=[]
        x_axis_converted=[]
        y_axis_converted=[]
        z_axis_converted=[]
        gyro={} 
        gyro.update({'Size of data field':Kobuki.__gyro[1]})  
        gyro.update({'Frame id':Kobuki.__gyro[2]})
        gyro.update({'Followed data length':Kobuki.__gyro[3]})
        nvalue=2
        count=0
        iteration=4
        while(count!=4 and iteration<=(Kobuki.__gyro[3]*2)+nvalue):
             if(count==0):
                 x_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             elif(count==1):
                 y_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             elif(count==2):
                 z_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             if(count==3):
                 count=0
        for data in x_axis:
            x_axis_converted.append(int.from_bytes(data,'little'))
        for data in y_axis:
            y_axis_converted.append(int.from_bytes(data,'little'))
        for data in z_axis:
            z_axis_converted.append(int.from_bytes(data,'little')) 
        gyro.update({'x_axis_converted_to_int: ':x_axis_converted})
        gyro.update({'y_axis_converted_to_int: ':y_axis_converted})
        gyro.update({'z_axis_converted_to_int: ':z_axis_converted})    
        return gyro
    
    def gyro_raw_data(self):
        
        x_axis=[]
        y_axis=[]
        z_axis=[]
        gyro={} 
        gyro.update({'Size of data field':Kobuki.__gyro[1]})  
        gyro.update({'Frame id':Kobuki.__gyro[2]})
        gyro.update({'Followed data length':Kobuki.__gyro[3]})
        nvalue=2
        count=0
        iteration=4
        while(count!=4 and iteration<=(Kobuki.__gyro[3]*2)+nvalue):
             if(count==0):
                 x_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             elif(count==1):
                 y_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             elif(count==2):
                 z_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             if(count==3):
                 count=0
      
        gyro.update({'x_axis_rawdata: ':x_axis})
        gyro.update({'y_axis_rawdata: ':y_axis})
        gyro.update({'z_axis_rawdata: ':z_axis})    
        return gyro

    def gyro_velocity_data(self):
        
        digit_to_dps=0.00875
        x_axis=[]
        y_axis=[]
        z_axis=[]
        x_axis_velocity=[]
        y_axis_velocity=[]
        z_axis_velocity=[]
        gyro={} 
        gyro.update({'Size of data field':Kobuki.__gyro[1]})  
        gyro.update({'Frame id':Kobuki.__gyro[2]})
        gyro.update({'Followed data length':Kobuki.__gyro[3]})
        nvalue=2
        count=0
        iteration=4
        while(count!=4 and iteration<=(Kobuki.__gyro[3]*2)+nvalue):
             if(count==0):
                 x_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             elif(count==1):
                 y_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             elif(count==2):
                 z_axis.append(Kobuki.__gyro[iteration:iteration+nvalue])
                 count=count+1
                 iteration=iteration+nvalue
             if(count==3):
                 count=0
        for data in x_axis:
            for innerdata in data:
                y_axis_velocity.append((digit_to_dps*-1)*innerdata)
        for data in y_axis:
            for innerdata in data:
                x_axis_velocity.append(digit_to_dps*innerdata)
        for data in z_axis:
            for innerdata in data:
                z_axis_velocity.append(digit_to_dps*innerdata)
        gyro.update({'angular velocity of x: ':x_axis_velocity})
        gyro.update({'angular velocity of y: ':y_axis_velocity})
        gyro.update({'angular velocity of z: ':z_axis_velocity})
        return gyro

    def kobukistart(start,self):       
        th2 = threading.Thread(target=start)
        th2.start()
        th2.join()
        __th1.join()
    


  

                                                                                            