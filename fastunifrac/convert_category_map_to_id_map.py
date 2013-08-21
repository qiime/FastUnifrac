#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from fastunifrac.check_id_map import blank_header, bad_char_in_header, sampleid_missing, barcode_missing, linker_primer_missing, description_missing, BARCODE_KEY, LINKER_PRIMER_KEY, filename_has_space, check_bad_chars_sampleids, check_bad_chars
from os.path import splitext, split
from qiime.parse import parse_mapping_file
from cogent.seqsim.sequence_generators import IUPAC_DNA

NUM_NUCLEOTIDES_BARCODE = 12
class BarcodeGenerator(object):
	""" Generates unique barcodes """

	def __init__(self):
		self.Alphabet = [key for key in IUPAC_DNA if key == IUPAC_DNA[key]]
		self.Current_indexes = [0 for x in range(NUM_NUCLEOTIDES_BARCODE)]

	def __call__(self):
		barcode = ""
		for i in range(NUM_NUCLEOTIDES_BARCODE):
			barcode = barcode + self.Alphabet[self.Current_indexes[i]]
		self.updateIndexes(NUM_NUCLEOTIDES_BARCODE-1)
		return barcode

	def updateIndexes(self, index):
		if index == -1:
			print "Unable to create more uniques barcodes with " + NUM_NUCLEOTIDES_BARCODE + " nucleotides."
			quit()
		else:
			self.Current_indexes[index] = (self.Current_indexes[index] + 1) % len(self.Alphabet)
			if self.Current_indexes[index] == 0:
				self.updateIndexes(index-1)
		

#Perheps is better to add this in check_id_map for future changes
SAMPLE_ID_INDEX = 0
BARCODE_INDEX = 1
LINKER_PRIMER_INDEX = 2

DEFAULT_LINKER_PRIMER = "AAAAAAAAAAAAAAAAAAAAA"

def header_checks(header):
	#Check if there is any header empty
	header, err = blank_header(header)
	if err:
		raise ValueError,("%s" % err)

	#Check if there is any bad char in header and fix it
	header, err = bad_char_in_header(header)

	#Check if sample id exists and starts with "#"
	header[0] = "#" + header[0]
	header, err = sampleid_missing(header)
	if err:
		raise ValueError,("%s" % err)

	#Check if exists barcode header
	header, err = barcode_missing(header)
	need_to_add_barcode = True if err else False

	#Check if exists linker primer header
	header, err = linker_primer_missing(header)
	need_to_add_linker_primer = True if err else False

	#Check if exists description header and, if it isn't exists, add it
	header, err = description_missing(header)
	need_to_add_description = True if err else False

	return header, need_to_add_barcode, need_to_add_linker_primer, need_to_add_description

#Add barcode header and a barcode for each sample
def add_barcode(data):
	data[0].insert(BARCODE_INDEX, BARCODE_KEY)
	barcode_gen = BarcodeGenerator()
	for row in data[1:]:
		row.insert(BARCODE_INDEX, barcode_gen())
	return data

#Add linker primer header and a default linker primer for each sample
#linker primer default: "AAAAAAAAAAAAAAAAAAAAA"
def add_linker_primer(data):
	data[0].insert(LINKER_PRIMER_INDEX, LINKER_PRIMER_KEY)
	for row in data[1:]:
		row.insert(LINKER_PRIMER_INDEX, DEFAULT_LINKER_PRIMER)
	return data

#Add description header and a default description for each sample
#description default: sample id
def add_description(data):
	for row in data[1:]:
		row.append(row[SAMPLE_ID_INDEX])
	return data

def convert(in_lines):
	#Read the input file
	mapping_data, header, comments = parse_mapping_file(in_lines)

	#Do all header checks
	header, need_to_add_barcode, need_to_add_linker_primer, need_to_add_description = header_checks(header)

	#Add headers to data
	mapping_data.insert(0, header)

	#Check if there is any bad char in sample ids and fix it
	(mapping_data, f_type), errs = check_bad_chars_sampleids((mapping_data, 'error'))

	#Check if there is any bad char in the data
	(mapping_data, f_type), errs = check_bad_chars((mapping_data, 'error'))

	#Add barcode if needed
	mapping_data = add_barcode(mapping_data) if need_to_add_barcode else mapping_data

	#Add linker primer if needed
	mapping_data = add_linker_primer(mapping_data) if need_to_add_linker_primer else mapping_data

	#Add description if needed
	mapping_data = add_description(mapping_data) if need_to_add_description else mapping_data

	return mapping_data, comments

# Writes a row of a matrix in tab delimited mode to the given file
def writes_tab_delimited_row(outf, row):
	outf.write(row[0])
	for field in row[1:]:
		outf.write("\t"+field)
	outf.write("\n")

#Writes corrected data to the output file
def write_corrected_file(data, comments, output_fp):
	outf = open(output_fp, 'w')
	
	writes_tab_delimited_row(outf, data[0])
	
	for com in comments:
		outf.write("#"+com+"\n")
	
	for row in data[1:]:
		writes_tab_delimited_row(outf, row)

	outf.close()

def convert_category_map_to_id_map(input_fp, output_fp):
	fpath, ext = splitext(input_fp)
	input_dir, fname = split(fpath)

	#Check if the file name contains spaces and fix it, in case we need it 
	fname, err = filename_has_space(fname)

	if output_fp:
		#Check if the output file name contains spaces and fix it
		output_fp, err = filename_has_space(output_fp)
	else:
		output_fp = fname + "_corrected.txt"

	#Check if it's possible to create the output file
	try:
		outf = open(output_fp, 'w')
		outf.close()
	except IOError:
		print "Unable to create corrected output file " + output_fp
		quit()

	mapping_data, comments = convert(open(input_fp, 'U'))

	#Writes the output file
	write_corrected_file(mapping_data, comments, output_fp)