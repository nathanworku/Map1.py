#Imports
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
from folium.plugins import FastMarkerCluster, MarkerCluster
import branca.colormap as cm
import shapely
from shapely.wkt import loads
import json

def to_gdf(
    df, 
    geometry_column = 'geo', 
    epsg = '4326', 
    to_epsg= None):
  
    gdf = gpd.GeoDataFrame(df.copy())
    try:
        gdf[geometry_column] = gdf[geometry_column].apply(lambda x: loads(x))
    except TypeError:
        rows= gdf.shape[0]
        gdf.dropna(axis=0,subset=[geometry_column],inplace= True)
        if gdf.shape[0] < rows:
            row_drop= rows - gdf.shape[0]
            print('number of rows droped due to missing geometry: {}'.format(row_drop))
            gdf[geometry_column] = gdf[geometry_column].apply(lambda x: loads(x))  
    gdf = gdf.set_geometry(geometry_column)
    gdf.crs = {'init':'epsg:{}'.format(epsg)}
    if epsg != '4326' and to_epsg != None:
      gdf = gdf.to_crs({'init': 'epsg:4326'})
    elif to_epsg: 
      gdf = gdf.to_crs({'init': 'epsg:{}'.format(to_epsg)})
    else: pass
    return(gdf)

def _is_GeoDataFrame(data):
    return(type(data) == type(gpd.GeoDataFrame()))

def _get_geo_col(data):
    "Returns geometry column"
    return(data.geometry.name)

def _simplify_geometry(data,amount):
    "Simplifies the geometry"
    df= data.copy()
    try:
        geo_col = _get_geo_col(df)
        df[geo_col] = df.simplify(amount)
    except Exception as e:
        print('Simplify geometry failed\nMessage: {}'.format(e))
    return(df)

def _stringify_date(data):
    "As the geojson format doesn't alow for date format, they are turned into strings"
    date_cols =data.dtypes.reset_index()[data.dtypes.reset_index()[0].astype(np.str).str.contains('date')]['index'].to_list()
    if date_cols:
        for col in date_cols:
            data[col] = data[col].astype(np.str)
    return(data)

def _get_bounds(data):
    try:
        bounds = data.total_bounds
        x_mean = np.mean([bounds[0],bounds[2]])
        y_mean = np.mean([bounds[1],bounds[3]])
    except Exception as e:
        print('Error calculating bounds\nMessage: {}'.format(e))
    return([y_mean,x_mean])

def _load_json_geometry(data, geometry_column, epsg= 4326):
    try:
      gdf= gpd.GeoDataFrame(data.copy())
      rows= gdf.shape[0]
      gdf.dropna(axis=0,subset=[geometry_column],inplace= True)
      gdf[geometry_column] = gdf[geometry_column].apply(lambda x: loads(x))
      gdf = gdf.set_geometry(geometry_column)
      gdf.crs = f"EPSG:{epsg}"
      gdf= gdf.to_crs(epsg=4326)
      
      if gdf.shape[0] < rows:
          row_drop= rows - gdf.shape[0]
          print(f'number of rows droped due to missing geometry: {row_drop}')
    except Exception as e:
      #print(f'Failed to convert into GeoDataFrame\nMessage: {e}')
      raise e
    return(gdf)

def _cast_object_to_string(data):
  #used when geopandas.to_json() throws a "Invalid field type <class 'decimal.Decimal'>" exception
  d_types= data.dtypes
  type_dict= d_types[d_types == 'object'].to_dict()

  for val in type_dict.keys():
    type_dict[val] = np.str
  
  data= data.astype(type_dict)
  return(data)    

def gdf_prep(
    data, 
    geometry_column= None, 
    epsg = 4326, 
    to_epsg= None):
    """Takes a dataframe with a geometry column in geojson format and converts it to geopandas dataframe.\n
      df: Pandas dataframe\n
      geometry_column: Specify field containing geojson field\n
      epsg: Specify the EPSG coordinate system of the data. Default 4326 (WGS84), this will be used to both set and convert it to WGS84 if needed.\n
      to_epsg: Use when wanting to convert to different coordinate system than WGS84"""
    
    df = data.copy()
    if not _is_GeoDataFrame(df) and not geometry_column:
        raise Exception('Data needs to be in a GeoDataFrame alternatively set the geometry_column parameter')
    
    try:
        df= _load_json_geometry(df, geometry_column, epsg= epsg)
    except Exception as e:
        try:
          if _is_GeoDataFrame(df) and geometry_column:
            df= df.set_geometry(geometry_column)
            df.crs= epsg
          if _is_GeoDataFrame(df):
            df.crs= epsg
            
        except Exception as e:
          print('gdf_prep caught an exception:')
          raise e
    try: 
        if not all(df.is_valid):
          print(f'Dropped {(~df.is_valid).sum()} rows due to invalid geometry')
          df = df[df.is_valid]
        if to_epsg:
          df= df.to_crs(epsg= to_epsg)
          return(df)
        else: return(df)
    except Exception as e:
        print(f'Message: {e}')
        raise e


def add_colormap(
    data, 
    color_column= None,
    color_list= None, 
    color_min_val= None, 
    color_max_val= None,
    step= None,
    fill_color = None,
    output_color_ramp= False):
    """Outputs a color ramp as a list or as a color ramp function used for visualisation when 'output_color_ramp' is True.\n
    color_column: field to be used to calculate the color ramp.\n
    color_list: list of colors to build the color ramp ex ['green','white', 'red'] otherwise sets a red to blue ramp as a default.\n
    color_min_val: set a minimum range for the color ramp. Used when limiting the color range.\n
    color_max_val: set a maximum range for the color ramp. Used when limiting the color range.\n
    step: conver to steps instead of a continuas range\n
    fill_color: Sets a fill color, used mainly in the other functions.\n
    output_color_ramp: outputs a color ramp dunction instead that can be visualised"""
  
    df = data.copy()
    try:
        if color_column == None:
            #set default or fill color if color column isn't provided
            fill_color = '#49B5FA' if not fill_color else fill_color
            color_ramp= cm.LinearColormap([fill_color,fill_color])
            colors= [color_ramp(0) for x in range(len(df))]
        elif df[color_column].dtype in [np.int, np.float]:
            #process linear colormaps
            color_ramp = cm.LinearColormap(
                color_list if color_list != None else ['#FE6C94','#27AAFF'],
                vmin = color_min_val if color_min_val != None else df[color_column].min(),
                vmax = color_max_val if color_max_val != None else df[color_column].max()
                )
            color_ramp = color_ramp.to_step(step) if step != None else color_ramp
            colors= [color_ramp(i) for i in df[color_column].to_list()]
        else:
            #process categorical colormaps
            keys = df[color_column].unique()
            step_map = np.arange(start= 0,stop= 1, step= 1/len(keys))

            color_ramp = cm.LinearColormap(color_list) if color_list else cm.linear.Set1_08
            color_ramp = color_ramp.to_step(len(keys)+1)
            
            values = [color_ramp(x) for x in step_map]
            map_dict = dict(zip(keys,values))
            colors = df[color_column].map(map_dict).to_list()
    except:
        color_ramp = cm.LinearColormap(['#EE0000','#EE0000'])
        colors= [color_ramp(0) for i in range(len(df))]
    if output_color_ramp:
      return(color_ramp)
    else: return(colors)
    
    
def _add_map(
    map_centroid, 
    basemap= 'dark',
    zoom_start = 12 ):
    """Creates the initial background map\n\n
    data: geodataframe used to center the map\n
    basemap: background map style, choose between ['normal', 'dark','light']\n
    zoom_start: set initial zoom level\n
    \nexample:\n
    m = add_map(data= gdf)\n
    add_layer(data= gdf, color_column= 'color_values').add_to(m)\n
    add_map_controls(m)
    m.save('my_map.html') #Used when needing to plot large amounts of data which notebook can't handle"""
  
    map_tiles = {'normal':'OpenStreetMap','dark':'CartoDB dark_matter','light':'CartoDB positron'}

    try:
        map_instance = folium.Map(
        location= map_centroid,
        zoom_start = zoom_start,
        tiles = map_tiles[basemap])
        return(map_instance)
    except Exception as e:
        print('Folium.Map failed to initiate\nMessage: {}'.format(e))

def _add_layer(
    data, 
    layer_name= None, 
    simplify= 0, 
    fill_color= None, 
    color_column= None, 
    color_list= None, 
    color_min_val= None, 
    color_max_val= None,
    color_step= None,
    fill_opacity= 0.7, 
    line_color= None,
    line_opacity = 1, 
    line_weight= 3,
    hover_color= 'grey',
    hover_fields= 'all',):
    """Add and style a map layer\n
    data: Geodataframe\n
    layer_name: Name of layer that can be seen in the layer panel\n
    simplify: Simplifies geometry, used when geometries are complex and become heavy\n
    fill_color: Specifies a fixed color to be used for all the geometries\n
    color_column: Field to be used to calculate the color ramp.\n
    color_list: List of colors to build the color ramp ex ['green','white', 'red'] otherwise sets a red to blue ramp as a default.\n
    color_min_val: set a minimum range for the color ramp. Used when limiting the color range.\n
    color_max_val: Set a maximum range for the color ramp. Used when limiting the color range.\n
    step: conver to steps instead of a continuas range\n
    fill_opacity: The layer opacity set between 0 and 1.\n
    line_opacity: The line opacity set between 0 and 1\n
    line_weight: Used to specify line width\n
    hover_color: Color to be used when the cursor hovers over a feature\n
    hover_field: Fields to show when hovering over a feature.\n
    \nexample:\n
    m = add_map(data= gdf)\n
    add_layer(data= gdf, color_column= 'color_values').add_to(m)\n
    add_map_controls(m)
    m.save('my_map.html') #Used when needing to plot large amounts of data which notebook can't handle"""
    
    df = data.copy()
    df= _simplify_geometry(data, amount= simplify)
    df= _stringify_date(df)
    
    #Add_color column
    df['color'] = add_colormap(
        data=df, 
        color_column= color_column, 
        color_list= color_list,
        fill_color= fill_color,
        color_min_val= color_min_val, 
        color_max_val= color_max_val,
        step= color_step)
    
    #Hover fields             
    if hover_fields == 'all':
        hover_list= df.drop([_get_geo_col(df),'color'],axis=1).columns.to_list()
    else: 
        hover_list= hover_fields
        
    #Converts df to json
    try:
      df_json= df.to_json()
      json_data= json.loads(df_json)
    except TypeError:
      df_json= _cast_object_to_string(df).to_json()
      json_data= json.loads(df_json)

    #Folium geojson layer
    map_instance = folium.GeoJson(
        data = json_data,
        name = layer_name if layer_name != None else str(np.random.randint(10)),
        style_function = lambda x: {
            'fillColor': x['properties']['color'], 
            'fillOpacity': fill_opacity, 
            'opacity': line_opacity, 
            'weight': line_weight, 
            'color': line_color if line_color else '#239FD0'},
        tooltip = folium.GeoJsonTooltip(fields= hover_list) if hover_fields != None else None,
        highlight_function= lambda x: {
            'fillColor': hover_color,
            'color': hover_color})
    return(map_instance)


def _add_point_layer(
    data,
    layer_name= None,
    cluster= True,
    radius= 10,
    hover_column= None,
    color_column= None, 
    color_list=None, 
    color_min_val=None, 
    color_max_val=None,
    step=None, 
    fill= True,
    fill_color=None,
    fill_opacity= 0.5,
    line_weight= 3,
    line_opacity= 1
    ):
    """Add and style a pointlayer\n
    data: Geodataframe\n
    layer_name: Name of layer that can be seen in the layer panel\n
    cluster: Whether points close to each other sould be clustered together (recommended for larger number of points)\n
    radius: The size of the points.\n
    hover_column: Fields to show when hovering over a feature.\n
    color_column: Field to be used to calculate the color ramp.\n
    color_list: List of colors to build the color ramp ex ['green','white', 'red'] otherwise sets a red to blue ramp as a default.\n
    color_min_val: set a minimum range for the color ramp. Used when limiting the color range.\n
    color_max_val: Set a maximum range for the color ramp. Used when limiting the color range.\n
    step: conver to steps instead of a continuas range\n
    fill: Whether the inner part of the circle should have a fill color.\n
    fill_color: Specifies a fixed color to be used for all the geometries\n
    fill_opacity: The layer opacity set between 0 and 1.\n
    line_weight: Used to specify line width\n
    line_opacity: The line opacity set between 0 and 1\n
    \nexample:\n
    m = add_map(data= gdf)\n
    add_point_layer(data= gdf, color_column= 'color_values', cluster= False).add_to(m)\n
    add_map_controls(m)
    m.save('my_map.html') #Used when needing to plot large amounts of data which notebook can't handle"""
    
    df = data.copy()
    if cluster:
        mc = MarkerCluster(name= "Marker Cluster" if layer_name == None else layer_name)
    else: mc = folium.FeatureGroup()
    
    df['color'] = add_colormap(
        data= df,
        color_column=color_column, 
        color_list=color_list, 
        color_min_val=color_min_val, 
        color_max_val=color_max_val, 
        step=step, 
        fill_color=fill_color)
    
    df['x'] = df.geometry.x
    df['y'] = df.geometry.y
    
    for idx, row in df.iterrows():
        html = ''
        for index, values in zip(row.index, row.values):
            html += r'<dt><b>{}:</b> {}</dt>'.format(index,values)
            
        iframe = folium.IFrame(html= html,width= 200,height= 150)
        
        marker_layer= folium.CircleMarker(
            location= [row['y'], row['x']],
            radius= radius, 
            popup= folium.Popup(iframe,parse_html=True),
            tooltip= None if not hover_column else folium.Tooltip(text=row[hover_column]),
            weight= line_weight,
            color= row['color'],
            opacity= line_opacity,
            fill= fill,
            fill_color= row['color'] if not fill_color else fill_color,
            fill_opacity= fill_opacity
            ).add_to(mc)
    return(mc)


def _add_time_layer(
    data, 
    time_column,
    period= 'P1D',
    duration= 'P1D',
    date_options=' YYYY-MM-DD',
    transition_time= 1000,
    radius= 7,
    fill_color= None,
    color_column= None,
    color_list= None,
    color_min_val= None, 
    color_max_val= None,
    line_opacity= 0.7,
    fill_opacity= 0.7):
    """Add and style a temporal (animation) layer\n
    data: Geodataframe\n
    time_column: Date/timestamp column.
    period: Used to construct the array of available times starting from the first available time. Format: ISO8601 Ex: ‘P1M’ 1/month, ‘P1D’ 1/day, ‘PT1H’ 1/hour, and ‘PT1M’ 1/minute\n
    duration: Period of time which the features will be shown on the map after their time has passed. If None, all previous times will be shown. Format: ISO8601 Duration ex: ‘P1M’ 1/month, ‘P1D’ 1/day, ‘PT1H’ 1/hour, and ‘PT1M’ 1/minute\n
    date_options: Format to be displayed in the map.\n
    transition_time: The duration in ms of a transition from between timestamps.\n
    radius: The size of the points.\n
    fill_color: Specifies a fixed color to be used for all the geometries\n
    color_column: Field to be used to calculate the color ramp.\n
    color_list: List of colors to build the color ramp ex ['green','white', 'red'] otherwise sets a red to blue ramp as a default.\n
    color_min_val: set a minimum range for the color ramp. Used when limiting the color range.\n
    color_max_val: Set a maximum range for the color ramp. Used when limiting the color range.\n
    opacity: The layer opacity set between 0 and 1.\n
    \nexample:\n
    m = add_map(data= gdf)\n
    add_time_layer(data= gdf, time_column= 'datetime', color_column= 'color_values').add_to(m)\n
    add_map_controls(m)
    m.save('my_temporal_map.html') #Used when needing to plot large amounts of data which notebook can't handle"""
    
    df = data.copy()
    
    colors = add_colormap(
        df, 
        color_column= color_column, 
        color_list= color_list,
        color_min_val=color_min_val, 
        color_max_val=color_max_val,
        fill_color = fill_color)

    df= _stringify_date(df)
    df['time'] = df[time_column]
    df['icon'] = 'circle'

    try:
      df_json= df.to_json()
      json_data= json.loads(df_json)
    except TypeError:
      df_json= _cast_object_to_string(df).to_json()
      json_data= json.loads(df_json)

    for feature, color in zip(json_data['features'],colors):
        feature['properties']['style'] = {'fillColor': color, 'color': color, 'fillOpacity': fill_opacity}
        feature['properties']['iconstyle'] = {'fillColor': color, 'stroke': 'True','radius': radius,'opacity': line_opacity}

    output= plugins.TimestampedGeoJson(
        json_data,
        transition_time= 1000,
        loop= True,
        auto_play= True,
        add_last_point=True,
        period= period,
        duration= duration,
        min_speed= 0.1,
        max_speed=10,
        loop_button= True,
        date_options='YYYY-MM-DD HH:mm:ss',
        time_slider_drag_update= True)
    return(output)


def _add_map_controls(
    map_instance,
    minimap= True, 
    mouse_position= True, 
    measure_controll= True, 
    draw= True):
    """Add aditional map controlls and features to the map\n
    map_instance: The map instance that was used to initialize the add_map() function\n
    minimap: Add minimap in the bottom left\n
    mouse_position: Coordinate information on hover\n
    measure_controll: adds a feature that allows the user to measure distance on the map\n
    draw: Adds the ability to draw different geometries on a map and save it as geojson
    \nexample:\n
    m = add_map(data= gdf)\n
    add_layer(data= gdf, color_column= 'color_values').add_to(m)\n
    add_map_controls(m)
    m.save('my_map.html') #Used when needing to plot large amounts of data which notebook can't handle
    """
    
    map_instance= map_instance
    folium.TileLayer('OpenStreetMap').add_to(map_instance)
    folium.TileLayer('CartoDB dark_matter').add_to(map_instance)
    folium.TileLayer('CartoDB positron').add_to(map_instance)
    folium.LayerControl().add_to(map_instance)
    
    plugins.Fullscreen(
        position='topleft',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=False).add_to(map_instance)
    
    if minimap:
        plugins.MiniMap(
            tile_layer='OpenStreetMap', 
            position='bottomleft',
            toggle_display= True,
            minimized= False).add_to(map_instance)
    else: pass
    
    if mouse_position:
        fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(
            position='bottomleft', 
            separator=' | ', 
            prefix="Mouse:",
            lat_formatter=fmtr,
            lng_formatter=fmtr
            ).add_to(map_instance)
    else: pass
    
    if measure_controll:
        plugins.MeasureControl(
            secondary_length_unit='kilometers',
            secondary_area_unit='sqkilometers',
            position= 'bottomright'
            ).add_to(map_instance)
    else: pass
    
    if draw:
        plugins.Draw(
            export=True
        ).add_to(map_instance)
    else: pass
    
    return(map_instance)


class create_map():
    """
    Sets general map properties.\n
    basemap: (Choose between: ['dark','light','normal'], default: 'normal')\n
    zoom_start: (int, default: 12) Sets starting zoom position.\n
    minimap: (boolean, default: True) Add a minimap to the bottom left.\n
    mouse_position: (boolean, default: True) show mouse coordinates.\n
    measure_controll: (boolean, default: True) adds a measure feature in order to measure distance.\n
    draw: (boolean, default: True) adds features to allow the user to draw and export various shapes\n
    """
    def __init__(self, basemap= 'normal', zoom_start = 12, minimap= True, mouse_position= True, measure_controll= True, draw= True):
        self.basemap= basemap
        self.zoom_start= zoom_start
        self.minimap= minimap
        self.mouse_position= mouse_position
        self.measure_controll= measure_controll
        self.draw= draw
        self.layer_list= []
        self.mean_centroid= []
    
    def add_layer(
        self,
        data,
        geometry_column= None,
        layer_name= None, 
        simplify= 0,
        cluster= True,
        radius= 10,
        fill_color= None, 
        fill_opacity= 0.7, 
        color_column= None, 
        color_list= None, 
        color_min_val= None, 
        color_max_val= None,
        color_step= None,
        line_color= None,
        line_opacity = 1, 
        line_weight= 3,
        hover_color= 'grey',
        hover_fields= 'all'):
        """
        Allows the user to add and style geographical data to a map.\n
        data: Geodataframe or a regular pandas data frame. In the case of a regular data frame, a geometry column needs to be specified containing a geojson string.\n
        geometry_column: Used when data isn't already in a geodataframe but has a geojson column.
        layer_name: Name of layer that can be seen in the layer panel\n
        simplify: Simplifies geometry, used when geometries are complex and become heavy\n
        cluster: Used to cluster points close to each other together\n
        fill_color: Specifies a fixed color to be used for all the geometries\n
        fill_opacity: The layer opacity set between 0 and 1.\n
        color_column: Field to be used to calculate the color ramp.\n
        color_list: List of colors to build the color ramp ex ['green','white', 'red'] otherwise sets a red to blue ramp as a default.\n
        color_min_val: set a minimum range for the color ramp. Used when limiting the color range.\n
        color_max_val: Set a maximum range for the color ramp. Used when limiting the color range.\n
        step: conver to steps instead of a continuas range\n
        line_color: Line color to be used.\n
        line_opacity: The line opacity set between 0 and 1\n
        line_weight: Used to specify line width\n
        hover_color: Color to be used when the cursor hovers over a feature\n
        hover_field: Fields to show when hovering over a feature.\n
        \nexample:\n
        m = add_map(data= gdf)\n
        add_layer(data= gdf, color_column= 'color_values').add_to(m)\n
        add_map_controls(m)
        m.save('my_map.html') #Used when needing to plot large amounts of data which notebook can't handle"""
        
        df = data.copy()

        df= gdf_prep(data= df, geometry_column= geometry_column, to_epsg= 4326)
        
        point_df= df[(df.geom_type == 'Point')]
        geom_df= df[~(df.geom_type == 'Point')]

        if not point_df.empty:
          map_instance= _add_point_layer(
              data= point_df,
              layer_name= layer_name,
              cluster= cluster,
              radius= radius,
              hover_column= None,
              color_column= color_column,
              color_list= color_list,
              color_min_val= color_min_val,
              color_max_val= color_max_val,
              step= color_step,
              fill= True,
              fill_color= fill_color,
              fill_opacity= fill_opacity,
              line_weight= line_weight,
              line_opacity= line_opacity)
          
          self.layer_list += [map_instance]
          
        if not geom_df.empty:
          map_instance= _add_layer(
            data= geom_df,
            layer_name= layer_name, 
            simplify= simplify,
            fill_color= fill_color, 
            color_column= color_column, 
            color_list= color_list, 
            color_min_val= color_min_val, 
            color_max_val= color_max_val,
            color_step= color_step,
            fill_opacity= fill_opacity,
            line_color= line_color, 
            line_opacity= line_opacity, 
            line_weight= line_weight,
            hover_color= hover_color,
            hover_fields= hover_fields)
          
          self.layer_list += [map_instance]
        
        bounds= _get_bounds(df)
        self.mean_centroid += [bounds]
    
    def add_time_layer(
        self,
        data, 
        time_column,
        geometry_column= None,
        period= 'P1D',
        duration= 'P1D',
        date_options='YYYY-MM-DD',
        transition_time= 1000,
        radius= 7,
        fill_color= None,
        color_column=None,
        color_list=None,
        color_min_val=None, 
        color_max_val=None,
        line_opacity= 0.7,
        fill_opacity= 0.7):
        
        df= gdf_prep(data= data, geometry_column= geometry_column)

        map_instance= _add_time_layer(
            data= df, 
            time_column= time_column,
            period= period,
            duration= duration,
            date_options= date_options,
            transition_time= transition_time,
            radius= radius,
            fill_color= fill_color,
            color_column= color_column,
            color_list= color_list,
            color_min_val= color_min_val, 
            color_max_val= color_max_val,
            line_opacity= line_opacity,
            fill_opacity= fill_opacity)
        
        self.layer_list += [map_instance]
        
        bounds= _get_bounds(df)
        self.mean_centroid += [bounds]
        
    def show(self, save= None):
        """Displays the map\n
        save: path and filename, ex: my_map.html"""
        mean_centroid= np.mean(np.array(self.mean_centroid),axis=0)

        map_instance = _add_map(
            map_centroid= mean_centroid, 
            basemap= self.basemap, 
            zoom_start= self.zoom_start)
        
        for layer in self.layer_list:
            layer.add_to(map_instance)
            
        _add_map_controls(
            map_instance= map_instance, 
            minimap= self.minimap, 
            mouse_position= self.mouse_position,
            measure_controll= self.measure_controll,
            draw= self.draw)
        if save:
          map_instance.save(save)
        else:
          return(map_instance)