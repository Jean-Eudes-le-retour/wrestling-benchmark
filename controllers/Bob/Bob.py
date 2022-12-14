# Copyright 1996-2022 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controller example for the Robot Wrestling Tournament.
   Demonstrates how to access sensors and actuators"""

from controller import Robot, Motion


class Wrestler (Robot):
    def __init__(self):
        Robot.__init__(self)
        self.timeStep = int(self.getBasicTimeStep())  # retrieves the WorldInfo.basicTimeTime (ms) from the world file

        # camera
        self.cameraTop = self.getDevice("CameraTop")
        self.cameraBottom = self.getDevice("CameraBottom")
        self.cameraTop.enable(4 * self.timeStep)
        self.cameraBottom.enable(4 * self.timeStep)

        # there are 7 controllable LEDs on the NAO robot, but we will use only the ones in the eyes
        self.leds = []
        self.leds.append(self.getDevice('Face/Led/Right'))
        self.leds.append(self.getDevice('Face/Led/Left'))

        # shoulder pitch motors
        self.RShoulderPitch = self.getDevice("RShoulderPitch")
        self.LShoulderPitch = self.getDevice("LShoulderPitch")

        # load motion files
        self.loop = Motion('motions/loop.motion')


    def run(self):
        self.RShoulderPitch.setPosition(0)  # arms in front, zombie mode
        self.LShoulderPitch.setPosition(0)

        self.loop.setLoop(True)
        self.loop.play()

        self.leds[0].set(0xff0000)  # set eyes to red, kill mode activated
        self.leds[1].set(0xff0000)

        while self.step(self.timeStep) != -1:
            t = self.getTime()
            if t == 27:
                self.LShoulderPitch.setPosition(-1.57)  # victory
                self.RShoulderPitch.setPosition(-1.57)
                self.leds[0].set(0x00ff00)  # set eyes to green
                self.leds[1].set(0x00ff00)
            pass


# create the Robot instance and run main loop
wrestler = Wrestler()
wrestler.run()
