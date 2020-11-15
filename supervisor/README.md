# Supervisor

This application handles root-level tasks for the application:

* Gettting sensor data at a regular interval
* updating the display
* Handling button presses
* Flipping operating modes

It runs as part of a systemd service

# TODO
- [X] Write the sensor data to a series of JSON files in a folder
- [x] Create systemd file to start this process
- [X] Create a command socket that can take REST requests
- [ ] Allow it to flip into Setup mode and back into client mode
- [ ] read button presses and process short (info), long(setup mode), and very long press (Factory reset)
- [ ] Process messages that will allow it to change the screen display
