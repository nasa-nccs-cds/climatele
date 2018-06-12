import matplotlib.pyplot as plt
from climatele.test.access_results import *
from climatele.project import *

projectName = "MERRA2_EOFs"
outDir = "/tmp/"
start_year = 1980
end_year = 2000
varName = "ts"
experiment = projectName + '_'+str(start_year)+'-'+str(end_year) + '_' + varName
project = Project( outDir, projectName )
file_path = os.path.dirname(os.path.realpath(__file__))

enso = open("enso_data.txt", "r")
text = enso.read()
strdata = []
data = []
for i in text.split():
    strdata.append(i.strip())
for i in strdata:
    if float(i) > 1979:
        strdata.remove(i)
    else:
        data.append(float(i))
# adj_data = []
# for i in range(len(data)):
#     adj_data.append(i*(455./230.))
num_data = []
for i in data:
    num_data.append(i*90)

pcVarList = project.getVariableNames( experiment, PC )
pcVariable = project.getVariable( pcVarList[0], experiment, PC)

plt.plot(range(len(data)),num_data, color = "g", label = "ENSO Data")
plt.plot(range(len(pcVariable.data)),pcVariable.data, color = "r", label = "EOF mode 1")
plt.title("ENSO data and EOF mode 1, 1980-2000")
plt.legend()
plt.show()