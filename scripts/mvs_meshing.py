import ecto

from opendm import io
from opendm import log
from opendm import system
from opendm import context

class MVSMeshingCell(ecto.Cell):

    #def declare_params(self,params):
        
    def declare_io(self,params,inputs,outputs):
        inputs.declare("tree","Struct with paths", [])
        inputs.declare("args", "Struct with paths",[])
        inputs.declare("reconstruction","list of ODMReconstructions", [])
        outputs.declare("reconstruction", "list of ODMReconstructions", [])

    def process(self, inputs, outputs):

        #Benchmarking
        start_time = system.now_raw()

        log.ODM_INFO('Running OpenMVS Cell')

        # get inputs
        args = self.inputs.args
        tree = self.inputs.tree
        reconstruction = self.inputs.reconstruction

        # check if we rerun cell or not
        rerun_cell = (args.rerun is not None and args.rerun == 'mvs_meshing') or \
                     (args.rerun_all) or \
                     (args.rerun_from is not None and 'mvs_meshing' in args.rerun_from)

        if not io.file_exists(tree.openmvs_dense_mesh_model) or rerun_cell:
            log.ODM_DEBUG('Reconstruct Mesh')

            system.run('%s %s' % (context.openmvs_meshing_path, tree.openmvs_dense_scene))
            system.run('chmod 744 %s' % tree.openmvs_dense_mesh_model)
        else:
            log.ODM_WARNING('Found a valid file in: %s' % tree.openmvs_dense_mesh_model)

        outputs.reconstruction = reconstruction
        if args.time:
            system.benchmark(start_time, tree.benchmarking, 'MVS_Meshing')

        log.ODM_INFO('Running MVS Meshing Cell - Finished')
        return ecto.OK if args.end_with != 'mvsmeshing' else ecto.QUIT
