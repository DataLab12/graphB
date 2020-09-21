declare -a plot_options=(22)
echo "|++++++++++| Putting in a bunch of sbatch jobs:"
for plot in "${plot_options[@]}"
do
    sbatch sbatch_singular_plot.sh $plot &
    echo "|+| Submitted batch job: plot $plot"
done
echo "|++++++++++| sbatch jobs sent in."
