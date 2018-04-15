#!/bin/bash

source venv/bin/activate

while read p;
do 
	python scraper.py ${p}
done < All_Orgs_full.txt
