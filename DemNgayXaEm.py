import os
import sys
import table

fileTypes = ['php', 'html', 'css', 'js', 'ctp', 'tpl'];
class CodeFile:
  def __init__(self, file):
    self.filePath = file

  def getCountTotalLine(self):
    return sum(1 for line in open(self.filePath, 'rb'))

  def getFileType(self):
      tmp = self.filePath.split(".")
      return tmp[len(tmp)-1]

  def getCountEmptyLine(self):
    with open(self.filePath, 'rb') as f:
        count = sum(line.isspace() for line in f)
    return count
     
  def getCountSingleLineCommentOfHtml(self):
    count = 0
    for line in open(self.filePath, 'rb').readlines():
        line = line.strip()
        if line:
	    if (line.startswith('<!--') and line.endswith('-->')):
	        count += 1
    return count + self.getCountSingleLineCommentOfJs() + self.getCountSingleLineCommentOfCss()
    
  def getCountSingleLineCommentOfPhp(self):
    count = 0
    for line in open(self.filePath, 'rb').readlines():
        line = line.strip()
        if line:
	    if (line.startswith('//')):
	        count += 1
    return count
    
  def getCountSingleLineCommentOfJs(self):
    count = 0
    for line in open(self.filePath, 'rb').readlines():
        line = line.strip()
        if line:
	    if (line.startswith('//')):
	        count += 1
    return count
    
  def getCountSingleLineCommentOfCss(self):
    count = 0
    for line in open(self.filePath, 'rb').readlines():
        line = line.strip()
        if line:
	    if (line.startswith('/*') and line.endswith('*/')):
	        count += 1
    return count
    
  def getCountSingleLineCommentOfTpl(self):
    count = 0
    for line in open(self.filePath, 'rb').readlines():
        line = line.strip()
        if line:
     	    if (line.startswith('{*') and line.endswith('*}')):
     	        count += 1
    return count + self.getCountSingleLineCommentOfHtml()
    
  def getCountMultiLineCommentOf(self, start, end):
      inComment = False
      count = 0
      for line in open(self.filePath, 'rb').readlines():
        line = line.strip()
        if line:
            if (not inComment and line.startswith(start) and end not in line):
                inComment = True
                count += 1
            elif (inComment and end not in line):
                count += 1
            elif (inComment and line.endswith(end)):
                count += 1
                inComment = False
      return count
      
  def getCountMultiLineCommentOfHtml(self):
      return self.getCountMultiLineCommentOf('/*','*/') + self.getCountMultiLineCommentOf('<!--','-->')
  def getCountMultiLineCommentOfCss(self):
      return self.getCountMultiLineCommentOf('/*','*/')
  def getCountMultiLineCommentOfJs(self):
      return self.getCountMultiLineCommentOf('/*','*/')
  def getCountMultiLineCommentOfPhp(self):
      return self.getCountMultiLineCommentOf('/*','*/')
  def getCountMultiLineCommentOfTpl(self):
      return self.getCountMultiLineCommentOf('{*','*}') + self.getCountMultiLineCommentOfHtml()
  def getCountMultiLineCommentOfCtp(self):
      return self.getCountMultiLineCommentOf('/*','*/')
      
def listFiles(dir):
    r = []
    subdirs = [x[0] for x in os.walk(dir)]
    for subdir in subdirs:
        files = os.walk(subdir).next()[2]
        if (len(files) > 0):   
            for file in files:
                fileExt = getFileType(file)
		if fileExt in fileTypes:
                    r.append(subdir + "/" + file)
    return r

def getFileType(filePath):
      tmp = filePath.split(".")
      return tmp[len(tmp)-1]
      
def demNgayXaEm(dir):
    files = listFiles(dir);
    dnxe = []
    total = 0
    for file in files:
        x = CodeFile(file)
        fileType = x.getFileType()
        numOfEmptyLine = x.getCountEmptyLine()
        numOfTotalLine = x.getCountTotalLine()
        if(fileType == 'html'):
          numOfSingleCommentLine = x.getCountSingleLineCommentOfHtml()
          numOfMultiCommentLine = x.getCountMultiLineCommentOfHtml()
        elif(fileType == 'php'):
          numOfSingleCommentLine = x.getCountSingleLineCommentOfPhp()
          numOfMultiCommentLine = x.getCountMultiLineCommentOfPhp()
        elif(fileType == 'js'):
          numOfSingleCommentLine = x.getCountSingleLineCommentOfJs()
          numOfMultiCommentLine = x.getCountMultiLineCommentOfJs()
        elif(fileType == 'css'):
          numOfSingleCommentLine = x.getCountSingleLineCommentOfCss()
          numOfMultiCommentLine = x.getCountMultiLineCommentOfCss()
        elif(fileType == 'ctp'):
          numOfSingleCommentLine = x.getCountSingleLineCommentOfCtp()
          numOfMultiCommentLine = x.getCountMultiLineCommentOfCtp()
        elif(fileType == 'tpl'):
          numOfSingleCommentLine = x.getCountSingleLineCommentOfTpl()
          numOfMultiCommentLine = x.getCountMultiLineCommentOfTpl()
        else: 
          numOfSingleCommentLine = 0
          numOfMultiCommentLine = 0
        finalTotal = numOfTotalLine - numOfSingleCommentLine - numOfMultiCommentLine - numOfEmptyLine
        total += finalTotal
        dataList = (file, numOfTotalLine, numOfEmptyLine, numOfSingleCommentLine, numOfMultiCommentLine, finalTotal)
        dnxe.append(dataList)

    sys.stdout.write('State Capitals (source: Wikipedia)\n\n')
    headings = ['File', 'Total Line', 'Empty lines', 'Comment lines (single)', 'Comment lines (multi)', 'Final total']
    fields = [0, 1, 2, 3, 4, lambda rec: rec[1] - rec[2] - rec[3] - rec[4]]
    align = [('^', '<'), ('^', '^'), ('^', '^'), ('^', '^'), ('^', '^'), ('^','^')]
    table.table(sys.stdout, dnxe, fields, headings, align)
    print("-------------------------------------------------------------------------------------------------------------")
    print("Total lines of code exclude empty lines and comment lines: " + str(total))
    
demNgayXaEm(sys.argv[1:][0])

