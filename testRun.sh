cd graphB

conda activate graphB 

python run.py

python run.py 3

conda deactivate

find /data-test/Data/*.h5 -depth -print -delete | wc -l

cd ..
