declare -a quartile_options=(13 19 20 21 22 23)
echo "|++++++++++| Putting in a bunch of sbatch jobs:"
for quartile in "${quartile_options[@]}"
do
    sbatch sbatch_singular_quartile_df.sh $quartile &
    echo "|+| Submitted batch job: quartile $quartile"
done
echo "|++++++++++| sbatch jobs sent in."