import xml.etree.ElementTree as et

filehandler = open(r"C:\Users\RajnishKumarVENDORRo\Downloads\AN\tmp\ASC_SOU_PETSMART_I_850_3010.mxl",encoding="utf-8")
raw_data = et.parse(filehandler)
data_root = raw_data.getroot()


inp_format_tag=data_root[3][0]
out_format_tag=data_root[4][0]

   # constant index to corresponding value is stored here
if inp_format_tag.tag.split('}')[1]=='EDISyntax':
    print("&&&&&&&&&&&&&&&&&")
    input_format='EDI'

for child in data_root:
    #print(child.tag.split('}')[1])
    input_format = "EDI"

for child in inp_format_tag:
    if child.tag.split('}')[1] == "Group":
        print(child.tag)
        for children in child:
            if children.tag.split('}')[1] == "ExplicitRule":
                print(children.tag)
            if children.tag.split('}')[1] == "Group":
                print(children.tag)