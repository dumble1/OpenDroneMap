import ecto, os, json
from shutil import copyfile

from opendm import io
from opendm import log
from opendm import system
from opendm import context
from opendm import types
from opendm.dem import commands
from opendm.cropper import Cropper


class ODMDEMCell(ecto.Cell):
    def declare_params(self, params):
        params.declare("verbose", 'print additional messages to console', False)

    def declare_io(self, params, inputs, outputs):
        inputs.declare("tree", "Struct with paths", [])
        inputs.declare("args", "The application arguments.", {})
        inputs.declare("reconstruction", "list of ODMReconstructions", [])

    def process(self, inputs, outputs):
        # Benchmarking
        start_time = system.now_raw()

        log.ODM_INFO('Running ODM DEM Cell')

        # get inputs
        args = self.inputs.args
        tree = self.inputs.tree
        las_model_found = io.file_exists(tree.odm_georeferencing_model_las)

        # check if we rerun cell or not
        rerun_cell = (args.rerun is not None and
                      args.rerun == 'odm_dem') or \
                     (args.rerun_all) or \
                     (args.rerun_from is not None and
                      'odm_dem' in args.rerun_from)

        #log.ODM_INFO('Classify: ' + str(args.pc_classify != "none"))
        #log.ODM_INFO('Create DSM: ' + str(args.dsm))
        #log.ODM_INFO('Create DTM: ' + str(args.dtm))
        #log.ODM_INFO('DEM input file {0} found: {1}'.format(tree.odm_georeferencing_model_las, str(las_model_found)))

        # Setup terrain parameters
    #    terrain_params_map = {
    #        'flatnonforest': (1, 3), 
    #        'flatforest': (1, 2), 
    #        'complexnonforest': (5, 2), 
    #        'complexforest': (10, 2)
    #    }
    #    terrain_params = terrain_params_map[args.dem_terrain_type.lower()]             
    #    slope, cellsize = terrain_params

        # define paths and create working directories
        odm_dem_root = tree.path('dem')
        if not io.dir_exists(odm_dem_root):
            system.mkdir_p(odm_dem_root)
       
       # Do we need to process anything here?
        if las_model_found:
            dsm_output_filename = os.path.join(odm_dem_root, 'outfile.tif')

            if (not io.file_exists(dsm_output_filename)) or \
                rerun_cell:
                
                system.run('pdal pipeline %s' % (tree.dem_json))
                system.run('gdalwarp -cutline %s -crop_to_cutline %s %s' % (tree.dem_shp, tree.dem_gray, tree.dem_trim_gray))
                system.run('python %s %s %s'(tree.gray2rgb, tree.dem_trim_gray, dsm_output_filename))


            else:
                log.ODM_WARNING('Found existing outputs in: %s' % odm_dem_root)
        else:
            log.ODM_WARNING('DEM will not be generated')

        if args.time:
            system.benchmark(start_time, tree.benchmarking, 'Dem')

        log.ODM_INFO('Running ODM DEM Cell - Finished')
        return ecto.OK if args.end_with != 'odm_dem' else ecto.QUIT
