#!/usr/bin/env python

import grass.script as gscript
import os

def main():
    # set resolution of the region to 1km 
    gscript.run_command('g.region', res=1000)                                                               

    # import vector files osm
    gscript.run_command('v.import', input=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\osm\fire_stations.geojson", output='fire_stations')
    gscript.run_command('v.import', input=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\osm\buildings.geojson", output='buildings')

    # import vector files fire incidents
    gscript.run_command('v.import', input=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\fire_incidents\fire_archive_V1_89293.shp", output='fire_incidents')

    # import raster file landcover
    gscript.run_command('r.import', input=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\corine_landcover_2018\CLC2018_tarragona.tif", output='landcover')

    # import raster file dem
    gscript.run_command('r.import', input=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\srtm_mosaik.tif\srtm_mosaik.tif", output='dem')

    # set region 
    gscript.run_command('r.slope.aspect', elevation='dem@risk_analysis', slope='slope')

    # reclass slope
    gscript.run_command('r.reclass', input='slope@risk_analysis', output='slope_re', rules=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\slope_class")
    
    # check reclassification values
    gscript.run_command('r.info', map='slope_re@risk_analysis')
    
    # convert
    gscript.run_command('g.region', raster='slope_re@risk_analysis')
    gscript.run_command('r.resample', input='slope_re@risk_analysis', output='slope_reclassified')

    # reclass landuse
    gscript.run_command('r.reclass', input='landcover@risk_analysis', output='landcover_re', rules=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\landuse")
    
    # check reclassification values
    gscript.run_command('r.info', map='landcover_re@risk_analysis')

    # convert
    gscript.run_command('g.region', raster='landcover_re@risk_analysis')
    gscript.run_command('r.resample', input='landcover_re@risk_analysis', output='landcover_reclassified')

    # create grid
    gscript.run_command('v.mkgrid', map='grid_fire', box='1000,1000')

    # count fire incidents
    gscript.run_command('v.vect.stats', points='fire_incidents', areas='grid_fire', count_column='fire_count')

    # to raster
    gscript.run_command('v.to.rast', input='grid_fire', output='fire_raster', use='attr', attribute_column='fire_count')

    # propability
    gscript.run_command('r.mapcalc', expression='propability = (if ( fire_raster @ risk_analysis > 15, 15, fire_raster @ risk_analysis) * 100 / 15)')

    # reclassify probabilty
    gscript.run_command('r.reclass', input='propability', output='propability_reclassified', rules=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\prop_class")
    
    # create points
    gscript.run_command('v.to.points', input='buildings', output='buildings_points')

    # create raster map
    gscript.run_command('v.kernel', input='buildings_points', output='buildings_density', radius=10000, multiplier=100000)
    
    # reclass buildings 
    gscript.run_command('r.reclass', input='buildings_density', output='buildings_density_re', rules=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\buildings_density_class.txt")
    
    # convert 
    gscript.run_command('g.region', raster='buildings_density_re')
    gscript.run_command('r.resample', input='buildings_density_re', output='buildings_density_reclassified')

    # create points
    gscript.run_command('v.to.points', input='fire_stations', output='fire_stations_points')
    
    # convert to raster 
    gscript.run_command('v.to.rast', input='fire_stations_points', output='fire_stations_raster', use='val')  
    
    # calculate distance
    gscript.run_command('r.grow.distance', input='fire_stations_raster@risk_analysis' distance='fire_stations_distance')

    # reclass fire stations distance 
    gscript.run_command('r.reclass', input='fire_stations_distance', output='fire_stations_distance_re', rules=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\fire_stations_distance_class.txt")

    # check reclassification values
    gscript.run_command('r.info', map='fire_stations_distance_re')
    
    # convert
    gscript.run_command('g.region', raster='fire_stations_distance_re')
    gscript.run_command('r.resample', input='fire_stations_distance_re', output='fire_stations_distance_reclassified')




if __name__ == '__main__':
    main()
