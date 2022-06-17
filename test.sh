#!/bin/bash

start_time=`date +%s`
cd sec_scrapper &&
python3 edgar_crawler.py &&
python3 extract_items_10k.py &&
cd ../nlp_pipeline &&
python3 main.py &&
cd ..
end_time=`date +%s`
echo Execution Time was `expr $end_time - $start_time` s.