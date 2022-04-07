*****
Kobukidriver
*****
Kobukidriver is a python driver for Kobuki quanser qbot2 which helps in control and utilization of the mobile robot.You can build numerous application with the help of the driver.

Links
=====

- Project: 
- PyPi: 

Quickstart
==========

Install using pip:


::

    pip install kobukidriver

  

kobukidriver works in both windows and linux

Features
--------

- Develop any mobile robot applications 
- Gyro sensor data
- Docking IR data
- Inertial sensor data
- Cliff sensor data
- current data
- general purpose input data
- Basic sensor data
- Set/Clear LED
- Set digital output pin
- Control mobile robot speed
- Play inbuilt/custom sounds 

Examples
--------

Get started by importing the ``Kobuki`` class:

.. code-block:: python

     #import the kobuki class
    from kobukidriver import Kobuki
    #create the instance for the kobuki
    kobuki_instance=Kobuki()#raise error if kobuki is not connected

Example code for reading basic sensor datas from Kobuki robot

.. code-block:: python

    from kobukidriver import Kobuki
    kobuki_instance=Kobuki()
    basic_sensor_data=kobuki_instance.basic_sensor_data()
    print(basic_sensor_data)#prints the basic sensor data from the robot
    
Steps for building the mobile robot application using the driver
.. code-block:: python

    from kobukidriver import Kobuki
    kobuki_instance=Kobuki()
    
