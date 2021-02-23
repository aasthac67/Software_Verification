import re
import pickle

files = ["Fine.dot", "Issue.dot", "Spec1.dot", "Submission.dot"]
current_states = []
events = dict()
for fil in range(len(files)):
	f = open(files[fil],"r")
	for line in f.readlines():
		x = re.search("->", line)
		if x:
			start = False
			lis = []
			start_ind = 0
			for i in range(len(line)):
				if line[i]=='"' and start == False:
					start = True
					start_ind = i
				elif line[i]=='"' and start == True:
					start = False
					lis.append(line[start_ind+1:i])
			if "__init_" in lis[0]:
				current_states.append(lis[1])
			else:

				evs = lis[2].split("\\n")
				for e in evs:
					if e not in events.keys():
						events[e] = [0]*len(files)
						events[e][fil] = (lis[0], lis[1])
					else:
						events[e][fil] = (lis[0], lis[1])

store = dict()
store["Events"] = events
store["Initial_States"] = current_states

pickle.dump( store, open( "save.p", "wb" ) )


