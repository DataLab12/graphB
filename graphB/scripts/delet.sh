#!/bin/bash

for i in {1..9}
do
	find . -name "R100$i.h5" -type f -delete
done
for i in {10..99}
do
        find . -name "R10$i.h5" -type f -delete
done
for i in {100..600}
do
        find . -name "R1$i.h5" -type f -delete
done
