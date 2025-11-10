# Eload Wrapper
## _Download and Operation_

## Download
- Go into the dist folder and download the executable file (Expect something like "dist/Eload Wrapper V1.exe")
- In your download folder - double click to run it. 

## Operation
- Connect the Eload to the computer
- On the GUI you should see that there is an option at Serial Port. If not hit the refresh button.
- If there is an option for the Serial Ports dropdown, select the one you seek to use and hit Connect. The status should change to connected and the plots should begin updating.
- On the plotting side, clicking on each of the loads should toggle its plot. 

### Running A Test
- On the left side, select the channel that you seek to add a load to. 
- Hit the dropdown and select from one of the following: 
- Constant Load: Open-Loop Control, the load just gets open a certain amount (0 - 5A) 
- Constant Current: Closed-Loop Control of the output current (0 - 5A) until a certain voltage cutoff. 
- Profile: Closed loop control that starts at a certain current (Starting Current) and grows a certain amounts (Current Increment) every certain amount of time (Seconds Per Step) until it either reaches the ending current (Target) or the voltage of the load dips below a certain cutoff (Voltage Cutoff)
- Select the test, enter in your values, and hit start test. The screen should update accordingly and give the test info. 
- Hit STOP TEST to stop the test. 
- Clicking different loads that are currently running tests also shows their test info and allows you to stop/start multiple tests at the same time. 
