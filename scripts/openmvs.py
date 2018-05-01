import ecto

from opendm import io
from opendm import log
from opendm import system
from opendm import context

class ODMOpenMVSCell(ecto.Cell):

    def declare_params(self, params):
        params.declare("cores", 'The maximum number of cores to use '
                                'in dense reconstruction.', context.num_cores) 
    def declare_io(self, params, inputs, outputs):
        inputs.declare("tree", "Struct with paths", [])
        inputs.declare("args", "Struct with paths", [])
        inputs.declare("reconstruction", "list of ODMReconstructions", [])
        outputs.declare("reconstruction", "list of ODMReconstructions", [])

    def process(self, inputs, outputs):

        # Benchmarking
        start_time = system.now_raw()

        log.ODM_INFO('Running ODM OpenMVS Cell')

        # get inputs
        args = self.inputs.args
        tree = self.inputs.tree
        reconstruction = self.inputs.reconstruction

        # check if we rerun cell or not
        rerun_cell = (args.rerun is not None and
                      args.rerun == 'openmvs') or \
                     (args.rerun_all) or \
                     (args.rerun_from is not None and
                      'openmvs' in args.rerun_from)

        if not io.file_exists(tree.openmvs_model) or rerun_cell:
            log.ODM_DEBUG('Writing OpenMVS vis in: %s' % tree.openmvs_model_data)

            #copy bundle file to openmvs dir
            from shutil import copyfile
            copyfile(tree.opensfm_scene,
                     tree.openmvs_scene)

            system.run('%s %s' % (context.openmvs_densify_path, tree.openmvs_scene))
        
        else:
            log.ODM_WARNING('Found a valid OpenMVS file in: %s' %
                            tree.openmvs_model)
        
        ###Reconstruct
        if not io.file_exists(tree.openmvs_tex_scene):
            log.ODM_DEBUG('Reconstruct Mesh')
            system.run('%s %s' % (context.openmvs_meshing_path, tree.openmvs_dense_scene))
        else:
            log.ODM_WARNING('Found a valid file in: %s' % tree.openmvs_tex_scene)
        
        ###Texturing
        if not io.file_exists(tree.scene_dense_mesh_texture):
            log.ODM_DEBUG('Texturing Mesh')
            system.run('%s %s' % (context.openmvs_tex_path, tree.openmvs_tex_scene))




        outputs.reconstruction = reconstruction

        if args.time:
            system.benchmark(start_time, tree.benchmarking, 'OpenMVS')

        log.ODM_INFO('Running ODM OpenMVS Cell - Finished')
        return ecto.OK if args.end_with != 'openmvs' else ecto.QUIT
