from flask import * 
import re
import pickle

app = Flask(__name__)  

ret = 0
evs = 0
fns = 0
add_list=[]
fname = ""
@app.route('/done_log', methods=['POST'])
def done_log():
	global add_list
	global evs
	global fname
	#f = open(fname, "r")
	f1 = open("new_"+fname, "w")

	with open(fname) as f:
		lines = [line.rstrip() for line in f]
	num = 0
	for line in lines:
		num+=1
		f1.write(line)
		f1.write("\n")
		for a in add_list:
			if a[2] == str(num):
				print("adding")
				f1.write("\t"*int(a[3])+'print("'+evs["events"][int(a[0])-1].splitlines()[0].split(".")[1]+":"+ret["result"][int(a[1])-1].split(".")[1]+'")')
				f1.write("\n")


	return "Done"



@app.route('/handle_data', methods=['POST'])
def handle_data():
	global ret
	global evs
	global fns
	global add_list

	print(evs, type(evs))
	en = request.form['event_number']
	fn = request.form['function_number']
	ln = request.form['line_number']
	il = request.form['indent_level']
	add_list.append([en,fn,ln,il])
	print("Function",fn)
	print("Line",ln)
	print("Event",en)
	print(ret)
	print(evs["events"][int(en)-1])
	print(ret["result"][int(fn)-1])
	evs["events"][int(en)-1] = evs["events"][int(en)-1] + "\n\t" + ret["result"][int(fn)-1].split(".")[1] + ": " + ln
	
	return render_template("all.html", res = ret, evs = evs, fns = fns)

def parse_py(name):
	txt = []
	funcs = []
	exp = "def "
	with open(name) as f:
		lines = [line.rstrip() for line in f]
	found = False
	pg = []
	index = 0
	orig_ln=0
	for line in lines:
		orig_ln+=1
		x = re.search(exp, line)
		if not (x == None):
			if index >= 1:
				indi = {index-1:pg}
				funcs.append(indi)
				pg = []
			found = True
			index+=1
			txt.append(str(index)+". "+line)
			#txt.append(line)
		if found:
			pg.append(str(orig_ln)+ ".\t" + line)

	if index >= 1:
		indi = {index-1:pg}
		funcs.append(indi)
		pg = []

	#print(funcs)
	return txt, funcs

def parse_file(name, extension):
	if extension == "c":
		return parse_c(name)
	elif extension == "py":
		return parse_py(name)

def process_file(fname):
	x = fname.split(".")
	if len(x) >=2:
		if x[1] == "c" or x[1]=="cpp" or x[1]=="py":
			res = parse_file(fname, x[1])
			return res
		else:
			return x[1]
	else:
		return ""
 
@app.route('/')  
def upload():  
    return render_template("upload.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
	global ret
	global evs
	global fns
	global fname
	if request.method == 'POST':  
		f = request.files['file'] 
		fname = f.filename
		f.save(f.filename)
		res, fns = process_file(f.filename)
		ret = {"result":res}

		store = pickle.load( open( "./Verification/save.p", "rb" ) )

		Events = []
		index  = 1
		for k in store["Events"].keys():
			#print(k)
			Events.append(str(index)+". "+k)
			index+=1

		evs = {"events":Events}
        #print(re,evs)
		return render_template("all.html", res = ret, evs = evs, fns = fns)  
  
if __name__ == '__main__':  
    app.run(debug = True,  port ="2020")
