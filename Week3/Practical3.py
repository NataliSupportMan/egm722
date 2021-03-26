#!/usr/bin/env python
# coding: utf-8

# # EGM722 - Week 3 Practical: Vector data using shapely and geopandas
# 
# ## Overview
# 
# Up to now, you have gained some experience working with basic features of python, and used cartopy and matplotlib to create a map. In each of these practicals, you have loaded different vector datasets using a module called geopandas. In this week's practical, we'll be looking at working vector data in a bit more depth, including the different geometry types available using shapely, analyses like spatial joins and summarizing based on attributes, and how to reproject vector data from one coordinate reference system to another.
# 
# 
# ## Objectives
# -  Gain experience working with different vector data types using shapely
# -  Use geopandas to re-project vector datasets from one coordinate reference system to another
# -  Summarize features using the groupby method of a GeoDataFrame
# -  Learn how to perform different vector data operations using geopandas and shapely
# 
# ## Data provided
# 
# In the data\_files folder, you should have the following:
# -  NI_roads.shp, a shapefile of roads in Northern Ireland
# -  Counties.shp, a shapefile of county outlines for Northern Ireland
# -  NI_Wards.shp, a shapefile of electoral wards for Northern Ireland
# 
# ## 1. Getting started
# 
# In this practical, we'll be working with vector data. As a quick refresher, the three main types of vector data that we will work with are:
# 
# -  __Point__: point data represent a single point in space. For our purposes, points are either two-dimensional (x, y) or three-dimensional (x, y, z). In shapely, the corresponding __class__ of data is a __Point__.
# -  __Line__: lines are a sequence of at least two points that are joined together. In shapely, the corresponding __class__ of data is known as a __LineString__.
# -  __Polygon__: polygons are a sequence of at least three points that are connected to form a ring, as well as any additional rings that represent holes in the polygon. In shapely, the corresponding __class__ of data is a __Polygon__.
# 
# We can also have __Collections__ of vector data, where each feature represents a collection of __Point__, __Line__, or __Polygon__ objects. In shapely, these are represented as __MultiPoint__, __MultiLineString__, or __MultiPolygon__ objects.
# 
# To get started, run the following cell to import geopandas and shapely.

# In[1]:


# this lets us use the figures interactively
get_ipython().run_line_magic('matplotlib', 'notebook')

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon


# ## 2. Shapely geometry types
# ### 2.1 Points
# As we saw in Week 1, to create a Point, we pass x, y (and optionally, z) coordinates to the Point class constructor:

# In[2]:


pt = Point(-6.677, 55.150) # creates a 2d point with coordinates -6.677, 55.150
pt2 = Point(-6.658, 55.213)

pt3d = Point(86.925278, 27.988056, 8848.86) # creates a 3d point

print(pt) # print a well-known text (WKT) representation of the Point object


# The last line, `print(pt)`, prints a [well-known-text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) (WKT) representation of the __Point__ object. WKT is a standard representation of vector geometry objects - most `python` libraries and GIS softwares are able to read and/or translate WKT into other formats, such as ESRI Shapefiles, GeoJSON, etc.
# 
# Remember that in python, we can find the attributes and methods for an object by looking up the documentation (for shapely, this can be found [here](https://shapely.readthedocs.io/en/stable/manual.html)), or using the built-in function `dir()`. To find out more about a particular function, we can use the built-in function `help()` (or, in jupyter notebooks/ipython, the `?` operator).
# 
# As an example, let's use the built-in function `dir()` to look at the methods and attributes associated with the __Point__ class:
# 
# ```python
# In [1]: print(dir(pt))
# ['__and__', '__array_interface__', '__bool__', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__geo_interface__', '__geom__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__or__', '__p__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__weakref__', '__xor__', '_crs', '_ctypes_data', '_geom', '_get_coords', '_is_empty', '_lgeos', '_ndim', '_other_owned', '_repr_svg_', '_set_coords', 'almost_equals', 'area', 'array_interface', 'array_interface_base', 'boundary', 'bounds', 'buffer', 'centroid', 'contains', 'convex_hull', 'coords', 'covers', 'crosses', 'ctypes', 'difference', 'disjoint', 'distance', 'empty', 'envelope', 'equals', 'equals_exact', 'geom_type', 'geometryType', 'has_z', 'hausdorff_distance', 'impl', 'interpolate', 'intersection', 'intersects', 'is_closed', 'is_empty', 'is_ring', 'is_simple', 'is_valid', 'length', 'minimum_clearance', 'minimum_rotated_rectangle', 'overlaps', 'project', 'relate', 'relate_pattern', 'representative_point', 'simplify', 'svg', 'symmetric_difference', 'to_wkb', 'to_wkt', 'touches', 'type', 'union', 'within', 'wkb', 'wkb_hex', 'wkt', 'x', 'xy', 'y', 'z']
# ```
# 
# Here, in addition to the __special__ or __magic__ methods (denoted with \_\_ at the beginning and end of the method name), there are a number of methods that we might find useful, including `Point.distance()`. To see what this method does, we can use `help(Point.distance)`:
# 
# ~~~python
# In [2]: help(Point.distance)
# Help on method distance in module shapely.geometry.base:
# 
# distance(other) method of shapely.geometry.point.Point instance
#     Unitless distance to other geometry (float)
# ~~~
# 
# So, `Point.distance()` provides the distance from the point object to some other geometry. Because shapely does not directly deal with coordinate systems, this distance is __unitless__. This means that __we have to make sure that the two objects have the same reference system - if we do not, the distance returned will not make sense.__ We will cover working with coordinate reference systems later on in the practical.
# 
# <span style="color:#009fdf;font-size:1.1em;font-weight:bold">Use the cell below to work out how we can access the x, y coordinates of a __Point__ object. Can you see more than one way to do this? If so, are there differences between them?</span>

# In[3]:


pt = Point(-6.677, 55.150)
pt2 = Point(-6.658, 55.213)
points_df = gpd.GeoDataFrame({'geometry': [pt, pt2]}, crs='EPSG:4326')
points_df = points_df.to_crs('EPSG:29901')
points_df2 = points_df.shift() #We shift the dataframe by 1 to align pnt1 with pnt2
points_df.distance(points_df2)


# One of the common operations we might want to do with a Point object is to create a __buffer__ around the point. In the list of associated methods and attributes of Point objects above, you should see there is a method called `buffer`. A look at the help for this method:
# 
# ```python
# In [3]: help(Point.buffer)
# Help on method buffer in module shapely.geometry.base:
# 
# buffer(distance, resolution=16, quadsegs=None, cap_style=1, join_style=1, mitre_limit=5.0, single_sided=False) method of shapely.geometry.point.Point instance
#     Get a geometry that represents all points within a distance
#     of this geometry.
#     
#     A positive distance produces a dilation, a negative distance an
#     erosion. A very small or zero distance may sometimes be used to
#     "tidy" a polygon.
#     
#     Parameters
#     ----------
#     distance : float
#         The distance to buffer around the object.
#     resolution : int, optional
#         The resolution of the buffer around each vertex of the
#         object.
# ...
# ```
# 
# shows that `buffer` takes a __positional parameter__ of _distance_, as well as a number of __keyword parameters__ that determine how the buffer operation is done. Remember that the buffer distance will be in the same coordinate system as our point - shapely does not, by itself, do any conversion between coordinate systems or units. 
# 
# Note that the object returned by buffer is a Polygon, rather than a point - this makes sense, as the buffer is a two-dimensional surface around the point location.   

# In[4]:


pt_buffer = pt.buffer(0.001)
print(type(pt_buffer))


# ### 2.2. LineStrings
# Instead of using a single x, y coordinate pair, a __LineString__ object takes either a list of __Point__ objects, or a list of coordinate __tuples__:

# In[5]:


line1 = LineString([pt, pt2]) # method one of creating a LineString, using a list of Point objects
line2 = LineString([(-6.677, 55.150), (-6.658, 55.213)]) # method two, using a list of coordinate tuples

print(line1)
print(line2)

line1.equals(line2) # check to see if these are the same geometry


# The coordinates of a __LineString__ are stored as a __tuple__ in an attribute called __xy__. The __tuple__ has two items representing the X and Y coordinate values. If we want the x and y coordinates as separate variables, we can access them using their respective indices:
# 
# ```python
# In [4]: x = line1.xy[0]
# In [5]: y = line1.xy[1]
# ```
# 
# We can also combine this using __tuple assignment__, or __unpacking__, which assigns values from a __tuple__ on the right-hand side of the assignment to a comma-separated grouping of variables on the left-hand side:

# In[6]:


x, y = line1.xy

print(x)
print(y)


# __LineString__ objects have a number of the same methods that __Point__ objects do, including `buffer` and `distance`. __LineString__ objects also have a `length` (just like with distance, it is __unitless__):

# In[7]:


print(line1.length)


# We can also find the `centroid` (center) of the __LineString__:

# In[8]:


center = line1.centroid # get the centerpoint of the line
print(line1.centroid)


# The last two methods of __LineString__ objects that we will explore for now are `project` and `interpolate`:
# 
# ```python
# In [6]: help(LineString.project)
# Help on function project in module shapely.geometry.base:
# 
# project(self, other, normalized=False)
#     Returns the distance along this geometry to a point nearest the
#     specified point
#     
#     If the normalized arg is True, return the distance normalized to the
#     length of the linear geometry.
# ```
# 
# So `project` returns the distance along the __LineString__ that comes closest to the __Point__ (or other object). `interpolate`, on the other hand, does something a bit different:
# 
# ```python
# In [7]: help(LineString.interpolate)
# Help on function interpolate in module shapely.geometry.base:
# 
# interpolate(self, distance, normalized=False)
#     Return a point at the specified distance along a linear geometry
#     
#     Negative length values are taken as measured in the reverse
#     direction from the end of the geometry. Out-of-range index
#     values are handled by clamping them to the valid range of values.
#     If the normalized arg is True, the distance will be interpreted as a
#     fraction of the geometry's length.
# ```
# 
# it returns the point along the line at a specified distance; the distance can be in the units of the __LineString__'s coordinates (`normalized=False`), or it can be as a fraction of the total length of the __LineString__ (`normalized=True`).

# In[9]:


line1.project(center) / line1.length # check to see how far along the line our centerpoint is

print(center)
print(line1.interpolate(0.5, normalized=True))


# ###  2.3. Polygons
# The last basic geometry type we will look at in this practical are __Polygon__ objects. Similar to __LineString__ objects, we can create a __Polygon__ object using a list of coordinate pairs, or a list of __Point__ objects:

# In[10]:


poly1 = Polygon([(-6.677, 55.150), (-6.658, 55.213), (-6.722, 55.189)])
poly2 = Polygon([pt, pt2, Point(-6.722, 55.189)])

print(poly1) # print a well
print(poly2)
print(poly1.equals(poly2))


# Note that even though we only passed three __Point__ objects (or coordinate pairs) to the __Polygon__ constructor, the __Polygon__ has four vertices, with the first and last vertex being the same - this is because the __Polygon__ exterior is _closed_. Note also the double parentheses - this is because a __Polygon__ potentially has two sets of coordinates - the _Shell_, or _exterior_, and _holes_, or _interiors_. To create a __Polygon__ with a hole in it, we would need to pass a list of coordinates that describe the _holes_:

# In[11]:


polygon_with_hole = Polygon(shell=[(-6.677, 55.150), (-6.658, 55.213), (-6.722, 55.189)],
                            holes=[[(-6.684, 55.168), (-6.704, 55.187), (-6.672, 55.196)]]) # note the double brackets

print(polygon_with_hole)


# Note the double brackets in the `holes` keyword argument - this is necessary, because `holes` is expecting a sequence of coordinate sequences that describe the _holes_ - effectively, a list of __Polygon__ shells.
# 
# Accessing the coordinates of a __Polygon__ object is a little more complicated than it is for __Point__ and __LineString__ objects - this is because __Polygon__ objects have two sets of coordinates, the exterior (_shell_) and interior (_holes_). But, the `exterior` attribute of the __Polygon__ is just a __LinearRing__ (a special case of __LineString__ where the first and last coordinates are the same), and the `interiors` attribute is an __InteriorRingSequence__ (basically, a collection of __LinearRings__ that have to obey [additional rules](https://shapely.readthedocs.io/en/stable/manual.html#polygons)):

# In[12]:


print(polygon_with_hole.exterior) # this is a single LinearRing
for lr in polygon_with_hole.interiors: # this is potentially multiple LinearRing objects
    print(lr)


# __Polygon__ objects have nonzero `area` and non-zero `length` (perimeter) - as with the equivalent attributes for __Point__ and __LineString__ objects, these are __unitless__. __Polygon__ objects also have a `centroid`, and we can bound the geometry using _either_ the minimum bounding box parallel to the coordinate axes (`envelope`), or a rotated minimum bounding box (`minimum_rotated_rectangle`):

# In[13]:


print('perimeter: ', poly1.length) # print the perimeter
print('area: ', poly1.area) # print the area
print('centroid: ', poly1.centroid) # get the centerpoint of the rectangle
print('bounding coordinates: ', poly1.bounds) # get the minimum x, minimum y, maximum x, maximum y coordinates
print('bounding box: ', poly1.envelope) # get the minimum bounding rectangle of the polygon, parallel to the coordinate axes
print('rotated bounding box: ', poly1.minimum_rotated_rectangle) # get the smallest possible rectangle that covers the polygon


# There are a number of additional methods that we will cover more as we continue through the practicals - for now, this should be enough to give an idea for how these geometry objects work.
# 
# ### 2.4 Interactions between geometry objects
# `shapely` also provides a number of methods that we can use to check the spatial relationship between different objects. For example, the following code shows how we can use the `contains` [method](https://shapely.readthedocs.io/en/stable/manual.html#object.contains) of a shapely geometry object to see whether a __Point__ (or other geometry) is located fully within the object:

# In[14]:


poly = Polygon([(0, 0), (2, 0), (2, 3), (0, 3)])
pt1 = Point(0, -0.1)
pt2 = Point(1, 1)

print(poly.contains(pt1))
print(poly.contains(pt2))


# We can also check to see whether two geometry objects [intersect](https://shapely.readthedocs.io/en/stable/manual.html#object.intersects) using the `intersects` method. To actually get the intersection of the two geometries, we use the `intersection` method, which returns the geometry of the intersection (whether this is a __Point__, a __LineString__, a __Polygon__, or a mixed collection of geometries depends on the geometries and how they intersect): 

# In[15]:


line1 = LineString([(0, 0), (1, 1)])
line2 = LineString([(0, 1), (1, 0)])

print(line1.intersects(line2)) # intersects() returns True if the geometries touch/intersect/overlap, False otherwise
print(line1.intersects(poly))
print(line1.intersection(line2)) # if the geometries intersect, this will be the Point(s) of intersection


# There are a number of other methods provided by `shapely` that we can use to determine the relationship between geometry objects, including `touches`, `within`, and `overlaps`. Have a look at the full list from the [shapely user manual](https://shapely.readthedocs.io/en/stable/manual.html) to see the rest.
# 
# ## 3. geopandas GeoDataFrames

# We have used geopandas in the past two practicals to read provided shapefiles and work with the data they contain - in Practical 1, we translated a comma-separated variable (CSV) file into a shapefile, and in Practical 2, we read shapefile data and plotted it on a map using `cartopy`.
# 
# This week, we will extend this introduction to look at how we can use geopandas to do various GIS analyses, such as spatial joins and clipping operations, as well as projecting from one coordinate reference system to another.
# 
# To begin, load the __NI_roads__ dataset from the __data_files__ folder and print the __header__ (first 5 lines of the __GeoDataFrame__):

# In[16]:


roads = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\egm722\Week3\data_files\NI_roads.shp')
print(roads.head())


# So this dataset has three columns: __SURVEY__, __Road_class__, and __geometry__. Note that each of the geometries is a __LineString__ object, which means...
# 
# ### 3.1 Coordinate reference systems using PROJ
# To start with, let's see if we can figure out how many kilometers of motorway are represented in the dataset - i.e., the sum of the length of all of the __LineString__ objects that have the attribute _MOTORWAY_. First, Let's check what the coordinate reference system (CRS) of our __GeoDataFrame__ is, using the `crs` attribute:

# In[17]:


roads.crs


# So this dataset has a _Geographic_ coordinate reference system, __EPSG:4326__. EPSG codes (originally organized by the European Petroleum Survey Group) are a common way of working with coordinate reference systems. Each CRS in the [EPSG registry](https://epsg.org/home.html) has a unique code and standard well-known text representation.
# 
# The `crs` attribute of the __GeoDataFrame__ is actually a __pyproj.CRS__ object. [pyproj](https://pyproj4.github.io/pyproj/stable/) is a python interface to the [PROJ](https://proj.org/) library, which is a software for transforming geospatial coordinates from one CRS to another.
# 
# Each __pyproj.CRS__ object provides a number of methods for converting to different formats, including well-known text, EPSG codes, JavaScript Object Notation (JSON), and PROJ string (i.e., `'+proj=longlat +datum=WGS84 +no_defs +type=crs'`).
# 
# Because this is a _Geographic_ CRS, the length information provided by `LineString.length` will also be in geographic units, which doesn't really make sense for us - we first have to convert the __GeoDataFrame__ to a different CRS. To do this, we can use the method `to_crs`:
# 
# ```python
# In [8]: help(roads.to_crs)
# Help on method to_crs in module geopandas.geodataframe:
# 
# to_crs(crs=None, epsg=None, inplace=False) method of geopandas.geodataframe.GeoDataFrame instance
#     Transform geometries to a new coordinate reference system.
#     
#     Transform all geometries in an active geometry column to a different coordinate
#     reference system.  The ``crs`` attribute on the current GeoSeries must
#     be set.  Either ``crs`` or ``epsg`` may be specified for output.
#     
#     This method will transform all points in all objects. It has no notion
#     or projecting entire geometries.  All segments joining points are
#     assumed to be lines in the current projection, not geodesics. Objects
#     crossing the dateline (or other projection boundary) will have
#     undesirable behavior.
# ...
# ```
# 
# So, to transform the __GeoDataFrame__ to a different CRS, we have to provide either a CRS or an EPSG code. We can also choose to do this in place (`inplace=True`), or assign the output to a new __GeoDataFrame__ object (`inplace=False`). Let's transform the __GeoDataFrame__ to Irish Transverse Mercator, and assign the output to a new variable, __roads_itm__. 
# 
# <span style="color:#009fdf;font-size:1.1em;font-weight:bold">Using the search function on the [EPSG registry](https://epsg.org/search/by-name), or using an internet search, look up the EPSG code for the Irish Transverse Mercator CRS and enter it in the method call below:</span>

# In[83]:


roads_itm = roads.to_crs(epsg=2157)

print(roads_itm.head())


# Note that only the __geometry__ column has changed - instead of geographic coordinates (e.g., (-6.21243, 54.48706)), the points in each __LineString__ should be in a projected CRS (e.g., (715821.764, 861315.722)). Now, when we access the `length` attributes of our __LineString__ objects, the units will be in meters (the same units as our CRS).
# 
# ### 3.2 Summarizing data using geopandas
# So that's the first part of our problem solved - our coordinates are in meters, and the lengths will be as well. The next step is to select all of the features that correspond to Motorways and sum the lengths. We saw an example of this in Practical 1 - we can slice the __GeoDataFrame__ by returning all of the rows where `'Road_class' == 'MOTORWAY'`:

# In[26]:


roads_itm[roads_itm['Road_class'] == 'MOTORWAY']


# But first, we might want to add a column to our __GeoDataFrame__ that contains the `length` of each of the features. To do this, we can _iterate_ over the rows of the __GeoDataFrame__ using the `iterrows` method:
# 
# ```python
# In [9]: help(roads_itm.iterrows)
# Iterate over DataFrame rows as (index, Series) pairs.
# 
# Yields
# ------
# index : label or tuple of label
#     The index of the row. A tuple for a `MultiIndex`.
# data : Series
#     The data of the row as a Series.
# ...
# ```
# 
# Because `iterrows` returns an (index, Series) pair at each step, we use __tuple assignment__ in our `for` loop. This gives us two variables, `i` and `row`, which we can use in the `for` loop. `i` corresponds to the `index` of the `row`, while `row` corresponds to the actual data of the `row`, with each of the columns that the full __GeoDataFrame__ has.
# 
# We can access each column in the same way that we do for the full __GeoDataFrame__ - either `row[column]` or `row.column`. We can assign a new column in the original __GeoDataFrame__ using the `.loc` [property](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html), which uses either a _label_ or a __Boolean array__ to index the __GeoDataFrame__. So the line below,
# 
# ```python
# roads_itm.loc[i, 'Length'] = row['geometry'].length
# ```
# 
# assigns the `length` property of the row's geometry to a new column, __Length__, at the corresponding index. Putting it all together, it looks like this:

# In[27]:


for i, row in roads_itm.iterrows(): # iterate over each row in the GeoDataFrame
    roads_itm.loc[i, 'Length'] = row['geometry'].length # assign the row's geometry length to a new column, Length
    
print(roads_itm.head()) # print the updated GeoDataFrame to see the changes


# Finally, we can subset our __GeoDataFrame__ to select only _MOTORWAY_ features, and sum their length:

# In[29]:


sum_roads = roads_itm['Length'].sum()
sum_motorway = roads_itm[roads_itm['Road_class'] == 'MOTORWAY']['Length'].sum()
print('{:.2f} total m of roads'.format(sum_roads))
print('{:.2f} total m of motorway'.format(sum_motorway))


# In the cell above, look at the `print` function argument:
# 
# ```python
# print('{:.2f} total m of motorway'.format(sum_motorway))
# ```
# 
# Here, we use the `format` [string method](https://docs.python.org/3.8/library/string.html#format-string-syntax) and curly braces ({ }) to insert the value of our `sum_motorway` variable. Note that within the curly braces, there is a _format specification_ - rather than printing the string in an unformatted way (which would contain a lot of extra decimal places), we can tell the `format` method to clean up the output using `:` and a [format specification](https://docs.python.org/3.8/library/string.html#formatspec). In this case, `.2f` tells the `format` method format the number to have 2 places after the decimal.
# 
# Let's say now that we want to find the sum of all of the different road classes in our dataset. We could, of course, repeat the exercise above for each of the different values of _Road_class_. But, __pandas__ (and by extension, __geopandas__) provide a nicer way to summarize data based on certain properties: the `groupby` [method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html). The `groupby` method returns an object that contains information about the groups; to see different properties, we can call methods like `mean`, `median`, `sum`, etc.
# 
# If we want to summarize our dataset by _Road_class_ and find the `sum` of the _Length_ of each group, then, it would like this:

# In[30]:


roads_itm.groupby(['Road_class'])['Length'].sum() / 1000 # convert to km


# The `groupby` method returns a __GeoDataFrame__, which we can then index to return a single column, _Length_. As this is a numeric column, we can also use arithmetic on it to divide by a conversion factor. The `groupby` method is a very useful way to quickly summarize a __DataFrame__ (or a __GeoDataFrame__ - remember that this is a __child__ class of __DataFrame__).
# 
# ## 4. Spatial data operations using geopandas and shapely
# Oftentimes in GIS analysis, we want to summarize our data spatially, as well as thematically. In this section, we will be looking at two examples of this kind of analysis: first, using a [spatial join](https://gisgeography.com/spatial-join/), and second, using a clipping operation.
# 
# The cell below will load the Counties shapefile in __data_files__ and test whether the CRS of the `counties` __GeoDataFrame__ is the same as the CRS of the `roads_itm` __GeoDataFrame__. Remember that the __shapely__ geometry objects in the __GeoDataFrame__ don't have any inherent information about the CRS of the object. So, in order to perform operations like a spatial join, we have to first ensure that the two __GeoDataFrame__ objects have the same CRS.
# 
# <span style="color:#009fdf;font-size:1.1em;font-weight:bold">If, when you first load the shapefile, the test below returns False, write a line of code that will ensure that the test returns True.</span>

# In[73]:


counties = gpd.read_file(r'E:\GIS\GIS_Practicals\GIS_Course EGM722 Practicals\GitHub\egm722\Week3\data_files\Counties.shp') # load the Counties shapefileif
counties = counties.to_crs(epsg=29900) # your line of code might go here.
if counties.crs == roads_itm.crs:
    print("Same CRS:", counties.crs, roads_itm.crs)# test if the crs is the same for roads_itm and counties.
else:
    print("Not the same CRS")
    


# Now that the two __GeoDataFrame__ objects have the same CRS, we can proceed with the spatial join using `gpd.sjoin`:

# In[65]:


join = gpd.sjoin(counties, roads_itm, how='inner', lsuffix='left', rsuffix='right') # perform the spatial join
join # show the joined table


# Now, we can see that our table has additional columns - we have the unnamed _index_, _COUNTY_ID_, _CountyName_, _Area_SqKM_, _OBJECTID_, and _geometry_ from the `counties` __GeoDataFrame__, and _index_right_ (because it has the same name as _index_ in the left __GeoDataFrame__), _SURVEY_, _Road_class_, and _Length_ from the `roads_itm` __GeoDataFrame__.
# 
# Like we did with `roads_itm`, we can again summarize our __GeoDataFrame__ using `groupby`; this time, we'll use the _CountyName_ property to see the total length of roads by each county, and by _Road_class_:

# In[66]:


join_total = join['Length'].sum() # find the total length of roads in the join GeoDataFrame
print(join.groupby(['CountyName', 'Road_class'])['Length'].sum() / 1000) # summarize the road lengths by CountyName, Road_class

print(sum_roads / join_total) # check that the total length of roads is the same between both GeoDataFrames; this should be 1.


# We can see that the total length of roads is __not__ the same in both __GeoDataFrame__ objects - our `join` __GeoDataFrame__ has somehow increased the length of roads.
# 
# In reality, what has happened here is that we have double-counted any road feature that is located in multiple counties - you can also see this by comparing the total number of objects in the `join` __GeoDataFrame__ and the `roads_itm` __GeoDataFrame__. Obviously, we don't want to double-count roads - to get around this, we can use the `gpd.clip` method to clip `roads_itm` to each of the county boundaries in the `counties` __GeoDataFrame__:
# 
# ```python
# In [10]: help(gpd.clip)
# Help on function clip in module geopandas.tools.clip:
# 
# clip(gdf, mask, keep_geom_type=False)
#     Clip points, lines, or polygon geometries to the mask extent.
#     
#     Both layers must be in the same Coordinate Reference System (CRS).
#     The `gdf` will be clipped to the full extent of the clip object.
#     
#     If there are multiple polygons in mask, data from `gdf` will be
#     clipped to the total boundary of all polygons in mask.
# ...
# ```
# 
# But, we have to do this for each of the boundaries - `gpd.clip` will take the total boundary for the __GeoDataFrame__ if there are multiple __Polygon__ objects. Using a `for` loop to loop over the `counties` __GeoDataFrame__, we can clip `roads_itm` to each county, and combine the results in another __GeoDataFrame__:

# In[70]:


clipped = [] # initialize an empty list
for county in counties['CountyName'].unique():
    tmp_clip = gpd.clip(roads_itm, counties[counties['CountyName'] == county]) # clip the roads by county border
    for i, row in tmp_clip.iterrows():
        tmp_clip.loc[i, 'Length'] = row['geometry'].length # we have to update the length for any clipped roads
        tmp_clip.loc[i, 'CountyName'] = county # set the county name for each road feature    
    clipped.append(tmp_clip) # add the clipped GeoDataFrame to the 

# pandas has a function, concat, which will combine (concatenate) a list of DataFrames (or GeoDataFrames)
# we can then create a GeoDataFrame from the combined DataFrame, as the combined DataFrame will have a geometry column.
clipped_gdf = gpd.GeoDataFrame(pd.concat(clipped))
clip_total = clipped_gdf['Length'].sum()

print(sum_roads / clip_total) # check that the total length of roads is the same between both GeoDataFrames; this should be close to 1.


# So we don't have perfect overlap, but this has more to do with the fact that there isn't perfect overlap between the `counties` boundary and the `roads` features - there are a good number of places where the roads extend beyond the boundary. To fix this, we could first clip `roads_itm` to the entire `counties` __GeoDataFrame__, which would eliminate these extraneous stretches of road. For now, though, agrement to within .01% is acceptable for our purposes - much better than the 1.5% disagreement from the spatial join alone.
# 
# <span style="color:#009fdf;font-size:1.1em;font-weight:bold">To wrap up, write a line or two of code in the cell below that will summarize the `clipped_gdf` __GeoDataFrame__ by county and road type. Which county has the most Motorways? The most roads in total?</span>

# In[82]:


sum_county = clipped_gdf['CountyName'].sum()
sum_road = clipped_gdf['Road_class'].sum()
print(sum_road, sum_county)


# ## 5. Exercise and next steps
# Now that you've gained some experience working with `shapely` geometry objects and `geopandas` __GeoDataFrame__ objects, have a look at __exercise_script.py__ in this folder. Using the topics covered in the Week 2 practical and this practical, modify this script to do the following:
# 1. Load the counties and ward data
# 2. Using a spatial join, summarize the total population by county. What county has the highest population? What about the lowest?
# 3. Create a map like the one below to show population information by census area, with the county boundaries plotted overtop of the chloropleth map.
# 
# ![](sample_map.png)
# 
# ### Additional exercise questions
# 1. Are there any Wards that are located in more than one county? If so, how many, and what is the total population of these Wards?
# 2. What Ward has the highest population? What about the lowest population?
# 3. Repeat the exercise above using __exercise_script.py__, but this time use the population density (in number of residents per square km).

# In[ ]:




