#Primerdesign exsig Mag protocol by Alastair Plant, 07/06/2021.
#V4: Full run test, no mixing by pipetting, reduced volume for shallow plate, changed blowout timing to prevent bubbling

#Import standard classes
from opentrons import robot, containers, instruments

robot.comment("exsig v4")
robot.comment("GLHF!")


# Initialise plate, trough and tip rack containers
tiprack_1 = containers.load('tiprack-200ul', 'B2')
reagents = containers.load('96-deep-well', 'B1')
plate = containers.load('96-flat', 'C2')
mag = containers.load('96-flat', 'D2')
waste = containers.load('point', 'C1')
trash = containers.load('point','D1')

# Initialise pipette
pMulti = instruments.Pipette(
    axis="a",
    max_volume=200,
    tip_racks=[tiprack_1],
    trash_container = trash,
    channels=8)

# Set the robot head speed in mm per s. Default = 5000. Z axis travel is not affected.
robot.head_speed(6000)


#Function to remove buffer from rows of wells. Specify values for number of rows (1-12) and number of times to pipette out buffer (for volumes exceeding pipette capacity)
#Tips are replaced between rows to prevent contamination
def remBuf(rowNum,iterNum,vol):
    for i in range(rowNum):
        pMulti.pick_up_tip()
        for j in range(iterNum):
            pMulti.aspirate(vol, mag.rows(i))
            pMulti.dispense(vol, waste)
        pMulti.blow_out(waste)
        pMulti.drop_tip(trash)
    robot.home()
#    robot.pause()
    robot.comment("Move the plate off the mag rack then resume")

#Function to apply buffer to rows of wells then mix by pipetting. Specify values for number of rows k (1:12) and location of wash reagNum (0:x)
def addBuf(rowNum,reagNum,iterNum,vol):
    for k in range(rowNum):
        pMulti.pick_up_tip()
        for l in range(iterNum):
            pMulti.aspirate(vol, reagents.rows(reagNum))
            pMulti.dispense(vol, plate.rows(k))
        pMulti.blow_out(plate.rows(k))
        pMulti.drop_tip(trash)
    robot.home()


#Liquid transfer to calibrate - pipette 100ul e.g. two times to trough (1.6ml total), expect mass change 1.6g
def liqCal(repNum):
    pMulti.pick_up_tip()
    for i in range(repNum):
        pMulti.aspirate(100, reagents.rows(1))
        pMulti.dispense(100, plate.rows(1))
        pMulti.blow_out(plate.rows(1))
    pMulti.drop_tip(trash)



# Define number of rows through which to iterate, hence number of samples. Ensure sufficient tips are available
n = 1



# Remove waste from the wells k number of times (plate ON mag rack), then add a wash (plate OFF mag rack)

# Remove extraction buffer
robot.comment("Removing extraction buffer")
remBuf(n,3,150)
robot.comment("Move the plate off the mag rack then resume")
robot.pause()

# Add Wash Buffer 1
robot.comment("Next Step: Add W1")
addBuf(n,0,2,100)
robot.comment("Move the plate to the mag rack then resume")
robot.pause()

# Remove Wash Buffer 1
robot.comment("Next Step: Remove W1")
remBuf(n,2,100)
robot.comment("Move the plate off the mag rack then resume")
robot.pause()

# Add Wash Buffer 2
robot.comment("Next Step: Add W2")
addBuf(n,1,2,100)
robot.comment("Move the plate to the mag rack then resume")
robot.pause()

# Remove Wash Buffer 2
robot.comment("Next Step: Remove W2")
remBuf(n,2,100)
robot.comment("Move the plate off the mag rack then resume")
robot.pause()

# Add Wash Buffer 3
robot.comment("Next Step: Add W3")
addBuf(n,2,2,100)
robot.comment("Move the plate to the mag rack then resume")
robot.pause()

# Remove Wash Buffer 3
robot.comment("Next Step: Remove W3")
remBuf(n,2,100)
robot.comment("Move the plate off the mag rack then resume")
robot.pause()

# Add Elution Buffer
robot.comment("Next Step: Add EB")
addBuf(n,3,2,100)
robot.comment("Move the plate to the mag rack then transfer RNA to your RT-PCR plate")


#liqCal(4)

#Ensure that the robot is not paused so that the next program can be run
robot.resume()
