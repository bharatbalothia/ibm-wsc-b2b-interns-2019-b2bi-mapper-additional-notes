from pyparsing import *
import pyparsing as pp
import re

def preprocess(pre_n, pre_o, globalVariables):
    for line in pre_o:
        flag = 0
        for ind, letter in enumerate(line):
            if line[ind] == '"':
                if flag == 0:
                    flag = 1  ## means that a string has started
                else:
                    flag = 0
            if flag == 1 and line[ind] == '+':
                line = line[:ind] + " plus999 " + line[ind + 1:]  ## changing plus op
            if flag == 1 and line[ind] == '-':
                line = line[:ind] + " minus999 " + line[ind + 1:]
            if flag == 1 and line[ind] == '<':
                line = line[:ind] + " less999 " + line[ind + 1:]
            if flag == 1 and line[ind] == '>':
                line = line[:ind] + " greater999 " + line[ind + 1:]
            if flag == 1 and line[ind] == '*':
                line = line[:ind] + " multiply999 " + line[ind + 1:]
            if flag == 1 and line[ind] == '/':
                line = line[:ind] + " divide999 " + line[ind + 1:]
            if flag == 1 and line[ind] == '<<':
                line = line[:ind] + " leftshift999 " + line[ind + 1:]
            if flag == 1 and line[ind] == '>>':
                line = line[:ind] + " rightshift999 " + line[ind + 1:]
        # print(line)
        pre_n.write(line)


def xml_field_func(field_ptr, grp_name, field_ct, fo, xml_tag, rec_id, globalVariables):
    # if field_ptr[3].text=='0':
    #     return
    globalVariables.dict_useless[field_ptr[0].text] = field_ptr[1].text
    if field_ptr[1].text in globalVariables.dict_name_id:
        if field_ptr[3].text == '1':
            globalVariables.list_dup_in_field.append(field_ptr[1].text)
    globalVariables.dict_name_id[field_ptr[1].text] = field_ptr[0].text
    # print(field_ptr[0].text)
    datatype = ''
    for children in field_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            if children.text != None:
                # print(children.text)
                # print("**********************************")
                # print(field_ptr[0].text)
                # print("**********************************")
                temp_list = children.text.split(';')
                for item in temp_list:
                    globalVariables.ip_count
                    globalVariables.ip_count = globalVariables.ip_count + 1
                    globalVariables.dict_field[globalVariables.ip_count] = field_ptr[1].text
                fo.write(children.text)
                fo.write('\n')

        if children.tag.split('}')[1] == 'ImplicitRuleDef':
            if children[0].tag.split('}')[1] == 'UseConstant':
                globalVariables.dict_ip_ct[field_ptr[0].text] = children[0][0].text
            if children[0].tag.split('}')[1] == 'UseSelect':
                fieldfrom = field_ptr[0].text
                tablename_temp = children[0][0].text.split()
                tablename = ' '.join(tablename_temp[-2:])
                subtable = children[0][1].text
                Mapfrom = children[0][3][0].text
                fieldto = children[0][3][1].text
                globalVariables.dict_ip_select[fieldto] = [tablename, subtable, Mapfrom, fieldfrom]
        if children.tag.split('}')[1] == "StoreLimit":
            for tags in children:
                if tags.tag.split('}')[1] == "DataType":
                    datatype = tags.text
            if datatype == 'numeric':
                datatype = 'integer'

    # exit()
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append('')
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(grp_name)
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(field_ptr[1].text)

    ### enter in globalVariables.dict_1 the record
    globalVariables.dict_1.setdefault(rec_id, []).append('')
    globalVariables.dict_1.setdefault(rec_id, []).append(grp_name)
    globalVariables.dict_1.setdefault(rec_id, []).append(field_ptr[1].text)

    field_ct_str = str(field_ct)
    if len(field_ct_str) == 1:
        field_ct_str = '0' + field_ct_str
    l = [grp_name, field_ct_str]
    globalVariables.dict_ind_field[field_ptr[1].text] = l
    globalVariables.dict_opposite[''.join(l)] = field_ptr[1].text
    name_field = ''.join(globalVariables.dict_ind_field[field_ptr[1].text])
    if not (xml_tag == '$$$' or xml_tag == 'XXX' or (name_field).split('_')[0] == 'TEMP'):
        #     print(xml_tag)
        # else:
        globalVariables.field_set.add(name_field)
        # print(xml_tag)
    globalVariables.dict_type[name_field] = datatype.lower()


def xml_record_func(rec_ptr, grp_name, field_ct, fo, xml_tag, globalVariables):
    rec_id = rec_ptr[0].text
    for children in rec_ptr:
        if children.tag.split('}')[1] == 'Field':
            xml_field_func(children, grp_name, field_ct, fo, xml_tag, rec_id, globalVariables)


def xml_particle_func(particle_ptr, grp_name, fo, globalVariables):
    field_ct = 1
    for children in particle_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            for categ in children:
                if categ.text != None:
                    temp_list = categ.text.split(';')
                    for item in temp_list:
                        globalVariables.ip_count = globalVariables.ip_count + 1
                        globalVariables.dict_field[globalVariables.ip_count] = particle_ptr[1].text
                    fo.write(categ.text)
                    fo.write('\n')
        if children.tag.split('}')[1] == "XMLParticleGroup":
            xml_particle_func(children, grp_name, fo, globalVariables)
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_group_func(children, grp_name, field_ct, fo, globalVariables)
            field_ct = field_ct + 1


def xml_group_func(group_ptr, grp_name, field_ct, fo, globalVariables):
    xml_tag = ''
    if globalVariables.inp_grp_name == '':
        globalVariables.inp_grp_name = group_ptr[1].text
    for children in group_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            for categ in children:
                if categ.text != None:
                    temp_list = categ.text.split(';')
                    for item in temp_list:
                        globalVariables.ip_count = globalVariables.ip_count + 1
                        globalVariables.dict_field[globalVariables.ip_count] = group_ptr[1].text
                    fo.write(categ.text)
                    fo.write('\n')
        if children.tag.split('}')[1] == "XMLTag":
            xml_tag = children.text
        if children.tag.split('}')[1] == "XMLParticleGroup":
            xml_particle_func(children, group_ptr[1].text, fo, globalVariables)
        if children.tag.split('}')[1] == "XMLRecord":
            xml_record_func(children, grp_name, field_ct, fo, xml_tag, globalVariables)
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_group_func(children, group_ptr[1].text, field_ct, fo, globalVariables)


def field_func(field_ptr, grp_name, seg_name, field_ct, field_tag, fo, globalVariables):
    if field_ptr[3].text == '0':
        return
    # from constants import count
    datatype = ''
    if field_ptr[1].text == 'ELEMENT_1':
        print("DAIODHW")
        print(seg_name)
        print(grp_name)
        # exit()
    globalVariables.dict_useless[field_ptr[0].text] = field_ptr[1].text
    if field_ptr[1].text in globalVariables.dict_name_id:
        if field_ptr[3].text == '1':
            globalVariables.list_dup_in_field.append(field_ptr[1].text)
    globalVariables.dict_name_id[field_ptr[1].text] = field_ptr[0].text
    for children in field_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            if children.text != None:
                temp_list = children.text.split(';')
                for item in temp_list:
                    globalVariables.ip_count = globalVariables.ip_count + 1
                    globalVariables.dict_field[globalVariables.ip_count] = field_ptr[1].text
                fo.write(children.text)
                fo.write('\n')

        if children.tag.split('}')[1] == "StoreLimit":
            for tags in children:
                if tags.tag.split('}')[1] == "DataType":
                    datatype = tags.text
            if datatype == 'numeric':
                datatype = 'integer'

        if children.tag.split('}')[1] == 'ImplicitRuleDef':
            if children[0].tag.split('}')[1] == 'UseConstant':
                rule = field_ptr[1].text + ' = ' + globalVariables.dict_constant[int(children[0][0].text)][2] + " ;"
                cond = ''
                if children[0][1].text != '-1':
                    cond = "If " + globalVariables.dict_1[children[0][1].text][2] + " exists "
                globalVariables.dict_token[field_ptr[1].text] = [['', cond, rule]]
                globalVariables.dict_ip_ct[field_ptr[0].text] = children[0][0].text
            if children[0].tag.split('}')[1] == "UseCode":
                print(children[0][1].text)
                print(globalVariables.dict_1)
                code_note = ''
                if children[0][2] == 'yes':
                    code_note += "Raise a compliance error if the code is not found in the list "
                if children[0][1].text in globalVariables.dict_1:
                    code_note += "Select codelist value from Table " + children[0][0].text + " where field value = " + \
                                 field_ptr[1].text + " and assign it to field " + \
                                 globalVariables.dict_1[children[0][1].text][2]
                    # globalVariables.dict_notes[field_ptr[1].text] = code_note
                    print(globalVariables.dict_1[children[0][1].text][2])
                    exit()
                    globalVariables.dict_token[globalVariables.dict_1[children[0][1].text][2]] = [
                        [[globalVariables.dict_1[children[0][1].text][2]], '', code_note]]
                # else:
                #     code_note += "Select codelist value from Table "+ children[0][0].text + " where field value = " +  field_ptr[1].text + " and assign it to field " +  field_ptr[1].text
                #     # globalVariables.dict_notes[field_ptr[1].text] = code_note
                #     globalVariables.dict_token[field_ptr[1].text]=[[[field_ptr[1].text],'',code_note]]

            if children[0].tag.split('}')[1] == 'UseSelect':
                fieldfrom = field_ptr[0].text
                tablename_temp = children[0][0].text.split()
                tablename = ' '.join(tablename_temp[-2:])
                subtable = children[0][1].text
                Mapfrom = children[0][3][0].text
                fieldto = children[0][3][1].text
                print([tablename, subtable, Mapfrom, fieldfrom])
                v = [tablename, subtable, Mapfrom, fieldfrom]
                print(v)
                print(globalVariables.dict_1)
                # exit()
                if fieldto in globalVariables.dict_1:
                    select_stmt = "Populate " + v[2] + " from CODELIST equal " + children[0][0].text + " into " + \
                                  globalVariables.dict_1[fieldto][2] + " where sendercode equals " + field_ptr[
                                      1].text + '\n'
                    dict_ip_select[fieldto] = [tablename, subtable, Mapfrom, fieldfrom]
                    globalVariables.dict_token[globalVariables.dict_1[fieldto][2]] = [
                        [globalVariables.dict_1[fieldto][2], '', select_stmt]]
                else:
                    select_stmt = "Populate " + v[2] + " from CODELIST equal " + children[0][0].text + " into " + \
                                  field_ptr[1].text + " where sendercode equals " + field_ptr[1].text + '\n'
                    dict_ip_select[fieldto] = [tablename, subtable, Mapfrom, fieldfrom]
                    globalVariables.dict_token[field_ptr[1].text] = [
                        [globalVariables.dict_1[fieldto][2], '', select_stmt]]

    # print(field_ptr[0].text)
    # exit()
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(grp_name)
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(seg_name)
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(field_ptr[1].text)
    if seg_name == '$$$':
        print(grp_name)
        print(seg_name)
        print(field_ptr[1].text)
    field_ct_str = str(field_ct)
    if len(field_ct_str) == 1:
        field_ct_str = '0' + field_ct_str
    # if seg_name.split('_')[0]=="TEMP":
    #     l=[seg_name,field_ct_str]
    # else:
    #     l=[field_tag,field_ct_str]
    l = [seg_name, field_ct_str]
    globalVariables.dict_ind_field[field_ptr[1].text] = l
    globalVariables.dict_opposite[''.join(l)] = field_ptr[1].text
    globalVariables.dict_tag_inp[''.join(l)] = [field_tag, field_ct_str]
    name_field = ''.join(globalVariables.dict_ind_field[field_ptr[1].text])
    # if not (field_tag=='$$$' or field_tag=='XXX' or (name_field).split('_')[0]=='TEMP'):
    # #     print(field_tag)
    # # else:
    #     globalVariables.field_set.add(name_field)
    # print(field_tag)
    if (field_tag == '$$$' or field_tag == 'XXX' or (name_field).split('_')[0] == 'TEMP'):
        print(field_tag)
        print((name_field).split('_')[0])
        # exit()
    else:
        globalVariables.field_set.add(name_field)
    globalVariables.dict_type[name_field] = datatype.lower()
    globalVariables.dict_opposite_group[''.join(l)] = grp_name


def seg_func(seg_ptr, grp_name, fo, comp_count, flag, globalVariables):
    # from constants import count
    i = 0
    field_ct = 1
    field_tag = ''
    for children in seg_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            for categ in children:
                if categ.text != None:
                    temp_list = categ.text.split(';')
                    for item in temp_list:
                        globalVariables.ip_count
                        globalVariables.ip_count = globalVariables.ip_count + 1
                        # for cc in seg_ptr:
                        #     if cc.tag.split('}')[1]=='BlockSig':
                        globalVariables.dict_field[globalVariables.ip_count] = seg_ptr[1].text
                    fo.write(categ.text)
                    fo.write('\n')
        if children.tag.split('}')[1] == 'BlockSig':
            field_tag = children[0].text

        if children.tag.split('}')[1] == "Composite":
            # print(children.tag)
            comp_count += 1
            print(children[0].text)
            if children[1].text in globalVariables.list_in_composite:
                globalVariables.list_dup_in_composite.append(children[1].text)
            else:
                globalVariables.list_in_composite.append(children[1].text)
            seg_func(children, seg_ptr[1].text, fo, comp_count, 1, globalVariables)
        elif children.tag.split('}')[1] == "Field":
            # print(children.tag)
            if flag == 0:
                field_func(children, grp_name, seg_ptr[1].text, field_ct, field_tag, fo, globalVariables)
            else:
                # field_func(children,grp_name,seg_ptr[1].text,field_ct,field_tag,fo,globalVariables)
                field_func(children, grp_name, 'Composite_' + grp_name + '_' + str(comp_count), field_ct, field_tag, fo,
                           globalVariables)
            field_ct = field_ct + 1


def group_func(group_ptr, fo, globalVariables):
    # from constants import count
    if globalVariables.inp_grp_name == '':  # store the head group name.. this part would run only once
        globalVariables.inp_grp_name = group_ptr[1].text
        print(globalVariables.inp_grp_name)
    for children in group_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            for categ in children:
                if categ.text != None:
                    temp_list = categ.text.split(';')
                    for item in temp_list:
                        globalVariables.ip_count
                        globalVariables.ip_count = globalVariables.ip_count + 1
                        globalVariables.dict_field[globalVariables.ip_count] = group_ptr[1].text
                    fo.write(categ.text)
                    fo.write('\n')

        if children.tag.split('}')[1] == "Group":
            # print(children.tag)
            comp_count = 0
            group_func(children, fo, globalVariables)
        elif children.tag.split('}')[1] == "Segment":
            # print(children.tag)
            comp_count = 0
            seg_func(children, group_ptr[1].text, fo, comp_count, 0, globalVariables)
        elif children.tag.split('}')[1] == "PosRecord":
            comp_count = 0
            seg_func(children, group_ptr[1].text, fo, comp_count, 0, globalVariables)
        elif children.tag.split('}')[1] == "VarDelimRecord":
            comp_count = 0
            seg_func(children, group_ptr[1].text, fo, comp_count, 0, globalVariables)


def xml_output_field_func(field_ptr, grp_name, field_op_ct, op_file, group_ptr, globalVariables):
    # group_ptr[5].text=''
    # if field_ptr[3].text=='0':
    #     return
    datatype = ''
    temp_id = field_ptr[0].text
    temp_des = field_ptr[2].text
    globalVariables.dict_notes[field_ptr[1].text] = ['', '', '', '', '', '']
    globalVariables.dict_useless[field_ptr[0].text] = field_ptr[1].text
    if field_ptr[1].text in globalVariables.dict_opposite_name_id:
        if field_ptr[3].text == '1':
            globalVariables.list_dup_out_field.append(field_ptr[1].text)

    globalVariables.dict_opposite_name_id[field_ptr[1].text] = field_ptr[0].text
    for children in field_ptr:
        if children.tag.split('}')[1] == "Link":
            print("SDSD")
            temp_ip = children.text
            if temp_ip in globalVariables.dict_1:
                globalVariables.link_notes_set.add(temp_id)
                link_list = globalVariables.dict_1[temp_ip]
                if (len(link_list) == 3 and link_list[0].split('_')[0].lower() != 'temp'
                        and link_list[1].split('_')[0].lower() != 'temp' and link_list[2].split('_')[
                            0].lower() != 'temp'):
                    name = link_list[2]
                    if name in globalVariables.dict_ind_field:
                        note = "Map " + (''.join(globalVariables.dict_ind_field[name]))
                        dollar = note.split()[1]
                        if dollar[1] == '$':
                            note = ''
                        # note="Map  "+link_list[0]+"/"+link_list[1]+"/"+link_list[2]
                        globalVariables.dict_notes[field_ptr[1].text][2] = note + '\n'
                        # print(note)
                        # exit()
                # if(len(link_list)==3 and (link_list[0].split('_')[0]=='TEMP'
                # or link_list[1].split('_')[0]=='TEMP' or link_list[2].split('_')[0]=='TEMP')):
                if len(link_list) == 3:
                    globalVariables.dict_op.setdefault(temp_id, []).append(globalVariables.dict_1[temp_ip][2])
                    globalVariables.dict_op.setdefault(temp_id, []).append(temp_des)
                # print(temp_id)
                # print(temp_des)

        if children.tag.split('}')[1] == "ExplicitRule":
            if children.text != None:
                print("output rule")
                print(children.text)
                temp_list = children.text.split(';')
                for item in temp_list:
                    globalVariables.op_count
                    globalVariables.op_count = globalVariables.op_count + 1
                    globalVariables.dict_op_field[globalVariables.op_count] = field_ptr[1].text
                op_file.write(children.text)
                op_file.write('\n')

        if children.tag.split('}')[1] == "StoreLimit":
            for tags in children:
                if tags.tag.split('}')[1] == "DataType":
                    datatype = tags.text
            if datatype == 'numeric':
                datatype = 'integer'

        if children.tag.split('}')[1] == 'ImplicitRuleDef':
            if children[0].tag.split('}')[1] == 'UseConstant':
                globalVariables.standard_notes_set.add(temp_id)
                cond = ''
                print(field_ptr[1].text)
                if children[0][1].text != '-1':
                    cond = children[0][1].text
                globalVariables.dict_op_ct[field_ptr[0].text] = [children[0][0].text, cond]
            acc_note = ''
            acc_flag = 0
            if children[0].tag.split('}')[1] == 'UseAccumulator':
                for child_child in children[0]:
                    acc_id = child_child[0].text
                    acc_flag = 0
                    for acc_child in child_child:
                        print(acc_child.text)
                        print(acc_child)
                        if acc_child.text == 'Increment primary':
                            acc_note += " increment the value of accumulator " + acc_id + " and " + " use the value of accumulator " + acc_id
                            acc_flag = 1
                        if acc_child.text == 'Use primary' and acc_flag == 0:
                            if acc_id in globalVariables.dict_sum:
                                acc_note = "Sum of values in the fields " + ' '.join(globalVariables.dict_sum[acc_id])
                            else:
                                acc_note += " Use the value of accumulator " + acc_id
                        if acc_child.text == 'Zero primary':
                            acc_note += "Make value of acuumulator " + acc_id + "zero"
                        if acc_child.text == 'Multiply with primary':
                            acc_note += 'Map multiply acuumulator ' + acc_id + " with value of " + field_ptr[1].text
                        if acc_child.text == 'Divide by primary':
                            acc_note += "Map value of accumulator " + acc_id + " divided by value of " + field_ptr[
                                1].text
                        if acc_child.text == 'Divide primary by field':
                            acc_note += 'Map value of ' + field_ptr[
                                1].text + " divided by value of accumulator " + acc_id
                        if acc_child.text == 'Modulo with primary':
                            acc_note += 'Map remainder of accumulator ' + acc_id + " divided by value of " + field_ptr[
                                1].text
                        if acc_child.text == 'Modulo with field':
                            acc_note += 'Map remainder of ' + field_ptr[
                                1].text + " divided by value of accumulator " + acc_id
                        if acc_child.text == 'Laod Primary':
                            acc_note += "Load contents of the field " + field_ptr[
                                1].text + " into accumulator " + acc_id
                        if acc_child.text == 'Move primary to alternate':
                            acc_note += ' Move accumulator ' + acc_id + ' value to '
                        if acc_child.text == 'Sum in primary':
                            l = [field_ptr[1].text]
                            if acc_id in globalVariables.dict_sum:
                                globalVariables.dict_sum[acc_id].append(l)
                            else:
                                globalVariables.dict_sum[acc_id] = l
                        if acc_child.tag.split('}')[1] == 'AccumulatorAlternate':
                            acc_note += " Accumulator " + acc_child.text
                            print(acc_note)
                        globalVariables.dict_notes[field_ptr[1].text][4] = acc_note
                globalVariables.standard_notes_set.add(temp_id)
            loop_note = ''
            if children[0].tag.split('}')[1] == 'UseLoopCount':
                loop_note = "Map number of times " + group_name + " repeats "
                print(loop_note)
            code_note = ''
            if children[0].tag.split('}')[1] == "UseCode":
                code_note = ""
                if children[0][2] == 'yes':
                    code_note += "Raise a compliance error if the code is not found in the list "
                code_note = "Select codelist value from Table " + children[0][0].text + " where field value = " + \
                            field_ptr[1].text + " and assign it to field " + children[0][1].text
                globalVariables.dict_notes[field_ptr[1].text][1] = code_note
            if children[0].tag.split('}')[1] == 'UseSelect':
                fieldfrom = field_ptr[0].text
                tablename_temp = children[0][0].text.split()
                tablename = ' '.join(tablename_temp[-2:])
                subtable = children[0][1].text
                Mapfrom = children[0][3][0].text
                fieldto = children[0][3][1].text
                globalVariables.dict_op_select[fieldto] = [tablename, subtable, Mapfrom, fieldfrom]
                globalVariables.standard_notes_set.add(fieldto)
            if children[0].tag.split('}')[1] == 'UseSystemVariable':
                datatype = ''
                format = ''
                for items in field_ptr[12]:
                    if items.tag.split('}')[1] == 'DataType':
                        datatype = items.text
                    if items.tag.split('}')[1] == 'Format':
                        format = items.text
                globalVariables.dict_op_date[field_ptr[0].text] = [datatype, format]
                globalVariables.standard_notes_set.add(temp_id)

    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append('')
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(grp_name)
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(field_ptr[1].text)

    field_ct_str = str(field_op_ct)
    if len(field_ct_str) == 1:
        field_ct_str = '0' + field_ct_str
    l = [grp_name, field_ct_str]
    globalVariables.dict_ind_field[field_ptr[1].text] = l
    globalVariables.dict_opposite_out[''.join(l)] = field_ptr[1].text
    name_field = field_ptr[1].text
    name = ''.join(globalVariables.dict_ind_field[name_field])
    globalVariables.field_set.add(name)
    globalVariables.dict_type[''.join(l)] = datatype.lower()


def xml_output_record_func(rec_ptr, grp_name, field_op_ct, op_file, group_ptr, globalVariables):
    for children in rec_ptr:
        if children.tag.split('}')[1] == 'Field':
            xml_output_field_func(children, grp_name, field_op_ct, op_file, group_ptr, globalVariables)


def xml_output_particle_func(particle_ptr, grp_name, op_file, globalVariables):
    field_op_ct = 1
    for children in particle_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            for categ in children:
                if categ.text != None:
                    temp_list = categ.text.split(';')
                    for item in temp_list:
                        globalVariables.op_count
                        globalVariables.op_count = globalVariables.op_count + 1
                        globalVariables.dict_op_field[globalVariables.op_count] = particle_ptr[1].text
                    op_file.write(categ.text)
                    op_file.write('\n')
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_func(children, grp_name, field_op_ct, op_file, globalVariables)
            field_op_ct = field_op_ct + 1
        if children.tag.split('}')[1] == "XMLParticleGroup":
            xml_output_particle_func(children, grp_name, op_file, globalVariables)


def xml_output_group_func(group_ptr, grp_name, field_ct, op_file, globalVariables):
    if globalVariables.out_grp_name == '':
        globalVariables.out_grp_name = group_ptr[1].text
    for children in group_ptr:
        if children.tag.split('}')[1] == "ExplicitRule":
            for categ in children:
                if categ.text != None:
                    temp_list = categ.text.split(';')
                    for item in temp_list:
                        globalVariables.op_count
                        globalVariables.op_count = globalVariables.op_count + 1
                        globalVariables.dict_op_field[globalVariables.op_count] = group_ptr[1].text
                    op_file.write(categ.text)
                    op_file.write('\n')
        if children.tag.split('}')[1] == "XMLParticleGroup":
            name = children[1].text
            ct_loop = children[7].text
            globalVariables.dict_seg_loop[name] = ct_loop
            xml_output_particle_func(children, group_ptr[1].text, op_file, globalVariables)
        if children.tag.split('}')[1] == "XMLRecord":
            name = children[1].text
            ct_loop = children[7].text
            globalVariables.dict_seg_loop[name] = ct_loop
            xml_output_record_func(children, grp_name, field_ct, op_file, group_ptr, globalVariables)
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_func(children, group_ptr[1].text, field_ct, op_file, globalVariables)


def output_field(group_name, field_ptr, seg_name, field_tag, field_op_ct, op_file, name, ct_loop, globalVariables):
    # field_ptr[5].text = ''
    if field_ptr[3].text == '0':
        return
    datatype = ''
    temp_id = field_ptr[0].text
    temp_des = field_ptr[2].text
    globalVariables.dict_notes[field_ptr[1].text] = ['', '', '', '', '', '']
    globalVariables.dict_useless[field_ptr[0].text] = field_ptr[1].text
    if field_ptr[1].text in globalVariables.dict_opposite_name_id:
        if field_ptr[1].text == '1':
            globalVariables.list_dup_out_field.append(field_ptr[1].text)

    globalVariables.dict_opposite_name_id[field_ptr[1].text] = field_ptr[0].text
    # globalVariables.dict_1.setdefault(field_ptr[0].text, []).append('')
    # globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(seg_name)
    # globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(field_ptr[1].text)
    for child in field_ptr:
        if child.tag.split('}')[1] == "Link":
            temp_ip = child.text
            if temp_ip in globalVariables.dict_1:
                globalVariables.link_notes_set.add(temp_id)
                link_list = globalVariables.dict_1[temp_ip]
                print("DS2")
                print(link_list)
                if (len(link_list) == 3 and link_list[0].split('_')[0].lower() != 'temp'
                        and link_list[1].split('_')[0].lower() != 'temp' and link_list[2].split('_')[
                            0].lower() != 'temp'):
                    name_name = link_list[2]
                    if name_name in globalVariables.dict_ind_field:
                        note = "Map  " + (''.join(globalVariables.dict_ind_field[name_name]))
                        dollar = note.split()[1]
                        if dollar[1] == '$':
                            note = ''
                        # note="Map  "+link_list[0]+"/"+link_list[1]+"/"+link_list[2]
                        globalVariables.dict_notes[field_ptr[1].text][2] = note + '\n'
                # if(len(link_list)==3 and (link_list[0].split('_')[0]=='TEMP'
                # or link_list[1].split('_')[0]=='TEMP' or link_list[2].split('_')[0]=='TEMP')):
                if len(link_list) == 3:
                    globalVariables.dict_op.setdefault(temp_id, []).append(globalVariables.dict_1[temp_ip][2])
                    globalVariables.dict_op.setdefault(temp_id, []).append(temp_des)

        if child.tag.split('}')[1] == "ExplicitRule":
            if child.text != None:
                temp_list = child.text.split(';')
                for item in temp_list:
                    globalVariables.op_count
                    globalVariables.op_count = globalVariables.op_count + 1
                    globalVariables.dict_op_field[globalVariables.op_count] = field_ptr[1].text
                op_file.write(child.text)
                op_file.write('\n')

        if child.tag.split('}')[1] == "StoreLimit":
            for tags in child:
                if tags.tag.split('}')[1] == "DataType":
                    datatype = tags.text
            if datatype == 'numeric':
                datatype = 'integer'

        if child.tag.split('}')[1] == 'ImplicitRuleDef':
            if child[0].tag.split('}')[1] == 'UseConstant':
                globalVariables.standard_notes_set.add(temp_id)
                cond = ''
                print(field_ptr[1].text)
                if child[0][1].text != '-1':
                    cond = child[0][1].text
                globalVariables.dict_op_ct[field_ptr[0].text] = [child[0][0].text, cond]
            acc_note = ''
            acc_flag = 0
            if child[0].tag.split('}')[1] == 'UseAccumulator':
                for child_child in child[0]:
                    acc_id = child_child[0].text
                    acc_flag = 0
                    for acc_child in child_child:
                        print(acc_child.text)
                        print(acc_child)
                        if acc_child.text == 'Increment primary':
                            acc_note += " increment the value of accumulator " + acc_id + " and " + " use the value of accumulator " + acc_id
                            acc_flag = 1
                        if acc_child.text == 'Use primary' and acc_flag == 0:
                            if acc_id in globalVariables.dict_sum:
                                acc_note = "Sum of values in the fields " + ' '.join(globalVariables.dict_sum[acc_id])
                            else:
                                acc_note += " Use the value of accumulator " + acc_id
                        if acc_child.text == 'Zero primary':
                            acc_note += "Make value of acuumulator " + acc_id + "zero"
                        if acc_child.text == 'Multiply with primary':
                            acc_note += 'Map multiply acuumulator ' + acc_id + " with value of " + field_ptr[1].text
                        if acc_child.text == 'Divide by primary':
                            acc_note += "Map value of accumulator " + acc_id + " divided by value of " + field_ptr[
                                1].text
                        if acc_child.text == 'Divide primary by field':
                            acc_note += 'Map value of ' + field_ptr[
                                1].text + " divided by value of accumulator " + acc_id
                        if acc_child.text == 'Modulo with primary':
                            acc_note += 'Map remainder of accumulator ' + acc_id + " divided by value of " + field_ptr[
                                1].text
                        if acc_child.text == 'Modulo with field':
                            acc_note += 'Map remainder of ' + field_ptr[
                                1].text + " divided by value of accumulator " + acc_id
                        if acc_child.text == 'Laod Primary':
                            acc_note += "Load contents of the field " + field_ptr[
                                1].text + " into accumulator " + acc_id
                        if acc_child.text == 'Move primary to alternate':
                            acc_note += ' Move accumulator ' + acc_id + ' value to '
                        if acc_child.text == 'Sum in primary':
                            l = [field_ptr[1].text]
                            if acc_id in globalVariables.dict_sum:
                                globalVariables.dict_sum[acc_id].append(l)
                            else:
                                globalVariables.dict_sum[acc_id] = l
                        if acc_child.tag.split('}')[1] == 'AccumulatorAlternate':
                            acc_note += " Accumulator " + acc_child.text
                            print(acc_note)
                        globalVariables.dict_notes[field_ptr[1].text][4] = acc_note
                globalVariables.standard_notes_set.add(temp_id)
            loop_note = ''
            if child[0].tag.split('}')[1] == 'UseLoopCount':
                loop_note = "Map number of times " + group_name + " repeats "
                print(loop_note)
            code_note = ''
            if child[0].tag.split('}')[1] == "UseCode":
                code_note = ""
                if child[0][2] == 'yes':
                    code_note += "Raise a compliance error if the code is not found in the list "
                code_note = "Select codelist value from Table " + child[0][0].text + " where field value = " + \
                            field_ptr[1].text + " and assign it to field " + child[0][1].text
                globalVariables.dict_notes[field_ptr[1].text][1] = code_note
            if child[0].tag.split('}')[1] == 'UseSelect':
                fieldfrom = field_ptr[0].text
                tablename_temp = child[0][0].text.split()
                tablename = ' '.join(tablename_temp[-2:])
                subtable = child[0][1].text
                Mapfrom = child[0][3][0].text
                fieldto = child[0][3][1].text
                globalVariables.dict_op_select[fieldto] = [tablename, subtable, Mapfrom, fieldfrom]
                globalVariables.standard_notes_set.add(fieldto)
            if child[0].tag.split('}')[1] == 'UseSystemVariable':
                datatype = ''
                format = ''
                for items in field_ptr[12]:
                    if items.tag.split('}')[1] == 'DataType':
                        datatype = items.text
                    if items.tag.split('}')[1] == 'Format':
                        format = items.text
                globalVariables.dict_op_date[field_ptr[0].text] = [datatype, format]
                globalVariables.standard_notes_set.add(temp_id)

    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append('')
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(seg_name)
    globalVariables.dict_1.setdefault(field_ptr[0].text, []).append(field_ptr[1].text)

    field_ct_str = str(field_op_ct)
    if len(field_ct_str) == 1:
        field_ct_str = '0' + field_ct_str
    l = [seg_name, field_ct_str]
    globalVariables.dict_ind_field[field_ptr[1].text] = l
    # print(l)
    globalVariables.dict_opposite_out[''.join(l)] = field_ptr[1].text
    name_field = field_ptr[1].text
    name = ''.join(globalVariables.dict_ind_field[name_field])
    globalVariables.field_set.add(name)
    globalVariables.dict_tag_out[''.join(l)] = [field_tag, field_ct_str]
    globalVariables.dict_type[''.join(l)] = datatype.lower()
    globalVariables.dict_opposite_group_out[''.join(l)] = group_name


def output_seg(group_name, seg_ptr, op_file, name, ct_loop, comp_count, flag, globalVariables):
    field_op_ct = 1
    field_tag = ''
    for children in seg_ptr:
        if children.tag.split('}')[1] == "Composite":
            if children[1].text in globalVariables.list_out_composite:
                globalVariables.list_dup_out_composite.append(children[1].text)
            else:
                globalVariables.list_out_composite.append(children[1].text)
            comp_count += 1
            output_seg(seg_ptr[1].text, children, op_file, name, ct_loop, comp_count, 1, globalVariables)
        if children.tag.split('}')[1] == 'BlockSig':
            field_tag = children[0].text
        elif children.tag.split('}')[1] == "Field":
            if flag == 0:
                output_field(group_name, children, seg_ptr[1].text, field_tag, field_op_ct, op_file, name, ct_loop,
                             globalVariables)
            else:
                output_field(group_name, children, 'Composite' + str(comp_count), field_tag, field_op_ct, op_file, name,
                             ct_loop, globalVariables)
            field_op_ct = field_op_ct + 1


def output_group(group_ptr, op_file, globalVariables):
    group_name = group_ptr[1].text
    if globalVariables.out_grp_name == '':  # saving the head group name
        globalVariables.out_grp_name = group_ptr[1].text  # will do this only the first time this function runs
        print(globalVariables.out_grp_name)
    for children in group_ptr:
        if children.tag.split('}')[1] == "Group":
            group_name = children[1].text
            print(group_name)
            output_group(children, op_file, globalVariables)
        elif children.tag.split('}')[1] == "Segment":
            name = children[1].text
            ct_loop = children[7].text
            globalVariables.dict_seg_loop[name] = ct_loop
            comp_count = 0
            output_seg(group_name, children, op_file, name, ct_loop, comp_count, 0, globalVariables)

        elif children.tag.split('}')[1] == "PosRecord":
            name = children[1].text
            ct_loop = children[7].text
            globalVariables.dict_seg_loop[name] = ct_loop
            comp_count = 0
            output_seg(group_name, children, op_file, name, ct_loop, comp_count, 0, globalVariables)
        elif children.tag.split('}')[1] == "VarDelimRecord":
            name = children[1].text
            ct_loop = children[7].text
            globalVariables.dict_seg_loop[name] = ct_loop
            comp_count = 0
            output_seg(group_name, children, op_file, name, ct_loop, comp_count, 0, globalVariables)


def xml_initialize_dict(data_root, fo, globalVariables):
    for child in data_root[3][0]:
        if child.tag.split('}')[1] == "XMLElementGroup":
            xml_group_func(child, child[1].text, 0, fo, globalVariables)


def edi_initialize_dict(data_root, fo, globalVariables):
    for child in data_root[3][0]:
        if child.tag.split('}')[1] == "Group":
            group_func(child, fo, globalVariables)


def xml_initialize_output_dict(data_root, op_file, globalVariables):
    for child in data_root[4][0]:
        if child.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_func(child, child[1].text, 0, op_file, globalVariables)


def edi_initialize_output_dict(data_root, op_file, globalVariables):
    for child in data_root[4][0]:
        if child.tag.split('}')[1] == "Group":
            output_group(child, op_file, globalVariables)


def initialize_variable_set(data_root, fo, globalVariables):
    print("dkfjdk")
    for children in data_root[0]:
        # print(children.tag.split('}'))
        if children.tag.split('}')[1] == 'ExplicitRule':
            print("exp")
            for tags in children:
                print(tags.tag)
                globalVariables.ip_count
                if tags.tag != '' and tags.tag.split('}')[1] == 'PreSessionRule':
                    if tags.text != '':
                        temp_list = tags.text.split(';')
                        for item in temp_list:
                            globalVariables.ip_count = globalVariables.ip_count + 1
                            globalVariables.dict_field[globalVariables.ip_count] = 'PRE_SESSION'
                        fo.write(tags.text)
                        fo.write('\n')
                if tags.tag != '' and tags.tag.split('}')[1] == 'PostSessionRule':
                    print("yo")
                    print(tags.text)
                    if not tags.text and not tags.text is None:
                        print("oyoo")
                        temp_list = tags.text.split(';')
                        for item in temp_list:
                            globalVariables.ip_count = globalVariables.ip_count + 1
                            globalVariables.dict_field[globalVariables.ip_count] = 'POST_SESSION'
                        fo.write(tags.text)
                        fo.write('\n')


### def grammar(rule):
INT = CaselessKeyword("integer")
STR = CaselessKeyword("string")
OBJECT = CaselessKeyword("object")
if_key = CaselessKeyword("if")
then_key = CaselessKeyword("then")
begin_key = CaselessKeyword("begin")
end_key = CaselessKeyword("end")
else_key = CaselessKeyword("else")
years = CaselessKeyword("years")
months = CaselessKeyword("months")
weeks = CaselessKeyword("weeks")
days = CaselessKeyword("days")
hours = CaselessKeyword("hours")
minutes = CaselessKeyword("minutes")
seconds = CaselessKeyword("seconds")
else_if = CaselessKeyword("else if")
while_key = CaselessKeyword('while')
semicol = Literal(';')
comma = Literal(',')
mul = Literal("*")
div = Literal("/")
plus = Literal('+')
equal = Literal('=').setResultsName('EQUALS')
not_equal = Literal('!=')
greater = Literal('>')
less = Literal('<')
greater_equal = Literal('>=')
less_equal = Literal('<=')
and_key = Literal('&')
or_key = Literal('|')
percent = Literal('%')
left_shift = Literal('<<')
right_shift = Literal('>>')
minus = Literal('-')
expression = Forward()
expression_without_ref = Forward()
arr_exp = ZeroOrMore(Literal('[') + expression_without_ref + Literal(']'))
variable = Word(alphanums + '_' + ':') + Optional(arr_exp)
variable_num = Word(alphanums + '_' + ':').setResultsName('NUM') + Optional(arr_exp)
variable_ref = Word(alphanums + '_' + ':').setResultsName('REF') + Optional(arr_exp)
variable_var = Word(alphanums + '_' + ':').setResultsName('VARIABLES') + Optional(arr_exp)
variable_upd = Word(alphanums + '_' + ':').setResultsName('UPDATE') + Optional(arr_exp)
variable_str = Word(alphanums + '_' + ':').setResultsName('STRING') + Optional(arr_exp)
string = STR + Literal('[') + Word(nums) + Literal(']')
identifier = variable_var + ZeroOrMore(comma + variable_var)
real = CaselessKeyword("real")
DateTime = CaselessKeyword("datetime")
var_type = INT | string | OBJECT | real | DateTime
declare_stmt = var_type.setResultsName('VARTYPE') + identifier + semicol
field_name_up = (ZeroOrMore(Literal('$') + variable + arr_exp + Literal('.')) + Literal('#') + variable_upd + arr_exp)
field_name = (ZeroOrMore(Literal('$') + variable + arr_exp + Literal('.')) + Literal('#') + variable_ref + arr_exp)
field_name_wo = (ZeroOrMore(Literal('$') + variable + arr_exp + Literal('.')) + Literal('#') + variable + arr_exp)
str_var = ((Literal('"') | Literal("'")) + Word(
    alphanums + '' + " " + "_" + "\\" + "|" + "/" + '%' + '$' + "#" + "-" + "." + ":" + "=" + ')' + '(' + "*" + "<" + ">" + '^' + "'" + "+" + "," + "?").setResultsName(
    'STRING') + (Literal('"') | Literal("'"))) | (Literal('"') + Literal('"')) | Literal("'") + Literal("'")
str_var_ref = (Literal('"') | Literal("'")) + Word(
    alphanums + '' + " " + "_" + "\\" + "|" + "/" + '%' + '$' + "#" + "-" + "." + ":" + '(' + ')' + "=" + "*" + "<" + ">" + '^' + "'" + "+" + "," + "?").setResultsName(
    'REF') + (Literal('"') | Literal("'")) | (Literal('"') + Literal('"')) | Literal("'") + Literal("'")
str_var_format = (Literal('"') | Literal("'")) + Word(
    alphanums + '' + ' ' + "_" + "\\" + "|" + "/" + '%' + '$' + "#" + "-" + "." + ":" + "=" + "*" + '(' + ')' + "<" + ">" + '^' + "'" + "+" + "," + "?").setResultsName(
    'FORMAT') + (Literal('"') | Literal("'")) | (Literal('"') + Literal('"')) | Literal("'") + Literal("'")
str_var_up = (Literal('"') | Literal("'")) + Word(
    alphanums + '' + ' ' + "_" + "\\" + "|" + "/" + '%' + '$' + "#" + "-" + "." + ":" + "=" + "*" + '(' + ')' + "<" + ">" + '^' + "'" + "+" + "," + "?").setResultsName(
    'UPDATE') + (Literal('"') | Literal("'")) | (Literal('"') + Literal('"')) | Literal("'") + Literal("'")
group_name = Literal('$') + variable_ref
grp_name_with_arr = Literal('$') + variable_ref + arr_exp
grp_name_upd = Literal('$') + variable_upd + arr_exp

func_type = Forward()
collate = CaselessKeyword("collate") + ZeroOrMore(Literal('(')) + grp_name_with_arr + ZeroOrMore(
    comma + field_name_wo) + comma + grp_name_with_arr + ZeroOrMore(
    comma + field_name_wo) + comma + grp_name_upd + ZeroOrMore(Literal(')'))
get = CaselessKeyword("get") + (years | months | weeks | days | hours | minutes | seconds) + ZeroOrMore(
    Literal('(')) + (field_name | str_var_ref | variable_ref) + ZeroOrMore(Literal(')'))
getcurrloc = CaselessKeyword("getcurrentlocationindex") + ZeroOrMore(Literal('(')) + ZeroOrMore(Literal(')'))
index = CaselessKeyword("index") + ZeroOrMore(Literal('(')) + (
            field_name | variable_ref | Word(nums).setResultsName('REF')) + ZeroOrMore(Literal(')'))
numerrors = CaselessKeyword("numerrors") + ZeroOrMore(Literal('(')) + ZeroOrMore(Literal(')'))
occurrencetot = CaselessKeyword("occurrencetotal") + ZeroOrMore(Literal('(')) + (
            field_name | str_var_ref | variable_ref) + ZeroOrMore(Literal(')'))
readblock = CaselessKeyword("readblock") + ZeroOrMore(Literal('(')) + (
            field_name | str_var_ref | variable_ref) + ZeroOrMore(Literal(')'))
writeblock = CaselessKeyword("writeblock") + ZeroOrMore(Literal('(')) + (
            field_name | str_var_ref | variable_ref) + ZeroOrMore(Literal(')'))
unreadblock = CaselessKeyword("unreadblock") + ZeroOrMore(Literal('(')) + ZeroOrMore(Literal(')'))
next_int = variable + Literal('.') + CaselessKeyword("nextint") + Literal('(') + Literal(')')
set_scale = CaselessKeyword("setScale") + Literal('(') + (Word(nums) | variable | str_var) + ZeroOrMore(
    comma + (Word(nums) | variable | str_var)) + Literal(')')
format = variable + Literal('.') + CaselessKeyword("format") + Literal('(') + variable + Literal(')')
messagebox = CaselessKeyword('messagebox') + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | field_name | str_var) + ZeroOrMore(
    comma + (Word(nums) | expression | variable_ref | field_name | str_var)) + ZeroOrMore(Literal(')'))
sort = CaselessKeyword('sort') + ZeroOrMore(Literal('(')) + group_name.setResultsName(
    'GROUP') + arr_exp + comma + field_name + ZeroOrMore(comma + field_name) + ZeroOrMore(Literal(')'))
cerror = CaselessKeyword("cerror") + ZeroOrMore(Literal('(')) + Word(nums) + comma + (
            field_name | str_var | variable) + Optional(comma + (str_var | variable)) + ZeroOrMore(Literal(')'))
trimleft = CaselessKeyword("trimleft") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | field_name | str_var) + Optional(
    comma + (expression | (Word(nums).setResultsName('NUM')) | (str_var) | variable)) + ZeroOrMore(Literal(')'))
trimright = CaselessKeyword("trimright") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | field_name | str_var) + Optional(
    comma + (expression | (Word(nums).setResultsName('NUM')) | (str_var) | variable)) + ZeroOrMore(Literal(')'))
count = CaselessKeyword("count") + ZeroOrMore(Literal('(')) + group_name + arr_exp + Literal('[') + (
            Literal('*') | Literal('&')) + Literal(']') + ZeroOrMore(Literal(')'))
aton = CaselessKeyword("aton") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | str_var | field_name) + ZeroOrMore(Literal(')'))
eof = CaselessKeyword("eof") + ZeroOrMore(Literal('(')) + Literal('0') + ZeroOrMore(Literal(')'))
sum = CaselessKeyword("sum") + ZeroOrMore(Literal('(')) + ZeroOrMore(str_var) + ZeroOrMore(Literal(')'))
trim = CaselessKeyword("trim") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | str_var | field_name) + Optional(
    comma + (expression | variable_str | str_var | field_name)) + ZeroOrMore(Literal(')'))
strstr = CaselessKeyword("strstr") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | field_name | str_var) + comma + (
                     expression | variable | field_name_up | str_var) + ZeroOrMore(Literal(')'))
ntoa = CaselessKeyword("ntoa") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | str_var | field_name) + comma + (variable_upd | field_name_up) + ZeroOrMore(
    Literal(')'))
atoi = CaselessKeyword("atoi") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | str_var | field_name) + ZeroOrMore(Literal(')'))
func_exp = variable + plus + Word(nums)
# mid = CaselessKeyword("mid") + ZeroOrMore(Literal('(')) + (variable_ref|expression|field_name|str_var) + comma + (Word(nums)|expression|variable).setResultsName('START') + comma + (Word(nums)|expression|variable).setResultsName('END') + ZeroOrMore(Literal(')'))
mid = CaselessKeyword("mid") + ZeroOrMore(Literal('(')) + (variable_ref | expression | field_name | str_var) + comma + (
            Word(nums) | expression | variable).setResultsName('START') + comma + (
                  Word(nums) | expression | variable).setResultsName('END') + ZeroOrMore(Literal(')'))
left = CaselessKeyword("left") + ZeroOrMore(Literal('(')) + (
            expression | variable_ref | field_name | str_var) + comma + (
                   (Word(nums).setResultsName('NUM')) | expression | (str_var) | variable) + ZeroOrMore(Literal(')'))
right = CaselessKeyword("right") + ZeroOrMore(Literal('(')) + (
(variable_ref | expression | field_name | str_var)) + comma + (
                    (Word(nums).setResultsName('NUM')) | expression | (str_var) | variable) + ZeroOrMore(Literal(')'))
date = (CaselessKeyword("date") + ZeroOrMore(Literal('(')) + (str_var_format | (Word(nums))) + ZeroOrMore(
    comma + (func_type | str_var | field_name | variable_ref | (Word(nums)))) + ZeroOrMore(Literal(')')))
strdate = CaselessKeyword("strdate") + ZeroOrMore(Literal('(')) + (
            variable_ref | str_var | field_name) + comma + str_var_format + comma + (
                      field_name_up | variable_upd) + ZeroOrMore(Literal(')'))
new = CaselessKeyword("new") + ZeroOrMore(Literal('(')) + (str_var | field_name | variable) + (
    ZeroOrMore(comma + (str_var | field_name | variable))) + Literal(")")
accum = CaselessKeyword("accum") + ZeroOrMore(Literal('(')) + Word(nums) + ZeroOrMore(Literal(')'))
concat = CaselessKeyword("concat") + ZeroOrMore(Literal('(')) + (field_name_up | variable_upd) + comma + (
            field_name | str_var_ref | variable_ref) + comma + (
                     Word(nums).setResultsName('NUM') | variable_num) + ZeroOrMore(Literal(')'))
delete = CaselessKeyword("delete") + ZeroOrMore(Literal('(')) + (
            field_name | variable | grp_name_with_arr) + ZeroOrMore(Literal(')'))
years_func = CaselessKeyword("years") + ZeroOrMore(Literal('(')) + (
            expression | field_name | variable_ref | str_var_ref | Word(nums + '-').setResultsName('REF')) + ZeroOrMore(
    Literal(')'))
months_func = CaselessKeyword("months") + ZeroOrMore(Literal('(')) + (
            expression | field_name | variable_ref | str_var_ref | Word(nums + '-').setResultsName('REF')) + ZeroOrMore(
    Literal(')'))
weeks_func = CaselessKeyword("weeks") + ZeroOrMore(Literal('(')) + (
            expression | field_name | variable_ref | str_var_ref | Word(nums + '-').setResultsName('REF')) + ZeroOrMore(
    Literal(')'))
days_func = CaselessKeyword("days") + ZeroOrMore(Literal('(')) + (
            expression | field_name | variable_ref | str_var_ref | Word(nums + '-').setResultsName('REF')) + ZeroOrMore(
    Literal(')'))
hours_func = CaselessKeyword("hours") + ZeroOrMore(Literal('(')) + (
            expression | field_name | variable_ref | str_var_ref | Word(nums + '-').setResultsName('REF')) + ZeroOrMore(
    Literal(')'))
minutes_func = CaselessKeyword("minutes") + ZeroOrMore(Literal('(')) + (
            expression | field_name | variable_ref | str_var_ref | Word(nums + '-').setResultsName('REF')) + ZeroOrMore(
    Literal(')'))
seconds_func = CaselessKeyword("seconds") + ZeroOrMore(Literal('(')) + (
            expression | field_name | variable_ref | str_var_ref | expression | Word(nums + '-').setResultsName(
        'REF')) + ZeroOrMore(Literal(')'))
length_str = CaselessKeyword("len") + ZeroOrMore(Literal('(')) + (
            expression | str_var | field_name | variable_ref) + ZeroOrMore(Literal(')'))
exist = CaselessKeyword("exist") + ZeroOrMore(Literal('(')) + (variable_ref | field_name) + ZeroOrMore(Literal(')'))
empty = CaselessKeyword("empty") + ZeroOrMore(Literal('(')) + (field_name_up | variable) + ZeroOrMore(Literal(')'))
set_func = CaselessKeyword("set") + (years | months | weeks | days | hours | minutes | seconds) + ZeroOrMore(
    Literal('(')) + (field_name_up | variable_upd) + comma + (
                       field_name | variable_ref | str_var | Word(nums)) + ZeroOrMore(Literal(')'))
func_type << Optional(Literal('!')) + (
            atoi | ntoa | mid | left | right | date | strdate | years_func | months_func | weeks_func | days_func | hours_func | minutes_func | seconds_func | new | concat | delete | set_func | aton | exist | count | trim | eof | sum | strstr | length_str | trimleft | accum | trimright | sort | cerror | empty | messagebox | collate | get | getcurrloc | index | numerrors | occurrencetot | readblock | writeblock | unreadblock)
# expression << (next_int|format|func_type|variable_ref|Word(nums+"-").setResultsName('REF')|field_name|str_var_ref)+ZeroOrMore((plus|mul|div|left_shift|right_shift|Literal('.')|minus)+ (next_int|format|func_type|set_scale|variable_ref|Word(nums+"-").setResultsName('REF')|field_name|str_var_ref))
expression << ZeroOrMore('(') + (next_int | format | func_type | variable_ref | Word(nums + "-").setResultsName(
    'REF') | field_name | str_var_ref) + ZeroOrMore(Literal('(')) + ZeroOrMore(
    (plus | mul | div | left_shift | right_shift | Literal('.') | minus) + ZeroOrMore(Literal('(')) + (
                next_int | format | func_type | set_scale | variable_ref | Word(nums + "-").setResultsName(
            'REF') | field_name | str_var_ref) + ZeroOrMore(Literal(')'))) + ZeroOrMore(Literal(')'))
expression_without_ref << ZeroOrMore('(') + (
            func_type | variable | Word(nums + "-") | field_name_wo | str_var) + ZeroOrMore(Literal('(')) + ZeroOrMore(
    (plus | mul | div | left_shift | right_shift | Literal('.') | minus) + ZeroOrMore(Literal('(')) + (
                func_type | set_scale | variable | Word(nums + "-") | field_name_wo | str_var) + ZeroOrMore(
        Literal(')'))) + ZeroOrMore(Literal(')'))
# expression << format
var_assign = variable_upd + Literal('=') + ZeroOrMore('(') + expression + ZeroOrMore(')') + semicol
field_assign = field_name_up + equal + expression + semicol
operator = (Literal(
    '=') | not_equal | less_equal | greater_equal | greater | less | greater_equal | minus).setResultsName('OPERATOR')
join_op = ((and_key | or_key | CaselessKeyword("and") | CaselessKeyword("or"))).setResultsName('JOIN_OP')
# condition = (func_type + operator + (func_type|variable.setResultsName('UPDATE')|Word(nums+"-"+'.').setResultsName('UPDATE')|field_name_up|str_var_up))|((variable_ref|field_name) + operator + (func_type|Word(nums+"-"+'.')|variable_ref|field_name|str_var))|func_type
# conditions = condition + ZeroOrMore(join_op + condition)
condition = (ZeroOrMore(Literal('(')) + func_type + ZeroOrMore(Literal('(')) + ZeroOrMore(
    operator + ZeroOrMore(Literal('(')) + (func_type | Word(nums + "-" + '.').setResultsName(
        'UPDATE') | variable_upd | field_name_up | str_var_up) + ZeroOrMore(Literal(')'))) + ZeroOrMore(
    Literal(')'))) | (ZeroOrMore(Literal('(')) + (variable_ref | field_name) + ZeroOrMore(Literal('(')) + ZeroOrMore(
    operator + ZeroOrMore(Literal('(')) + (
                func_type | Word(nums + "-" + '.') | variable_ref | field_name | str_var) + ZeroOrMore(
        Literal(')'))) + ZeroOrMore(Literal(')'))) | func_type
conditions = ZeroOrMore(Literal('(')) + condition + ZeroOrMore(Literal('(')) + ZeroOrMore(
    join_op + ZeroOrMore(Literal('(')) + condition + ZeroOrMore(Literal(')')))
func_assign = (variable_upd | field_name_up) + equal + func_type + semicol
func_assign_wo_semicol = (variable_upd | field_name_up) + equal + func_type
var_assign_wo_semicol = variable_upd + Literal('=') + expression
field_assign_wo_semicol = field_name_up + equal + expression
assign_stmt_without_semicolon = (var_assign_wo_semicol | field_assign_wo_semicol | func_assign_wo_semicol)
assign_stmt = (var_assign | field_assign | func_assign)
While_stmt = Forward()
if_stmt = Forward()
select = CaselessKeyword('Select') + (variable | field_name | str_var) + ZeroOrMore(
    comma + (variable | field_name | str_var)) + CaselessKeyword('into') + (variable_upd | field_name_up) + ZeroOrMore(
    comma + (variable_upd | field_name_up)) + CaselessKeyword('from') + variable + CaselessKeyword(
    'where') + conditions + semicol
update = CaselessKeyword('Update') + (variable_upd | field_name_up) + CaselessKeyword(
    'set') + assign_stmt_without_semicolon + CaselessKeyword('where') + conditions + semicol
# statement=Forward()
# if_stmt << if_key + conditions + then_key +  ((statement)|(begin_key + ZeroOrMore(statement) + end_key))+ Optional(else_key +((statement)|(begin_key + ZeroOrMore(statement) + end_key)))
sql_stmt = update | select
While_stmt << while_key + conditions + CaselessKeyword('do') + Optional((declare_stmt | assign_stmt | (
            func_type + semicol) | if_stmt | sql_stmt | While_stmt | CaselessKeyword('continue;') | CaselessKeyword(
    'break;')) | (begin_key + ZeroOrMore(
    declare_stmt | assign_stmt | (func_type + semicol) | if_stmt | sql_stmt | While_stmt | CaselessKeyword(
        'break;') | CaselessKeyword('continue;')) + end_key))
if_stmt << if_key + conditions + then_key + Optional(
    (declare_stmt | assign_stmt | (func_type + semicol) | if_stmt | sql_stmt | While_stmt) | (begin_key + ZeroOrMore(
        declare_stmt | assign_stmt | (func_type + semicol) | if_stmt | sql_stmt | While_stmt | CaselessKeyword(
            'continue;') | CaselessKeyword('break;')) + end_key)) + Optional(else_if + conditions + then_key + (
            (declare_stmt | assign_stmt | (func_type + semicol) | if_stmt | sql_stmt | While_stmt) | (
                begin_key + ZeroOrMore(
            declare_stmt | assign_stmt | (func_type + semicol) | if_stmt | sql_stmt | While_stmt | CaselessKeyword(
                'continue;') | CaselessKeyword('break;')) + end_key))) + Optional(else_key + (
            (declare_stmt | assign_stmt | if_stmt | (func_type + semicol) | sql_stmt | While_stmt) | (
                begin_key + ZeroOrMore(
            declare_stmt | assign_stmt | (func_type + semicol) | if_stmt | sql_stmt | While_stmt | CaselessKeyword(
                'continue;') | CaselessKeyword('break;')) + end_key)))
statement = pp.Group(declare_stmt) | pp.Group(assign_stmt) | pp.Group(func_type + semicol) | pp.Group(
    if_stmt) | pp.Group(sql_stmt) | pp.Group(While_stmt) | conditions | (func_type)
start = ZeroOrMore(statement)
join_list = ["!", "&", "and", "or", "!"]
func_list = ["atoi", "ntoa", "mid", "left", "right", "date", "strdate", "new", "concat", "delete", "len", "set", "sort",
             "strstr", "trim", "sum", "eof", "aton", "count", "exist", "years", "months", "weeks", "days", "hours",
             "minutes", "seconds", "cerror", "trimleft", "accum", "trimright", "sort", " cerror", "empty", "collate",
             "get", "getcurrentlocationindex", "index", "numerrors", "readblock", "writeblock", "unreadblock",
             "occurrencetotal", "messagebox"]


### to process the functions + functions coming in the assignment statements of if-statements
def function_for_functions_new(tokens, func_name, exist, globalVariables):
    print("entering into functions fn")
    rule_str = ' '.join(tokens)  # tokens is the list of tokens of the rule
    print(rule_str)
    rule_tokens = statement.parseString(rule_str)
    print(rule_tokens)
    rule_tokens_list = rule_tokens[0]  # rule_tokens[0] is the parsed list of tokens
    rule_tokens_list = list(rule_tokens_list)
    if 'accum' == rule_tokens_list[2]:
        print("ASDA")
    rule_tokens = repr(rule_tokens)  # to get tokens with certain tags
    rule_tokens = eval(rule_tokens)  # rule_tokens[0][0][1] would be having all the named tokens
    ref = ""
    upd = ""
    rule = ""
    if 'REF' in rule_tokens[0][0][1]:  # REF- i.e. what is being referred
        ref = rule_tokens[0][0][1]['REF'][0]

        # if ref not in globalVariables.field_set:
        #     return ""
    if 'accum' in rule_tokens_list:
        print("WQDWQ")
        ref = 'accumulator '
    if 'UPDATE' in rule_tokens[0][0][1]:  # UPDATE-what is being updated
        upd = rule_tokens[0][0][1]['UPDATE'][0]
    if func_name == "get":
        tokens = list(tokens)
        ind = tokens.index("get")  # ind+1 would give (years/months/weeks/days)..etc
        rule = " get number of " + tokens[ind + 1] + " in " + ref

    if func_name == "index":
        rule = " current loop count of " + ref
    if func_name == "readblock":
        rule = " read " + ref
    if func_name == "writeblock":
        rule = " write into " + ref
    if func_name == "unreadblock":
        rule = " unread the last block "
    if func_name == "getcurrentlocationindex":
        rule = upd + " the current location index"
    if func_name == "occurrencetotal":
        rule = upd + " total number of occurrences of " + ref
    if func_name == "collate":
        if 'REF' in rule_tokens[0][0][1] and len(rule_tokens[0][0][1]['REF']) > 1:  # in collate 2 groups are referred
            ref = ' and '.join(rule_tokens[0][0][1]['REF'])
        rule = " combine " + ref + " to form " + upd
    if func_name == "numerrors":
        rule = upd + " current count of errors "
    if func_name == "messagebox":
        rule = " print " + ref
    if func_name == "ntoa":
        print(ref)
        rule = " string value of " + ref
    if func_name == "accum":
        rule = " value of accumulator "
    if func_name == "empty":
        rule = upd + " = make the value of the field NULL "
    if func_name == "atoi":
        rule = " integer value of " + ref
    if func_name == "mid":
        print("################3333")
        st = int(rule_tokens[0][0][1]['START'][0]) + 1  # get the start index
        end = (rule_tokens[0][0][1]['END'][0])  # get the end index
        rule = upd + " =  substring of " + ref + " from position " + str(
            st) + " to " + end + " characters from that position "
        if exist == 1:
            rule = rule + " not empty "
    if func_name == "left":
        num = ''
        if 'NUM' in rule_tokens[0][0][1]:
            num = int(rule_tokens[0][0][1]['NUM'][0])
        rule = str(num) + " characters from left of " + ref
    if func_name == "right":
        num = ''
        if 'NUM' in rule_tokens[0][0][1]:
            num = int(rule_tokens[0][0][1]['NUM'][0])
        rule = str(num) + " characters from right of " + ref
    if func_name == "date":
        format = ''
        if 'FORMAT' in rule_tokens[0][0][1]:
            format = rule_tokens[0][0][1]['FORMAT'][0]
            rule = ref + " in format " + format
        else:
            rule = "set date as " + rule_str.split('=')[1]
    if func_name == "years":
        ref = ''
        if 'REF' in rule_tokens[0][0][1]:
            ref = rule_tokens[0][0][1]['REF'][0]
            rule = ref + " number of years"
        else:
            rule = ''
    if func_name == "months":
        ref = ''
        if 'REF' in rule_tokens[0][0][1]:
            ref = rule_tokens[0][0][1]['REF'][0]
            rule = ref + " number of months"
        else:
            rule = ''
    if func_name == "weeks":
        ref = ''
        if 'REF' in rule_tokens[0][0][1]:
            ref = rule_tokens[0][0][1]['REF'][0]
            rule = ref + " number of weeks"
        else:
            rule = ''
    if func_name == "days":
        ref = ''
        if 'REF' in rule_tokens[0][0][1]:
            ref = rule_tokens[0][0][1]['REF'][0]
            rule = ref + " number of days"
        else:
            rule = ''
    if func_name == "hours":
        ref = ''
        if 'REF' in rule_tokens[0][0][1]:
            ref = rule_tokens[0][0][1]['REF'][0]
            rule = ref + " number of hours"
        else:
            rule = ''
    if func_name == "minutes":
        ref = ''
        if 'REF' in rule_tokens[0][0][1]:
            ref = rule_tokens[0][0][1]['REF'][0]
            rule = ref + " number of minutes"
        else:
            rule = ''
    if func_name == "seconds":
        ref = ''
        if 'REF' in rule_tokens[0][0][1]:
            ref = rule_tokens[0][0][1]['REF'][0]
            rule = ref + " number of seconds"
        else:
            rule = ''
    if func_name == "strdate":
        format = rule_tokens[0][0][1]['FORMAT'][0]
        rule = ref + " in format " + format
    if func_name == "len":
        rule = " length of " + ref
    if func_name == "set":
        rule = "set " + " as " + ref
    if func_name == "concat":
        num = rule_tokens[0][0][1]['NUM'][0]
        print(num)
        str_temp = rule_tokens[0][0][1]['REF'][0]
        print(str_temp)  # the string to be concatenated
        if ref == '':
            rule = "concatenate " + num + " chars of string " + str_temp + " to " + upd
        else:
            rule = "concatenate " + num + " chars of " + str_temp + " to " + upd
    if func_name == "strstr":
        if (tokens[6] == '"'):
            substring = tokens[7]
        else:
            substring = tokens[6]
        rule = " = substring " + substring + " starts at " + upd
    if func_name == "trim":
        string = ''
        if 'STRING' in rule_tokens[0][0][1]:
            string = rule_tokens[0][0][1]['STRING'][0]
        if ',' in tokens:
            rule = upd + " = remove leading and trailing whitespaces from " + ref
        else:
            rule = upd + " = remove leading and trailing characters" + string + " from " + ref
    if func_name == "trimleft":
        string = ''
        print("WD")
        print(tokens)
        if 'STRING' in rule_tokens[0][0][1]:
            string = rule_tokens[0][0][1]['STRING'][0]
        if ',' in tokens:  # i.e there is only one argument given to the function
            rule = "remove white spaces from left side of " + ref
        else:
            rule = "remove " + string + " from left side of " + ref
    if func_name == "trimright":
        string = ''
        if 'STRING' in rule_tokens[0][0][1]:
            string = rule_tokens[0][0][1]['STRING'][0]
        if tokens[5] == '"':  # i.e only one argument given to the function
            rule = "remove white spaces from right side of " + ref
        else:
            rule = "remove " + string + " from right side of " + ref
    if func_name == "sort":
        group = ''
        if 'ref':
            ref = rule_tokens[1]['REF']
        ref_str = 'and'.join(ref)
        if 'GROUP' in rule_tokens[1]:
            group = rule_tokens[1]['GROUP'][0]
        rule = 'Sort ' + group + " based on field " + ref
    if func_name == "cerror":
        rule = " compliance error in " + ref
    if func_name == "sum":
        string = rule_tokens[0][0][1]['STRING'][0]
        if (string[0] == "n" or string[0] == "N"):
            rule = "add negative value of the field to the sum total"
        else:
            rule = "add negative value of the field to the sum total"
    if func_name == "eof":
        rule = "check for end of file"
        ref = ""
    if func_name == "aton":
        rule = upd + " = real number value of string " + ref
    if func_name == "count":
        # print(ref)
        rule = " = number of iterations in the group " + ref
    if func_name == "delete":
        return
    if func_name == "new":
        return
    if func_name == "exist":
        if exist == 1:  # exist is given as argument to the function
            rule = ref + " does not exists "
        else:
            rule = ref + " exists "

    return rule


def ass_func(tokens, index_start, globalVariables):
    print("hi")
    # print(tokens)
    print("FWEFFFFFFFFFFFFFFFFFF")
    rule = []
    i = index_start
    store_op = []
    op_in = 0
    while i < len(tokens) and tokens[i] != ';':
        if tokens[i] == '+' or tokens[i] == '*' or tokens[i] == '/' or tokens[i] == '<<' or tokens[i] == '>>' or tokens[
            i] == '>' or tokens[i] == '<' or tokens[i] == '-':
            store_op.append(tokens[i])
        rule.append(tokens[i])
        i = i + 1
    # if not rule:
    #     return
    if tokens[index_start] == 'delete' or tokens[index_start] == 'sort':
        return '', '', i, ''
    print(store_op)
    print("OPERATORSSSSSSSSSSSSSSSSSSSS")
    rule.append(';')

    # code to change field no. to name
    new_rule = []
    x = 0
    print(rule)
    while x < len(rule):
        if rule[x] == '$':
            if 'count' in rule:
                new_rule.append(rule[x])
                x = x + 1
                while rule[x] != '[':
                    new_rule.append(rule[x])
                    x = x + 1
                while rule[x] != ';':
                    x = x + 1
                new_rule.append('[')
                new_rule.append('&')
                new_rule.append(']')
                new_rule.append(')')
                new_rule.append(';')
                break
            while x < len(rule) and rule[x] != '#':
                x = x + 1
            x = x + 1
            if x < len(rule) and rule[x] in globalVariables.dict_ind_field:
                t = ''.join(globalVariables.dict_ind_field[rule[x]])
            else:
                t = rule[x]
            new_rule.append(t)
            x = x + 1
            continue
        if rule[x] == '#':
            x = x + 1
            if rule[x] in globalVariables.dict_ind_field:
                t = ''.join(globalVariables.dict_ind_field[rule[x]])
            else:
                t = rule[x]
            new_rule.append(t)
            x = x + 1
            continue
        new_rule.append(rule[x])
        x = x + 1
    print(new_rule)
    print("this is the new rule in ass_function")
    x_rules = ' '.join(new_rule)
    assign_stmts = re.split('\+|\*|/|>>|<<|-', x_rules)
    # assign_stmts = re.split('[\-!?:]+',x_rules)
    final_stmt = ''
    print(assign_stmts)
    for ind, stmts in enumerate(assign_stmts):
        print("HI")
        print(stmts)
        if stmts[len(stmts) - 1] != ';':
            stmts = stmts + ';'
        exist = 0
        if stmts.find('!') >= 0:
            stmts = stmts.replace('!', '')
            exist = 1
        func_tokens = start.parseString(stmts)
        temporary_rule = ''
        print("******************S")
        if func_tokens:
            for token in func_tokens[0]:

                if token in func_list:
                    print("got a function token")
                    temporary_rule = function_for_functions_new(func_tokens[0], token, exist, globalVariables)
                    print(temporary_rule)
                    print("got the above rule from fn")
                    break
                if token == 'Update' or token == 'select':
                    break
        if not temporary_rule:
            temporary_rule = stmts
        if ind == 0:
            final_stmt = temporary_rule
        else:
            if len(store_op) != 0 and op_in < len(store_op):
                if store_op[op_in] == '<<':
                    final_stmt = final_stmt + 'add' + temporary_rule
                elif store_op[op_in] == '>>':
                    final_stmt = final_stmt + 'subtract' + temporary_rule
                else:
                    final_stmt = final_stmt + store_op[op_in] + temporary_rule
                op_in = op_in + 1
            else:
                final_stmt = temporary_rule

    final_stmt = final_stmt.replace(';', '')
    print(final_stmt)

    rule_str = ' '.join(rule)
    print("*************************************")
    print(rule_str)
    rule_tokens = start.parseString(rule_str)
    rule_tokens = repr(rule_tokens[0])
    rule_tokens = eval(rule_tokens)
    print(rule_tokens)
    x = ""
    if 'UPDATE' in rule_tokens[1]:
        x = rule_tokens[1]['UPDATE'][0]
    y = ""
    if 'REF' in rule_tokens[1]:
        y = rule_tokens[1]['REF']
    return x, y, i, final_stmt


### for processing the functions used in normal assignment statements


def function_for_functions(tokens, func_name, exist, globalVariables):
    rule_str = ''.join(tokens)  #
    print(rule_str)
    rule_tokens = statement.parseString(rule_str)
    # if 'left' in rule_tokens:
    #     print(rule_tokens)
    #     exit()
    rule_tokens = repr(rule_tokens)
    rule_tokens = eval(rule_tokens)
    ref = ""
    upd = ""
    rule = ""
    if 'REF' in rule_tokens[1]:
        ref = rule_tokens[1]['REF'][0]
        # if ref=='sendercode':
        #     ref=rule_tokens[1]['REF'][1]
        if ref == '0374:3':
            print(tokens)
            exit()
        if ref not in globalVariables.field_set:
            print(ref)
            return ""
    if 'UPDATE' in rule_tokens[1]:
        upd = rule_tokens[1]['UPDATE'][0]
    if func_name == "ntoa":
        rule = upd + " = string value of " + ref
    if func_name == "atoi":
        rule = upd + " = integer value of " + ref
    if func_name == "accum":
        rule = " value of accumulator "
    if func_name == "empty":
        rule = upd + " = make the value of the field NULL "
    if func_name == "get":
        tokens = list(tokens)
        ind = tokens.index("get")
        rule = " number of " + tokens[ind + 1] + " in " + upd
    if func_name == "index":
        rule = " current loop count of " + ref
    if func_name == "readblock":
        rule = " read " + ref
    if func_name == "writeblock":
        rule = " write into " + ref
    if func_name == "unreadblock":
        rule = " unread the last block "
    if func_name == "getcurrentlocationindex":
        rule = upd + " = the current location index"
    if func_name == "occurrencetotal":
        rule = upd + " = total number of occurrences of " + ref
    if func_name == "collate":
        if 'REF' in rule_tokens[1] and len(rule_tokens[1]['REF']) > 1:
            ref = ' and '.join(rule_tokens[1]['REF'])
        rule = " combining " + ref + " to form " + upd
    if func_name == "numerrors":
        rule = upd + " = current count of errors "
    if func_name == "messagebox":
        rule = " print " + ref
    if func_name == "mid":
        # if ref not in globalVariables.field_set:
        #     print(ref)
        #     exit()
        #     return ""
        st = int(rule_tokens[1]['START'][0]) + 1
        end = int(rule_tokens[1]['END'][0])
        if upd == "":
            rule = " substring of " + ref + " from position " + str(st) + " to " + str(end) + " from that position "
            if exist == 1:
                rule = rule + " not empty "
            else:
                rule = upd + " = substring of " + ref + " from position " + str(st) + " to " + str(
                    end) + " from that position "
        else:
            rule = "if " + upd + " equals substring of " + ref + " from  " + str(st) + " to " + str(
                end) + " from that position "
    if func_name == "left":
        num = ''
        str_val = ''
        if 'STRING' in rule_tokens[1]:
            str_val = rule_tokens[1]['STRING'][0]
        if 'NUM' in rule_tokens[1]:
            num = int(rule_tokens[1]['NUM'][0])
        if upd == "":
            rule = " extract " + str(num) + " characters from left of " + ref
            if exist == 1:
                rule = rule + " and if it is empty"
            else:
                rule = " if " + str(num) + " characters from left of " + ref + " equals to " + str_val
                # rule = "extract " + str(num) + " characters from left of " + ref
        else:
            rule = "if " + upd + " equals extract " + str(num) + " characters from left  of " + ref
    if func_name == "right":
        num = int(rule_tokens[1]['NUM'][0])
        rule = str(num) + " characters from right of " + ref + ' = ' + upd
    if func_name == "date":
        format = rule_tokens[1]['FORMAT'][0]
        rule = upd + " = " + ref + " in format " + format
    if func_name == "years":
        rule = ref + " number of years"
    if func_name == "months":
        rule = ref + " number of months"
    if func_name == "weeks":
        rule = ref + " number of weeks"
    if func_name == "days":
        rule = ref + " number of days"
    if func_name == "hours":
        rule = ref + " number of hours"
    if func_name == "minutes":
        rule = ref + " number of minutes"
    if func_name == "seconds":
        rule = ref + " number of seconds"
    if func_name == "strdate":
        format = rule_tokens[1]['FORMAT'][0]
        rule = upd + " = " + ref + " in format " + format
    if func_name == "len":
        rule = upd + " = length of " + ref
    if func_name == "set":
        rule = "set " + upd + " as " + ref
    if func_name == "concat":
        num = rule_tokens[1]['NUM'][0]
        str_temp = rule_tokens[1]['REF'][0]
        if ref == '':
            rule = "concatenate " + num + " chars of string " + str_temp + " to " + upd
        else:
            rule = "concatenate " + num + " chars of " + ref + " to " + upd
    if func_name == "strstr":
        if (tokens[6] == '"'):
            substring = tokens[5]
            print("HI")
        else:
            print("by")
            substring = tokens[4]
        if upd == '':
            rule = " substring " + substring
        else:
            if upd == '-1':
                rule = ref + " string does not contain " + substring
            else:
                rule = " substring " + substring + " position  equals " + upd
        print(rule)

    if func_name == "trim":
        string = ''
        if 'STRING' in rule_tokens[1]:
            string = rule_tokens[1]['STRING'][0]
        if tokens[5] == '"':
            rule = upd + " = remove leading and trailing whitespaces from " + ref
        else:
            rule = upd + " remove leading and trailing charactor:" + string + " from " + ref
    if func_name == "trimleft":
        string = ''
        if 'STRING' in rule_tokens[1]:
            string = rule_tokens[1]['STRING'][0]
        if ',' in tokens:
            rule = "remove white spaces from left side of " + ref
        else:
            rule = "remove " + string + " from left side of " + ref
    if func_name == "trimright":
        string = ''
        if 'STRING' in rule_tokens[1]:
            string = rule_tokens[1]['STRING'][0]
        if tokens[5] == '"':
            rule = "remove white spaces from right side of " + ref
        else:
            rule = "remove " + string + " from right side of " + ref
    if func_name == "sort":
        group = ''
        if 'ref':
            ref = rule_tokens[1]['REF']
        ref_str = 'and'.join(ref)
        if 'GROUP' in rule_tokens[1]:
            group = rule_tokens[1]['GROUP'][0]
        rule = 'Sort ' + group + " based on field " + ref
    if func_name == "cerror":
        rule = " compliance error in " + ref
    if func_name == "sum":
        string = rule_tokens[1]['STRING'][0]
        if (string[0] == "n" or string[0] == "N"):
            rule = "add negative value of the field to the sum total"
        else:
            rule = "add negative value of the field to the sum total"
    if func_name == "eof":
        rule = "check for end of file"
        ref = ""
    if func_name == "aton":
        rule = upd + " = real number value of string " + ref
    if func_name == "count":
        # print(ref)
        rule = upd + " = number of iterations in the group " + ref
    if func_name == "delete":
        return
    if func_name == "new":
        return
    if func_name == "exist":
        if exist == 1:
            rule = " if " + ref + " does not exists "
        else:
            rule = " if " + ref + " exists "
    if upd in globalVariables.dict_token:
        globalVariables.dict_token[upd].append([[ref], "", rule])
    else:
        temp = []
        temp.append([[ref], "", rule])
        globalVariables.dict_token[upd] = temp
    return rule


def assign_func(index, tokens, ip_or_op, dict_token, globalVariables):
    rule_str = ''.join(tokens)
    rule_str = rule_str.replace('=', ' = ')
    rule_tokens = statement.parseString(rule_str)
    rule_tokens = repr(rule_tokens)
    rule_tokens = eval(rule_tokens)
    ref = ""
    if 'REF' in rule_tokens[0][0][1]:
        ref = rule_tokens[0][0][1]['REF']
    upd = rule_tokens[0][0][1]['UPDATE'][0]
    print(ref)
    print(upd)
    if ref == '':
        return ''
    flag = 0
    print(globalVariables.dict_op_field)
    if ip_or_op == 0:
        field = globalVariables.dict_field[index]
    else:
        field = globalVariables.dict_op_field[index]

    t = field
    if field in globalVariables.dict_ind_field:
        t = ''.join(globalVariables.dict_ind_field[field])
        flag = 1
    print(t)

    right_side = ''
    for ind, item in enumerate(ref):
        if ind != 0:
            right_side += ' + '
        if item in globalVariables.dict_ind_field:
            right_side += ''.join(globalVariables.dict_ind_field[item])
        else:
            right_side += item

    if right_side:
        rule = upd + " = " + right_side
    else:
        rule = rule_str

    l = []
    if upd in globalVariables.variable_set:
        l = [ref, '', rule]
    elif ip_or_op == 1:
        print(ref)
        if len(ref) == 1 and ref[
            0] not in globalVariables.variable_set:  # lef(ref)==1 means only one thing on right side..probably string
            l = [ref, '', "Hardcode " + ref[0]]
        else:
            # if len(rule.split())
            l = [ref, '', rule]
    else:  # t is the field where this rule is written
        if t == 'PRE_SESSION' or t == 'POST_SESSION':  # if in pression or postSession, no need of " if field exists"  in the notes
            l = [ref, '', rule]
        else:
            l = [ref, '', rule]
            # l=[ref, 'if '+ t +" exists ", rule]

    # elif ip_or_op==1:
    #     print(ref)
    #     if len(ref)==1 and ref[0] not in globalVariables.variable_set:
    #         l=[ref,'', "Hardcode "+ ref[0]]
    #     else:
    #     # if len(rule.split())
    #         l=[ref,'',rule]
    # else:
    #     l=[ref, 'if '+ t +" exists ", rule]
    # CHANG IN ASSIGN
    if upd in dict_token:
        dict_token[upd].append(l)
    else:
        temp = []
        temp.append(l)
        dict_token[upd] = temp

    return rule


### for processing the conditions of if functions
def if_util(tokens, index, globalVariables):
    cond = []
    i = index
    while tokens[i] != 'then':
        cond.append(tokens[i])
        i = i + 1
    new_cond = []
    x = 0
    print("COND")
    print(cond)
    while x < len(cond):
        if cond[x] == '$':
            if 'count' in cond:
                new_cond.append(cond[x])
                x = x + 1
                while cond[x] != '[':
                    new_cond.append(cond[x])
                    x = x + 1
                while cond[x] != '*':
                    x = x + 1
                x = x + 3
                new_cond.append('[')
                new_cond.append('*')
                new_cond.append(']')
                new_cond.append(')')
                # new_cond.append(';')
                while x < len(cond):
                    new_cond.append(cond[x])
                    x = x + 1
                break

            while x < len(cond) and cond[x] != '#':
                x = x + 1
            x = x + 1
            if cond[x] in globalVariables.dict_ind_field:
                t = ''.join(globalVariables.dict_ind_field[cond[x]])
                new_cond.append(t)
            else:
                new_cond.append(cond[x])
            x = x + 1
            continue
        if cond[x] == '#':
            x = x + 1
            if cond[x] in globalVariables.dict_ind_field:
                t = ''.join(globalVariables.dict_ind_field[cond[x]])
                new_cond.append(t)
            else:
                new_cond.append(cond[x])

            x = x + 1
            continue
        if cond[x] in globalVariables.dict_ind_field:
            t = ''.join(globalVariables.dict_ind_field[cond[x]])
            new_cond.append(t)
        else:
            new_cond.append(cond[x])

        x = x + 1
    cond_str = ' '.join(new_cond)
    cond_str = cond_str.replace(';', '')
    print("cond_str")
    print(cond_str)
    # cond_tokens=conditions.parseString(''.join(cond))
    cond_tokens = conditions.parseString(cond_str)
    cond_tokens = repr(cond_tokens)
    cond_tokens = eval(cond_tokens)
    rule = ""
    op_count = 0
    functions = []
    op_list = []
    print("cond_tokens")
    print(cond_tokens)
    if 'JOIN_OP' in cond_tokens[1]:
        op_list = cond_tokens[1]['JOIN_OP']
        functions = re.split('&|\|| or | and ', cond_str)
        print(op_list)
    else:
        functions = [cond_str]
    exist = 0
    print("STRING")
    print(cond_str)
    print(functions)
    # globalVariables.op_count=len(functions)-1
    for rules in functions:
        x_rules = rules
        if rules.find('!') >= 0:
            rules = rules.replace('!', '')
            exist = 1
        func_tokens = conditions.parseString(rules)
        flag = 0
        fl = 1
        for rule_token in func_tokens:
            if rule_token in func_list:
                temporary_rule = function_for_functions(func_tokens, rule_token, exist, globalVariables)
                if not temporary_rule:
                    fl = 0
                    print("YES")
                rule += temporary_rule + " "
                # if globalVariables.op_count==0 and rule_token=="exist":
                #     rule=rule.replace("if","")
                print(rule)
                flag = 1
                break
        rules = rules + ";"
        if flag == 0:
            # if func_tokens[0] in globalVariables.field_set:
            for rule_token in func_tokens:
                if rule_token == '=':
                    rule += x_rules + " "
                    flag = 1
                    break
            if op_count == 0:
                rule_t = " if " + rule
                rule = rule_t
        print(rule)
        if len(functions) == 1 or op_count == len(functions) - 1:
            break
        if fl == 1:
            rule += op_list[op_count] + " "
            op_count += 1

    make_shift_check = ['&', 'and', '|', 'or']
    make_shift_list = rule.split()
    if len(make_shift_list) != 0:
        if make_shift_list[len(make_shift_list) - 1] in make_shift_check:
            del make_shift_list[-1]
    cond_tokens = cond_tokens[1]['REF']
    # return cond_tokens, ''.join(new_cond),i+1
    if rule:
        print(rule)
        print("dfjkd")
        if make_shift_list and make_shift_list[0] != 'if':
            return cond_tokens, "if " + ' '.join(make_shift_list), i + 1
        else:
            return cond_tokens, ' '.join(make_shift_list), i + 1
    else:
        return cond_tokens, '', i + 1


### making dictionary for select and update statements
def sql_func(tokens, dict_token, ip_or_op, globalVariables):
    # print(tokens)
    i = 0
    while i < len(tokens):
        if tokens[i] == 'where':
            break
        i = i + 1
    sql_cond_tokens = tokens[i + 1:]
    sql_cond_tokens.append('then')
    print(sql_cond_tokens)
    sql_cond_tokens, rule_sql_cond, index = if_util(sql_cond_tokens, 0, globalVariables)
    print("edfew")
    print(rule_sql_cond)
    print("efew")
    # exit()
    rule = ' '.join(tokens)
    rule_tokens = statement.parseString(rule)
    rule_tokens = repr(rule_tokens)
    rule_tokens = eval(rule_tokens)
    upd = rule_tokens[0][0][1]['UPDATE'][0]
    ref = []
    new_rule = ''
    i = 0
    rule = rule.split('where')
    print(rule)
    s_flag = 0
    if rule_sql_cond.find('sendercode') != -1:
        s_flag = 1
    rule_sql_cond = rule_sql_cond.replace('sendercode', rule_tokens[0][0][1]['REF'][0])
    # changeeeeeeeeeeeeeee
    if s_flag == 1:
        new_rule = rule[0] + " where sendercode = " + rule_sql_cond
    else:
        new_rule = rule[0] + rule_sql_cond
    print(new_rule)
    # send_ind = new_rule.find('sendercode')
    # and_ind = new_rule.rfind('and')
    # new_new_rule = new_rule[:send_ind - 1] + ' ' + new_rule[and_ind + 4:] + " and " + new_rule[send_ind:and_ind]
    if 'REF' in rule_tokens[0][0][1]:
        ref = rule_tokens[0][0][1]['REF']
    if upd in dict_token:
        if ip_or_op == 0:
            dict_token[upd].append([ref, "", new_rule])
        else:
            dict_token[upd].append([ref, "", new_rule])
    else:
        temp = []
        temp.append([ref, "", new_rule])
        if ip_or_op == 0:
            dict_token[upd] = temp
        else:
            globalVariables.dict_op_token[upd] = temp
    print(new_rule)
    # exit()


### for processing each of the statements inside the if statement
def eval_sent(tokens, index, stack, dict_token, globalVariables):
    i = index
    if i < len(tokens) and (tokens[i].lower() == 'continue' or tokens[i] == 'break'):
        return i + 2
    if i < len(tokens) and tokens[i] == 'if':
        i = if_func(tokens, i, stack, dict_token, globalVariables)
        return i
    else:
        update, ref, i, rule = ass_func(tokens, i, globalVariables)

        # print(tokens[i])
        temp_list = []
        temp_str = ""
        for list_temp in stack:
            temp_list.extend(list_temp[0])
            if temp_str:
                temp_str += (" and " + list_temp[1])
            else:
                temp_str = list_temp[1]
        temp_list.extend(ref)
        if update in dict_token:
            dict_token[update].append([temp_list, temp_str, rule])
        else:
            temp = []
            temp.append([temp_list, temp_str, rule])
            dict_token[update] = temp
        return i + 1


### for processing if statement
def if_func(tokens, index, stack, dict_token, globalVariables):
    print(tokens)
    i = index + 1
    cond_tokens, cond_str, i = if_util(tokens, i, globalVariables)
    temp = [cond_tokens, cond_str]
    print("this is the list")
    print(temp)
    stack.append(temp)
    temp_list = []
    if i < len(tokens) and tokens[i] == 'begin':
        i = i + 1
        while i < len(tokens) and tokens[i] != 'end':
            i = eval_sent(tokens, i, stack, dict_token, globalVariables)
        temp_list = stack.pop()
    else:
        i = eval_sent(tokens, i, stack, dict_token, globalVariables)
        temp_list = stack.pop()

    if i < len(tokens) and tokens[i] == 'end':
        i = i + 1

    while i < len(tokens) and tokens[i] == 'else if':
        print("ok else if")
        i = i + 1
        c_t, c_s, i = if_util(tokens, i, globalVariables)
        t = [c_t, c_s]
        stack.append(t)

        if i < len(tokens) and tokens[i] == 'begin':
            i = i + 1
            while i < len(tokens) and tokens[i] != 'end':
                i = eval_sent(tokens, i, stack, dict_token, globalVariables)
            stack.pop()
        else:
            i = eval_sent(tokens, i, stack, dict_token, globalVariables)
            stack.pop()

    if i < len(tokens) and tokens[i] == 'else':
        temp_str = temp_list[1]
        # print(temp_str)
        # new_str='!('+temp_str+')'
        new_str = temp_str.replace('=', ' != ')
        new_list = [temp_list[0], new_str]
        stack.append(new_list)
        i = i + 1
        if tokens[i] == 'begin':
            i = i + 1
            while tokens[i] != 'end':
                i = eval_sent(tokens, i, stack, dict_token, globalVariables)
            stack.pop()
        else:
            eval_sent(tokens, i, stack, dict_token, globalVariables)
            stack.pop()
    return i


### handling normal declaration function
def decl_func(tokens, ip_or_op, globalVariables):
    rule = ' '.join(tokens)
    rule_tokens = statement.parseString(rule)
    rule_tokens = repr(rule_tokens)
    rule_tokens = eval(rule_tokens)
    print(rule_tokens)
    var_type = ''
    if 'VARTYPE' in rule_tokens[0][0][1]:
        var_type = (rule_tokens[0][0][1]['VARTYPE'][0])
    print(var_type)
    list_of_variables = rule_tokens[0][0][1]['VARIABLES']
    print(list_of_variables)
    if ip_or_op == 0:
        for item in list_of_variables:
            globalVariables.dict_type[item] = var_type.lower()
            globalVariables.variable_set.add(item)
    else:
        for item in list_of_variables:
            globalVariables.dict_op_type[item] = var_type.lower()
            globalVariables.variable_set.add(item)


### removing comments from the whole rule textfile
def remove_comments(nf, of, globalVariables):
    for line in of:
        # print(line)
        length = len(line)
        i = 0
        while (i < length - 1 and not (line[i] == '/' and line[i + 1] == '/')):
            i = i + 1
        if (i != 0):
            temp = line[:i]
            nf.write(temp)
            nf.write('\n')

    nf.close()
    of.close()


def handle_java(line_list, arr_java, null_flag, globalVariables):
    for ind, line in enumerate(line_list):
        if not line:
            continue
        if (null_flag == 1):
            line_list[ind] = ''
            if ';' in line:
                null_flag = 0
                continue
        obj_split = line.split(' ', 1)
        if obj_split[0].lower() == 'object':
            for item in obj_split[1].split():
                item = item.replace(';', '')
                arr_java.append(item.strip())
        if obj_split[0].strip() in arr_java:
            line_list[ind] = ''
            continue
        obj_split_sec = line.split('.', 1)
        if obj_split_sec[0].strip() in arr_java:
            line_list[ind] = ''
            continue
        flag = 0
        # print("helo")
        split_list = line.split('=', 1)
        if len(split_list) == 1:
            continue
        left_part = split_list[0]
        # print(left_part)
        if len(left_part.strip().split()) > 1:
            continue
        right_part = split_list[1]
        for item in arr_java:
            # print(item)
            if item.strip() in right_part:
                print(item)
                field_name = left_part.split('#')
                if len(field_name) > 1:
                    arr_java.append(field_name[1].strip())
                arr_java.append(left_part.strip())
                flag = 1
                break
        if flag == 1:
            if ';' not in line:
                null_flag = 1
            line_list[ind] = left_part + " = java;"
            # print("final_line")
            # print(line_list[ind])

    block_code = '\n'.join(line_list)
    arr_java = list(set(arr_java))
    # print(arr_java)
    return block_code


# def check_for_java(tokens):
#     java_str=' '.join(tokens)
#     if 'java' in java_str:
#         return 1
#     return 0


### processing of each rule and entering into into the globalVariables.dict_token
### ip_or_op - 0 is for input side rules... 1 is for output side rules
def make_dictionary(result, dict_token, ip_or_op, globalVariables):
    for index, result_token in enumerate(result):
        print(result_token)
        flag = 0
        if 'while' in (name.lower() for name in result_token):
            continue
        if result_token[0] == 'if':
            stack = []
            i = if_func(result_token, 0, stack, dict_token, globalVariables)
            flag = 1
            continue

        if result_token[0].lower() == 'update' or result_token[0].lower() == 'select':
            sql_func(result_token, dict_token, ip_or_op, globalVariables)
            flag = 1
            continue

        for rule_token in result_token:
            if rule_token in func_list:
                print("SOWMITHHHHHHH")
                upd, ref, n, rule = ass_func(result_token, 0, globalVariables)
                if upd in dict_token:
                    dict_token[upd].append([ref, "", rule])
                else:
                    t = []
                    t.append([ref, "", rule])
                    dict_token[upd] = t

                # print(globalVariables.dict_token)
                flag = 1
                break

        if flag == 0:
            for rule_ind, rule_token in enumerate(result_token):
                if rule_token == '=':
                    if result_token[rule_ind + 1] == '0' or (
                            result_token[rule_ind + 1] == '"' and result_token[rule_ind + 2] == '"'):
                        # print(result_token)
                        # exit()
                        if result_token[0] != '#' and result_token[0] != '$':
                            flag = 2
                            break
                    print("SDDDDDD")
                    # print(index)
                    assign_func(index, result_token, ip_or_op, dict_token, globalVariables)
                    flag = 2
                    break

        if flag == 0:
            print("TTTTTTTTTTTTTT")
            print(result_token)
            decl_func(result_token, ip_or_op, globalVariables)
        # print(globalVariables.dict_token)

    # print(globalVariables.dict_token)
    print("this is the final dictionary")


count = 0


def find_in_dict_token(var, note, temp_dict, inp_op, old_var, list_recur, globalVariables):
    list_recur.append(var.strip())
    global count
    count += 1
    print(count)
    if inp_op == 0:
        print("start of find_in_dict_token")
        if var not in globalVariables.dict_token:
            return
        temp_lists = globalVariables.dict_token[var]
        print("temp_list")
        print("FORrecursion")
        print(temp_lists)
    else:
        print("start of find_in_dict_token_OP")
        if (var not in globalVariables.dict_op_token) and (var not in globalVariables.dict_token):
            print("EXIT")
            return
        temp_lists = []
        if var in globalVariables.dict_token:
            temp_lists = globalVariables.dict_token[var]
        if var in globalVariables.dict_op_token:
            temp_lists.extend(globalVariables.dict_op_token[var])
        print("temp_list")
        print(temp_lists)
    list_note = []
    for list_temp in temp_lists:
        print("list-temp")
        print(list_temp)
        temp_list_note = []
        x = list_temp[0]
        x = (list(set(x)))
        flag = 0
        for var_var in x:
            # if var_var.strip()==old_var.strip():
            if var_var.strip() in list_recur:
                continue
            if var_var == var:
                continue
            if (var_var in globalVariables.dict_token) and (inp_op == 0):
                temp_list_note.extend(
                    find_in_dict_token(var_var, note, temp_dict, inp_op, var, list_recur, globalVariables))
            if ((var_var in globalVariables.dict_token) or (var_var in globalVariables.dict_op_token)) and (
                    inp_op == 1):
                temp_list_note.extend(
                    find_in_dict_token(var_var, note, temp_dict, inp_op, var, list_recur, globalVariables))
        temp_note = ""
        if var not in globalVariables.dict_ind_field:
            print(count)
            print("NOTES FOR VARIABLE")
            print(list_temp)
            if list_temp[2] and list_temp[2].split()[0].lower() == 'select':
                print("NOTES FOR SQL STATEMENTS")
                str_t = list_temp[2].split()[1] + " " + (' '.join(list_temp[2].split()[4:]))
                temp_dict[var] = [str_t]
                list_temp[2] = ''
                flag = 1
                list_note = []
            else:
                print("NOTE FOR NON SQL")
                if var in temp_dict:
                    if len(list_temp[2].split('=')) >= 2:
                        temp_dict[var].append(list_temp[2].split('=')[1])
                else:
                    if len(list_temp[2].split('=')) >= 2:
                        temp_dict[var] = [list_temp[2].split('=')[1]]
            for item in temp_list_note:
                if flag == 0:
                    if list_temp[1]:
                        temp_note = " and " + list_temp[1] + " and " + list_temp[2] + " "
                    else:
                        temp_note = " and " + list_temp[2] + "\n"
                    item += temp_note
                    print(list_note , "Hello")
                    list_note.append(item)
                    print(list_note ,"Hello")
            if not temp_list_note:
                if flag == 0:
                    temp_note = ""
                    if list_temp[1]:
                        temp_note += list_temp[1] + " and " + list_temp[2] + " "
                    else:
                        temp_note = temp_note + list_temp[2]
                    print(list_note , "Hello00000")
                    list_note.append(temp_note)
                    print(list_note , "Hello00000")
        else:
            print("NOTES FOR NON-VARIABLE")
            if not temp_list_note:
                print("entering if")
                temp_note = ""
                if not list_temp[1]:
                    temp_note = temp_note + list_temp[2] + "\n"
                else:
                    temp_note = temp_note + list_temp[1] + " and " + list_temp[2] + " "
                list_note.append(temp_note)
            else:
                print('entering else')
                for item in temp_list_note:
                    print("item")
                    print(item)
                    temp_note += " and " + item
                if not list_temp[1]:
                    temp_note += " and " + list_temp[2] + "\n"
                else:
                    temp_note += " and " + list_temp[1] + " and " + list_temp[2]
                list_note.append(temp_note)

    print(list_note)
    return list_note


### arithmetic 'and' implement
def replace_add(st, inp_op, globalVariables):
    flag = 0
    list_of_values = st.split('+')
    if len(list_of_values) == 1:
        return st
    for value in list_of_values:
        value = value.strip()
        if value in globalVariables.field_set:
            var_type = ''
            if inp_op == 0:
                if value in globalVariables.dict_type:
                    var_type = globalVariables.dict_type[value]
            else:
                if value in globalVariables.dict_op_type:
                    var_type = globalVariables.dict_op_type[value]
            if var_type == 'integer':
                flag = 1
                break

        if value.isdigit():
            flag = 1
            print("Yes")
            break
        ll = value.split()
        for it in ll:
            if it == 'integer' or it == 'product' or it == 'divide':
                flag = 1
                break
    if flag == 1:
        res = ' and '.join(list_of_values)
        return 'addition of ' + res
    else:
        return ' + '.join(list_of_values)


### arithmetic 'multiply' implement
def replace_mul(st, globalVariables):
    i = 0
    print(st)
    while i < len(st):
        if st[i] == '*' or st[i] == '/':
            print("HU")
            j = i
            while st[j] != '+' and j > 0:
                j = j - 1
            if j != 0:
                j = j + 1
            print(j)
            print(st[i])
            if (st[i]) == '*':
                st = st[:j] + " product of " + st[j:]  # replacing *.. putitng product of
                i = i + 12  # skipping string "product of"
            else:
                print("LLLLLLLLLL")
                st = st[:j] + " divide " + st[j:]  # similar to multiply
                i = i + 8
            print(st)
            print(st[i])
            print("SDS")
            while i < len(st) and st[i] != '+':
                i = i + 1
        i = i + 1
    st = st.replace('*', " and ")  # for multiple variables multiplying
    st = st.replace('/', " by ")
    return st


### for the right side in the notes, remove variables...
### temp_dict will be given to get the values to be replaced with
def get_dest(dest, temp_dict, dc, globalVariables):
    print("entering get_dest")  # dest is the right side of the rule
    print(temp_dict)  # temp_dict would be having the value of the variables
    temp_list = dest.split('+')
    print("result of split")
    print(temp_list)
    for ind, var in enumerate(temp_list):
        var = var.replace(';', '')
        ll = var.split()
        print("result of splitting")
        print(ll)
        for i, tk in enumerate(ll):
            if tk.strip() in temp_dict:
                if temp_dict[tk]:
                    res = temp_dict[tk][
                        0]  # one var could have multiple values assigned at diff places...extracting the first one
                    dc[tk] = res  # putting the extracted value into a temp dictionary dc
                    temp_dict[tk].pop(0)  # removing the extracted value
                    temp = get_dest(res, temp_dict, dc, globalVariables)
                    ll[i] = temp
        temp_list[ind] = ' '.join(ll)

    return '+'.join(temp_list)


def format_ind_note(note, globalVariables):
    print("FORMAT_IND_NOTE")
    note = note.replace('=', ' = ')
    ll = note.split()
    for i in ll:
        if i == 'CODELIST':
            return note
    print("entering formatting::::::")
    format_dict = {}
    note = note.replace('!=""', " is not empty ")
    note = note.replace('&', " and ")
    note = note.replace('! = ""', " is not empty ")
    note = note.replace('Populate', 'Populate ')
    note = note.replace('|', " or ")
    c_t = note.split('then')  # separating the condition and the rule
    if len(c_t) == 1:
        return note
    condition_list = re.split('and', c_t[0])  # get all conditions -- ct[0] is the string having all conditions
    print("result of splitting on and")
    print(condition_list)
    for x_ind, x in enumerate(condition_list):
        condition_list[x_ind] = x.strip()
    print("after removing spaces")
    print(condition_list)
    condition_list_new = []
    for x in condition_list:  # to exclude the repetitive conditions
        if x.lower() not in (name.lower() for name in condition_list_new):  # removing duplicate conditions
            condition_list_new.append(x)
    # condition_list=list(set(condition_list))
    print(condition_list_new)
    for index, condition in enumerate(condition_list_new):
        print(condition)
        condition = condition.replace('Else', '')
        condition = condition.replace('if', '')
        condition = condition.replace('If', '')
        condition = condition.replace(';', '')
        var_list = condition.split('=')
        print("result of splitting on ========")
        print(var_list)
        temp_string = var_list[0].replace('!', '')
        if len(var_list) == 2:
            print("is it here")
            if var_list[0].strip() == var_list[1].strip():  # if it is a "var=var" type of conditions, remove it
                print("is it an equal condition")
                print(condition)
                condition_list_new[index] = ''
            elif ((var_list[0].strip() in globalVariables.variable_set) and (len(var_list[0].split()) == 1)) or (
                    temp_string.strip() in globalVariables.variable_set):  # if it is "var=a" type of condition
                print("or here")
                if var_list[0].strip() in format_dict:  # if the value of variable is known, dont remove the condition
                    continue
                format_dict[var_list[0].strip()] = var_list[1]  # saving the value of var in format_dict
                condition_list_new[index] = ''  # remove the condition after saving it
                print(condition_list_new)
                # exit()

    # for item in enumerate(condition_list):
    #     if item=='':
    #         condition_list.remove(item)
    condition_list_new = list(filter(None, condition_list_new))  # to reomve empty conditions
    print("this is the foramtting dictionary")
    print(format_dict)

    for index, condition in enumerate(condition_list_new):
        var_list = condition.split()
        for ind, item in enumerate(var_list):
            if item.strip() in format_dict:  # if anywhere a variable is being referred, replace it with its saved value
                var_list[ind] = format_dict[item]
        condition_list_new[index] = ' '.join(var_list)

    for index, condition in enumerate(condition_list_new):
        print("variableremove")
        var_list = condition.split()
        for ind, item in enumerate(var_list):
            temp_string = item.replace('!', '')
            if temp_string.strip() in globalVariables.variable_set:
                print(temp_string)
                print(condition_list_new)  # if anywhere a variable is being referred, replace it with its saved value
                condition_list_new[index] = ''
                print(condition_list_new)
                if temp_string == 'Var_LIN03':
                    exit()
                break
    condition_list_new = list(filter(None, condition_list_new))

    return_note = ' and '.join(condition_list_new)
    # return_note='If '+return_note
    return return_note + " then " + c_t[1]  # c_t[1] is the rule


def final_note_for_field(field_ptr, temp_id, inp_op, globalVariables):
    if inp_op == 0:
        temp_list = globalVariables.dict_op[temp_id]
        # globalVariables.f.write(temp_list[0] + " Mapped to " + globalVariables.dict_useless[temp_id] + "\n")
    else:
        # globalVariables.f.write("FIELD: " + temp_id+"\n")
        temp_list = [temp_id]

    note = ""
    temp_dict = {}
    print("field")
    print(temp_list[0])
    count = 0
    list_recur = []
    list_note = find_in_dict_token(temp_list[0], note, temp_dict, inp_op, '', list_recur, globalVariables)

    print(list_note)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(temp_dict)
    if not list_note:
        return

    if list_note[0].split()[0] == 'Hardcode':
        return list_note[0]
    final_note = ""
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(list_note)
    for list_temp in list_note:
        lines = list_temp.split("\n")

        for line in lines:
            ind_note = ''
            if line:

                ll = line.split()
                sql = 0
                if len(ll) >= 2 and ll[0] == 'and' and ll[1].lower() == 'if':
                    ll.pop(0)
                if ll[0].lower() == 'select':
                    sql = 1
                if ll[0].lower() == "if":
                    ll.pop(0)
                    # if flag==0:
                    ll.insert(0, "If")
                    #     flag=1
                    # else:
                    #     ll.insert(0,"Else if")
                l = len(ll) - 1
                equal_ind = 0
                while l != 0:
                    if (ll[l] == '='):
                        equal_ind = l
                    if (ll[l] == 'and'):
                        ll[l] = 'then'
                        break
                    l = l - 1
                if equal_ind != 0:
                    del ll[l + 1:equal_ind + 1]
                    if l == 0:
                        ll[0] = " Map  "
                    else:
                        ll.insert(l + 1, " Map  ")

                    ind_note = ' '.join(ll)
                    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                    print(ind_note)
                    dest_temp = ind_note.split('Map ')
                    dest = dest_temp[1]
                    print(dest)
                    dc = {}
                    dd = get_dest(dest, temp_dict, dc, globalVariables)
                    print(dd)
                    print("thois is dd")
                    print(dc)
                    print("printing the dictionary created")
                    dest_temp[0] = dest_temp[0].replace('!=""', " is not empty ")
                    split_list = re.split('\s', dest_temp[0])
                    print(split_list)
                    print("list split")
                    for split_ind, split_item in enumerate(split_list):
                        if split_item in dc:
                            split_list[split_ind] = dc[split_item]
                    split_result = ' '.join(split_list)
                    fla = 1
                    print(dd)
                    while fla == 1:
                        print("HI")
                        fla = 0
                        if dd.find('" ') >= 0:
                            dd = dd.replace('" ', '"')
                            fla = 1
                            print("FIRST")
                        if dd.find(' "') >= 0:
                            dd = dd.replace(' "', '"')
                            fla = 1
                            print("sec")
                    dd = dd.replace('+', ' + ')
                    dd = dd.replace('""', '" "')
                    print(dd)
                    if dd[0] == '"':
                        dd_t = replace_mul(dd, globalVariables)
                        dd_t = dd_t.replace("divide  \" by \"", "\"/\"")
                        dd_t = replace_add(dd_t, inp_op, globalVariables)
                        if dd_t.find('divide') == -1 and dd_t.find('by') != -1:
                            dd_t = dd_t.replace('by', 'divided by')
                        if sql == 0:
                            ind_note = split_result + " Populate " + dd_t
                        else:
                            ind_note = split_result + " and name = " + dd_t
                            ind_note = ind_note.replace(' then ', '')
                    else:
                        dd_t = replace_mul(dd, globalVariables)
                        dd_t = dd_t.replace("divide  \" by \"", "\"/\"")
                        dd_t = replace_add(dd_t, inp_op, globalVariables)
                        if dd_t.find('divide') == -1 and dd_t.find('by') != -1:
                            dd_t = dd_t.replace('by', 'divided by')
                        ind_note = split_result + ' Map  ' + dd_t
                else:
                    ind_note = ' '.join(ll)
                fla = 1
                # print(dd)

                while fla == 1:
                    print("HI")
                    fla = 0
                    if ind_note.find('" ') >= 0:
                        ind_note = ind_note.replace('" ', '"')
                        fla = 1
                        print("FIRST")
                    if ind_note.find(' "') >= 0:
                        ind_note = ind_note.replace(' "', '"')
                        fla = 1
                        print("sec")
                ind_note = ind_note.replace("\"then", "\" then")

                print(ind_note)

                # print(dd)
                print(ind_note)
                print("ind_note")
                ind_note = format_ind_note(ind_note, globalVariables)

                print(ind_note)
                print("ind_note")

                final_note += (ind_note + "\n")
                final_note = final_note.replace('  ', ' ')
                print("KK")
                print(final_note)
                print("DS3")
    print(final_note)
    print("fInalnote")
    if final_note.split()[0] == 'then':
        final_note = final_note.replace(' then  ', '')

    return final_note


### to generate notes for each of the fields
def output_field_note(field_ptr, inp_op, globalVariables):
    if field_ptr[3].text == '0':
        return
    if inp_op == 0:
        temp_id = field_ptr[0].text
        final_note = ''
        if temp_id in globalVariables.dict_op_ct:
            print(temp_id)
            const_val = int(globalVariables.dict_op_ct[temp_id][0])
            if const_val in globalVariables.dict_constant:
                globalVariables.f.write("FIELD: " + globalVariables.dict_useless[temp_id] + "\n")
                if globalVariables.dict_op_ct[temp_id][1]:
                    final_note += "If " + globalVariables.dict_1[globalVariables.dict_op_ct[temp_id][1]][
                        2] + " exists then "
                final_note += "Hardcode " + "\"" + globalVariables.dict_constant[const_val][2] + "\"" + '\n'
                print(final_note)
                globalVariables.f.write(final_note)
                globalVariables.f.write('\n')
                # globalVariables.f.write('\n')
                globalVariables.dict_notes[field_ptr[1].text][0] = final_note

        select_stmt = ''
        if temp_id in globalVariables.dict_op_select:
            v = globalVariables.dict_op_select[temp_id]
            fieldto = globalVariables.dict_useless[temp_id]
            fieldfrom = globalVariables.dict_useless[v[3]]
            select_stmt = "Populate " + v[2] + " from CODELIST = " + globalVariables.dict_constant[int(v[1])][
                2] + " into " + fieldto + " where " + v[0] + " = " + fieldfrom + '\n'
            globalVariables.dict_notes[field_ptr[1].text][1] = select_stmt

        date_note = ''
        if temp_id in globalVariables.dict_op_date:
            format = globalVariables.dict_op_date[temp_id][1]
            date_note = "Map current DateTime in format " + format
            globalVariables.dict_notes[field_ptr[1].text][5] = date_note

        if temp_id in globalVariables.dict_op:
            link_note = final_note_for_field(field_ptr, temp_id, 0, globalVariables)
            if link_note:
                globalVariables.dict_notes[field_ptr[1].text][2] = link_note


    else:
        temp_id = field_ptr[1].text
        output_note = ''
        if temp_id in globalVariables.dict_op_token:
            if temp_id in globalVariables.dict_opposite_name_id:
                field_id = globalVariables.dict_opposite_name_id[temp_id]
            output_note = final_note_for_field(field_ptr, temp_id, 1, globalVariables)
            if output_note[0] == '#':
                output_note = 'Populate ' + output_note.split('Populate')[1]
            globalVariables.dict_notes[field_ptr[1].text][3] = output_note


def output_seg_note_op(seg_ptr, globalVariables):
    for children in seg_ptr:
        if children.tag.split('}')[1] == "Composite":
            output_seg_note_link(children, globalVariables)
            output_seg_note_op(children, globalVariables)
        elif children.tag.split('}')[1] == "Field":
            output_field_note(children, 1, globalVariables)


def output_seg_note_link(seg_ptr, globalVariables):
    for children in seg_ptr:
        if children.tag.split('}')[1] == "Composite":
            output_seg_note_link(children, globalVariables)
            output_seg_note_op(children, globalVariables)
        elif children.tag.split('}')[1] == "Field":
            output_field_note(children, 0, globalVariables)


def output_group_note(group_ptr, globalVariables):
    for children in group_ptr:
        if children.tag.split('}')[1] == "Group":
            output_group_note(children, globalVariables)
        elif children.tag.split('}')[1] == "Segment":
            output_seg_note_link(children, globalVariables)
            output_seg_note_op(children, globalVariables)
        elif children.tag.split('}')[1] == "PosRecord":
            output_seg_note_link(children, globalVariables)
            output_seg_note_op(children, globalVariables)
        elif children.tag.split('}')[1] == "VarDelimRecord":
            output_seg_note_link(children, globalVariables)
            output_seg_note_op(children, globalVariables)


def xml_output_rec_note_link(rec_ptr, globalVariables):
    for children in rec_ptr:
        if children.tag.split('}')[1] == "Field":
            output_field_note(children, 0, globalVariables)


def xml_output_rec_note_op(rec_ptr, globalVariables):
    for children in rec_ptr:
        if children.tag.split('}')[1] == "Field":
            output_field_note(children, 1, globalVariables)


def xml_output_particle_note(particle_ptr, globalVariables):
    for children in particle_ptr:
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_note(children, globalVariables)
        if children.tag.split('}')[1] == "XMLParticleGroup":
            xml_output_particle_note(children, globalVariables)


def xml_output_group_note(group_ptr, globalVariables):
    for children in group_ptr:
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_note(children, globalVariables)
        elif children.tag.split('}')[1] == "XMLParticleGroup":
            xml_output_particle_note(children, globalVariables)
        elif children.tag.split('}')[1] == "XMLRecord":
            xml_output_rec_note_link(children, globalVariables)
            xml_output_rec_note_op(children, globalVariables)


def edi_make_notes(data_root, globalVariables):
    for child in data_root[4][0]:
        if child.tag.split('}')[1] == "Group":
            output_group_note(child, globalVariables)
    # print(globalVariables.dict_notes)


def xml_make_notes(data_root, globalVariables):
    for child in data_root[4][0]:
        if child.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_note(child, globalVariables)


def initialize_const_Map(data_root, globalVariables):
    sowmith = 0
    # if data_root.text=='UseConstant':
    print(len(data_root))
    # exit()
    # if len(data_root)>=7:
    for real_child in data_root:
        if real_child.tag.split('}')[1] == 'ConstantMap':
            for child in real_child:
                print("SA")
                print(data_root[6])
                const_list = [str(child[0].text), str(child[1].text), str(child[2].text)]
                globalVariables.dict_constant[sowmith] = const_list
                sowmith = sowmith + 1


def check_for_note(list_from_dict, i, globalVariables):
    note = ''
    output_note = list_from_dict[3]
    output_note_list = output_note.split('\n')
    print(output_note_list)
    flag = 0
    for line in output_note_list:
        line_list = line.split()
        if 'accumulator' in line_list:
            note = list_from_dict[4]
            break
        if not line:
            continue
        if (line.split()[0].lower() == 'populate' or line.split()[0].lower() == 'hardcode') and len(
                line.split('+')) == 1:
            note = line
            break
        # note=''
        if i != 3 and flag == 0:
            note = list_from_dict[i]
            flag = 1
        if line.split()[0].lower() == 'if':
            note = note + "\n" + line + "\n"
        elif line.split()[0].lower() == 'select':
            note = note + "\n" + line + "\n"
            split_list = line.split()
            end_ptr = len(split_list) - 1
            while split_list[end_ptr] != '=':
                end_ptr = end_ptr - 1
            split_list_res = split_list[end_ptr + 1:]
            fields = ' '.join(split_list_res)
            field_list = fields.split('+')
            flag = 0
            for item in field_list:
                item_id = ''
                if item.strip() in globalVariables.dict_opposite:  # globalVariables.dict_opposite to be created -- with key as name of the field and value as name
                    item_id = globalVariables.dict_opposite[item.strip()]
                elif item.strip() in globalVariables.dict_opposite_out:
                    item_id = globalVariables.dict_opposite_out[item.strip()]
                if item_id in globalVariables.dict_notes:
                    if globalVariables.dict_notes[item_id.strip()][2]:
                        if flag == 0:
                            note += "where " + item_id + " is: " + '\n'
                            note += globalVariables.dict_notes[item_id.strip()][2]
                            flag = 1
                        else:
                            note += "and " + item_id + " is: " + '\n'
                            note += globalVariables.dict_notes[item_id.strip()][2]

        elif line.split()[0].lower() == 'update':
            note = note + "\n" + line + "\n"
        else:
            note = note + line
    if note:
        return note
    else:
        return output_note


def change_format(note, i_f, o_f, globalVariables):
    note = note.replace('minus999', '-')
    note = note.replace('plus999', '+')
    note = note.replace('divide999', '/')
    note = note.replace('multiply999', '*')
    note = note.replace('less999', '<')
    note = note.replace('greater999', '>')
    note = note.replace('leftshift999', '<<')
    note = note.replace('rightshift999', '>>')
    print("change_format")
    line_list = note.split('\n')
    for line_ind, line in enumerate(line_list):
        print(line)
        token_list = line.split()
        for ind, token in enumerate(token_list):
            if token in globalVariables.dict_opposite:
                field = globalVariables.dict_opposite[token]
                if field in globalVariables.dict_name_id:  ## that is it's input field
                    if i_f == 'IDOC' or i_f == 'XML' or i_f == 'CSV':
                        field_id = (globalVariables.dict_name_id[field])
                        # print(globalVariables.dict_1)
                        # exit()
                        field_name_list = globalVariables.dict_1[field_id]
                        token_list[ind] = field_name_list[1] + "/" + field_name_list[2]
                    if i_f == 'EDI':
                        grp_name = globalVariables.dict_opposite_group[token]
                        if grp_name != globalVariables.inp_grp_name:
                            # token_list[ind] = grp_name+"/"+''.join(globalVariables.dict_tag_out[token])
                            if globalVariables.dict_tag_inp[token][0]:
                                token_list[ind] = grp_name + "/" + ''.join(globalVariables.dict_tag_inp[token])
                            else:
                                token_list[ind] = grp_name + "/" + token
                        else:
                            print(globalVariables.dict_tag_inp[token])
                            # token_list[ind] = ''.join(globalVariables.dict_tag_out[token])
                            if globalVariables.dict_tag_inp[token][0]:
                                token_list[ind] = ''.join(globalVariables.dict_tag_inp[token])
                            else:
                                token_list[ind] = token
                        # if grp_name!=globalVariables.inp_grp_name:
                        #     token_list[ind] = grp_name+"/"+''.join(globalVariables.dict_tag_inp[token]) #dict_tag_inp[token]-tagName+sequenceNumber
                        # else:
                        #     token_list[ind] = ''.join(globalVariables.dict_tag_inp[token])
            elif token in globalVariables.dict_opposite_out:
                field = globalVariables.dict_opposite_out[token]
                if field in globalVariables.dict_opposite_name_id:  ## that is it's output field
                    print("is ite herer")
                    if o_f == 'IDOC' or o_f == 'XML' or o_f == 'CSV':
                        field_id = globalVariables.dict_opposite_name_id[field]
                        print("yo")
                        print(field_id)
                        field_name_list = globalVariables.dict_1[field_id]
                        token_list[ind] = field_name_list[1] + "/" + field_name_list[2]
                    if o_f == 'EDI':
                        print("FD")
                        print(token)
                        grp_name = globalVariables.dict_opposite_group_out[token]
                        if grp_name != globalVariables.out_grp_name:
                            # token_list[ind] = grp_name+"/"+''.join(globalVariables.dict_tag_out[token])
                            if globalVariables.dict_tag_out[token][0]:
                                token_list[ind] = grp_name + "/" + ''.join(globalVariables.dict_tag_out[token])
                            else:
                                token_list[ind] = grp_name + "/" + token
                        else:
                            print(globalVariables.dict_tag_out[token])
                            # token_list[ind] = ''.join(globalVariables.dict_tag_out[token])
                            if globalVariables.dict_tag_out[token][0]:
                                token_list[ind] = ''.join(globalVariables.dict_tag_out[token])
                            else:
                                token_list[ind] = token
        print(' '.join(token_list))
        line_list[line_ind] = ' '.join(token_list)
    print('\n'.join(line_list))
    return '\n'.join(line_list)


def output_field_note_combine(field_ptr, i_f, o_f, pseudo_pointer, globalVariables):
    # print("output_field_note_combine")
    # if field_ptr[3].text=='0':
    #     return
    if field_ptr[3].text == '0':
        if o_f == "XML":
            globalVariables.link_notes_set.discard(pseudo_pointer[0].text)
            globalVariables.standard_notes_set.discard(pseudo_pointer[0].text)
            globalVariables.extended_notes_set.discard(pseudo_pointer[0].text)
        else:
            globalVariables.link_notes_set.discard(field_ptr[0].text)
            globalVariables.standard_notes_set.discard(field_ptr[0].text)
            globalVariables.extended_notes_set.discard(field_ptr[0].text)
        return

    globalVariables.f.write("field name")
    globalVariables.f.write(field_ptr[1].text)
    globalVariables.f.write("\n")

    temp_id = field_ptr[1].text

    list_from_dict = globalVariables.dict_notes[temp_id]
    if not list_from_dict[0] and not list_from_dict[1] and not list_from_dict[2] and not list_from_dict[3] and not \
    list_from_dict[4] and not list_from_dict[5]:
        return
    print(list_from_dict)
    print("DS1")
    if list_from_dict[0]:
        if o_f == "XML":
            globalVariables.link_notes_set.discard(pseudo_pointer[0].text)
            globalVariables.standard_notes_set.discard(pseudo_pointer[0].text)
        else:
            globalVariables.standard_notes_set.discard(field_ptr[0].text)
            globalVariables.link_notes_set.discard(field_ptr[0].text)
        if list_from_dict[3]:
            note = ''
            note = check_for_note(list_from_dict, 0, globalVariables)
            note = change_format(note, i_f, o_f, globalVariables)
            print("CH")
            print(note)
            # exit()
            note_note = note.split()
            if note_note[0].lower() == 'hardcode':
                note_note[1] = '"' + note_note[1]
                note_note[len(note_note) - 1] = note_note[len(note_note) - 1] + '"'
            note = ' '.join(note_note)
            field_ptr[5].text = note
            if o_f == "XML":
                globalVariables.extended_notes_set.discard(pseudo_pointer[0].text)
            else:
                globalVariables.extended_notes_set.discard(field_ptr[0].text)
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')

        else:
            note = list_from_dict[0]
            note_tmp = note.split('\n')
            for j, notes in enumerate(note_tmp):
                tokens = notes.split()
                print("toks")
                print(tokens)
                for i, token in enumerate(tokens):
                    if token in globalVariables.dict_ind_field:
                        tokens[i] = ''.join(globalVariables.dict_ind_field[token])
                notes = ' '.join(tokens)
                note_tmp[j] = notes
            note = '\n'.join(note_tmp)
            note = change_format(note, i_f, o_f, globalVariables)
            field_ptr[5].text = note
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')
        return

    if list_from_dict[4]:
        if o_f == "XML":
            globalVariables.link_notes_set.discard(pseudo_pointer[0].text)
            globalVariables.standard_notes_set.discard(pseudo_pointer[0].text)
        else:
            globalVariables.standard_notes_set.discard(field_ptr[0].text)
            globalVariables.link_notes_set.discard(field_ptr[0].text)
        if list_from_dict[3]:
            note = ''
            note = check_for_note(list_from_dict, 4, globalVariables)
            note_note = note.split()
            if note_note[0].lower() == 'hardcode':
                note_note[1] = '"' + note_note[1]
                note_note[len(note_note) - 1] = note_note[len(note_note) - 1] + '"'
            note = ' '.join(note_note)
            field_ptr[5].text = note
            if o_f == "XML":
                globalVariables.extended_notes_set.discard(pseudo_pointer[0].text)
            else:
                globalVariables.extended_notes_set.discard(field_ptr[0].text)
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')
        else:
            note = list_from_dict[4]
            note_tmp = note.split('\n')
            for j, notes in enumerate(note_tmp):
                tokens = notes.split()
                print("toks")
                print(tokens)
                for i, token in enumerate(tokens):
                    if token in globalVariables.dict_ind_field:
                        tokens[i] = ''.join(globalVariables.dict_ind_field[token])
                notes = ' '.join(tokens)
                note_tmp[j] = notes
            note = '\n'.join(note_tmp)
            note = change_format(note, i_f, o_f, globalVariables)
            field_ptr[5].text = note
            print("IS IT PRINTING>>>>>>>>>>>>>>>>>>>>>>IS IT >>>>>>>>>>>>>>>IS IT")
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')
        return

    if list_from_dict[5]:
        if o_f == "XML":
            globalVariables.link_notes_set.discard(pseudo_pointer[0].text)
            globalVariables.standard_notes_set.discard(pseudo_pointer[0].text)
        else:
            globalVariables.standard_notes_set.discard(field_ptr[0].text)
            globalVariables.link_notes_set.discard(field_ptr[0].text)
        if list_from_dict[3]:
            note = ''
            note = check_for_note(list_from_dict, 5, globalVariables)
            note = change_format(note, i_f, o_f, globalVariables)
            note_note = note.split()
            if note_note[0].lower() == 'hardcode':
                note_note[1] = '"' + note_note[1]
                note_note[len(note_note) - 1] = note_note[len(note_note) - 1] + '"'
            note = ' '.join(note_note)
            field_ptr[5].text = note
            if o_f == "XML":
                globalVariables.extended_notes_set.discard(pseudo_pointer[0].text)
            else:
                globalVariables.extended_notes_set.discard(field_ptr[0].text)
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')
        else:
            note = list_from_dict[5]
            # note_tmp=note.split('\n')
            # for j,notes in enumerate(note_tmp):
            #     tokens=notes.split()
            #     print("toks")
            #     print(tokens)
            #     for i,token in enumerate(tokens):
            #         if token in globalVariables.dict_ind_field:
            #             tokens[i]=''.join(globalVariables.dict_ind_field[token])
            #     notes =' '.join(tokens)
            #     note_tmp[j]=notes
            # note='\n'.join(note_tmp)
            # note=change_format(note,i_f,o_f,globalVariables)
            field_ptr[5].text = note
            print("IS IT PRINTING>>>>>>>>>>>>>>>>>>>>>>IS IT >>>>>>>>>>>>>>>IS IT")
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')
        return

    if list_from_dict[1]:
        if o_f == "XML":
            globalVariables.link_notes_set.discard(pseudo_pointer[0].text)
            globalVariables.standard_notes_set.discard(pseudo_pointer[0].text)
        else:
            globalVariables.standard_notes_set.discard(field_ptr[0].text)
            globalVariables.link_notes_set.discard(field_ptr[0].text)
        note = list_from_dict[1]
        split_list = note.split()
        end_ptr = len(split_list) - 1
        while split_list[end_ptr] != '=':
            end_ptr = end_ptr - 1
        split_list_res = split_list[end_ptr + 1:]
        print(split_list_res)
        fields = ' '.join(split_list_res)
        field_list = fields.split('+')
        print(field_list)
        flag = 0
        for item in field_list:
            if item.strip() in globalVariables.dict_notes:
                if globalVariables.dict_notes[item.strip()][2]:
                    if flag == 0:
                        note += "where " + item + " is: " + '\n'
                        note += globalVariables.dict_notes[item.strip()][2]
                        flag = 1
                    else:
                        note += "and " + item + " is: " + '\n'
                        note += globalVariables.dict_notes[item.strip()][2]
            print(note)

        if list_from_dict[3]:
            note = check_for_note(list_from_dict, 1, globalVariables)
            note_note = note.split()
            if note_note[0].lower() == 'hardcode':
                note_note[1] = '"' + note_note[1]
                note_note[len(note_note) - 1] = note_note[len(note_note) - 1] + '"'
            note = ' '.join(note_note)
            if o_f == "XML":
                globalVariables.extended_notes_set.discard(pseudo_pointer[0].text)
            else:
                globalVariables.extended_notes_set.discard(field_ptr[0].text)
        note_tmp = note.split('\n')
        for j, notes in enumerate(note_tmp):
            tokens = notes.split()
            print("toks")
            print(tokens)
            for i, token in enumerate(tokens):
                if token in globalVariables.dict_ind_field:
                    tokens[i] = ''.join(globalVariables.dict_ind_field[token])
            notes = ' '.join(tokens)
            note_tmp[j] = notes
        note = '\n'.join(note_tmp)
        note = change_format(note, i_f, o_f, globalVariables)
        field_ptr[5].text = note
        globalVariables.f.write("************" + '\n')
        globalVariables.f.write(note)
        globalVariables.f.write('\n')
        return

    if list_from_dict[2]:
        if o_f == "XML":
            globalVariables.link_notes_set.discard(pseudo_pointer[0].text)
        else:
            globalVariables.link_notes_set.discard(field_ptr[0].text)
        if list_from_dict[3]:
            note = ''
            note = check_for_note(list_from_dict, 2, globalVariables)
            note = change_format(note, i_f, o_f, globalVariables)
            note_note = note.split()
            if note_note[0].lower() == 'hardcode':
                note_note[1] = '"' + note_note[1]
                note_note[len(note_note) - 1] = note_note[len(note_note) - 1] + '"'
            note = ' '.join(note_note)
            new_line = note.split()
            new_line_count = 0;
            if new_line[0] == 'Map':
                new_line[1] = new_line[1] + "\n"
            # for ind,c in enumerate(new_line):
            #     if c=='Map':
            #         new_line_count+=1
            #         if new_line_count>1:
            #             new_line[ind]="\n"+c
            #             print(new_line)
            note = ' '.join(new_line)

            field_ptr[5].text = note
            if o_f == "XML":
                globalVariables.extended_notes_set.discard(pseudo_pointer[0].text)
            else:
                globalVariables.extended_notes_set.discard(field_ptr[0].text)
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')
        else:
            note = list_from_dict[2]
            note_tmp = note.split('\n')
            for j, notes in enumerate(note_tmp):
                tokens = notes.split()
                print("toks")
                print(tokens)
                for i, token in enumerate(tokens):
                    if token in globalVariables.dict_ind_field:
                        print(globalVariables.dict_ind_field[token])
                        if globalVariables.dict_ind_field[token][1] != '$$$':
                            tokens[i] = ''.join(globalVariables.dict_ind_field[token])
                notes = ' '.join(tokens)
                note_tmp[j] = notes
            note = '\n'.join(note_tmp)
            print(note)
            note = change_format(note, i_f, o_f, globalVariables)
            dollar = note.split()[1]
            if len(dollar) > 1:
                if dollar[1] == '$':
                    note = ''
            field_ptr[5].text = note
            globalVariables.f.write("************" + '\n')
            globalVariables.f.write(note)
            globalVariables.f.write('\n')
        return

    if list_from_dict[3]:
        note = ''
        note = check_for_note(list_from_dict, 3, globalVariables)
        print("d")
        print(note)
        note = change_format(note, i_f, o_f, globalVariables)
        print(note)
        # exit()
        # print(note)
        note_note = note.split()
        if note_note[0].lower() == 'hardcode':
            note_note[1] = '"' + note_note[1]
            note_note[len(note_note) - 1] = note_note[len(note_note) - 1] + '"'
        note = ' '.join(note_note)
        field_ptr[5].text = note
        if o_f == "XML":
            globalVariables.extended_notes_set.discard(pseudo_pointer[0].text)
        else:
            globalVariables.extended_notes_set.discard(field_ptr[0].text)
        # print("g")
        # print(note)
        # print("globalVariables.F")
        # print(field_ptr[5].text)
        # exit()
        globalVariables.f.write("************" + '\n')
        globalVariables.f.write(note)
        globalVariables.f.write('\n')


def output_seg_note_combine(seg_ptr, inp_format, out_format, globalVariables):
    for children in seg_ptr:
        if children.tag.split('}')[1] == "Composite":
            output_seg_note_combine(children, inp_format, out_format, globalVariables)
        elif children.tag.split('}')[1] == "Field":
            output_field_note_combine(children, inp_format, out_format, '', globalVariables)


def output_group_note_combine(group_ptr, inp_format, out_format, globalVariables):
    for children in group_ptr:
        if children.tag.split('}')[1] == "Group":
            output_group_note_combine(children, inp_format, out_format, globalVariables)
        elif children.tag.split('}')[1] == "Segment":
            output_seg_note_combine(children, inp_format, out_format, globalVariables)
        elif children.tag.split('}')[1] == "PosRecord":
            output_seg_note_combine(children, inp_format, out_format, globalVariables)
        elif children.tag.split('}')[1] == "VarDelimRecord":
            output_seg_note_combine(children, inp_format, out_format, globalVariables)


def xml_output_rec_note_combine(rec_ptr, i_f, o_f, group_ptr, globalVariables):
    # print("rec")
    rec_type = ''
    for children in rec_ptr:
        if children.tag.split('}')[1] == "RecordType":
            rec_type = children.text
        if children.tag.split('}')[1] == "Field":
            if rec_type.lower() == 'pcdata':
                output_field_note_combine(group_ptr, i_f, o_f, children, globalVariables)
            else:
                output_field_note_combine(children, i_f, o_f, children, globalVariables)


def xml_output_particle_note_combine(particle_ptr, i_f, o_f, globalVariables):
    # print("particle")
    for children in particle_ptr:
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_note_combine(children, i_f, o_f, globalVariables)
        if children.tag.split('}')[1] == "XMLParticleGroup":
            xml_output_particle_note_combine(children, i_f, o_f, globalVariables)


def xml_output_group_note_combine(group_ptr, i_f, o_f, globalVariables):
    # print("grouop")
    for children in group_ptr:
        if children.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_note_combine(children, i_f, o_f, globalVariables)
        elif children.tag.split('}')[1] == "XMLParticleGroup":
            xml_output_particle_note_combine(children, i_f, o_f, globalVariables)
        elif children.tag.split('}')[1] == "XMLRecord":
            xml_output_rec_note_combine(children, i_f, o_f, group_ptr, globalVariables)


def edi_populate_notes(data_root, i_f, o_f, globalVariables):
    for child in data_root[4][0]:
        if child.tag.split('}')[1] == "Group":
            output_group_note_combine(child, i_f, o_f, globalVariables)


def xml_populate_notes(data_root, i_f, o_f, globalVariables):
    for child in data_root[4][0]:
        if child.tag.split('}')[1] == "XMLElementGroup":
            xml_output_group_note_combine(child, i_f, o_f, globalVariables)


# out_list=answer.split('/')
# output_file=out_list[len(out_list)-1]
# output_file='output' + '/'+output_file

def sort_java_arr(globalVariables):
    # adding fields having java code to arr_java_out
    for item in globalVariables.arr_java_inp:
        if item in globalVariables.dict_name_id:
            globalVariables.arr_java_out.add(globalVariables.dict_name_id[item])
        if item in globalVariables.dict_opposite_name_id:
            globalVariables.arr_java_out.add(globalVariables.dict_opposite_name_id[item])
    globalVariables.link_notes_set.difference_update(
        globalVariables.standard_notes_set)  # if a field has link+standard rule, it should be removed from link_set
    globalVariables.link_notes_set.difference_update(globalVariables.extended_notes_set)  # similar logic
    globalVariables.link_notes_set.difference_update(globalVariables.arr_java_out)

    globalVariables.standard_notes_set.difference_update(globalVariables.extended_notes_set)
    globalVariables.standard_notes_set.difference_update(globalVariables.arr_java_out)
    globalVariables.extended_notes_set.difference_update(globalVariables.arr_java_out)


def write_func(data_root, etree, raw_data, filenameUploaded, outputPath, globalVariables):
    print(filenameUploaded)
    # # exit()
    # out_list=answer.split('/')
    # output_file=out_list[len(out_list)-1]
    # output_file='output' + '\\'+output_file
    # output_file=os.getcwd()+'\\'+output_file
    # output_file=output_file.replace('\\','/')
    # print(output_file)
    # print("S")
    # # exit()
    finalNotesPath = outputPath + '/' + filenameUploaded
    data_root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    etree.register_namespace("", "http://www.stercomm.com/SI/Map")
    raw_data.write(finalNotesPath, encoding='utf-8', xml_declaration=True)
    # globalVariables.f.close()
    return finalNotesPath


def make_log(lf, globalVariables):
    for item in globalVariables.arr_java_out:
        field_list = globalVariables.dict_1[item]
        field = field_list[1] + '/' + field_list[2]
        note = "Field " + field + " has java code."
        lf.write(note)
        lf.write('\n')
    for item in globalVariables.link_notes_set:
        field_list = globalVariables.dict_1[item]
        field = field_list[1] + '/' + field_list[2]
        note = "Field " + field + " having link, not populated"
        lf.write(note)
        lf.write('\n')
    for item in globalVariables.standard_notes_set:
        field_list = globalVariables.dict_1[item]
        field = field_list[1] + '/' + field_list[2]
        note = "Field " + field + " having standard rule, not populated"
        lf.write(note)
        lf.write('\n')
    for item in globalVariables.extended_notes_set:
        field_list = globalVariables.dict_1[item]
        field = field_list[1] + '/' + field_list[2]
        note = "Field " + field + " having extended rule, not populated"
        lf.write(note)
        lf.write('\n')
    if globalVariables.list_dup_in_field:
        lf.write("Duplicate Fields in INPUT Side\n")
    for item in globalVariables.list_dup_in_field:
        lf.write(item)
        lf.write(" ")
    if globalVariables.list_dup_out_field:
        lf.write("Duplicate Fields in OUTPUT Side\n")
    for item in globalVariables.list_dup_out_field:
        lf.write(item)
        lf.write(" ")
    # if globalVariables.list_dup_in_composite:
    #     lf.write("Duplicate Composite Elements in INPUT Side\n")
    # for item in globalVariables.list_dup_in_composite:
    #     lf.write(item)
    #     lf.write(" ")
    # if globalVariables.list_dup_out_composite:
    #     lf.write("Duplicate Composite Elements in OUTPUT Side\n")
    # for item in globalVariables.list_dup_out_composite:
    #     lf.write(item)
    #     lf.write(" ")
