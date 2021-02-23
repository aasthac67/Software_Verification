import pickle

store = pickle.load( open( "save.p", "rb" ) )

Events = store["Events"]
curr_states = store["Initial_States"]

log = open("log.txt", "r")

for line in log.readlines():
	event = line.split(":")[0]
	function = line.split(":")[1]
	valid = True
	for i in range(len(Events[event])):
		if Events[event][i] == 0:
			continue
		if curr_states[i] != Events[event][i][0]:
			valid = False
			print("Event ", event," Not expected")
			break
		else:
			curr_states[i] = Events[event][i][1]
		if not valid:
			break
	if not valid:
		break

if valid:
	print("Test successful!")


