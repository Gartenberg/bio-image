from fiji.plugin.trackmate.visualization.hyperstack import HyperStackDisplayer
from fiji.plugin.trackmate.io import TmXmlReader
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate.providers import DetectorProvider
from fiji.plugin.trackmate.providers import TrackerProvider
from fiji.plugin.trackmate.providers import SpotAnalyzerProvider
from fiji.plugin.trackmate.providers import EdgeAnalyzerProvider
from fiji.plugin.trackmate.providers import TrackAnalyzerProvider
from java.io import File
#from java.io import FileFilter
from javax.swing import JFileChooser
from javax.swing.filechooser import FileFilter
from javax.swing.filechooser import FileNameExtensionFilter
import sys
from ij import IJ
class XMLFilter(FileFilter):
	def __init__(self,suffix):
		sekf_suffix=suffix
	def accept(self,f):
		ext=getExtension(f)
		print ext
		if filekun.isDirectory()==True:
			print 'bb'
			IJ.log('bb')
			return True
		elif ext=='.xml':
			IJ.log('bb')
			return True
		else:
			print 'cc'
			IJ.log('bb')
			return True
	def getDescription(self):
		return 'xml files'
		
	def getExtension(self,f):
		filename=f.getName()
		print filename
		filenana,file_extension=os.path.splitext(filename)
		return   file_extension

argvs = sys.argv
argc = len(argvs)
defaultpath='/'
frontoutputpath2= '/'

xmlfil=XMLFilter('kike')
print xmlfil.getDescription()
chooser=JFileChooser()
fakefile = File(defaultpath)
chooser.setCurrentDirectory(fakefile)
chooser.setDialogTitle("Select xml file");
chooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES)
chooser.setAcceptAllFileFilterUsed(False)
InputFolderPath=''
if(chooser.showOpenDialog(None)==JFileChooser.APPROVE_OPTION):
	IJ.log("getCrrentDirectory(): " +chooser.getCurrentDirectory().toString())
	InputFolderPath=chooser.getSelectedFile().toString()
else:
	IJ.log("No selection");
file = File(InputFolderPath)
  
# We have to feed a logger to the reader.
logger = Logger.IJ_LOGGER
  
#-------------------
# Instantiate reader
#-------------------
  
reader = TmXmlReader(file)
if not reader.isReadingOk():
    sys.exit(reader.getErrorMessage())
model = reader.getModel()

spots = model.getSpots()
spotIterator = spots.iterator(False)
chooser2=JFileChooser()
fakefile = File(defaultpath)
chooser2.setCurrentDirectory(fakefile)
chooser2.setDialogTitle("Select Folder");
chooser2.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
chooser2.setAcceptAllFileFilterUsed(False)
frontoutputpath2=''
if(chooser2.showOpenDialog(None)==JFileChooser.APPROVE_OPTION):
	IJ.log("getCrrentDirectory(): " +chooser2.getCurrentDirectory().toString())
	frontoutputpath2=chooser2.getSelectedFile().toString()
else:
	IJ.log("No selection");

frontoutputpath2= frontoutputpath2+'/CavityTrack.txt'

out_f=open(frontoutputpath2,"w")
#tracking id starts from zero
for id in model.getTrackModel().trackIDs(True):
	print(str(id))
	edges = model.getTrackModel().trackEdges(id)
	spotslist=[]
	for edge in edges:
		source=model.getTrackModel().getEdgeSource(edge)
		target=model.getTrackModel().getEdgeTarget(edge)
		sid=source.ID()
		tid=target.ID()
		xs=source.getFeature('POSITION_X')
		ys=source.getFeature('POSITION_Y')
		ts=source.getFeature('FRAME')
		zs=source.getFeature('POSITION_Z')
		snos=-1
		snot=tid
		sinfo=(sid,xs,ys,ts+1,zs,snos,snot)
		spotslist.append(sinfo)
		xt=target.getFeature('POSITION_X')
		yt=target.getFeature('POSITION_Y')
		tt=target.getFeature('FRAME')
		zt=target.getFeature('POSITION_Z')
		tnos=sid
		tnot=-1
		tinfo=(tid,xt,yt,tt+1,zt,tnos,tnot)
		spotslist.append(tinfo)
	print('pre')
	sortedlist=sorted(spotslist, key=lambda student: student[0])
	#Make list ofID
	IDlist=[]
	for spot in sortedlist:
		print('ID='+str(spot[0]))
		if spot[0] in IDlist:
			pass
		else:
			IDlist.append(spot[0])
	for unko in IDlist:
		print('IDlisted='+str(unko))
		Mother=[]
		Daughter=[]
		x=[]
		y=[]
		t=[]
		z=[]
		for spot in sortedlist:
			if spot[0]==unko:
				Mother.append(spot[5])
				Daughter.append(spot[6])
				x.append(spot[1])
				y.append(spot[2])
				t.append(spot[3])
				z.append(spot[4])
		if len(Mother)==1:
			new_line = str(int(x[0])) +" " + str(int(y[0])) +" " + str(int(z[0])) +" " + str(int(t[0])) +" " + str(unko) +" " + str(int(Mother[0])) +" " + str(int(Daughter[0])) +" " + str(int(-1)) +" " + str(int(len(Mother)))+" \n"
			out_f.write(new_line)
		elif len(Mother)==2:
			mum=-1
			if Mother[0]==-1:
				if Mother[1]!=-1:
					mum=Mother[1]
			else:
				mum=Mother[0]
			daus=[]
			if Daughter[0]!=-1:
				daus.append(Daughter[0])
			if Daughter[1]!=-1:
				daus.append(Daughter[1])
			if len(daus)==1:
				new_line = str(int(x[0])) +" " + str(int(y[0])) +" " + str(int(z[0])) +" " + str(int(t[0]))  +" " + str(unko) +" " + str(int(mum)) +" " + str(int(daus[0])) +" " + str(int(-1))   +" " + str(int(len(Mother)))+" \n"
				out_f.write(new_line)
			elif len(daus)==2:
				new_line = str(int(x[0])) +" " + str(int(y[0])) +" " + str(int(z[0])) +" " + str(int(t[0]))  +" " + str(unko) +" " + str(int(mum)) +" " + str(int(daus[0])) +" " + str(int(daus[1])) +" " + str(int(len(Mother)))   +" \n"
				out_f.write(new_line)
			else:
				sys.exit(1)
		elif len(Mother)==3:
			mum=-1
			if Mother[0]==-1:
				if Mother[1]!=-1:
					mum=Mother[1]
				elif Mother[2]!=-1:
					mum=Mother[2]
				else:
					sys.exit(4)
					
			else:
				mum=Mother[0]
			daus=[]
			if Daughter[0]!=-1:
				daus.append(Daughter[0])
			if Daughter[1]!=-1:
				daus.append(Daughter[1])
			if Daughter[2]!=-1:
				daus.append(Daughter[2])
			if len(daus)==1:
				sys.exit(2)
			elif len(daus)==2:
				new_line = str(int(x[0])) +" " + str(int(y[0])) +" " + str(int(z[0])) +" " + str(int(t[0]))  +" " + str(unko)+" " + str(int(mum)) +" " + str(int(daus[0])) +" " + str(int(daus[1])) +" " + str(int(len(Mother)))    +" \n"
				out_f.write(new_line)
			else:
				sys.exit(3)


out_f.close()
