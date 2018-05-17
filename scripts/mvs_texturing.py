import ecto

from opendm import io
from opendm import log
from opendm import system
from opendm import context

class MVSTexturingCell(ecto.Cell):
    
    #def declare_params(self, params):

    def declare_io(self, params, inputs, outputs):
        inputs.declare("tree","Struct with paths", [])
        inputs.declare("args", "Struct with paths", [])
        inputs.declare("reconstruction", "list of ODMReconstructions", [])
        outputs.declare("reconstruction", "list of ODMReconstructions", [])

    def process(self, inputs, outputs):

        # Benchmarking
        start_time = system.now_raw()

        log.ODM_INFO('Running Texturing Cell')

        # get inputs
        args = self.inputs.args
        tree = self.inputs.tree
        reconstruction = self.inputs.reconstruction
        # check rerun
        rerun_cell = (args.rerun is not None and args.rerun == 'mvs_texturing') or \
                     (args.rerun_all) or \
                     (args.rerun_from is not None and 'mvs_texturing' in args.rerun_from)

        if not io.file_exists(tree.openmvs_tex_model) or rerun_cell:
            log.ODM_DEBUG('Texturing Mesh')

            system.run('%s %s --export-type obj --resolution-level 6 --min-resolution 640' % (context.openmvs_tex_path, tree.openmvs_dense_mesh_scene))
            system.run('chmod 744 %s' % tree.openmvs_tex_model)

        else:
            log.ODM_WARNING('Found a valid file in: %s' % tree.openmvs_tex_model)

        outputs.reconstruction =reconstruction

        if args.time:
            system.benchmark(start_time, tree.benchmarking, 'MVSTexturing')

        log.ODM_INFO('Running MVS Texturing Cell - Finished')
        return ecto.OK if args.end_with != 'mvstexturing' else ecto.QUIT
