#!/bin/bash

hive -f /projects/scripts/sql/create_product_table.hql


hive -e "LOAD DATA LOCAL INPATH '/projects/data/' INTO TABLE testdb.products;"

hive -e "select count(1) from testdb.products;"

# hive -e "LOAD DATA INPATH 'gs://dulcet-record-319917-tf-state/data/' INTO TABLE testdb.products;"