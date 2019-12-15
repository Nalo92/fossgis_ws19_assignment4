#!/usr/bin/env python
import grass.script as gscript
import os


def main():
    # calculate hazard from the preprocessed data
    gscript.run_command('r.mapcalc', expression='hazard = ((propability_reclassified@risk_analysis * 0.4 + slope_reclassified@risk_analysis * 0.2 + landcover_reclassified@risk_analysis * 0.4') *1000)

    # check data range
    gscript.run_command('r.info', map='hazard')

    # reclassify hazard
    gscript.run_command('r.reclass', input='hazard', output='hazard_re', rules=r"C:\Users\Ich\Desktop\Geographie Master\Semester 1\FOSSGIS\Assignments\fossgis_ws19_assignment4\assignment4_data\assignment4_data\hazard_class.txt")

    # convert
    gscript.run_command('g.region', raster='hazard_re')
    gscript.run_command('r.resample', input='hazard_re', output='hazard_reclassified')

    # calculate risk
    gscript.run_command('r.mapcalc', expression='risk = (hazard_reclassified@risk_analysis * buildings_density_reclassified@risk_analysis * fire_stations_distance_reclassified@risk_analysis)'
if __name__ == '__main__':
    main()
