import csv
import os
import os.path
import re
import numpy

rootdir = "./PowerTraces"

def ImportFile():
	traces=[]
	for parent,dirnames,filenames in os.walk(rootdir):
	    for filename in filenames:
	    	#read all of power trace files,and get PlainText,CipherText and Power Trace 
	        pattern = re.compile(r'trace_n=(.[0-9]*)_m=(.[A-Za-z0-9]*)_c=(.[A-Za-z0-9]*)_mask=\.csv',flags=0)
	        res=pattern.search(filename)
	        
	        index=int(res.group(1))
	        pt=res.group(2)
	        ct=res.group(3)

	        csv_reader = csv.reader(open(rootdir+"/"+filename))

	        flag=0;
	        pn=[]
	        for row in csv_reader:
	           flag=flag+1;
	           if(flag==2):
	             if(len(row)>1000):
	             	row.pop()
	             pn=row
	             break
	        # break
	        # print(pn)
	        #index  pt=PlainText ct=CipherText pn= PointsNumer of PowerTrace
	        trace=(index,pt,ct,pn)
	        traces.append(trace)


	traces.sort();
	return traces
	# print(traces);

#split text by length
def cut_text(text,lenth): 
   textArr = re.findall('.{'+str(lenth)+'}', text) 
   for i in range(len(textArr)):
   	  textArr[i]=int(textArr[i],16)
   return textArr

#save to numpy file for CPA attack
def Save2Npy(traces):
	pts=[]
	pns=[]
	cts=[]
	pcts=[]
	for trace in traces:
	   # print(trace)
	   pt=trace[1]
	   ct=trace[2]

	   cut_pts=cut_text(pt,2)
	   cut_cts=cut_text(ct,2)

	   pts.append(cut_pts)
	   cts.append(cut_cts)
	   pcts.append([cut_pts,cut_cts])

	   pn=trace[3]
	   # print(pn)
	   pns.append(pn)
	numpy.save("pts.npy",pts)
	numpy.save("pcts.npy",pcts)
	numpy.save("pns.npy",pns)
	print(numpy.shape(numpy.load("pts.npy")))
	print(numpy.shape(numpy.load("pcts.npy")))
	print(numpy.shape(numpy.load("pns.npy")))





traces=ImportFile()
Save2Npy(traces)
