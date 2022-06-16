#!/bin/bash

start_time=`date +%s`
cd sec-scrapper &&
python3 edgar_crawler.py &&
python3 extract_items_10k.py &&
cd ../NLP_Pipeline &&
python3 nlp_pipeline.py &&
cd ..
end_time=`date +%s`
echo Execution Time was `expr $end_time - $start_time` s.