#/bin/bash

#
#	usage: migrate.sh sql_file_name
#

cp $1 tempfile.sql

perl -pi.bak -e "BEGIN{undef $/;} s/(\sN'[^'\r\n]*)[\r\n]+([^']+[\r\n]*)*'/\1'/smg" tempfile.sql
perl -pi.bak -e "s/N''/N'-'/g" tempfile.sql

python mssql_to_postgres.py tempfile.sql
rm tempfile.sql
