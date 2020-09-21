import os
import warnings
import matplotlib  as mpl
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
import statistics
import pandas as pd

from postprocess.df_creation import postprocess_tree_df, postprocess_vertex_df, get_users_map
from dataset_paths import get_plots_folder, get_full_unsym_csr_adj

# Parameter Settings! Could be used to adjust to individual analysis
FIG_SIZE_HEIGHT = 5
FIG_SIZE_WIDTH = 5.5
SEABORN_FONT_SCALE = 2
LEGEND_SIZE = 10
TITLE_SIZE = 14
LABEL_SIZE = 14
TICK_LABEL_SIZE = 12
SCATTER_ALPHA = 0.15

WINNER = 1
LOSER = 0
VOTER = -1
COLOR_CHART = {
        LOSER: (1, 0.6, 0.6, 1),
        WINNER: (0.08, 0.75, 0, 1),
        VOTER: (0.7, 0.35, 0.35, 0),
        'T': 'blue',
        'PVT': 'purple',
        'PCTC0': 'black',
        'PVC0': 'blue'
}

def postprocess_all_plots(config_obj):
    postprocess_tree_bias_vs_c0(config_obj)
    postprocess_vertex_status_vs_id(config_obj)
    postprocess_histograms(config_obj)

def create_if_not_exists(directory_to_possibly_create):
  if not os.path.exists(directory_to_possibly_create):
    os.makedirs(directory_to_possibly_create)

def save_fig(fig, directory, file_name, df=None):
    FULL_FILE_PATH = directory + file_name
    create_if_not_exists(directory)
    fig.savefig(FULL_FILE_PATH)
    if df is not None:
        csv_path = os.path.splitext(FULL_FILE_PATH)[0]+'.csv'
        df.to_csv(csv_path, encoding='utf-8', index = False)

def set_size(fig, width=FIG_SIZE_WIDTH, height=FIG_SIZE_HEIGHT):
    fig.set_size_inches(width, height)
    plt.tight_layout()

def get_colors():
    return np.array([
        [0.1, 0.1, 0.1],          # black
        [0.4, 0.4, 0.4],          # very dark gray
        [0.7, 0.7, 0.7],          # dark gray
        [0.9, 0.9, 0.9],          # light gray
        [0.984375, 0.7265625, 0], # dark yellow
        [1, 1, 0.9]               # light yellow
    ])

def get_outlier_colors(df, status, outcome, g_mean, g_std, r_mean, r_std):
    colors = []
    for index, row in df.iterrows():
        color = (0, 0, 0, 0)
        if row[outcome] == 'L' and row[status] > g_mean - g_std and not (row[status] < r_mean + r_std and row[status] > r_mean - r_std): # is red and is in green rect and NOT in red rect
            color = COLOR_CHART[row[outcome]]
        elif row[outcome] == 'W' and row[status] < r_mean + r_std and not (row[status] < g_mean + g_std and row[status] > g_mean - g_std): # is green and is in red rect and NOT in green rect
            color = COLOR_CHART[row[outcome]]
        colors.append(color)
    return colors

def status_vs_ID_content(df):
    fig, ax = plt.subplots()

    if len(df.columns) > 3: ## if ID mapping file was used
      df = df.astype({'Original ID':'int32'}, {'outcome':'int32'})
      x = df.columns[1]
      y1 = df.columns[2]
    else:
      x = df.columns[1]
      y1 = df.columns[0]
    
    LINE_WIDTH = 1
    if 'outcome' in df.columns:
        if len(df.columns) > 3: ## if ID mapping file was used
          y2 = df.columns[4]
        else:
          y2 = df.columns[2]
        
        #ax.scatter(df[x], df[y1], c=df[y2].apply(lambda x: COLOR_CHART[x]), facecolors='none')

        w_df = df.loc[df['outcome'] == WINNER]
        l_df = df.loc[df['outcome'] == LOSER]
        n_df = df.loc[df['outcome'] == VOTER]
        
        ## select black/yellow or green/red option by commenting out other option 
           
        status_vs_ID_greenred(df, w_df, l_df, fig, ax, x, y1, y2)
        #status_vs_ID_blackyellow(df, w_df, l_df, n_df, fig, ax, x, y1, y2)
        

        ## left in just in case it's needed later
        #ax.scatter(df[x], df[y1], c=get_outlier_colors(df, y1, y2, mc0pct_promoted, stc0pct_promoted, mc0pct_not_promoted, stc0pct_not_promoted))
    else:
        mc0pct_na = df['% C0'].mean()
        stc0pct_na = df['% C0'].std()
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), y=mc0pct_na + stc0pct_na)
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), y=mc0pct_na)
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), y=mc0pct_na - stc0pct_na)
        plt.fill_between(df[x], mc0pct_na + stc0pct_na, mc0pct_na - stc0pct_na, color='gray', alpha=0.20)
        ax.scatter(df[x], df[y1])
        text = "Average status: " + str(mc0pct_na)
        props = dict(boxstyle = 'round', facecolor = 'wheat', alpha = .1)
        ax.text(.05, .05, text, transform=ax.transAxes, fontsize = 10, verticalalignment='top', bbox=props)
    return fig, ax

def status_vs_ID_blackyellow(df, w_df, l_df, n_df, fig, ax, x, y1, y2):
        LINE_WIDTH = 1
        ##combine winners and losers into one dataframe
        w_df.append(l_df)
        o_df = w_df
        
        o_df_length = list(o_df['Vert ID'])
        o_stdev = statistics.stdev(o_df_length)
        o_middle = statistics.median(o_df_length)
                
        n_df_length = list(n_df['Vert ID'])
        n_stdev = statistics.stdev(n_df_length)
        n_middle = statistics.median(n_df_length)
        
        x_axis_array = [i for i in range(9000)]
        y_axis_array = [i for i in range(100)]
                
        mc0pct_na = df['% C0'].mean()
        stc0pct_na = df['% C0'].std()
        ## put in mean and stdev lines
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), y=mc0pct_na + stc0pct_na)
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), y=mc0pct_na)
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), y=mc0pct_na - stc0pct_na)

        ax.axvline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), x= o_middle + o_stdev)
        ax.axvline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), x= o_middle)
        ax.axvline(linewidth=LINE_WIDTH, color=(0, 0, 0, 0.5), x= o_middle - o_stdev)

        ax.axvline(linewidth=LINE_WIDTH, color=(0.984375, 0.7265625, 0, 0.5), x= n_middle + n_stdev)
        ax.axvline(linewidth=LINE_WIDTH, color=(0.984375, 0.7265625, 0, 0.5), x= n_middle)
        ax.axvline(linewidth=LINE_WIDTH, color=(0.984375, 0.7265625, 0, 0.5), x= n_middle - n_stdev)
        ## gray/yellow fills 
        plt.fill_between(x_axis_array, mc0pct_na + stc0pct_na, mc0pct_na - stc0pct_na, color='gray', alpha='0.20')
        ax.fill_betweenx(y_axis_array, o_middle - o_stdev, o_middle + o_stdev,  color='gray', alpha='0.20')
        ax.fill_betweenx(y_axis_array, n_middle - n_stdev, n_middle + n_stdev, color='yellow', alpha='0.20')
                

        ## color settings for circles 
        TEMP_COLOR_CHART = {
            LOSER: (0, 0, 0, 1),
            WINNER: (0, 0, 0, 1),
            VOTER: (0.984375, 0.7265625, 0, 1)
        }
        ## create scatterplot
        ax.scatter(df[x], df[y1], facecolors = 'none', edgecolors = df[y2].apply(lambda x: TEMP_COLOR_CHART[x]))
        text = "Average status: " + str(mc0pct_na)
        props = dict(boxstyle = 'round', facecolor = 'wheat', alpha = .5)
        ax.text(.05, .05, text, transform=ax.transAxes, fontsize = 12, verticalalignment='top', bbox=props)
        return fig, ax

def status_vs_ID_greenred(df, w_df, l_df, fig, ax, x, y1, y2):
        LINE_WIDTH = 1
        mc0pct_promoted = w_df['% C0'].mean()
        stc0pct_promoted = w_df['% C0'].std()  
        mc0pct_not_promoted = l_df['% C0'].mean()
        stc0pct_not_promoted = l_df['% C0'].std()
        
        w_df_length = list(w_df['Vert ID'])
        w_stdev = statistics.stdev(w_df_length)
        w_middle = statistics.median(w_df_length)
        
        l_df_length = list(l_df['Vert ID'])
        l_stdev = statistics.stdev(l_df_length)
        l_middle = statistics.median(l_df_length)
        x_axis_array = [i for i in range(9000)]
        y_axis_array = [i for i in range(100)]
                
        mc0pct_na = df['% C0'].mean()
        stc0pct_na = df['% C0'].std()
        
        ## standard deviation and mean lines 
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 1, 0, 0.5), y=mc0pct_promoted + stc0pct_promoted)
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 1, 0, 0.5), y=mc0pct_promoted)
        ax.axhline(linewidth=LINE_WIDTH, color=(0, 1, 0, 0.5), y=mc0pct_promoted - stc0pct_promoted)

        ax.axhline(linewidth=LINE_WIDTH, color=(1, 0, 0, 0.5), y=mc0pct_not_promoted + stc0pct_not_promoted)
        ax.axhline(linewidth=LINE_WIDTH, color=(1, 0, 0, 0.5), y=mc0pct_not_promoted)
        ax.axhline(linewidth=LINE_WIDTH, color=(1, 0, 0, 0.5), y=mc0pct_not_promoted - stc0pct_not_promoted)
       
        ax.axvline(linewidth=LINE_WIDTH, color=(0, 1, 0, 0.5), x= w_middle + w_stdev)
        ax.axvline(linewidth=LINE_WIDTH, color=(0, 1, 0, 0.5), x= w_middle)
        ax.axvline(linewidth=LINE_WIDTH, color=(0, 1, 0, 0.5), x= w_middle - w_stdev)

        ax.axvline(linewidth=LINE_WIDTH, color=(1, 0, 0, 0.5), x= l_middle + l_stdev)
        ax.axvline(linewidth=LINE_WIDTH, color=(1, 0, 0, 0.5), x= l_middle)
        ax.axvline(linewidth=LINE_WIDTH, color=(1, 0, 0, 0.5), x= l_middle - l_stdev)
               
      
        ## green/red fills
        plt.fill_between(x_axis_array, mc0pct_promoted + stc0pct_promoted, mc0pct_promoted - stc0pct_promoted, color='green', alpha='0.20')
        plt.fill_between(x_axis_array, mc0pct_not_promoted + stc0pct_not_promoted, mc0pct_not_promoted - stc0pct_not_promoted, color='red', alpha='0.20')

        ax.fill_betweenx(y_axis_array, w_middle - w_stdev, w_middle + w_stdev,  color='green', alpha='0.20')
        ax.fill_betweenx(y_axis_array, l_middle - l_stdev, l_middle + l_stdev, color='red', alpha='0.20')
        ## color settings for circles   
        TEMP_COLOR_CHART = {
            LOSER: (1, 0, 0, 1),
            WINNER: (0.08, 0.75, 0, 1),
            VOTER: (1, 1, 0, 0)
        }
        ## create scatterplot
        ax.scatter(df[x], df[y1], facecolors = 'none', edgecolors = df[y2].apply(lambda x: TEMP_COLOR_CHART[x]))
        text = "Average status: " + str(mc0pct_na)
        props = dict(boxstyle = 'round', facecolor = 'wheat', alpha = .5)
        ax.text(.05, .05, text, transform=ax.transAxes, fontsize = 12, verticalalignment='top', bbox=props)
        return fig, ax

def status_vs_ID_style(fig, axes, title, xlabel, ylabel):
    # set_labels(fig, axes)
    # color_bars(axes, get_colors())
    set_size(fig)
    sb.set(font_scale=SEABORN_FONT_SCALE)
    set_size(fig, FIG_SIZE_WIDTH, FIG_SIZE_HEIGHT)
    axes.set_xlabel(xlabel, fontsize=LABEL_SIZE)
    axes.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    axes.set_title(title, fontsize=TITLE_SIZE)
    axes.tick_params(labelsize=TICK_LABEL_SIZE)
    axes.set(ylim=(0, 100))
    # axes.set(xlim=(0, 7200)) # TODO: Make this dependent on dataset
    # legend_elements = [Line2D([0], [0], marker='o', color=COLOR_CHART[WINNER], label='elected', markerfacecolor=COLOR_CHART[WINNER], markersize=15), 
    #            Line2D([0], [0], marker='o', color=COLOR_CHART[VOTER], label='voter', markerfacecolor=COLOR_CHART[VOTER], markersize=15),
    #            Line2D([0], [0], marker='o', color=COLOR_CHART[LOSER], label='not elected', markerfacecolor=COLOR_CHART[LOSER], markersize=15)]

    # legend_elements = [Line2D([0], [0], marker='o', color=COLOR_CHART['W'], label='votee', markerfacecolor=COLOR_CHART['W'], markersize=15), 
    #             Line2D([0], [0], marker='o', color=COLOR_CHART['N'], label='voter', markerfacecolor=COLOR_CHART['N'], markersize=15)]

    # axes.legend(handles=legend_elements, loc=0, prop={'size': LEGEND_SIZE})
    axes.set_facecolor('white')
    # axes.grid()
    axes.spines['bottom'].set_color('0.5')
    axes.spines['top'].set_color('0.5')
    axes.spines['right'].set_color('0.5')
    axes.spines['left'].set_color('0.5')
    # axes.grid(b=True, which='major', color='b', linewidth=1.0)
    axes.grid(b=True, which='major', color='gray', linewidth=0.15)
    #     plt.tick_params(axis='both', which='major', labelsize=32)
    # plt.tick_params(axis='both', which='minor', labelsize=32)
    plt.title(title, x=0.16, y=0.90, fontsize=TITLE_SIZE)
    axes.xaxis.set_label_coords(0.94, 0.08)

def bias_vs_c0_content(df):
    with warnings.catch_warnings():
        fig, ax = plt.subplots() 
        x = 'tree_bias_score'
        y1 = 'c0_pct'
        sb.regplot(x=x, y=y1, data=df, ax=ax, color=COLOR_CHART['PCTC0'], scatter_kws={'alpha': SCATTER_ALPHA, 's': 4})
    return fig, ax

def bias_vs_c0_style(fig, axes, title, xlabel, ylabel):
    sb.set(font_scale=SEABORN_FONT_SCALE)
    set_size(fig, FIG_SIZE_WIDTH, FIG_SIZE_HEIGHT)
    axes.set(ylim=(49, 80))
    axes.set(xlim=(-0.3, 0.80))
    axes.set_xlabel(xlabel, fontsize=LABEL_SIZE)
    axes.set_ylabel(ylabel, fontsize=LABEL_SIZE)
    axes.set_title(title, fontsize=TITLE_SIZE)
    axes.tick_params(labelsize=TICK_LABEL_SIZE)
    axes.set_facecolor('white')
    # axes.grid()
    axes.spines['bottom'].set_color('0.5')
    axes.spines['top'].set_color('0.5')
    axes.spines['right'].set_color('0.5')
    axes.spines['left'].set_color('0.5')
    axes.grid(b=True, which='major', color='gray', linewidth=0.15)
    # plt.title(title, y=0.90, x=0.48, fontsize=TITLE_SIZE)
    # axes.xaxis.set_label_coords(0.5, 0.08)
    # axes.yaxis.set_label_coords(0.08, 0.5)
    plt.title(title, x=0.22, y=0.90, fontsize=TITLE_SIZE)
    axes.xaxis.set_label_coords(0.90, 0.08)

def postprocess_vertex_status_vs_id(config_obj):
    print("-------- Creating vertex_status_vs_id Plot --------")
    component_list_weight = True
    df = postprocess_vertex_df(config_obj, True)
    user_map_df, ignore = get_users_map(config_obj)
    if not ignore: 
      ## merge the dataframe containing only the tagged IDs with the mapping dataframe
      merged = pd.merge(left = user_map_df, right = df, how = 'left', left_on = 'Tagged ID', right_on = 'Vert ID')
      ## drop any rows that didn't have information in both dataframes
      df = merged.dropna()
    fig, axes = status_vs_ID_content(df)

    title = 'status '#  + DISPLAY_DICT[matrix_name]
    xlabel = 'id'
    ylabel = ''
    status_vs_ID_style(fig, axes, title, xlabel, ylabel)
    if config_obj['has_labels']:
        if config_obj['weighted_status']:
            img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_weighted_outcomes.png"
        else:
            img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_unweighted_tiebreakNode" + str(config_obj['tiebreak_node']) + "_outcomes.png"
        save_dir = get_plots_folder(config_obj) + "status_vs_ID/outcomes/"
    else:
        if config_obj['weighted_status']:
            img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_weighted_no_outcomes.png"
        else:
            img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_unweighted_tiebreakNode" + str(config_obj['tiebreak_node']) + "_no_outcomes.png"
        save_dir = get_plots_folder(config_obj) + "status_vs_ID/no_outcomes/"
    create_if_not_exists(save_dir)
    outlier_df = df[~(np.abs(df['% C0'] - df['% C0'].mean()) > (df['% C0'].std()))] # from: https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-pandas-data-frame
    outliers = list(outlier_df['Vert ID'])
    outliers_file_path = os.path.splitext(save_dir + img_name)[0]+'.txt'
    with open(outliers_file_path, "w") as text_file:
        print("Number of Outliers: {}".format(len(outliers)), file=text_file)
        print("Outliers: {}".format(" ".join(str(x) for x in outliers)), file=text_file)
    save_fig(fig, save_dir, img_name, df)

def postprocess_tree_bias_vs_c0(config_obj):
    print("-------- Creating tree_bias_vs_c0 Plot --------")
    if config_obj['has_labels']:
        df = postprocess_tree_df(config_obj, True)
        # 'c0_pct', 'mean_tree_vertex_deg', 'num_changed_edges', 'pv_c0_pct', 'pv_c1_pct', 'pv_pct', 'stdev_tree_vertex_deg', 'tree_bias_score', 'tree_pendant_vertices']
        cols = ["tree_bias_score", "c0_pct", "pv_c0_pct", "pv_pct"]
        if not config_obj['has_labels']:
            print("This dataset has no labels, and therefore no bias measurement, and therefore can't plot bias vs c0: ", config_obj['dataset'])
            return None
        df = df[cols]
        fig, axes = bias_vs_c0_content(df)

        title = 'aMaj % ' # + DISPLAY_DICT[matrix_name]
        xlabel = "aBias"
        ylabel = '' # "% vertices in c0"
        bias_vs_c0_style(fig, axes, title, xlabel, ylabel)

        img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(config_obj['component_no']) + ".png"
        save_dir = get_plots_folder(config_obj) + "bias_vs_c0/"
        save_fig(fig, save_dir, img_name, df)
    else:
        print("Warning: this dataset has no labels, so we can't create a bias vs c0 plot.")
        return None

def in_deg_hist_content(csr_adj_matrix):
    MIN_DEG = 10
    col_sums = csr_adj_matrix.getnnz(axis=0)
    with warnings.catch_warnings():
        fig, ax = plt.subplots() 
 
        sb.distplot(a=col_sums[col_sums >= MIN_DEG], ax=ax)
    return fig, ax

def out_deg_hist_content(csr_adj_matrix):
    MIN_DEG = 10
    row_sums = csr_adj_matrix.getnnz(axis=1)
    with warnings.catch_warnings():
        fig, ax = plt.subplots() 
        sb.distplot(a=row_sums[row_sums >= MIN_DEG], ax=ax)
    return fig, ax

def deg_hist_style(fig, axes, title):
    set_size(fig)
    sb.set(font_scale=SEABORN_FONT_SCALE)
    set_size(fig, FIG_SIZE_WIDTH, FIG_SIZE_HEIGHT)
    axes.set_title(title, fontsize=TITLE_SIZE)
    axes.tick_params(labelsize=TICK_LABEL_SIZE)
    # axes.set(ylim=(0, 100))
    # axes.set(xlim=(0, 7200))
    
    axes.set_facecolor('white')
    # axes.grid()
    axes.spines['bottom'].set_color('0.5')
    axes.spines['top'].set_color('0.5')
    axes.spines['right'].set_color('0.5')
    axes.spines['left'].set_color('0.5')
    # axes.grid(b=True, which='major', color='b', linewidth=1.0)
    axes.grid(b=True, which='major', color='gray', linewidth=0.15)
    #     plt.tick_params(axis='both', which='major', labelsize=32)
    # plt.tick_params(axis='both', which='minor', labelsize=32)
    plt.title(title, x=0.16, y=0.90, fontsize=TITLE_SIZE)
    axes.xaxis.set_label_coords(0.94, 0.16)

def status_hist_content(df):
    with warnings.catch_warnings():
        fig, ax = plt.subplots() 
        sb.distplot(a=df['% C0'], ax=ax)
    return fig, ax

def status_hist_style(fig, axes, title):
    print("hi")

def postprocess_in_deg_histogram(config_obj, csr_adj_matrix):
    print("-------- Creating in_degree_Histogram --------")
    fig, axes = in_deg_hist_content(csr_adj_matrix)
    title = 'In Degree Histogram'
    deg_hist_style(fig, axes, title)
    img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(config_obj['component_no']) + ".png"
    save_dir = get_plots_folder(config_obj) + "in_deg_histogram/"
    save_fig(fig, save_dir, img_name)

def postprocess_out_deg_histogram(config_obj, csr_adj_matrix):
    print("-------- Creating out_degree_Histogram --------")
    fig, axes = out_deg_hist_content(csr_adj_matrix)
    title = 'Out Degree Histogram'
    deg_hist_style(fig, axes, title)
    img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(config_obj['component_no']) + ".png"
    save_dir = get_plots_folder(config_obj) + "out_deg_histogram/"
    save_fig(fig, save_dir, img_name)

def postprocess_status_histogram(config_obj):
    print("-------- Creating C0 Histogram --------")
    df = postprocess_vertex_df(config_obj, True)
    cols = ["Vert ID", "% C0"]

    df = df[cols]
    fig, axes = status_hist_content(df)

    title = 'status '
    status_hist_style(fig, axes, title)

    img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(config_obj['component_no']) + ".png"
    save_dir = get_plots_folder(config_obj) + "status_histogram/"
    save_fig(fig, save_dir, img_name, df)

def postprocess_histograms(config_obj):
    #print("-------- Creating histograms (in degree, out degree, C0) --------")
    print("-------- Creating C0 histogram --------")
    csr_adj_matrix = get_full_unsym_csr_adj(config_obj)
    #postprocess_in_deg_histogram(config_obj, csr_adj_matrix)
    #postprocess_out_deg_histogram(config_obj, csr_adj_matrix)
    postprocess_status_histogram(config_obj)
    print("-------- Done creating histograms --------------------------------")

