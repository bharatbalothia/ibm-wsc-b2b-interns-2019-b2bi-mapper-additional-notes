
def xml_output_field_func(field_ptr):
    for children in field_ptr:
        if children.tag.split('}')[1]=="Note":
            children.text=''    # here the notes are emptied

def xml_output_record_func(rec_ptr):
    for children in rec_ptr:
        if children.tag.split('}')[1]=='Field':
            xml_output_field_func(children)

def xml_output_particle_func(particle_ptr):
    for children in particle_ptr:
        if children.tag.split('}')[1]=="XMLElementGroup":
            xml_output_group_func(children)

def xml_output_group_func(group_ptr):
    for children in group_ptr:
        if children.tag.split('}')[1]=="XMLParticleGroup":
            xml_output_particle_func(children)
        if children.tag.split('}')[1]=="XMLRecord":
            xml_output_record_func(children)
        if children.tag.split('}')[1]=="XMLElementGroup":
            xml_output_group_func(children)

def output_field(field_ptr):
    for child in field_ptr:
        if child.tag.split('}')[1]=="Note":
            child.text=''       # notes emptied here for xml files

def output_seg(seg_ptr):
    for children in seg_ptr:
        if children.tag.split('}')[1]=="Composite":
            output_seg(children)
        elif children.tag.split('}')[1] == "Field":
            output_field(children)

def output_group(group_ptr):
    for children in group_ptr:
        if children.tag.split('}')[1]=="Group":
            output_group(children)
        elif children.tag.split('}')[1]=="Segment":
            output_seg(children)
        elif children.tag.split('}')[1]=="PosRecord":
            output_seg(children)



def empty_notes(data_root,etree,raw_data,dst):
    out_list=dst.split('/')
    output_file="tmp/"+ out_list[len(out_list)-1]        # reaching the location of the file
    for child in data_root[4][0]:
        if child.tag.split('}')[1]=="XMLElementGroup":      # to initiate the routine procedure of accessing each field used everywhere
            xml_output_group_func(child)
        if child.tag.split('}')[1] == "Group":
            output_group(child)

    data_root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    etree.register_namespace("", "http://www.stercomm.com/SI/Map")
    raw_data.write(output_file, encoding='utf-8', xml_declaration=True)
