# Step (0): Import Libraries
# -----------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import plot, draw, show
import seaborn as sns; sns.set()  # for plot styling
import random
import sys
import time
from shapely.geometry import Point
import geopandas as gpd #install packages manual: https://stackoverflow.com/questions/54734667/error-installing-geopandas-a-gdal-api-version-must-be-specified-in-anaconda
from geopandas import GeoDataFrame
from sklearn.cluster import KMeans
from kmodes.kprototypes import KPrototypes #k-prototypes algorithm https://pypi.org/project/kmodes/
import alphashape  #for drawing hull around scatter plot https://pypi.org/project/alphashape/, https://stackoverflow.com/questions/17553035/draw-a-smooth-polygon-around-data-points-in-a-scatter-plot-in-matplotlib
from descartes import PolygonPatch
#import cartopy.crs as ccrs


# Step (1): Read Data
#-----------------------------------------------------------------------------------
col_names = list(pd.read_csv("original_data/fatal-police-shootings-data-semicolon.csv",
                             sep=";",
                             nrows=0))

csv_data_original = pd.read_csv("original_data/fatal-police-shootings-data-semicolon.csv",
                       names = col_names,
                       skiprows=1,
                       dtype={'id': np.int64, #is optional; python can detect by itself;
                              #watch out when opening csv in Excel: if you press save, Excel might convert floats into date format.
                              #To prevent this, see instructions here: First load data into Excel with correct format
                              #https://support.insight.ly/hc/en-us/articles/212277188-How-to-open-a-CSV-file-in-Excel-to-fix-date-and-other-formatting-issues
                              #but converting this to csv again, everything gets lost again..so: see this solution with "="
                              # https://stackoverflow.com/questions/165042/stop-excel-from-automatically-converting-certain-text-values-to-dates
                              # you can specify the date format here
                              'name': object,
                              'date': object,
                              'manner_of_death': object,
                              'armed': object,
                              'age': np.float64, #for some reason only float works,...maybe because of NA values
                              'gender': object,
                              'race': object,
                              'city': object,
                              'state': object,
                              'signs_of_mental_illness': bool,
                              'threat_level': object,
                              'flee': object,
                              'body_camera': bool,
                              'longitude': np.float64,
                              'latitude': np.float64,
                              'is_geocoding_exact': bool
                              },
                       sep=";"#,
                       #nrows=10 #this restriction is for testing purposes
                       )
#print(csv_data.loc[:,["longitude","latitude"]])
#print(csv_data.longitude)
# print(tabulate(csv_data#,
#                #tablefmt="fancy_grid"
#                )) #this looks more beautiful than print(csv_data)
#print(csv_data.dtypes)

# Step (2): Manipulate Data (turn into gdf: geographic data file...)
#-----------------------------------------------------------------------------------
gdf = csv_data_original[csv_data_original['longitude'].notna() & csv_data_original['latitude'].notna()] #for geodata dataframe remove rows with now values for longitude and latitude
gdf = gpd.GeoDataFrame(gdf,
                       geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude) #transform longitude and latitude into a list of shapely
                       )
#print(gdf.head())
#print(gdf)

# Step (3): Settings, Parameters, ...
#-----------------------------------------------------------------------------------
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))  # world map

# Step (4): Plot all data into a map
#-----------------------------------------------------------------------------------
if(False):
    print("Plotting general data...")
    #restrict to United States of America
    ax = world[world.name == 'United States of America'].plot(
        color='white', edgecolor='black')
    gdf.plot(ax=ax, color='red', markersize=3)
    plt.suptitle("All police shooting data points from 02.01.2015 to 08.12.2020")
    ax.grid(False) # Hide grid lines
    ax.set_xticks([]); ax.set_yticks([]) # Hide axes ticks

    fig = plt.gcf() #get current figure (this is used because savefig will create a not suitable size)
    fig.set_size_inches((15, 5), forward=False)
    plt.savefig("img_rq1/data_plot_all_data.png", dpi=800) #dpi=800 etc.; looks different that if shown: so: dpi=fig.dpi, bbox_inches='tight',
    #plt.show()
    print("General data has been plotted.")

# Step (5): Plot map step by step based on time of shooting (doesnt work well due to runtime problems)
#-----------------------------------------------------------------------------------
if(False):
    print("Plotting data successively...")
    #sort dataframe by time of shooting
    gdf_sorted = gdf.sort_values(by = "date", ascending = True)
    gdf_count_row = gdf_sorted.shape[0]  # gives number of row count
    gdf_count_col = gdf_sorted.shape[1]  # gives number of col count

    ax = world[world.name == 'United States of America'].plot(
        color='white', edgecolor='black')

    #fig = plt.ion() #interactive on: for subsequent drawing...other possibilities are    #plt.pause(0.0000001): is too slow... #plt.show()    #draw()    #time.sleep(0.5)    #plt.close('plt') etc.
    for t in range(gdf_count_row):
        print("Shooting No. " + str(t))
        gdf_sorted.iloc[[t]].plot(ax=ax, color='red', markersize=3) #plot value no. n
        plt.pause(0.0000001)
        plt.suptitle("Police shooting on " + str(gdf_sorted.date.iloc[[t]].to_string(index=False)))

    ax.grid(False) # Hide grid lines
    ax.set_xticks([]); ax.set_yticks([]) # Hide axes ticks
    #plt.show()
    plt.waitforbuttonpress()
    print("Successively created data has been plotted.")


# Step (6): Cluster the data based on spatial information
#-----------------------------------------------------------------------------------
if(True):
    n_clusters = 3
    print("Plotting general data and cluster it...")
    ax = world[world.name == 'United States of America'].plot(
        color='white', edgecolor='black')

    df_for_clustering = gdf[['longitude', 'latitude']] #todo ggf. wieder aufsplitten......
    kmeans = KMeans(n_clusters=n_clusters, algorithm="auto")
    kmeans.fit(df_for_clustering) #compute k-means clustering
    y_kmeans = kmeans.predict(df_for_clustering) #compute cluster centers and predict cluster index for each sample

    df_clustered = df_for_clustering.copy() #for some reason it needs the copy() method otherwise there is a warning
    df_clustered['cluster'] = y_kmeans  # add cluster col

    #df_clustered['geometry'] = gdf[['geometry']]  # add back geo data needed for plotting --> this is wrong! wont convert dataframe to geodataframe; this is necessary for the plot!
    df_clustered = gpd.GeoDataFrame(df_clustered, geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude))

    cluster_types = np.arange(n_clusters) #creates ndarray from 0 to n #= cluster_types = df_clustered['cluster'].unique()
    list_of_used_colors = sns.color_palette("Set2", n_clusters) #see color palettes here: http://seaborn.pydata.org/tutorial/color_palettes.html
    color_map = dict(zip(cluster_types, list_of_used_colors))

    for current_cluster in cluster_types: #loop plot over clusters (for different color reasons); there is no other clean solution for geopandas
        df_clustered[df_clustered['cluster'] == current_cluster].plot(ax=ax,
                                                   color=color_map[current_cluster], #for individual color according to color_palette
                                                   markersize=5,
                                                   label="Cluster " + str(current_cluster))

    ax.legend(loc='best') #loc='upper right'
    plt.suptitle("All police shooting data points from 02.01.2015 to 08.12.2020 (clustered)")
    ax.grid(False) # Hide grid lines
    ax.set_xticks([]); ax.set_yticks([]) # Hide axes ticks

    fig = plt.gcf() #get current figure (this is used because savefig will create a not suitable size)
    fig.set_size_inches((15, 5), forward=False)
    plt.savefig("img_rq1/data_plot_all_data_clustered.png", dpi=800)
    #plt.show()
    print("General data has been plotted and clustered...")



# Step (7): Define function for plotting data depending on category
#-----------------------------------------------------------------------------------
def plot_map_divided_by_category(df, df_cat, cat_title, mode='silent'):
    """
    This function is for plotting the data separated by two location dimensions (longitude, latitude) and a third parameter/category on a map.
    The category of the data is visualized by a distinctive color on the map. This function just separates the data by the category.
    For clustering the data regarding the two spatial dimensions and the third category see the function plot_map_and_cluster

    :param df: dataframe including spatial data and at least one further category
    :param df_cat: selected category col in dataframe
    :param cat_title: title of category, only used for plotting
    :param mode: either 'silent' for calculation in background and saving the plots to files; or 'user' for iteraction (user needs to confirm to go to next topic)
    :return: plot the data (see description above)
    """
    print("Graph for the topic " + str(cat_title + " will be plotted..."))
    ax = world[world.name == 'United States of America'].plot(
        color='white', edgecolor='black')

    df = df[df[df_cat].notna()] #remove nan values (not available); might cause statistical problem; maybe print information here...
    categories = df[df_cat]
    category_types = categories.unique() #or: list(set(classes))
    amount_of_categories = len(category_types)
    list_of_used_colors = sns.color_palette("Set2", amount_of_categories) #see color palettes here: http://seaborn.pydata.org/tutorial/color_palettes.html
    color_map = dict(zip(category_types, list_of_used_colors))

    for current_category in category_types: #loop plot over categories (for different color reasons); there is no other clean solution for geopandas
        df[df[df_cat] == current_category].plot(ax=ax,
                                                   color=color_map[current_category], #for individual color according to color_palette
                                                   markersize=5,
                                                   label=current_category)

    ax.legend(loc='best') #loc='upper right'
    plt.suptitle("Police shootings depending on " + cat_title)
    ax.grid(False) # Hide grid lines
    ax.set_xticks([]); ax.set_yticks([]) # Hide axes ticks

    fig = plt.gcf() #get current figure (this is used because savefig will create a not suitable size)
    fig.set_size_inches((15, 5), forward=False)
    plt.savefig("img_rq1/data_plot_category_" + str(df_cat) + ".png", dpi=800)
    if(mode=='user'):
        plt.show()
    print("Data for the topic " + str(cat_title + " has been plotted..."))


# Step (8): Define function for clustering the already plotted data and plot this clustered data
#-----------------------------------------------------------------------------------
def plot_map_and_cluster(df, df_cat, cat_title, n_clusters=4, mode='silent'):
    """
    This function is for clustering data with two location dimensions (longitude, latitude) and a third parameter/category.
    It will visualize the clusters by plotting the data on a map. The spatial dimensions can be seen on map, the third category
    is seen by color, the cluster attribution can by seen by the shape and the edge color.
    For clustering the k-prototypes algorithm will be used.
    :param df: dataframe including spatial data and at least one further category
    :param df_cat: selected category col in dataframe
    :param cat_title: title of category, only used for plotting
    :param mode: either 'silent' for calculation in background and saving the plots to files; or 'user' for iteraction (user needs to confirm to go to next topic)
    :param n_clusters: amount of clusters for k prototype algorithm
    :return: cluster the data and plot the clustered data (see description above)
    """

    print("Clustering data for the topic " + str(cat_title + " will be plotted..."))
    df_relevant = df[['id', 'longitude', 'latitude', df_cat, 'geometry']]  # keep only the three dimensions relevant for clustering (longitude, latitue, df_cat), but also the ID and geometry shape data (for plotting)
    df_relevant = df_relevant[df_relevant[df_cat].notna()]  # remove nan values for third category; for long. and lat. already done, might cause statistical problem; maybe print information here...

    df_for_clustering = df_relevant[['longitude', 'latitude', df_cat]]  # remove ID entryand geometry shape data for the dataframe used for clustering algorithm
    df_ID = df_relevant[['id']]  # later map cluster result to ID
    ID_as_array = df_ID.to_numpy()  # convert to numpy ndarray
    geometry_data = df_relevant[['geometry']]

    kproto = KPrototypes(n_clusters=n_clusters, init='Huang', verbose=2, max_iter=100)
    clusters = kproto.fit_predict(df_for_clustering, categorical=[2])  # last col is category; remaining is numeric

    #cluster centroids of the trained mode are stored here:
    cluster_centroids = kproto.cluster_centroids_
    cluster_centroids_category = cluster_centroids[1]
    cluster_centroids_geodata = cluster_centroids[0]
    cluster_centroids_longitude = cluster_centroids_geodata[:,0]
    cluster_centroids_latitude = cluster_centroids_geodata[:,1]
    df_category = pd.DataFrame(data=np.array(cluster_centroids_category).flatten())
    df_longitude = pd.DataFrame(data=np.array(cluster_centroids_longitude).flatten())
    df_latitude = pd.DataFrame(data=np.array(cluster_centroids_latitude).flatten())
    df_centroids = pd.concat([df_category, df_longitude, df_latitude], axis=1, sort=False)
    df_centroids.columns = ['category', 'longitude', 'latitude']
    df_centroids = gpd.GeoDataFrame(df_centroids, # transform longitude and latitude again back into a list of shapely
                           geometry=gpd.points_from_xy(df_centroids.longitude, df_centroids.latitude)
                           )

    #training statistics
    #print("Cost: " + str(kproto.cost_))
    #print("Iteration: " + str(kproto.n_iter_))

    #attributions
    # for i, c in zip(ID_as_array, clusters):
    #     print("ID: {}, Cluster:{}".format(i, c))

    # add the cluster attribution as a new col to the dataframe and use it later as a forth dimension to plot; also add geometry data shape again
    df_clustered = df_relevant  # create a new df including the three categories, ID and cluster col
    df_clustered['cluster'] = clusters  # add cluster col
    df_clustered['geometry'] = geometry_data

    #add geometry shape data again; plot the data into but this time including the separation between clusters and including the cluster center/centroid/prototypes
    ax = world[world.name == 'United States of America'].plot(
        color='white', edgecolor='black')

    #colors depending on category
    categories = df_clustered[df_cat]
    category_types = categories.unique() #or: list(set(classes))
    amount_of_categories = len(category_types)
    list_of_used_colors = sns.color_palette("Set2", amount_of_categories) #see color palettes here: http://seaborn.pydata.org/tutorial/color_palettes.html
    color_map = dict(zip(category_types, list_of_used_colors))

    #shapes (markers) depending on cluster
    # clusters: already existing
    cluster_types = list(set(clusters))
    amount_of_clusters = len(cluster_types) #already done in prototype function: n_clusters=...
    list_of_potential_shapes = ["v", "^", "<", ">", "o", "s", "p", "P", "*", "X", "D"]
    list_of_used_shapes = list_of_potential_shapes[:amount_of_clusters]
    shape_map = dict(zip(cluster_types, list_of_used_shapes))

    #also border color (edgecolor) depending on cluster (for better visualization)
    list_of_potential_edgecolors = ['black', 'blue', 'red', 'violet', 'orange'] #'face' means: edge color = scatterplot color
    list_of_used_edgecolors = list_of_potential_edgecolors[:amount_of_clusters]
    edgecolor_map = dict(zip(cluster_types, list_of_used_edgecolors))

    for current_cluster in cluster_types: #loop over clusters
        for current_category in category_types:  # loop plot over categories (for different color reasons); there is no other clean solution for geopandas

            #plot all the normal points depending on category and cluster
            df_clustered[(df_clustered[df_cat] == current_category)&(df_clustered['cluster'] == current_cluster)].plot(ax=ax,
                                                       color=color_map[current_category], #for individual color for each category
                                                       markersize=12,
                                                       edgecolors=edgecolor_map[current_cluster],
                                                       linewidths=0.25,
                                                       marker=shape_map[current_cluster], #for individual shape for each cluster
                                                       label="Category: " + str(current_category) + " | Cluster: " + str(current_cluster))

        #for each cluster also add alpha shape (hull aroud data for better visualiziation): i dont do this cause cartopy package makes installation problems...
        #points = df_clustered[df_clustered['cluster'] == current_cluster]

        #for each cluser also print the center/prototype of the cluster; use also same color and edge color but other/bigger shape
        df_centroids.iloc[[current_cluster],:].plot( #first row is cluster one, second line is cluster two etc.
            ax=ax,
            color="black",  # for individual color for each category
            markersize=35,
            edgecolors=edgecolor_map[current_cluster],
            linewidths=0.25,
            marker=shape_map[current_cluster])  # for individual shape for each cluster

    ax.legend(loc='best') #loc='upper right'
    plt.suptitle("Police shootings depending on " + cat_title)
    ax.grid(False) # Hide grid lines
    ax.set_xticks([]); ax.set_yticks([]) # Hide axes ticks

    fig = plt.gcf()  # get current figure (this is used because savefig will create a not suitable size)
    fig.set_size_inches((15, 5), forward=False)
    plt.savefig("img_rq1/data_cluster_plot_category_" + str(df_cat) + ".png", dpi=800)
    if (mode == 'user'):
        plt.show()
    print("Clustering data for the topic " + str(cat_title + " has been plotted..."))


# Step (9): Plot data into map: divided by different categories
#-----------------------------------------------------------------------------------

#divided by death
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='manner_of_death', cat_title='manner of death')
    plot_map_and_cluster(df=gdf, df_cat='manner_of_death', cat_title='manner of death', n_clusters=5)

#divided by weapon
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='armed', cat_title='weapon')
    #if time available you could merge categories for better plotting, but I wont do that

#divided by gender
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='gender', cat_title='gender')
    plot_map_and_cluster(df=gdf, df_cat='gender', cat_title='gender', n_clusters=5)

#divided by race
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='race', cat_title='race')
    plot_map_and_cluster(df=gdf, df_cat='race', cat_title='race', n_clusters=5)

#divided by mental illness
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='signs_of_mental_illness', cat_title='signs of mental illness')
    plot_map_and_cluster(df=gdf, df_cat='signs_of_mental_illness', cat_title='signs of mental illness', n_clusters=5)

#divided by threat level
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='threat_level', cat_title='threat level')

#divided by escape
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='flee', cat_title='escape')

#divided by body camera
#-----------------------------------------------------------------------------------
if(True):
    plot_map_divided_by_category(df=gdf, df_cat='body_camera', cat_title='body camera')

print("Programm finished successfully.")