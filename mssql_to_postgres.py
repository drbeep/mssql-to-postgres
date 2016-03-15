#
#
#	usage: python script.py source_file_name output_file_name
#
#

import sys
import re
import codecs


def insertContentQueries(fileName):
	with codecs.open(fileName, 'r', 'utf-8') as f:
		for line in f:
			if line.startswith("INSERT"):
				yield line


def transformQueriesToBulkInsert(fileName):
	currentTableName = ""

	for insertQuery in insertContentQueries(fileName):
		insertQuery = transformSingleQuerySyntax(insertQuery)
		tableName = re.search(r'INSERT (\w+)', insertQuery).group(1)

		if currentTableName and currentTableName != tableName:
			yield ";\n\n"

		if not currentTableName or currentTableName != tableName:
			currentTableName = tableName

			bulkInsertStartLine = insertQuery
			bulkInsertStartLine = re.sub('INSERT', 'INSERT INTO', bulkInsertStartLine)
			bulkInsertStartLine = re.sub('VALUES.*', '', bulkInsertStartLine)

			yield bulkInsertStartLine + " VALUES\n"
			yield "\t" + re.sub(r'.*VALUES\s*', '', insertQuery)
		else:
			yield ",\n\t" + re.sub(r'.*VALUES\s*', '', insertQuery)



def transformSingleQuerySyntax(line):
	line = re.sub(r'\[(\w+)\]', r'\1', line)
	line = re.sub(r"N('[^']+')", r"\1", line)

	# TODO: fix that weird shit
	line = re.sub(r"CAST\(0x\w+ AS DateTime\)", "0", line)
	line = re.sub(r'[\n\r]', '', line)
	return line


with codecs.open(sys.argv[2], 'w', 'utf-8') as f:
	for x in transformQueriesToBulkInsert(sys.argv[1]):
		f.write(x)