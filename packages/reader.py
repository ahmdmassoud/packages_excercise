import json
import copy

def extract(inputfile,outputfile):
    with open('status.real','r') as f:
        data = f.readlines()
        output = []
        obj = {"PackagName":"","dependencies":"none","Description":""}
        x = 0 
        with open('output1.json','w') as outputfile:
            for line in data:
                x = x + 1
                if "Package" in line:
                    obj["PackagName"] = line.rstrip().split(" ")[-1]
                elif "Depends:" in line:
                    obj["dependencies"] = line.rstrip().split(":")[-1].split(",")
                elif "Description:" in line:
                    obj["Description"] = line.rstrip().split(":")[-1]
                    if (data[x+1].startswith(" ")):
                        obj["Description"] = obj["Description"] + data[x+1]
                    output.append(copy.deepcopy(obj))
            json.dump(output,outputfile)
            return output