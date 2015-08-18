#
# OCR correction
#

# force UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# set filenames
txtfile = 'gsc3_uniline.txt'
posfile = 'gsc_loc_all.txt'
newtxtfile = txtfile.replace('.txt','.new.txt')
newposfile = posfile.replace('.txt','.new.txt')

# read ocr-text file
with open(txtfile,'r') as txt:
	olddoc = txt.readline().strip().decode('utf8')
	newdoc = ''

# read golden-pos file
oldlist = []
newlist = []
with open(posfile,'r') as pos:
	for line in pos:
		cols = line.strip().decode('utf8').split('\t') # TSV
		start = int(cols[0]) # start position (0-based)
		stop = int(cols[1]) # stop position
		text = cols[2] # OCR place: stop-start == len(old)
		try:			
			newtext = cols[3] # correct place
		except IndexError:
			newtext = text
		oldlist.append((start,stop,text))
		newlist.append((start,stop,newtext)) # positions are not yet set
		if stop-start != len(text) or olddoc[start:stop] != text: # verify old position and text
			print("Error at {0}-{1}: {2}".format(start, stop, text))

# calculate new positions
for index,item in enumerate(newlist):
	(start,stop,text) = item
	if stop-start != len(text): # different text length => next positions change
		diff = (stop-start) - len(text) # negative if shorter, positive if longer
		stop = start + len(text) # update stop
		for _index,_item in enumerate(newlist[index:]):
			(_start,_stop,_text) = _item
			newlist[index+_index] = (_start-diff,_stop-diff,_text)
		newlist[index] = (start,stop,text) # save current position

# copy & update & verify new doc
cursor = 0
for index in range(0,len(oldlist)):
	(oldstart,oldstop,oldtext) = oldlist[index]
	(newstart,newstop,newtext) = newlist[index]
	newdoc += olddoc[cursor:oldstart] # copy up to start position
	newdoc += newtext # copy new text
	cursor = oldstop
	if newstop-newstart != len(newtext) or newdoc[newstart:newstop] != newtext: # verify new position and text
		print("Error at {0}-{1}: {2}".format(newstart, newstop, newtext))
newdoc += olddoc[cursor:] # copy up to end of doc

# write new files
print('Writing new text file in ' + newtxtfile)
with open(newtxtfile,'w') as out:
	out.write(newdoc.encode('utf8')+'\n')

print('Writing new positions in ' + newposfile)
with open(newposfile,'w') as out:
	for item in newlist:
		(newstart,newstop,newtext) = item
		line = '{0}\t{1}\t{2}'.format(newstart,newstop,newtext)
		out.write(line.encode('utf8')+'\n')


