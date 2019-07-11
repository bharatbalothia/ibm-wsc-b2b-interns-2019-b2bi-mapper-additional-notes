import xml.etree.ElementTree as et
from xml.etree import ElementTree as etree
from final_func import initialize_variable_set, initialize_const_Map, edi_initialize_dict, xml_initialize_dict, \
    make_log, remove_comments, preprocess, start, make_dictionary, edi_initialize_output_dict, \
    xml_initialize_output_dict, handle_java, edi_make_notes, sort_java_arr, xml_make_notes, edi_populate_notes, \
    xml_populate_notes, make_log, write_func
from final_remove_notes import empty_notes


class allDictVariables(object):  # all dictionaries are declared inside this and passed everywhre as globalVariables
    def __init__(self, path):
        # variables initialized
        self.dict_1 = {}
        # key-field id, value-list of grp_name,seg_name,field_name
        self.dict_op = {}
        # key-op_field_id, value-list of field_name of linked field,des of op_field(y!!!??)
        self.dict_useless = {}
        # key-field id, value-field name
        self.dict_field = {}
        # key-rule number, value-rule
        self.dict_op_field = {}
        # same as dict_field for output
        self.dict_ind_field = {}
        # key-field name, value-list of segment name and number
        self.dict_ip_ct = {}
        # for input standard constant rules
        self.dict_op_ct = {}
        # for output standard constant rules
        self.dict_constant = {}
        self.dict_type = {}
        self.dict_op_type = {}
        # same as dict_type for output
        self.dict_ip_select = {}
        # for input standard select rules
        self.dict_op_select = {}
        # for output standard select rules
        self.dict_token = {}
        # key-variable, value-list of lists where the variable is being Populated
        self.dict_op_token = {}
        # same but for output
        self.note_dict_token = {}
        self.dict_notes = {}
        self.dict_tag_inp = {}
        self.dict_tag_out = {}
        # key-id name, value-notes
        self.dict_opposite = {}
        self.dict_opposite_out = {}
        self.dict_opposite_name_id = {}
        self.dict_op_date = {}
        self.list_dup_in_field = []
        self.list_dup_out_field = []
        self.list_dup_in_composite = []
        self.list_dup_out_composite = []
        self.list_in_composite = []
        self.list_out_composite = []
        self.arr_java_inp = ['new']
        self.arr_java_out = set()
        self.dict_accumulator_move = {}
        self.dict_seg_loop = {}
        self.dict_sum = {}
        self.dict_op_acc = {}
        self.inp_grp_name = ''
        self.out_grp_name = ''
        self.link_notes_set = set()
        self.standard_notes_set = set()
        self.extended_notes_set = set()
        self.field_set = set()
        self.field_set.add('sendercode')
        self.field_set.add('receivercode')
        self.variable_set = set()
        self.ip_count = -1
        self.op_count = -1
        self.f = open(path, 'w')
        self.dict_name_id = {}
        self.dict_accumulator = {}
        self.dict_opposite_group = {}
        self.dict_opposite_group_out = {}


def an(filePathUploaded, outputPath, tempFilePath, filenameUploaded):
    #    application_window = tk.Tk()

    globalVariables = allDictVariables(tempFilePath + '/notes.txt')

    filePathInput = tempFilePath + '/' + filenameUploaded
    filehandler = open(filePathInput,encoding="utf-8")
    print(filehandler)
    raw_data = et.parse(filehandler)
    data_root = raw_data.getroot()  # data_root is the root node of the mxl file
    filehandler.close()
    fo = open(tempFilePath + "/writefile.txt", 'w')
    op_file = open(tempFilePath + "/op_writefile.txt", 'w')
    input_format = ''
    output_format = ''
    inp_format_tag = data_root[3][0].tag
    out_format_tag = data_root[4][0].tag
    empty_notes(data_root, etree, raw_data, filePathInput)

    initialize_variable_set(data_root, fo, globalVariables)  # all the variables in the file are stored in the set
    initialize_const_Map(data_root, globalVariables)  # constant index to corresponding value is stored here
    if inp_format_tag.split('}')[1] == 'EDISyntax':
        print("&&&&&&&&&&&&&&&&&")
        input_format = 'EDI'
        edi_initialize_dict(data_root, fo, globalVariables)
        # allcases = data_root_ddf.findall(".//EDIELEM")

    elif inp_format_tag.split('}')[1] == 'PosSyntax':
        input_format = 'IDOC'
        print("DW")
        # exit()
        edi_initialize_dict(data_root, fo, globalVariables)
        # allcases = data_root_ddf.findall(".//POSFIELD")
    elif inp_format_tag.split('}')[1] == 'VarDelimSyntax':
        input_format = 'CSV'
        print("csv")
        edi_initialize_dict(data_root, fo, globalVariables)
    elif inp_format_tag.split('}')[1] == 'XMLSyntax':
        input_format = 'XML'
        print("**********")
        xml_initialize_dict(data_root, fo, globalVariables)
        # allcases = data_root_ddf.findall(".//XMLPCDATA")

    # exit()
    fo.close()

    all_set = set()

    nf = open(tempFilePath + '/newfile.txt', 'w')
    of = open(tempFilePath + '/writefile.txt', 'r')
    remove_comments(nf, of, globalVariables)
    nf.close()
    of.close()
    pre_n = open(tempFilePath + '/prefile.txt', 'w')
    pre_o = open(tempFilePath + '/newfile.txt', 'r')
    preprocess(pre_n, pre_o, globalVariables)
    pre_n.close()
    pre_o.close()
    jf = open(tempFilePath + '/javafile.txt', 'w')
    line_list = [line.rstrip('\n') for line in open(tempFilePath + '/prefile.txt')]
    block_code = handle_java(line_list, globalVariables.arr_java_inp, 0, globalVariables)
    jf.write(block_code)  # javafile.txt is the final file from which all the rules are read
    jf.close()

    with open(tempFilePath + '/javafile.txt', 'r') as f_read:
        data = f_read.read().replace('\n', ' ')

    result = start.parseString(
        data)  # parse all the rules together... to check for parsing error.. put an exit() after this line and see if its parsing
    print("PARSE")
    print(result)
    make_dictionary(result, globalVariables.dict_token, 0, globalVariables)
    print("PARSE")
    print(globalVariables.dict_token)

    for k, v in globalVariables.dict_token.items():
        print(k)
        print(v)

    if out_format_tag.split('}')[1] == 'EDISyntax':  # same process for output is also followed
        print("&&&&&&&&&&&&&&&&&")
        output_format = 'EDI'
        edi_initialize_output_dict(data_root, op_file, globalVariables)
    elif out_format_tag.split('}')[1] == 'PosSyntax':
        output_format = 'IDOC'
        edi_initialize_output_dict(data_root, op_file, globalVariables)
    elif out_format_tag.split('}')[1] == 'VarDelimSyntax':
        output_format = 'CSV'
        edi_initialize_output_dict(data_root, op_file, globalVariables)
    elif out_format_tag.split('}')[1] == 'XMLSyntax':
        output_format = 'XML'
        xml_initialize_output_dict(data_root, op_file, globalVariables)

    op_file.close()

    op_nf = open(tempFilePath + '/op_newfile.txt', 'w')
    op_of = open(tempFilePath + '/op_writefile.txt', 'r')
    remove_comments(op_nf, op_of, globalVariables)
    op_nf.close()
    op_of.close()
    op_pre_n = open(tempFilePath + '/op_prefile.txt', 'w')
    op_pre_o = open(tempFilePath + '/op_newfile.txt', 'r')
    preprocess(op_pre_n, op_pre_o, globalVariables)
    op_pre_n.close()
    op_pre_o.close()
    op_jf = open(tempFilePath + '/op_javafile.txt', 'w')
    line_list_op = [line.rstrip('\n') for line in open(tempFilePath + '/op_prefile.txt')]
    block_code_op = handle_java(line_list_op, globalVariables.arr_java_inp, 0, globalVariables)
    op_jf.write(block_code_op)  # op_javafile the final file
    op_jf.close()

    with open(tempFilePath + '/op_javafile.txt', 'r') as op_f_read:
        op_data = op_f_read.read().replace('\n', ' ')

    op_result = start.parseString(op_data)
    print("OP_PARSE")
    print(op_result)
    # print(dict_op_field)              # output info is stored in the dict_op_token
    make_dictionary(op_result, globalVariables.dict_op_token, 1, globalVariables)

    print(globalVariables.dict_op_token)
    print("HOLA!")

    # initialize_const_Map(data_root)

    if output_format == 'EDI':  # this block would make all the notes and store them in dict_notes
        print("Is it here")
        edi_make_notes(data_root, globalVariables)
    elif output_format == 'IDOC':
        edi_make_notes(data_root, globalVariables)
    elif output_format == 'XML':
        xml_make_notes(data_root, globalVariables)
    elif output_format == 'CSV':
        edi_make_notes(data_root, globalVariables)
    # exit()

    sort_java_arr(globalVariables)  # to make the logfile...the notes set should be manipulated
    print(globalVariables.link_notes_set)
    print(globalVariables.standard_notes_set)
    print(globalVariables.extended_notes_set)

    if output_format == 'EDI':  # this block finally changes format and populates the notes at their fileds
        edi_populate_notes(data_root, input_format, output_format, globalVariables)
    elif output_format == 'IDOC':
        edi_populate_notes(data_root, input_format, output_format, globalVariables)
    elif output_format == 'CSV':
        edi_populate_notes(data_root, input_format, output_format, globalVariables)
    elif output_format == 'XML':
        print("did it enter...did it???????")
        xml_populate_notes(data_root, input_format, output_format, globalVariables)

    output = write_func(data_root, etree, raw_data, filenameUploaded, outputPath, globalVariables)

    for k, v in globalVariables.dict_notes.items():
        print(k)
        print(v)

    print(globalVariables.link_notes_set)
    print(globalVariables.standard_notes_set)
    print(globalVariables.extended_notes_set)
    logfile = filenameUploaded.split('.')[0] + '_logfile.txt'  # create path and the logfile
    logfile = tempFilePath + '/' + logfile
    print(logfile)
    lf = open(logfile, 'w')
    make_log(lf, globalVariables)
    lf.close()
    globalVariables.f.close()
    print(globalVariables.list_dup_in_field)
    print(globalVariables.list_dup_out_field)
    print(globalVariables.variable_set)
    print(globalVariables.list_dup_in_composite)
    return output, logfile

