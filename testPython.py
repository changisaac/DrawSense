#download python 3.0 above
#download pySerial
#download https://pyautogui.readthedocs.io/en/latest/
import serial
import time
import pyautogui
import math
import sys

#pyautogui.press('win')

runningAverageArray = []
rangeOfRunningAverage = 10

def getRunningAverage (varData):
	if len(runningAverageArray) <  rangeOfRunningAverage:
		runningAverageArray.append(varData)
		return varData
	else:
		# print ('Old List')
		# print (runningAverageArray)
		j = 0
		while j < rangeOfRunningAverage-1 :
			runningAverageArray [j] = runningAverageArray [j + 1]
			j = j+1
		runningAverageArray [rangeOfRunningAverage -1] = varData
			
		# print ('New Line')
		# print (runningAverageArray)
		running_sum = sum(runningAverageArray)
		result = running_sum / (len(runningAverageArray))

		#for i in range (len (runningAverageArray)):
		#	running_sum = sum - runningAverageArray[i - rangeOfRunningAverage] + runningAverageArray[i]
		#	result = sum / rangeOfRunningAverage
		return result
	
# while True:
# 	varData = input ("Please enter a value : ")
# 	runningAverageValue = getRunningAverage (varData)
# 	print 'Your average is: ', runningAverageValue

ser = serial.Serial("COM8", 9600)
text_file = open("\\Users\\Isaac\\Documents\\Projects\\DrawSense\\DrawSenseOutput.txt", "w")
calibration_values = [] #initially at length zero
user_input_threshholds = []

num_of_buttons = input('How many buttons are you callibrating:')
print('Remember to number your buttons, press any key to start callibrating procedure')
pause = input()

#base_value=0
prev_value=0
#the difference beterrn current sensor input from last input 
#difference=0
#event loop to retrieve callibration values 
for i in range(int(num_of_buttons)):
	print('Hold down BUTTON'+(str(i+1))+'... and press any key to begin callibration')
	pause = input()
	print('Now starting calibration for BUTTON'+(str(i+1))+'...\n\n')
	calibration_values.append([])

	for count in range(150):
		#print("gothere")
		ser.reset_input_buffer()
		ser_in = ser.readline().strip()
		curr_value = ser_in.decode('ascii')
		#run_ave = getRunningAverage(float(int(curr_value)))
		#difference = curr_value - prev_value
		try:
			calibration_values[i].append(curr_value)
		except ValueError:
			count = count -1
		
		print(curr_value)
		#time.sleep(0.5)
		if count%50 == 0 and count != 0:
			pause = input('Switch finger position then press any key to continue callibrating... ')

for j in range(len(calibration_values)):
	text_file.write("\n\n\n"+"BUTTON"+(str(j+1))+"\n\n\n")
	text_file.write(str(calibration_values[j]))
	text_file.write("\n\n\n")


#print(sum(calibration_values[0])/len(calibration_values[0]))
#print(sum(calibration_values[1])/len(calibration_values[1]))
#print(calibration_values)

#callibration function, param in callibration_values and get back quartet arrays
# Main Callibration Function

def getQuartilesArray (callibrationValuesUnsorted):
	quartilesArray = [[]]
	numOfButtons = len(callibrationValuesUnsorted)
	buttonNum = 0
	fieldNum = 0


	# Making lists for each button
	for i in range (numOfButtons-1):
		quartilesArray.append([])

	# Initializing new array for sorted values
	callibrationValues = [[]]
	for i in range (numOfButtons-1):
		callibrationValues.append([])


	for i in range (numOfButtons):
		for j in range (len(callibrationValuesUnsorted[i])):
			callibrationValues[i] = sorted (callibrationValuesUnsorted[i])
		
	# print ('sorted Array:')
	# print callibrationValues


	# Iterating through the array for each button
	for i in range(numOfButtons):
		numOfFields = len(callibrationValues[buttonNum])


		# finding first quartile
		firstQuartileFieldNum = ((numOfFields + 1)/ 4.0 )
		if firstQuartileFieldNum % 1.00 == 0:
			quartilesArray[buttonNum].append(callibrationValues[buttonNum][int(firstQuartileFieldNum-1)])

		# If interpolation is required
		else:
			fieldNumPrev = int (math.floor (firstQuartileFieldNum) )
			fieldNumNext = int (math.ceil (firstQuartileFieldNum) )
			fieldPrevValue = str(callibrationValues[buttonNum][fieldNumPrev - 1])
			fieldNextValue = str(callibrationValues[buttonNum][fieldNumNext - 1])
			fieldPrev = float(fieldPrevValue)
			fieldNext = float (fieldNextValue)
			firstQuartileValue = (((fieldNext - fieldPrev) * (float(firstQuartileFieldNum) - fieldNumPrev))/(fieldNumNext - fieldNumPrev) ) + fieldPrev
			quartilesArray[buttonNum].append(firstQuartileValue)

		# finding second quartile/ median
		medianFieldNum = ((numOfFields + 1)/ 2.0 )
		if medianFieldNum % 1.00 == 0:
			quartilesArray[buttonNum].append(callibrationValues [buttonNum] [ int (medianFieldNum - 1 )])

		# If interpolation is required
		else:
			fieldNumPrev = int (math.floor (medianFieldNum) )
			fieldNumNext = int (math.ceil (medianFieldNum) )
			fieldPrevValue = str(callibrationValues[buttonNum][fieldNumPrev - 1])
			fieldNextValue = str(callibrationValues [buttonNum] [fieldNumNext - 1])
			fieldPrev = float(fieldPrevValue)
			fieldNext = float (fieldNextValue)
			medianValue = (((fieldNext - fieldPrev) * (float(medianFieldNum) - fieldNumPrev))/(fieldNumNext - fieldNumPrev) ) + fieldPrev
			quartilesArray[buttonNum].append(medianValue)


		# finding third quartile
		secondQuartileFieldNum = ((3*(numOfFields + 1))/ 4.0 )
		if secondQuartileFieldNum % 1.00 == 0:
			quartilesArray[buttonNum].append(callibrationValues [buttonNum] [int (secondQuartileFieldNum - 1)])

		# If interpolation is required
		else:
			fieldNumPrev = int( math.floor (secondQuartileFieldNum) )
			fieldNumNext = int (math.ceil (secondQuartileFieldNum))
			fieldPrev = float(str(callibrationValues[buttonNum][fieldNumPrev - 1]))
			fieldNext = float(str(callibrationValues [buttonNum] [fieldNumNext - 1]))
			secondQuartileValue = (((fieldNext - fieldPrev) * (float(secondQuartileFieldNum) - fieldNumPrev))/(fieldNumNext - fieldNumPrev) ) + fieldPrev
			quartilesArray[buttonNum].append(secondQuartileValue)

		# Incrementing buttonNum to calculate quartiles and iterate through the array for the next button
		buttonNum = buttonNum + 1

	# Return a quartiles Array in the format 
	# [[Q1A, Q2A, Q3A] , [Q1B, Q2B, Q3B] , [Q1C, Q2C, Q3C], ...] 
	# where A, B, C are buttons
	return quartilesArray

quartilesArray = getQuartilesArray(calibration_values)
print ('Array output:')
print (quartilesArray)


button_commands = []
print('Entering button mapping configuration...')
default_option = input('Would you like to use the default game controller option (only configures first 4 buttons)? (Y/N)')
if default_option == 'Y':
	button_commands.append('')
	button_commands[0] = 'left'
	button_commands.append('')
	button_commands[1] = 'right'
	#button_commands[2] = 'left'
	#button_commands[3] = 'right'
	button_commands.append('')
	button_commands[len(button_commands)-1] = ''
else:
	for q in range(int(num_of_buttons)):
		button_commands.append('')
		button_commands[q] = input('What would you like the command for BUTTON '+(str(q+1))+' to be?')
		button_commands.append('')
		button_commands[len(button_commands)-1] = ''
		print('confirmed')
print('Fully Configured...')
print('Interface now ACTIVE')

#let quartet_values be the array
# quartet_values = [[]]
# quartet_values.append([])
# quartet_values.append([])
# quartet_values[0].append(1,2,3)
# quartet_values[1].append(3,4,5)
# quartet_values[2].append(5,6,7)



#EVENT LOOP
prev_button_index=0
count = 0
base = 0
while True:
	# for k in range(len(quartilesArray)):
	# 	in_button_ranges.append(False)
	ser.reset_input_buffer()
	ser_in = ser.readline().strip()
	curr_value = ser_in.decode('ascii')
	try:
		if count < 20:
			base = float(str(curr_value))
			count = count + 1
		curr_value_float = float(str(curr_value))
	except ValueError:
		curr_value_float = 20

	#getting running average
	curr_running_average = getRunningAverage(curr_value_float)


	buttons_in_range = []
	for m in range(len(quartilesArray)):
		if curr_value_float < quartilesArray[m][2] + 20 and curr_value_float > quartilesArray[m][0] - 10:
			buttons_in_range.append(m) #array of indices 
			#in quartileArray for which the sensed value falls within the accepted interval
	#buttons_in_range.append()
	if len(buttons_in_range) == 1:
		if buttons_in_range[0] == 0:
			pyautogui.press('left')
		elif buttons_in_range[0] == 1:
			pyautogui.press('right')
		#time.sleep(1)
	elif len( buttons_in_range) == 2:
		difference1 = abs(quartilesArray[0][1] - curr_value_float)
		difference2 = abs(quartilesArray[1][1] - curr_value_float)
		if difference1 < difference2:
			pyautogui.press('left')
		else:
			pyautogui.press('right')
		#time.sleep(1)





	# #sensed value in more than one button range
	# print(buttons_in_range)
	# new_button_index = 0
	# if len(buttons_in_range) > 1:
	# 	smallest_difference = 999
	# 	abs_difference = 0
	# 	for p in range(len(buttons_in_range)):
	# 		median = quartilesArray[buttons_in_range[p]][1]
	# 		abs_difference = abs(curr_running_average-median)
	# 		if abs_difference < smallest_difference:
	# 			smallest_difference = abs_difference
	# 			new_button_index = buttons_in_range[p]
	# 		pyautogui.press(button_commands[new_button_index])
	# elif len(buttons_in_range) == 1: 
	# 	new_button_index = buttons_in_range[0]
	# 	#pyautogui.press(button_commands[new_button_index])
	# 	if (buttons_in_range[0] == 0):
	# 		pyautogui.press("left")
	# 	if (buttons_in_range[0] == 1):
	# 		pyautogui.press("right")
	# 	print(new_button_index)
	# else:
	# 	new_button_index = buttons_in_range[len(buttons_in_range)-1]
	# 	#pyautogui.keyUp(button_commands[prev_button_index])


	# if new_button_index != prev_button_index: 
	# 	#execute_command(new_button_index, prev_button_index)
	# 	pyautogui.keyUp(button_commands[prev_button_index])
	# 	pyautogui.keyDown(button_commands[new_button_index])
	#print ('Previous Button Index: ' + str(prev_button_index))
	#print ('new_button_index: ' + str(new_button_index))
	#print ('Running Average: '+ str(curr_running_average))
	#prev_button_index = new_button_index


	
