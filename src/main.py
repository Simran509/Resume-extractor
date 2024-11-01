import pandas as pd
import os
import urllib.request
from getFilePath import App 
from tqdm import tqdm
from time import sleep
import shutil
import logging
import webbrowser

"""Global Variables"""
logFilePath=""

""" Create the Folder to store Extracted resumes """
def createFolder(ResumeFolder):
  path= ResumeFolder
  if(os.path.isdir(path)):
    print('\n[INFO] Folder with same name Found. Cleaning old files!')
    
    for f in os.listdir(path):
      os.remove(os.path.join(path, f))
    print('[INFO] Cleaning Done! Old Files removed from the Resume Folder.')
  else:
     
      os.makedirs(path,exist_ok=True)
      print('[INFO] Resume Folder Created')

""" Get column number of the Name of student """
def createNameListEnum(columns, nameList):
  nameListEnum = []
  for name in nameList:
    try:
      nameListEnum.append(columns.index(name))
    except Exception as e:
      print(name + " is not a valid column name")
  return nameListEnum

""" Get column number of the Roll Number of student """
def createRollNumberEnum(columns, rollNumberColumn):
  rollListEnum = 0
  try:
    rollListEnum=columns.index(rollNumberColumn)
  except Exception as e:
    print(rollNumberColumn + " is not a valid column name for roll number")
  return rollListEnum

""" Get column number of the Resume Links of student """
def createResumeColumnEnum(columns, resumeColumn):
  resumeColumnEnum = 0
  try:
    resumeColumnEnum = columns.index(resumeColumn)
  except Exception as e:
    print(resumeColumn + " is not a valid column name")
  return resumeColumnEnum

""" 
  Make File name of each resume.pdf
  Current Format: NAME_BATCH_ROLLNUMBER.pdf
"""
def getFileName(row, nameListEnum, rollListEnum):
  fileNames = []
  for nameIndex in nameListEnum:
    name = "_".join(str(row[nameIndex]).upper().split(" "))
    fileNames.append(name)
  
  rollNo="_".join(str(row[rollListEnum]).upper().split("/"))
  fileNames.append(rollNo)
  fileName = "_".join(fileNames)
  return fileName

""" Fetch Resume from the URL """
def fetchURLData(url, fileName, ResumeFolder):
  try:
    urllib.request.urlretrieve(url, ResumeFolder + "/" + fileName + '.pdf')
    return ""
  except Exception as e: 
    return fileName

def ResumeZIPGenerator(applicationList, nameList, rollNumberColumn, resumeColumn, ResumeFolder,parentFolder):

  
  logging.basicConfig(filename=logFilePath, filemode='w', 
      level=logging.DEBUG,
    format='%(levelname)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
  try: 
    createFolder(ResumeFolder)
  except Exception as e:
    logging.info("Folder already created")


  
  df = pd.read_csv(applicationList,encoding='Latin-1')
  print("File Path is correct")
  X = df.values
  n = len(X)
  noOfRows = len(df)
  columns = list(df.columns)
  # To prevent Error, Convert all strings to lowerCase for comparison
  for i in range(len(columns)):
    columns[i] = columns[i].lower()
  
  nameListEnum = createNameListEnum(columns,  nameList)
  rollListEnum = createRollNumberEnum(columns,  rollNumberColumn)
  resumeColumnEnum = createResumeColumnEnum(columns, resumeColumn)

  exception = []
  print('Extracting Resumes from Links.')
  with tqdm(total=noOfRows) as pbar:
    for i in range(noOfRows):
      fileName = getFileName(X[i], nameListEnum,rollListEnum)
      url = X[i][resumeColumnEnum]

      tmp = fetchURLData(url, fileName, ResumeFolder)
      if len(tmp) > 0: 
        errStatement="Name/RollNumber:" + tmp + " || Resume Link:"+ url
        exception.append(errStatement)

      pbar.update(1)
  programStatus=""
  if len(exception)==0:
    programStatus="Successful"
  else:
    programStatus="Partial"

  logging.info("Resume fetching completed.")
  logging.info("Status till now: " + programStatus)

  logging.info("Resume Downloaded: ("+str(noOfRows-len(exception))+") out of ("+ str(noOfRows)+")")
  if len(exception) > 0:
    print("The Resumes couldn't be fetched for the following students: CHECK LOG file ")
    logging.critical("The Resumes couldn't be fetched for the following students: ")
    for e in exception:
      print(e)
      logging.critical(e)

  print('[INFO] Extraction complete. Zipping the resume folder')
  logging.info("Extraction complete. Zipping the resume folder")
  shutil.make_archive(ResumeFolder, 'zip', ResumeFolder)


if __name__ == '__main__':
  

  # Add csv file path to the applicationList. GUI panel appears
  nap=App()
  applicationList=nap.getFilePath()
  nameList = ['name']
  resumeColumn = "resume"
  rollNumberColumn = "rollno"
  JobProfileName=(applicationList.split('/')[-1]).split('.')[0]
  JobProfileName=JobProfileName.replace(' ','_')
  parentFolder=nap.getDirectoryPath()
  logFilePath=parentFolder+"\\"+JobProfileName+"\\"+JobProfileName+'.log'

  ResumeFolder=parentFolder+"\\"+JobProfileName+"\\TIET_"+JobProfileName +"_Resumes"
  ResumeZIPGenerator(applicationList, nameList, rollNumberColumn, resumeColumn, ResumeFolder,parentFolder)
  print('Opening the parent Folder and Log file in explorer in 2 sec.')
  print("===========================================================")
  os.system('start '+ ResumeFolder)
  webbrowser.open(logFilePath)
