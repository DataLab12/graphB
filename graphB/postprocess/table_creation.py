import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import linear_model
import matplotlib.pyplot as plt
import six

from postprocess.df_creation import postprocess_tree_df, postprocess_vertex_df
from dataset_paths import get_tables_folder, get_matrix_names_for_type_and_dataset, get_df_folder, create_if_not_exists

def postprocess_all_tables(config_obj):
    postprocess_vertex_table(config_obj)
    postprocess_tree_table(config_obj)
    postprocess_tree_corr_table(config_obj)

def postprocess_tree_corr_table(config_obj):
    df = postprocess_tree_df(config_obj, True)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(df.corr(method='pearson'), annot=True, fmt='.2f', cmap=plt.get_cmap('coolwarm'), cbar=False, ax=ax)
    ax.set_yticklabels(ax.get_yticklabels(), rotation="horizontal")
    img_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(
        config_obj['component_no']) + ".png"
    save_dir = get_tables_folder(config_obj) + "tree_corr/"
    create_if_not_exists(save_dir)
    plt.savefig(save_dir + img_name, bbox_inches='tight', pad_inches=0.0)
    csv_name = config_obj['data_subset_type'] + "_" + config_obj['matrix_name'] + "_" + str(
        config_obj['component_no']) + ".csv"
    df.corr(method='pearson').to_csv(save_dir + csv_name, encoding='utf-8')


########################################################################
### function to generate twin tables
########################################################################

def get_tree_dfs_of_type(config_obj):
    return get_dfs_of_type(config_obj, "tree")


def get_vertex_dfs_of_type(config_obj):
    return get_dfs_of_type(config_obj, "vertex")


def get_dfs_of_type(config_obj, df_type):
    # step 1: go to configs/dataset/matrix_type/
    # step 2: get list of all folder names (i.e. WE1, WE2..)
    # step 3: create a new dictionary
    # step 4: for each folder name, create folder name : data dictionary key value pair
    # step 5: return
    matrix_names_list = get_matrix_names_for_type_and_dataset(config_obj)
    # print("matrix_names_list: ", matrix_names_list)
    df_dict = {
        matrix_name: pd.read_pickle(
            get_df_folder(config_obj) + config_obj['data_subset_type'] + "_" + matrix_name + "_" + str(
                config_obj['component_no']) + "_" + df_type + "_df.pkl")
        for matrix_name in matrix_names_list
    }
    # print("Df dict: ", df_dict)
    return df_dict


def postprocess_tree_table(config_obj):
    print("-------- Retrieving Tree Table --------")
    if config_obj['has_labels']:
        df_dict = get_tree_dfs_of_type(config_obj)
        matrix_list_sorted = [matrix_name for matrix_name in df_dict]
        matrix_list_sorted.sort()
        indices = np.array([matrix_name for matrix_name in matrix_list_sorted])
        cols = ['A', 'B', 'R^2', 'Centroid_X', 'Centroid_Y', 'STDev_X', 'STDev_Y', 'Mean_Point_Dif', 'Stdev_Point_Dif']
        data = [get_twin_table_row(df_dict[matrix_name]) for matrix_name in matrix_list_sorted]
        df = pd.DataFrame(data, index=indices, columns=cols).round(2).fillna("")
        ax = render_mpl_table(df)
        fig = ax.get_figure()

        img_name = config_obj['data_subset_type'] + ".png"
        save_dir = get_tables_folder(config_obj) + "tree/"
        print("Saving tree table to: ", save_dir + img_name)
        save_fig(fig, save_dir, img_name)
        df.to_csv(save_dir + config_obj['data_subset_type'] + '.csv', encoding='utf-8')
    else:
        print("Warning: this dataset has no labels, so we can't create a tree table.")


def get_twin_table_row(df):
    if df is not None:
        model = linear_model.LinearRegression()
        Centroid_X = None
        STDev_X = None
        Centroid_Y = None
        STDev_Y = None
        Mean_Point_Dif = None
        Stdev_Point_Dif = None
        R_Sq = None
        # df.fillna(0, inplace=True)
        # model = sm.ols(formula="aMaj ~ Det", data=df).fit()
        X = df['tree_bias_score'].values.reshape(-1, 1)
        y = df['aMaj_pct']
        try:
            model.fit(X, y)
        except ValueError:
            print("We have NaNs...")
            df.fillna(0, inplace=True)
            X = df['tree_bias_score'].values.reshape(-1, 1)
            model.fit(X, y)
        Centroid_X = df['tree_bias_score'].mean()
        STDev_X = df['tree_bias_score'].std()
        Centroid_Y = df['aMaj_pct'].mean()
        STDev_Y = df['aMaj_pct'].std()
        R_Sq = model.score(X, y)

        A = model.coef_[0]
        B = model.intercept_

        return [A, B, R_Sq, Centroid_X, Centroid_Y, STDev_X, STDev_Y, Mean_Point_Dif, Stdev_Point_Dif]
    else:
        return [np.nan for i in range(11)]


########################################################################
### function to generate shelf tables
########################################################################

def postprocess_vertex_table(config_obj):
    print("-------- Retrieving Vertex Table --------")
    df_dict = get_vertex_dfs_of_type(config_obj)
    cols = None
    data = None
    if config_obj['has_labels']:
        cols = ['Vertex Total', 'Promoted', 'Not Promoted', 'Voted', 'Mean aMaj Mem %', \
                'Stdev aMaj Mem %', 'Mean aMaj Mem % (Promoted)', 'Stdev aMaj Mem % (Promoted)', \
                'Mean aMaj Mem % (Not)', 'Stdev aMaj Mem % (Not)', 'Mean aMaj Mem % (Voted)',
                'Stdev aMaj Mem % (Voted)', \
                'Voted vs Total Delta', 'Voted vs Promoted Delta', 'Voted vs Not Delta']
        data = [get_outcome_shelf_table_row(df_dict[matrix_name]) for matrix_name in sorted(df_dict)]
    else:
        cols = ['Vertex Total', 'Mean aMaj Mem %', 'Stdev aMaj Mem %']
        data = [get_shelf_table_row(df_dict[matrix_name]) for matrix_name in sorted(df_dict)]
    df = pd.DataFrame(data, index=sorted(df_dict), columns=cols).round(2).fillna("")
    ax = render_mpl_table(df)
    fig = ax.get_figure()

    img_name = config_obj['data_subset_type'] + ".png"
    save_dir = get_tables_folder(config_obj) + "vertex/"
    print("Saving vertex table to: ", save_dir + img_name)
    save_fig(fig, save_dir, img_name)
    df.to_csv(save_dir + config_obj['data_subset_type'] + '.csv', encoding='utf-8')


def get_shelf_table_row(df):
    # cols = ['Vertex Total', 'Mean aMaj Mem %', 'Stdev aMaj Mem %']
    if df is not None:
        v_amt = len(df.index)
        mc0pct_total = df['% aMaj'].mean()
        stc0pct_total = df['% aMaj'].std()

        return [v_amt, mc0pct_total, stc0pct_total]
    else:
        return [np.nan for i in range(3)]


def get_outcome_shelf_table_row(df):
    if df is not None:
        w_df = df.loc[df['outcome'] == 1]
        l_df = df.loc[df['outcome'] == 0]
        n_df = df.loc[df['outcome'] == -1]

        v_amt = len(df.index)
        promoted = len(w_df.index)
        not_promoted = len(l_df.index)
        voted = len(n_df.index)
        mc0pct_total = df['% aMaj'].mean()
        stc0pct_total = df['% aMaj'].std()
        mc0pct_promoted = w_df['% aMaj'].mean()
        stc0pct_promoted = w_df['% aMaj'].std()
        mc0pct_not_promoted = l_df['% aMaj'].mean()
        stc0pct_not_promoted = l_df['% aMaj'].std()
        mc0pct_voted = n_df['% aMaj'].mean()
        stc0pct_voted = n_df['% aMaj'].std()

        voted_vs_total_delta = mc0pct_voted - mc0pct_total
        voted_vs_promoted_delta = mc0pct_voted - mc0pct_promoted
        voted_vs_not_promoted_delta = mc0pct_voted - mc0pct_not_promoted

        return [v_amt, promoted, not_promoted, voted, mc0pct_total, stc0pct_total,
                mc0pct_promoted, stc0pct_promoted, mc0pct_not_promoted, stc0pct_not_promoted,
                mc0pct_voted, stc0pct_voted,
                voted_vs_total_delta, voted_vs_promoted_delta, voted_vs_not_promoted_delta]
    else:
        return [np.nan for i in range(12)]


def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return ax


def save_fig(fig, directory, file_name):
    FULL_FILE_PATH = directory + file_name
    create_if_not_exists(directory)
    fig.savefig(FULL_FILE_PATH)
