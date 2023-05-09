'''
This code mostly copied from the Pozyx documentation.
The code is adapted to work for the digital twin demo.

----- Original comment -----
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python
This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as you move your device around!
----------------------------
'''

from pypozyx import (POZYX_POS_ALG_UWB_ONLY, POZYX_3D, Coordinates, POZYX_SUCCESS, PozyxConstants, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister, DeviceList, PozyxRegisters)

from pypozyx.tools.version_check import perform_latest_version_check

from mqtt_client import MqttClient

import time
import math

class ReadyToLocalize(object):
    '''Continuously calls the Pozyx positioning function and prints its position.'''

    def __init__(self, pozyx, anchors, algorithm=POZYX_POS_ALG_UWB_ONLY, dimension=POZYX_3D, height=1000, remote_id=None, topic='position', 
                 grid_size_x=2500, grid_size_y=2500, grids_amount_x=10, grids_amount_y=10):
        self.pozyx = pozyx

        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.remote_id = remote_id
        self.topic = topic

        self.x_scale = grid_size_x/grids_amount_x
        self.y_scale = grid_size_y/grids_amount_y

    def setup(self):
        '''Sets up the Pozyx for positioning by calibrating its anchor list.'''
        print(f'------------POZYX POSITIONING V{version} -------------\n')
        print('- System will manually configure tag\n')
        print('- System will auto start positioning\n')

        if self.remote_id is None:
            self.pozyx.printDeviceInfo(self.remote_id)
        else:
            for device_id in [None, self.remote_id]:
                self.pozyx.printDeviceInfo(device_id)

        print(f'\n------------POZYX POSITIONING V{version} -------------')

        self.setAnchorsManual(save_to_flash=False)
        self.printPublishConfigurationResult()

        # Setup MQTT connection and connect
        self.pozyx_mqtt = MqttClient(self.topic)
        self.pozyx_mqtt.connect_mqtt()


    def loop(self):
        '''Performs positioning and displays/exports the results.'''
        position = Coordinates()
        status = self.pozyx.doPositioning(
            position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
        if status == POZYX_SUCCESS:
            self.publishPosition(position)
        else:
            self.printPublishErrorCode('positioning')

    # Publish the position via the MQTT protocol
    def publishPosition(self, position):
        '''Publishes the Pozyx's position'''
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        
        print(position.x, position.y)

        # Translate the position to the correct grid
        pos_x = math.floor(position.x/self.x_scale) + 1
        pos_y = math.floor(position.y/self.x_scale) + 1
        self.pozyx_mqtt.publish(f'{pos_x}/{pos_y}')

    def printPublishErrorCode(self, operation):
        '''Prints the Pozyx's error'''
        error_code = SingleRegister()
        network_id = self.remote_id
        if network_id is None:
            self.pozyx.getErrorCode(error_code)
            print(f'LOCAL ERROR {operation}, {self.pozyx.getErrorMessage(error_code)}')
            return
        status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if status == POZYX_SUCCESS:
            print(f'ERROR {operation} on ID 0x{network_id:04x}, {self.pozyx.getErrorMessage(error_code)}')
        else:
            self.pozyx.getErrorCode(error_code)
            print(f"ERROR, couldn't retrieve remote error code, LOCAL ERROR {operation}, {self.pozyx.getErrorMessage(error_code)}")
            # Should only happen when not being able to communicate with a remote Pozyx.

    def setAnchorsManual(self, save_to_flash=False):
        '''Adds the manually measured anchors to the Pozyx's device list one for one.'''
        status = self.pozyx.clearDevices(remote_id=self.remote_id)
        for anchor in self.anchors:
            status &= self.pozyx.addDevice(anchor, remote_id=self.remote_id)
        if len(self.anchors) > 4:
            status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(self.anchors),
                                                       remote_id=self.remote_id)

        if save_to_flash:
            self.pozyx.saveAnchorIds(remote_id=self.remote_id)
            self.pozyx.saveRegisters([PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], remote_id=self.remote_id)
        return status

    def printPublishConfigurationResult(self):
        '''Prints and potentially publishes the anchor configuration result in a human-readable way.'''
        list_size = SingleRegister()

        self.pozyx.getDeviceListSize(list_size, self.remote_id)
        print('List size: {0}'.format(list_size[0]))
        if list_size[0] != len(self.anchors):
            self.printPublishErrorCode('configuration')
            return
        device_list = DeviceList(list_size=list_size[0])
        self.pozyx.getDeviceIds(device_list, self.remote_id)
        print('Calibration result:')
        print('Anchors found: {0}'.format(list_size[0]))
        print('Anchor IDs: ', device_list)

        for i in range(list_size[0]):
            anchor_coordinates = Coordinates()
            self.pozyx.getDeviceCoordinates(device_list[i], anchor_coordinates, self.remote_id)
            print('ANCHOR, 0x%0.4x, %s' % (device_list[i], str(anchor_coordinates)))

    def printPublishAnchorConfiguration(self):
        '''Prints and potentially publishes the anchor configuration'''
        for anchor in self.anchors:
            print('ANCHOR,0x%0.4x,%s' % (anchor.network_id, str(anchor.coordinates)))


if __name__ == '__main__':
    # Check for the latest PyPozyx version. Skip if this takes too long or is not needed by setting to False.
    check_pypozyx_version = True
    if check_pypozyx_version:
        perform_latest_version_check()

    # Shortcut to not have to find out the port yourself
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print('No Pozyx connected. Check your USB cable or your driver!')
        quit()

    remote_id = 0x684F  # Remote device network ID
    remote = True   # Whether to use a remote device
    if not remote:
        remote_id = None

    # Necessary data for calibration, change the IDs and coordinates yourself according to your measurement
    anchors = [DeviceCoordinates(0x1128, 1, Coordinates(0, 2500, 240)),
               DeviceCoordinates(0x116F, 1, Coordinates(2500, 0, 500)),
               DeviceCoordinates(0x116E, 1, Coordinates(2500, 2500, 0)),
               DeviceCoordinates(0x113B, 1, Coordinates(0, 0, 0))]

    # Positioning algorithm to use, other is PozyxConstants.POSITIONING_ALGORITHM_TRACKING
    algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
    # Positioning dimension. Others are PozyxConstants.DIMENSION_2D, PozyxConstants.DIMENSION_2_5D, PozyxConstants.DIMENSION_3D
    dimension = PozyxConstants.DIMENSION_2_5D
    #Hheight of device, required in 2.5D positioning
    height = 1

    pozyx = PozyxSerial(serial_port)
    r = ReadyToLocalize(pozyx, anchors, algorithm, dimension, height, remote_id)
    r.setup()
 
    while True:
        r.loop()
        time.sleep(0.10)
    