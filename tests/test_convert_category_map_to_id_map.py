#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.unit_test import TestCase, main
from fastunifrac.check_id_map import DESC_KEY, SAMPLE_ID_KEY, BARCODE_KEY, LINKER_PRIMER_KEY
from fastunifrac.convert_category_map_to_id_map import header_checks, add_barcode, add_linker_primer, add_description, convert, DEFAULT_LINKER_PRIMER

class CategoryMapToIdMapParserTest(TestCase):
	def test_header_checks(self):
		headers = [SAMPLE_ID_KEY, BARCODE_KEY, LINKER_PRIMER_KEY, DESC_KEY]
		result = (["#" + SAMPLE_ID_KEY, BARCODE_KEY, LINKER_PRIMER_KEY, DESC_KEY], False, False, False)
		self.assertEqual(header_checks(headers), result)

		headers = [SAMPLE_ID_KEY, BARCODE_KEY, DESC_KEY]
		result = (["#" + SAMPLE_ID_KEY, BARCODE_KEY, DESC_KEY], False, True, False)
		self.assertEqual(header_checks(headers), result)

		headers = [SAMPLE_ID_KEY, LINKER_PRIMER_KEY, DESC_KEY]
		result = (["#" + SAMPLE_ID_KEY, LINKER_PRIMER_KEY, DESC_KEY], True, False, False)
		self.assertEqual(header_checks(headers), result)

		headers = [SAMPLE_ID_KEY, BARCODE_KEY, LINKER_PRIMER_KEY]
		result = (["#" + SAMPLE_ID_KEY, BARCODE_KEY, LINKER_PRIMER_KEY, DESC_KEY], False, False, True)
		self.assertEqual(header_checks(headers), result)

		headers = [SAMPLE_ID_KEY, BARCODE_KEY, LINKER_PRIMER_KEY, "Bad#Header1", "Bad\\Header2", DESC_KEY]
		result = (["#" + SAMPLE_ID_KEY, BARCODE_KEY, LINKER_PRIMER_KEY, "BadHeader1", "BadHeader2", DESC_KEY], False, False, False)
		self.assertEqual(header_checks(headers), result)

		headers = [BARCODE_KEY, LINKER_PRIMER_KEY, DESC_KEY]
		self.assertRaises(ValueError, header_checks, headers)

		headers = [SAMPLE_ID_KEY, "", DESC_KEY]
		self.assertRaises(ValueError, header_checks, headers)

	def test_add_barcode(self):
		data = []
		data.append(["#" + SAMPLE_ID_KEY, "HEADER1", "HEADER2"])
		data.append(['S1','data','data'])
		data.append(['S2','data','data'])
		data.append(['S3','data','data'])
		result = []
		result.append(["#" + SAMPLE_ID_KEY, BARCODE_KEY, "HEADER1", "HEADER2"])
		result.append(['S1','AAAAAAAAAAAA','data','data'])
		result.append(['S2','AAAAAAAAAAAC','data','data'])
		result.append(['S3','AAAAAAAAAAAG','data','data'])
		self.assertEqual(add_barcode(data), result)

	def test_add_linker_primer(self):
		data = []
		data.append(["#" + SAMPLE_ID_KEY, "HEADER1", "HEADER2"])
		data.append(['S1','data','data'])
		data.append(['S2','data','data'])
		data.append(['S3','data','data'])
		result = []
		result.append(["#" + SAMPLE_ID_KEY, "HEADER1", LINKER_PRIMER_KEY, "HEADER2"])
		result.append(['S1','data',DEFAULT_LINKER_PRIMER,'data'])
		result.append(['S2','data',DEFAULT_LINKER_PRIMER,'data'])
		result.append(['S3','data',DEFAULT_LINKER_PRIMER,'data'])
		self.assertEqual(add_linker_primer(data),result)

	def test_add_description(self):
		data = []
		data.append(["#" + SAMPLE_ID_KEY, "HEADER1", DESC_KEY])
		data.append(['S1','data'])
		data.append(['S2','data'])
		data.append(['S3','data'])
		result = []
		result.append(["#" + SAMPLE_ID_KEY, "HEADER1", DESC_KEY])
		result.append(['S1','data','S1'])
		result.append(['S2','data','S2'])
		result.append(['S3','data','S3'])
		self.assertEqual(add_description(data),result)

	def test_convert(self):
		category_map_lines = category_map_correct.split('\n')
		mapping_data = []
		mapping_data.append(['#SampleID', 'BarcodeSequence', 'LinkerPrimerSequence', 'Description'])
		mapping_data.append(['S1', 'AAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S1'])
		mapping_data.append(['S2', 'AAAAAAAAAAAC', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S2'])
		mapping_data.append(['S3', 'AAAAAAAAAAAG', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S3'])
		comments = ['Comments','One comment more']
		self.assertEqual(convert(category_map_lines), (mapping_data, comments))

		category_map_lines = category_map_bad_char_sample_id.split('\n')
		mapping_data = []
		mapping_data.append(['#SampleID', 'BarcodeSequence', 'LinkerPrimerSequence', 'Description'])
		mapping_data.append(['S.1', 'AAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S1'])
		mapping_data.append(['S.2', 'AAAAAAAAAAAC', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S2'])
		mapping_data.append(['S.3', 'AAAAAAAAAAAG', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S3'])
		comments = ['Comments','One comment more']
		self.assertEqual(convert(category_map_lines), (mapping_data, comments))

		category_map_lines = category_map_bad_char_data.split('\n')
		mapping_data = []
		mapping_data.append(['#SampleID', 'BarcodeSequence', 'LinkerPrimerSequence', 'Description'])
		mapping_data.append(['S1', 'AAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAAA', 'Description_of_S1'])
		mapping_data.append(['S2', 'AAAAAAAAAAAC', 'AAAAAAAAAAAAAAAAAAAAA', 'Description_of_S2'])
		mapping_data.append(['S3', 'AAAAAAAAAAAG', 'AAAAAAAAAAAAAAAAAAAAA', 'Description_of_S3'])
		comments = ['Comments','One comment more']
		self.assertEqual(convert(category_map_lines), (mapping_data, comments))

		category_map_lines = category_map_no_barcode.split('\n')
		mapping_data = []
		mapping_data.append(['#SampleID', 'BarcodeSequence', 'LinkerPrimerSequence', 'Description'])
		mapping_data.append(['S1', 'AAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S1'])
		mapping_data.append(['S2', 'AAAAAAAAAAAC', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S2'])
		mapping_data.append(['S3', 'AAAAAAAAAAAG', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S3'])
		comments = ['Comments','One comment more']
		self.assertEqual(convert(category_map_lines), (mapping_data, comments))

		category_map_lines = category_map_no_linker_primer.split('\n')
		mapping_data = []
		mapping_data.append(['#SampleID', 'BarcodeSequence', 'LinkerPrimerSequence', 'Description'])
		mapping_data.append(['S1', 'AAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S1'])
		mapping_data.append(['S2', 'AAAAAAAAAAAC', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S2'])
		mapping_data.append(['S3', 'AAAAAAAAAAAG', 'AAAAAAAAAAAAAAAAAAAAA', 'Description of S3'])
		comments = ['Comments','One comment more']
		self.assertEqual(convert(category_map_lines), (mapping_data, comments))

		category_map_lines = category_map_no_description.split('\n')
		mapping_data = []
		mapping_data.append(['#SampleID', 'BarcodeSequence', 'LinkerPrimerSequence', 'Description'])
		mapping_data.append(['S1', 'AAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAAA', 'S1'])
		mapping_data.append(['S2', 'AAAAAAAAAAAC', 'AAAAAAAAAAAAAAAAAAAAA', 'S2'])
		mapping_data.append(['S3', 'AAAAAAAAAAAG', 'AAAAAAAAAAAAAAAAAAAAA', 'S3'])
		comments = ['Comments','One comment more']
		self.assertEqual(convert(category_map_lines), (mapping_data, comments))

		category_map_lines = category_map_only_sample_id.split('\n')
		mapping_data = []
		mapping_data.append(['#SampleID', 'BarcodeSequence', 'LinkerPrimerSequence', 'Header1', 'Header2', 'Header3', 'Description'])
		mapping_data.append(['S1', 'AAAAAAAAAAAA', 'AAAAAAAAAAAAAAAAAAAAA', 'data', 'data', 'data', 'S1'])
		mapping_data.append(['S2', 'AAAAAAAAAAAC', 'AAAAAAAAAAAAAAAAAAAAA', 'data', 'data', 'data', 'S2'])
		mapping_data.append(['S3', 'AAAAAAAAAAAG', 'AAAAAAAAAAAAAAAAAAAAA', 'data', 'data', 'data', 'S3'])
		comments = ['Comments','One comment more']
		self.assertEqual(convert(category_map_lines), (mapping_data, comments))

category_map_correct="""#SampleID	BarcodeSequence	LinkerPrimerSequence	Description
#Comments
#One comment more
S1	AAAAAAAAAAAA	AAAAAAAAAAAAAAAAAAAAA	Description of S1
S2	AAAAAAAAAAAC	AAAAAAAAAAAAAAAAAAAAA	Description of S2
S3	AAAAAAAAAAAG	AAAAAAAAAAAAAAAAAAAAA	Description of S3
"""

category_map_bad_char_sample_id="""#SampleID	BarcodeSequence	LinkerPrimerSequence	Description
#Comments
#One comment more
S#1	AAAAAAAAAAAA	AAAAAAAAAAAAAAAAAAAAA	Description of S1
S#2	AAAAAAAAAAAC	AAAAAAAAAAAAAAAAAAAAA	Description of S2
S#3	AAAAAAAAAAAG	AAAAAAAAAAAAAAAAAAAAA	Description of S3
"""

category_map_bad_char_data="""#SampleID	BarcodeSequence	LinkerPrimerSequence	Description
#Comments
#One comment more
S1	AAAAAAAAAAAA	AAAAAAAAAAAAAAAAAAAAA	Description#of#S1
S2	AAAAAAAAAAAC	AAAAAAAAAAAAAAAAAAAAA	Description#of#S2
S3	AAAAAAAAAAAG	AAAAAAAAAAAAAAAAAAAAA	Description#of#S3
"""

category_map_no_barcode="""#SampleID	LinkerPrimerSequence	Description
#Comments
#One comment more
S1	AAAAAAAAAAAAAAAAAAAAA	Description of S1
S2	AAAAAAAAAAAAAAAAAAAAA	Description of S2
S3	AAAAAAAAAAAAAAAAAAAAA	Description of S3
"""

category_map_no_linker_primer="""#SampleID	BarcodeSequence	Description
#Comments
#One comment more
S1	AAAAAAAAAAAA	Description of S1
S2	AAAAAAAAAAAC	Description of S2
S3	AAAAAAAAAAAG	Description of S3
"""

category_map_no_description="""#SampleID	BarcodeSequence	LinkerPrimerSequence
#Comments
#One comment more
S1	AAAAAAAAAAAA	AAAAAAAAAAAAAAAAAAAAA
S2	AAAAAAAAAAAC	AAAAAAAAAAAAAAAAAAAAA
S3	AAAAAAAAAAAG	AAAAAAAAAAAAAAAAAAAAA
"""

category_map_only_sample_id="""#SampleID	Header1	Header2	Header3
#Comments
#One comment more
S1	data	data	data
S2	data	data	data
S3	data	data	data
"""

if __name__ == '__main__':
	main()
