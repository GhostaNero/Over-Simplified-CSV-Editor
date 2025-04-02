userInput = input("")
inputList = userInput.split(" ")

postCount = int(inputList[0]) / 3
railingCount = int(inputList[1]) / 4
picketsCount = int(inputList[2]) / 16

# Initialize minVal to the first value
minVal = postCount
if minVal > railingCount:
    minVal = railingCount

if minVal > picketsCount:
    minVal = picketsCount

print(int(minVal * 4))