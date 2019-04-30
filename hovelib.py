##################################################################################################
#                                                                                                #
# Derived from Hove's Raspberry Pi Python Quadcopter Flight Controller.  Open Source @ GitHub    #
# PiStuffing/Quadcopter under GPL for non-commercial application.  Any code derived from         #
# this should retain this copyright comment.                                                     #
#                                                                                                #
# Copyright 2012 - 2018 Andy Baker (Hove) - andy@pistuffing.co.uk                                #
#                                                                                                #
##################################################################################################


from __future__ import division
from __future__ import with_statement

import sys
import time

import math
import smbus

MIN_SATS = 7
EARTH_RADIUS = 6371000  # meters
GRAV_ACCEL = 9.80665    # meters per second per second

RC_PASSIVE = 0
RC_TAKEOFF = 1
RC_FLYING = 2
RC_LANDING = 3
RC_DONE = 4
RC_ABORT = 5

SAMPLING_RATE = 500
MOTION_RATE = 75
FULL_FIFO_BATCHES = 20 # << int(512 / 12)

# mpu6050 = MPU6050(0x68, 1, 1)


####################################################################################################
#
#  Adafruit i2c interface enhanced with performance / error handling enhancements
#
####################################################################################################
class I2C:

    def __init__(self, address, bus=smbus.SMBus(1)):
        self.address = address
        self.bus = bus
        self.misses = 0

    def writeByte(self, value):
        self.bus.write_byte(self.address, value)

    def write8(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def writeList(self, reg, list):
        self.bus.write_i2c_block_data(self.address, reg, list)

    def readU8(self, reg):
        result = self.bus.read_byte_data(self.address, reg)
        return result

    def readS8(self, reg):
        result = self.bus.read_byte_data(self.address, reg)
        result = result - 256 if result > 127 else result
        return result

    def readU16(self, reg):
        hibyte = self.bus.read_byte_data(self.address, reg)
        result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)
        return result

    def readS16(self, reg):
        hibyte = self.bus.read_byte_data(self.address, reg)
        hibyte = hibyte - 256 if hibyte > 127 else hibyte
        result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)
        return result

    def readList(self, reg, length):
        "Reads a byte array value from the I2C device. The content depends on the device.  The "
        "FIFO read return sequential values from the same register.  For all other, sequestial"
        "regester values are returned"
        result = self.bus.read_i2c_block_data(self.address, reg, length)
        return result


####################################################################################################
#
#  Gyroscope / Accelerometer class for reading position / movement.  Works with the Invensense IMUs:
#
#  - MPU-6050
#  - MPU-9150
#  - MPU-9250
#
####################################################################################################
class MPU6050:
    i2c = None

    # Registers/etc.
    __MPU6050_RA_SELF_TEST_XG = 0x00
    __MPU6050_RA_SELF_TEST_YG = 0x01
    __MPU6050_RA_SELF_TEST_ZG = 0x02
    __MPU6050_RA_SELF_TEST_XA = 0x0D
    __MPU6050_RA_SELF_TEST_YA = 0x0E
    __MPU6050_RA_SELF_TEST_ZA = 0x0F
    __MPU6050_RA_XG_OFFS_USRH = 0x13
    __MPU6050_RA_XG_OFFS_USRL = 0x14
    __MPU6050_RA_YG_OFFS_USRH = 0x15
    __MPU6050_RA_YG_OFFS_USRL = 0x16
    __MPU6050_RA_ZG_OFFS_USRH = 0x17
    __MPU6050_RA_ZG_OFFS_USRL = 0x18
    __MPU6050_RA_SMPLRT_DIV = 0x19
    __MPU6050_RA_CONFIG = 0x1A
    __MPU6050_RA_GYRO_CONFIG = 0x1B
    __MPU6050_RA_ACCEL_CONFIG = 0x1C
    __MPU9250_RA_ACCEL_CFG_2 = 0x1D
    __MPU6050_RA_FF_THR = 0x1D
    __MPU6050_RA_FF_DUR = 0x1E
    __MPU6050_RA_MOT_THR = 0x1F
    __MPU6050_RA_MOT_DUR = 0x20
    __MPU6050_RA_ZRMOT_THR = 0x21
    __MPU6050_RA_ZRMOT_DUR = 0x22
    __MPU6050_RA_FIFO_EN = 0x23
    __MPU6050_RA_I2C_MST_CTRL = 0x24
    __MPU6050_RA_I2C_SLV0_ADDR = 0x25
    __MPU6050_RA_I2C_SLV0_REG = 0x26
    __MPU6050_RA_I2C_SLV0_CTRL = 0x27
    __MPU6050_RA_I2C_SLV1_ADDR = 0x28
    __MPU6050_RA_I2C_SLV1_REG = 0x29
    __MPU6050_RA_I2C_SLV1_CTRL = 0x2A
    __MPU6050_RA_I2C_SLV2_ADDR = 0x2B
    __MPU6050_RA_I2C_SLV2_REG = 0x2C
    __MPU6050_RA_I2C_SLV2_CTRL = 0x2D
    __MPU6050_RA_I2C_SLV3_ADDR = 0x2E
    __MPU6050_RA_I2C_SLV3_REG = 0x2F
    __MPU6050_RA_I2C_SLV3_CTRL = 0x30
    __MPU6050_RA_I2C_SLV4_ADDR = 0x31
    __MPU6050_RA_I2C_SLV4_REG = 0x32
    __MPU6050_RA_I2C_SLV4_DO = 0x33
    __MPU6050_RA_I2C_SLV4_CTRL = 0x34
    __MPU6050_RA_I2C_SLV4_DI = 0x35
    __MPU6050_RA_I2C_MST_STATUS = 0x36
    __MPU6050_RA_INT_PIN_CFG = 0x37
    __MPU6050_RA_INT_ENABLE = 0x38
    __MPU6050_RA_DMP_INT_STATUS = 0x39
    __MPU6050_RA_INT_STATUS = 0x3A
    __MPU6050_RA_ACCEL_XOUT_H = 0x3B
    __MPU6050_RA_ACCEL_XOUT_L = 0x3C
    __MPU6050_RA_ACCEL_YOUT_H = 0x3D
    __MPU6050_RA_ACCEL_YOUT_L = 0x3E
    __MPU6050_RA_ACCEL_ZOUT_H = 0x3F
    __MPU6050_RA_ACCEL_ZOUT_L = 0x40
    __MPU6050_RA_TEMP_OUT_H = 0x41
    __MPU6050_RA_TEMP_OUT_L = 0x42
    __MPU6050_RA_GYRO_XOUT_H = 0x43
    __MPU6050_RA_GYRO_XOUT_L = 0x44
    __MPU6050_RA_GYRO_YOUT_H = 0x45
    __MPU6050_RA_GYRO_YOUT_L = 0x46
    __MPU6050_RA_GYRO_ZOUT_H = 0x47
    __MPU6050_RA_GYRO_ZOUT_L = 0x48
    __MPU6050_RA_EXT_SENS_DATA_00 = 0x49
    __MPU6050_RA_EXT_SENS_DATA_01 = 0x4A
    __MPU6050_RA_EXT_SENS_DATA_02 = 0x4B
    __MPU6050_RA_EXT_SENS_DATA_03 = 0x4C
    __MPU6050_RA_EXT_SENS_DATA_04 = 0x4D
    __MPU6050_RA_EXT_SENS_DATA_05 = 0x4E
    __MPU6050_RA_EXT_SENS_DATA_06 = 0x4F
    __MPU6050_RA_EXT_SENS_DATA_07 = 0x50
    __MPU6050_RA_EXT_SENS_DATA_08 = 0x51
    __MPU6050_RA_EXT_SENS_DATA_09 = 0x52
    __MPU6050_RA_EXT_SENS_DATA_10 = 0x53
    __MPU6050_RA_EXT_SENS_DATA_11 = 0x54
    __MPU6050_RA_EXT_SENS_DATA_12 = 0x55
    __MPU6050_RA_EXT_SENS_DATA_13 = 0x56
    __MPU6050_RA_EXT_SENS_DATA_14 = 0x57
    __MPU6050_RA_EXT_SENS_DATA_15 = 0x58
    __MPU6050_RA_EXT_SENS_DATA_16 = 0x59
    __MPU6050_RA_EXT_SENS_DATA_17 = 0x5A
    __MPU6050_RA_EXT_SENS_DATA_18 = 0x5B
    __MPU6050_RA_EXT_SENS_DATA_19 = 0x5C
    __MPU6050_RA_EXT_SENS_DATA_20 = 0x5D
    __MPU6050_RA_EXT_SENS_DATA_21 = 0x5E
    __MPU6050_RA_EXT_SENS_DATA_22 = 0x5F
    __MPU6050_RA_EXT_SENS_DATA_23 = 0x60
    __MPU6050_RA_MOT_DETECT_STATUS = 0x61
    __MPU6050_RA_I2C_SLV0_DO = 0x63
    __MPU6050_RA_I2C_SLV1_DO = 0x64
    __MPU6050_RA_I2C_SLV2_DO = 0x65
    __MPU6050_RA_I2C_SLV3_DO = 0x66
    __MPU6050_RA_I2C_MST_DELAY_CTRL = 0x67
    __MPU6050_RA_SIGNAL_PATH_RESET = 0x68
    __MPU6050_RA_MOT_DETECT_CTRL = 0x69
    __MPU6050_RA_USER_CTRL = 0x6A
    __MPU6050_RA_PWR_MGMT_1 = 0x6B
    __MPU6050_RA_PWR_MGMT_2 = 0x6C
    __MPU6050_RA_BANK_SEL = 0x6D
    __MPU6050_RA_MEM_START_ADDR = 0x6E
    __MPU6050_RA_MEM_R_W = 0x6F
    __MPU6050_RA_DMP_CFG_1 = 0x70
    __MPU6050_RA_DMP_CFG_2 = 0x71
    __MPU6050_RA_FIFO_COUNTH = 0x72
    __MPU6050_RA_FIFO_COUNTL = 0x73
    __MPU6050_RA_FIFO_R_W = 0x74
    __MPU6050_RA_WHO_AM_I = 0x75

    #-----------------------------------------------------------------------------------------------
    # Compass output registers when using the I2C master / slave
    #-----------------------------------------------------------------------------------------------
    __MPU9250_RA_MAG_XOUT_L = 0x4A
    __MPU9250_RA_MAG_XOUT_H = 0x4B
    __MPU9250_RA_MAG_YOUT_L = 0x4C
    __MPU9250_RA_MAG_YOUT_H = 0x4D
    __MPU9250_RA_MAG_ZOUT_L = 0x4E
    __MPU9250_RA_MAG_ZOUT_H = 0x4F

    # Compass output registers when directly accessing via IMU bypass
    __AK893_RA_WIA = 0x00
    __AK893_RA_INFO = 0x01
    __AK893_RA_ST1 = 0x00
    __AK893_RA_X_LO = 0x03
    __AK893_RA_X_HI = 0x04
    __AK893_RA_Y_LO = 0x05
    __AK893_RA_Y_HI = 0x06
    __AK893_RA_Z_LO = 0x07
    __AK893_RA_Z_HI = 0x08
    __AK893_RA_ST2 = 0x09
    __AK893_RA_CNTL1 = 0x0A
    __AK893_RA_RSV = 0x0B
    __AK893_RA_ASTC = 0x0C
    __AK893_RA_TS1 = 0x0D
    __AK893_RA_TS2 = 0x0E
    __AK893_RA_I2CDIS = 0x0F
    __AK893_RA_ASAX = 0x10
    __AK893_RA_ASAY = 0x11
    __AK893_RA_ASAZ = 0x12

    __RANGE_ACCEL = 8                                                            #AB: +/- 8g
    __RANGE_GYRO = 250                                                           #AB: +/- 250o/s

    __SCALE_GYRO = math.radians(2 * __RANGE_GYRO / 65536)
    __SCALE_ACCEL = 2 * __RANGE_ACCEL / 65536

    def __init__(self, address=0x68, alpf=2, glpf=1):
        self.i2c = I2C(address)
        self.address = address

        self.min_az = 0.0
        self.max_az = 0.0
        self.min_gx = 0.0
        self.max_gx = 0.0
        self.min_gy = 0.0
        self.max_gy = 0.0
        self.min_gz = 0.0
        self.max_gz = 0.0

        self.ax_offset = 0.0
        self.ay_offset = 0.0
        self.az_offset = 0.0

        self.gx_offset = 0.0
        self.gy_offset = 0.0
        self.gz_offset = 0.0

        # Reset all registers
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_PWR_MGMT_1, 0x80)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Sets sample rate to 1kHz/(1+0) = 1kHz or 1ms (note 1kHz assumes dlpf is on - setting
        # dlpf to 0 or 7 changes 1kHz to 8kHz and therefore will require sample rate divider
        # to be changed to 7 to obtain the same 1kHz sample rate.
        #-------------------------------------------------------------------------------------------
        sample_rate_divisor = 1 # int(round(adc_frequency / SAMPLING_RATE))
        self.i2c.write8(self.__MPU6050_RA_SMPLRT_DIV, sample_rate_divisor - 1)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Sets clock source to gyro reference w/ PLL
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_PWR_MGMT_1, 0x01)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Gyro DLPF => 1kHz sample frequency used above divided by the sample divide factor.
        #
        # 0x00 =  250Hz @ 8kHz sampling - DO NOT USE, THE ACCELEROMETER STILL SAMPLES AT 1kHz WHICH PRODUCES EXPECTED BUT NOT CODED FOR TIMING AND FIFO CONTENT PROBLEMS
        # 0x01 =  184Hz
        # 0x02 =   92Hz
        # 0x03 =   41Hz
        # 0x04 =   20Hz
        # 0x05 =   10Hz
        # 0x06 =    5Hz
        # 0x07 = 3600Hz @ 8kHz
        #
        # 0x0* FIFO overflow overwrites oldest FIFO contents
        # 0x4* FIFO overflow does not overwrite full FIFO contents
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_CONFIG, 0x40 | glpf)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Disable gyro self tests, scale of +/- 250 degrees/s
        #
        # 0x00 =  +/- 250 degrees/s
        # 0x08 =  +/- 500 degrees/s
        # 0x10 = +/- 1000 degrees/s
        # 0x18 = +/- 2000 degrees/s
        # See SCALE_GYRO for conversion from raw data to units of radians per second
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_GYRO_CONFIG, int(round(math.log(self.__RANGE_GYRO / 250, 2))) << 3)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Accel DLPF => 1kHz sample frequency used above divided by the sample divide factor.
        #
        # 0x00 = 460Hz
        # 0x01 = 184Hz
        # 0x02 =  92Hz
        # 0x03 =  41Hz
        # 0x04 =  20Hz
        # 0x05 =  10Hz
        # 0x06 =   5Hz
        # 0x07 = 460Hz
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU9250_RA_ACCEL_CFG_2, alpf)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Disable accel self tests, scale of +/-8g
        #
        # 0x00 =  +/- 2g
        # 0x08 =  +/- 4g
        # 0x10 =  +/- 8g
        # 0x18 = +/- 16g
        # See SCALE_ACCEL for convertion from raw data to units of meters per second squared
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_ACCEL_CONFIG, int(round(math.log(self.__RANGE_ACCEL / 2, 2))) << 3)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Set INT pin to push/pull, latch 'til read, any read to clear
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_INT_PIN_CFG, 0x30)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Initialize the FIFO overflow interrupt 0x10 (turned off at startup).
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_INT_ENABLE, 0x00)
        time.sleep(0.1)

        #-------------------------------------------------------------------------------------------
        # Enabled the FIFO.
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_USER_CTRL, 0x40)

        #-------------------------------------------------------------------------------------------
        # Accelerometer / gyro goes into FIFO later on - see flushFIFO()
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_FIFO_EN, 0x00)

        #-------------------------------------------------------------------------------------------
        # Read ambient temperature
        #-------------------------------------------------------------------------------------------
        temp = self.readTemperature()

    def readTemperature(self):
        temp = self.i2c.readS16(self.__MPU6050_RA_TEMP_OUT_H)
        return temp

    def enableFIFOOverflowISR(self):
        #-------------------------------------------------------------------------------------------
        # Clear the interrupt status register and enable the FIFO overflow interrupt 0x10
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_INT_ENABLE, 0x10)
        self.i2c.readU8(self.__MPU6050_RA_INT_STATUS)

    def disableFIFOOverflowISR(self):
        #-------------------------------------------------------------------------------------------
        # Disable the FIFO overflow interrupt.
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_INT_ENABLE, 0x00)

    def numFIFOBatches(self):
        #-------------------------------------------------------------------------------------------
        # The FIFO is 512 bytes long, and we're storing 6 signed shorts (ax, ay, az, gx, gy, gz) i.e.
        # 12 bytes per batch of sensor readings
        #-------------------------------------------------------------------------------------------
        fifo_bytes = self.i2c.readU16(self.__MPU6050_RA_FIFO_COUNTH)
        fifo_batches = int(fifo_bytes / 12)  # This rounds down
        return fifo_batches

    def readFIFO(self, fifo_batches):
        #-------------------------------------------------------------------------------------------
        # Read n x 12 bytes of FIFO data averaging, and return the averaged values and inferred time
        # based upon the sampling rate and the number of samples.
        #-------------------------------------------------------------------------------------------
        ax = 0
        ay = 0
        az = 0
        gx = 0
        gy = 0
        gz = 0

        for ii in range(fifo_batches):
            sensor_data = []
            fifo_batch = self.i2c.readList(self.__MPU6050_RA_FIFO_R_W, 12)
            for jj in range(0, 12, 2):
                hibyte = fifo_batch[jj]
                hibyte = hibyte - 256 if hibyte > 127 else hibyte
                lobyte = fifo_batch[jj + 1]
                sensor_data.append((hibyte << 8) + lobyte)

            ax += sensor_data[0]
            ay += sensor_data[1]
            az += sensor_data[2]
            gx += sensor_data[3]
            gy += sensor_data[4]
            gz += sensor_data[5]

            '''
            self.max_az = self.max_az if sensor_data[2] < self.max_az else sensor_data[2]
            self.min_az = self.min_az if sensor_data[2] > self.min_az else sensor_data[2]

            self.max_gx = self.max_gx if sensor_data[3] < self.max_gx else sensor_data[3]
            self.min_gx = self.min_gx if sensor_data[3] > self.min_gx else sensor_data[3]

            self.max_gy = self.max_gy if sensor_data[4] < self.max_gy else sensor_data[4]
            self.min_gy = self.min_gy if sensor_data[4] > self.min_gy else sensor_data[4]

            self.max_gz = self.max_gz if sensor_data[5] < self.max_gz else sensor_data[5]
            self.min_gz = self.min_gz if sensor_data[5] > self.min_gz else sensor_data[5]
            '''

        return ax / fifo_batches, ay / fifo_batches, az / fifo_batches, gx / fifo_batches, gy / fifo_batches, gz / fifo_batches, fifo_batches / SAMPLING_RATE

    def flushFIFO(self):
        #-------------------------------------------------------------------------------------------
        # First shut off the feed in the FIFO.
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_FIFO_EN, 0x00)

        #-------------------------------------------------------------------------------------------
        # Empty the FIFO by reading whatever is there
        #-------------------------------------------------------------------------------------------
        SMBUS_MAX_BUF_SIZE = 32

        fifo_bytes = self.i2c.readU16(self.__MPU6050_RA_FIFO_COUNTH)

        for ii in range(int(fifo_bytes / SMBUS_MAX_BUF_SIZE)):
            self.i2c.readList(self.__MPU6050_RA_FIFO_R_W, SMBUS_MAX_BUF_SIZE)

        fifo_bytes = self.i2c.readU16(self.__MPU6050_RA_FIFO_COUNTH)

        for ii in range(fifo_bytes):
            self.i2c.readU8(self.__MPU6050_RA_FIFO_R_W)

        #-------------------------------------------------------------------------------------------
        # Finally start feeding the FIFO with sensor data again
        #-------------------------------------------------------------------------------------------
        self.i2c.write8(self.__MPU6050_RA_FIFO_EN, 0x78)

    def setGyroOffsets(self, gx, gy, gz):
        self.gx_offset = gx
        self.gy_offset = gy
        self.gz_offset = gz

    def scaleSensors(self, ax, ay, az, gx, gy, gz):
        qax = (ax - self.ax_offset) * self.__SCALE_ACCEL
        qay = (ay - self.ay_offset) * self.__SCALE_ACCEL
        qaz = (az - self.az_offset) * self.__SCALE_ACCEL

        qrx = (gx - self.gx_offset) * self.__SCALE_GYRO
        qry = (gy - self.gy_offset) * self.__SCALE_GYRO
        qrz = (gz - self.gz_offset) * self.__SCALE_GYRO

        return qax, qay, qaz, qrx, qry, qrz

    def initCompass(self):
        #-------------------------------------------------------------------------------------------
        # Set up the I2C master pass through.
        #-------------------------------------------------------------------------------------------
        int_bypass = self.i2c.readU8(self.__MPU6050_RA_INT_PIN_CFG)
        self.i2c.write8(self.__MPU6050_RA_INT_PIN_CFG, int_bypass | 0x02)

        #-------------------------------------------------------------------------------------------
        # Connect directly to the bypassed magnetometer, and configured it for 16 bit continuous data
        #-------------------------------------------------------------------------------------------
        self.i2c_compass = I2C(0x0C)
        self.i2c_compass.write8(self.__AK893_RA_CNTL1, 0x16);

    def readCompass(self):
        compass_bytes = self.i2c_compass.readList(self.__AK893_RA_X_LO, 7)

        #-------------------------------------------------------------------------------------------
        # Convert the array of 6 bytes to 3 shorts - 7th byte kicks off another read.
        # Note compass X, Y, Z are aligned with GPS not IMU i.e. X = 0, Y = 1 => 0 degrees North
        #-------------------------------------------------------------------------------------------
        compass_data = []
        for ii in range(0, 6, 2):
            lobyte = compass_bytes[ii]
            hibyte = compass_bytes[ii + 1]
            hibyte = hibyte - 256 if hibyte > 127 else hibyte
            compass_data.append((hibyte << 8) + lobyte)

        [mgx, mgy, mgz] = compass_data

        mgx = (mgx - self.mgx_offset) * self.mgx_gain
        mgy = (mgy - self.mgy_offset) * self.mgy_gain
        mgz = (mgz - self.mgz_offset) * self.mgz_gain

        return mgx, mgy, mgz

    def compassCheckCalibrate(self):
        rc = True
        while True:
            coc = input("'check' or 'calibrate'? ")
            if coc == "check":
                self.checkCompass()
                break
            elif coc == "calibrate":
                rc = self.calibrateCompass()
                break
        return rc

    def checkCompass(self):
        print("Pop me on the ground pointing in a known direction based on another compass.")
        input("Press enter when that's done, and I'll tell you which way I think I'm pointing")

        self.loadCompassCalibration()
        mgx, mgy, mgz = self.readCompass()

        #-------------------------------------------------------------------------------
        # Convert compass vector into N, S, E, W variants.  Get the compass angle in the
        # range of 0 - 359.99.
        #-------------------------------------------------------------------------------
        compass_angle = (math.degrees(math.atan2(mgx, mgy)) + 360) % 360

        #-------------------------------------------------------------------------------
        # There are 16 possible compass directions when you include things like NNE at
        # 22.5 degrees.
        #-------------------------------------------------------------------------------
        compass_points = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")
        num_compass_points = len(compass_points)
        for ii in range(num_compass_points):

            angle_range_min = (360 * (ii - 0.5) / num_compass_points)
            angle_range_max = (360 * (ii + 0.5) / num_compass_points)

            if compass_angle > angle_range_min and compass_angle <= angle_range_max:
                break
        else:
            ii = 0 # Special case where max < min when north.

        print("I think I'm pointing %s?" % compass_points[ii])


    def calibrateCompass(self):
        self.mgx_offset = 0.0
        self.mgy_offset = 0.0
        self.mgz_offset = 0.0
        self.mgx_gain = 1.0
        self.mgy_gain = 1.0
        self.mgz_gain = 1.0
        offs_rc = False

        #-------------------------------------------------------------------------------------------
        # First we need gyro offset calibration.  Flush the FIFO, collect roughly half a FIFO full
        # of samples and feed back to the gyro offset calibrations.
        #-------------------------------------------------------------------------------------------
        input("First, put me on a stable surface, and press enter.")

        # mpu6050.flushFIFO()
        # time.sleep(FULL_FIFO_BATCHES / SAMPLING_RATE)
        # nfb = mpu6050.numFIFOBatches()
        # qax, qay, qaz, qrx, qry, qrz, dt = mpu6050.readFIFO(nfb)
        # mpu6050.setGyroOffsets(qrx, qry, qrz)

        self.flushFIFO()
        time.sleep(FULL_FIFO_BATCHES / SAMPLING_RATE)
        nfb = self.numFIFOBatches()
        qax, qay, qaz, qrx, qry, qrz, dt = self.readFIFO(nfb)
        self.setGyroOffsets(qrx, qry, qrz)

        print("OK, thanks.  That's the gyro calibrated.")

        #-------------------------------------------------------------------------------------------
        # Open the offset file for this run
        #-------------------------------------------------------------------------------------------
        try:
            with open('CompassOffsets', 'ab') as offs_file:

                mgx, mgy, mgz = self.readCompass()
                max_mgx = mgx
                min_mgx = mgx
                max_mgy = mgy
                min_mgy = mgy
                max_mgz = mgz
                min_mgz = mgz

                #-----------------------------------------------------------------------------------
                # Collect compass X. Y compass values
                #-------------------------------------------------------------------------------
                print("Now, pick me up and rotate me horizontally twice until I say stop.")
                input("Press enter when you're ready to go.")

                self.flushFIFO()

                yaw = 0.0
                total_dt = 0.0

                print("ROTATION:    ")
                number_len = 0

                #-------------------------------------------------------------------------------
                # While integrated Z axis gyro < 2 pi i.e. 360 degrees, keep flashing the light
                #-------------------------------------------------------------------------------
                while abs(yaw) < 4 * math.pi:
                    time.sleep(10 / SAMPLING_RATE)

                    nfb = self.numFIFOBatches()
                    ax, ay, az, gx, gy, gz, dt = self.readFIFO(nfb)
                    ax, ay, az, gx, gy, gz = self.scaleSensors(ax, ay, az, gx, gy, gz)

                    yaw += gz * dt
                    total_dt += dt

                    mgx, mgy, mgz = self.readCompass()

                    max_mgx = mgx if mgx > max_mgx else max_mgx
                    max_mgy = mgy if mgy > max_mgy else max_mgy
                    min_mgx = mgx if mgx < min_mgx else min_mgx
                    min_mgy = mgy if mgy < min_mgy else min_mgy

                    if total_dt > 0.2:
                        total_dt %= 0.2

                        number_text = str(abs(int(math.degrees(yaw))))
                        if len(number_text) == 2:
                            number_text = " " + number_text
                        elif len(number_text) == 1:
                            number_text = "  " + number_text

                        print("\b\b\b\b%s" % number_text,
                        sys.stdout.flush())

                        print("Stop!")

                print()

                #-------------------------------------------------------------------------------
                # Collect compass Z values
                #-------------------------------------------------------------------------------
                print("\nGreat!  Now do the same but with my nose down.")
                input("Press enter when you're ready to go.")

                self.flushFIFO()

                rotation = 0.0
                total_dt = 0.0

                print("ROTATION:    ")
                number_len = 0

                #-------------------------------------------------------------------------------
                # While integrated X+Y axis gyro < 4 pi i.e. 720 degrees, keep flashing the light
                #-------------------------------------------------------------------------------
                while abs(rotation) < 4 * math.pi:
                    time.sleep(10 / SAMPLING_RATE)

                    nfb = self.numFIFOBatches()
                    ax, ay, az, gx, gy, gz, dt = self.readFIFO(nfb)
                    ax, ay, az, gx, gy, gz = self.scaleSensors(ax, ay, az, gx, gy, gz)

                    rotation += math.pow(math.pow(gx, 2) + math.pow(gy, 2), 0.5) * dt
                    total_dt += dt

                    mgx, mgy, mgz = self.readCompass()

                    max_mgz = mgz if mgz > max_mgz else max_mgz
                    min_mgz = mgz if mgz < min_mgz else min_mgz

                    if total_dt > 0.2:
                        total_dt %= 0.2

                        number_text = str(abs(int(math.degrees(rotation))))
                        if len(number_text) == 2:
                            number_text = " " + number_text
                        elif len(number_text) == 1:
                            number_text = "  " + number_text

                print(" ")

                #-------------------------------------------------------------------------------
                # Write the good output to file.
                #-------------------------------------------------------------------------------
                mgx_offset = (max_mgx + min_mgx) / 2
                mgy_offset = (max_mgy + min_mgy) / 2
                mgz_offset = (max_mgz + min_mgz) / 2
                mgx_gain = 1 / (max_mgx - min_mgx)
                mgy_gain = 1 / (max_mgy - min_mgy)
                mgz_gain = 1 / (max_mgz - min_mgz)

                offs_file.write("%f %f %f %f %f %f\n" % (mgx_offset, mgy_offset, mgz_offset, mgx_gain, mgy_gain, mgz_gain))

                #-------------------------------------------------------------------------------
                # Sanity check.
                #-------------------------------------------------------------------------------
                print("\nLooking good, just one last check to confirm all's well.")
                self.checkCompass()

                print("All done - ready to go!")
                offs_rc = True

        except EnvironmentError as e:
            print("Environment Error: '%s'" % e)

        return offs_rc

    def loadCompassCalibration(self):

        self.mgx_offset = 0.0
        self.mgy_offset = 0.0
        self.mgz_offset = 0.0
        self.mgx_gain = 1.0
        self.mgy_gain = 1.0
        self.mgz_gain = 1.0

        offs_rc = False
        try:
            with open('CompassOffsets', 'rb') as offs_file:
                mgx_offset = 0.0
                mgy_offset = 0.0
                mgz_offset = 0.0
                mgx_gain = 1.0
                mgy_gain = 1.0
                mgz_gain = 1.0

                for line in offs_file:
                    mgx_offset, mgy_offset, mgz_offset, mgx_gain, mgy_gain, mgz_gain = line.split()

                self.mgx_offset = float(mgx_offset)
                self.mgy_offset = float(mgy_offset)
                self.mgz_offset = float(mgz_offset)
                self.mgx_gain = float(mgx_gain)
                self.mgy_gain = float(mgy_gain)
                self.mgz_gain = float(mgz_gain)

        except EnvironmentError:
            #---------------------------------------------------------------------------------------
            # Compass calibration is essential to exclude soft magnetic fields such as from local
            # metal; enforce a recalibration if not found.
            #---------------------------------------------------------------------------------------
            print("Oops, something went wrong reading the compass offsets file 'CompassOffsets'")
            print("Have you calibrated it (--cc)?")

            offs_rc = False
        else:
            #---------------------------------------------------------------------------------------
            # Calibration results were successful.
            #---------------------------------------------------------------------------------------
            offs_rc = True
        finally:
            pass

        return offs_rc

    def calibrate0g(self):
        ax_offset = 0.0
        ay_offset = 0.0
        az_offset = 0.0
        offs_rc = False

        #-------------------------------------------------------------------------------------------
        # Open the ofset file for this run
        #-------------------------------------------------------------------------------------------
        try:
            with open('0gOffsets', 'ab') as offs_file:
                input("Rest me on my props and press enter.")
                self.flushFIFO()
                time.sleep(FULL_FIFO_BATCHES / SAMPLING_RATE)
                fifo_batches = self.numFIFOBatches()
                ax, ay, az, gx, gy, gz, dt = self.readFIFO(fifo_batches)
                offs_file.write("%f %f %f\n" % (ax, ay, az))

        except EnvironmentError:
            pass
        else:
            offs_rc = True

        return offs_rc

    def load0gCalibration(self):
        offs_rc = False
        try:
            with open('0gOffsets', 'rb') as offs_file:
                for line in offs_file:
                    ax_offset, ay_offset, az_offset = line.split()
            self.ax_offset = float(ax_offset)
            self.ay_offset = float(ay_offset)
            self.az_offset = float(az_offset)

        except EnvironmentError:
            pass
        else:
            pass
        finally:
            #---------------------------------------------------------------------------------------
            # For a while, I thought 0g calibration might help, but actually, it doesn't due to
            # temperature dependency, so it always returns default values now.
            #---------------------------------------------------------------------------------------
            self.ax_offset = 0.0
            self.ay_offset = 0.0
            self.az_offset = 0.0

            offs_rc = True

        return offs_rc

    def getStats(self):
        return (self.max_az * self.__SCALE_ACCEL,
                self.min_az * self.__SCALE_ACCEL,
                self.max_gx * self.__SCALE_GYRO,
                self.min_gx * self.__SCALE_GYRO,
                self.max_gy * self.__SCALE_GYRO,
                self.min_gy * self.__SCALE_GYRO,
                self.max_gz * self.__SCALE_GYRO,
                self.min_gz * self.__SCALE_GYRO)


####################################################################################################
#
# PID algorithm to take input sensor readings, and target requirements, and output an arbirtrary
# corrective value.
#
####################################################################################################
class PID:

    def __init__(self, p_gain, i_gain, d_gain):
        self.last_error = 0.0
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain
        self.i_error = 0.0

    def Error(self, input, target):
        return (target - input)


    def Compute(self, input, target, dt):
        #-------------------------------------------------------------------------------------------
        # Error is what the PID alogithm acts upon to derive the output
        #-------------------------------------------------------------------------------------------
        error = self.Error(input, target)

        #-------------------------------------------------------------------------------------------
        # The proportional term takes the distance between current input and target
        # and uses this proportially (based on Kp) to control the ESC pulse width
        #-------------------------------------------------------------------------------------------
        p_error = error

        #-------------------------------------------------------------------------------------------
        # The integral term sums the errors across many compute calls to allow for
        # external factors like wind speed and friction
        #-------------------------------------------------------------------------------------------
        self.i_error += (error + self.last_error) * dt
        i_error = self.i_error

        #-------------------------------------------------------------------------------------------
        # The differential term accounts for the fact that as error approaches 0,
        # the output needs to be reduced proportionally to ensure factors such as
        # momentum do not cause overshoot.
        #-------------------------------------------------------------------------------------------
        d_error = (error - self.last_error) / dt

        #-------------------------------------------------------------------------------------------
        # The overall output is the sum of the (P)roportional, (I)ntegral and (D)iffertial terms
        #-------------------------------------------------------------------------------------------
        p_output = self.p_gain * p_error
        i_output = self.i_gain * i_error
        d_output = self.d_gain * d_error

        #-------------------------------------------------------------------------------------------
        # Store off last error for integral and differential processing next time.
        #-------------------------------------------------------------------------------------------
        self.last_error = error

        #-------------------------------------------------------------------------------------------
        # Return the output, which has been tuned to be the increment / decrement in ESC PWM
        #-------------------------------------------------------------------------------------------
        return p_output, i_output, d_output


####################################################################################################
#
# PID algorithm subclass to come with the yaw angles error calculations.
#
####################################################################################################
class YAW_PID(PID):

    def Error(self, input, target):
        #-------------------------------------------------------------------------------------------
        # target and input are in the 0 - 2 pi range.  This is asserted. Results are in the +/- pi
        # range to make sure we spin the shorted way.
        #-------------------------------------------------------------------------------------------
        assert (abs(input) <= math.pi), "yaw input out of range %f" % math.degrees(input)
        assert (abs(target) <= math.pi), "yaw target out of range %f" % math.degrees(target)
        error = ((target - input) + math.pi) % (2 * math.pi) - math.pi
        return error


####################################################################################################
#
# Get the rotation angles of pitch, roll and yaw from the fixed point of earth reference frame
# gravity + lateral orientation (ultimately compass derived, but currently just the take-off
# orientation) of 0, 0, 1 compared to where gravity is distrubuted across the X, Y and Z axes of the
# accelerometer all based upon the right hand rule.
#
####################################################################################################
def GetRotationAngles(ax, ay, az):

    #-----------------------------------------------------------------------------------------------
    # What's the angle in the x and y plane from horizontal in radians?
    #-----------------------------------------------------------------------------------------------
    pitch = math.atan2(-ax, math.pow(math.pow(ay, 2) + math.pow(az, 2), 0.5))
    roll = math.atan2(ay, az)

    return pitch, roll


####################################################################################################
#
# Absolute angles of tilt compared to the earth gravity reference frame.
#
####################################################################################################
def GetAbsoluteAngles(ax, ay, az):

    pitch = math.atan2(-ax, az)
    roll = math.atan2(ay, az)

    return pitch, roll


####################################################################################################
#
# Convert a body frame rotation rate to the rotation frames
#
####################################################################################################
def Body2EulerRates(qry, qrx, qrz, pa, ra):

    #===============================================================================================
    # Axes: Convert a set of gyro body frame rotation rates into Euler frames
    #
    # Matrix
    # ---------
    # |err|   | 1 ,  sin(ra) * tan(pa) , cos(ra) * tan(pa) | |qrx|
    # |epr| = | 0 ,  cos(ra)           ,     -sin(ra)      | |qry|
    # |eyr|   | 0 ,  sin(ra) / cos(pa) , cos(ra) / cos(pa) | |qrz|
    #
    #===============================================================================================
    c_pa = math.cos(pa)
    t_pa = math.tan(pa)
    c_ra = math.cos(ra)
    s_ra = math.sin(ra)

    err = qrx + qry * s_ra * t_pa + qrz * c_ra * t_pa
    epr =       qry * c_ra        - qrz * s_ra
    eyr =       qry * s_ra / c_pa + qrz * c_ra / c_pa

    return epr, err, eyr


####################################################################################################
#
# Rotate a vector using Euler angles wrt Earth frame co-ordinate system, for example to take the
# earth frame target flight plan vectors, and move it to the quad frame orientations vectors.
#
####################################################################################################
def RotateVector(evx, evy, evz, pa, ra, ya):

    #===============================================================================================
    # Axes: Convert a vector from earth- to quadcopter frame
    #
    # Matrix
    # ---------
    # |qvx|   | cos(pa) * cos(ya),                                 cos(pa) * sin(ya),                               -sin(pa)          | |evx|
    # |qvy| = | sin(ra) * sin(pa) * cos(ya) - cos(ra) * sin(ya),   sin(ra) * sin(pa) * sin(ya) + cos(ra) * cos(ya),  sin(ra) * cos(pa)| |evy|
    # |qvz|   | cos(ra) * sin(pa) * cos(ya) + sin(ra) * sin(ya),   cos(ra) * sin(pa) * sin(ya) - sin(ra) * cos(ya),  cos(pa) * cos(ra)| |evz|
    #
    #===============================================================================================
    c_pa = math.cos(pa)
    s_pa = math.sin(pa)
    c_ra = math.cos(ra)
    s_ra = math.sin(ra)
    c_ya = math.cos(ya)
    s_ya = math.sin(ya)

    qvx = evx * c_pa * c_ya                        + evy * c_pa * s_ya                        - evz * s_pa
    qvy = evx * (s_ra * s_pa * c_ya - c_ra * s_ya) + evy * (s_ra * s_pa * s_ya + c_ra * c_ya) + evz * s_ra * c_pa
    qvz = evx * (c_ra * s_pa * c_ya + s_ra * s_ya) + evy * (c_ra * s_pa * s_ya - s_ra * c_ya) + evz * c_pa * c_ra

    return qvx, qvy, qvz


if __name__ == '__main__':
    sensor = MPU6050()
    compass_x, compass_y, compass_z = sensor.readCompass()
    print("X: {:d} \nY: {:d} \nZ: {:d}".format(compass_x, compass_y, compass_z))