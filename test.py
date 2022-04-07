from kobukidriver import Kobuki
k=Kobuki()
k.basic_sensor_data()
def start():
    pass
k.gyro_raw_data().gyro
k.kobukistart(start)


