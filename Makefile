split:
	rm -rf data/testing/01_split/*.csv;
	python -m src.vesseltrack_tools.file_management.split_file config/config_split.json

clean:
	rm -rf data/testing/02_cleaned/*.csv;
	python -m src.vesseltrack_tools.cleaning.data_cleaning config/config_cleaning.json 

maps:
	python -m src.vesseltrack_tools.density.export_density_maps config/config_density.json 

merge:
	rm -rf data/testing/04_merged/*.csv;
	python -m src.vesseltrack_tools.file_management.merge_files config/config_merge.json

trips:
	rm -rf data/testing/05_trips/*.csv;
	python -m src.vesseltrack_tools.trips.find_trips config/config_trips.json


reset_sample:
	rm -rf data/testing/05_trips/*.csv;
	rm -rf data/testing/04_merged/*.csv;

	rm -rf data/testing/03_density/*.vrt;
	rm -rf data/testing/03_density/*.csv;
	rm -rf data/testing/03_density/*.tif;
	rm -rf data/testing/03_density/*.tif.aux.xml;
	
	rm -rf data/testing/02_cleaned/*.csv;
	rm -rf data/testing/02b_kalman/*.csv;

	rm -rf data/testing/01_split/*.csv;
	rm -rf data/testing/metadata/*.csv;
	rm -rf data/testing/metadata/*.json;
	rm -rf data/testing/others/grids*.json;


all:
	make reset_sample;
	make split;
	make clean;
	make maps;