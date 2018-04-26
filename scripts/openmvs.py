import ecto

from opendm import io
from opendm import log
from opendm import system
from opendm import context

class ODMopenMVSCell(ecto.Cell):

    def declare_params(self, params):
        params.declare("cores", 'The maximum number of cores to use '
                                'in dense reconstruction.', context.num_cores) 
    def declare_io(self, params, inputs, outputs):
        inputs.declare("tree", "Struct with paths", [])
        intuts.declare("args", "Struct with paths", [])
        inputs.declare("reconstruction", "list of ODMReconstructions", [])
        outputs.declare("reconstruction", "list of ODMReconstructions", [])

    def process(self, inputs, outputs):

        # Benchmarking
        start_time = system.now_raw()

        log.ODM_INFO('Running ODM CMVS Cell')

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

        if not io.file_exists(tree.openmvs_bundle) or rerun_cell:
            log.ODM_DEBUG('Writing CMVS vis in: %s' % tree.openmvs_bundle)

            #copy bundle file to openmvs dir
            from shutil import copyfile
            copyfile(tree.opensfm_bundle,
                     tree.openmvs_bundle)

            kwargs = {
                    'bin': context.openmvs_path,
                    'prefix': self.inputs.tree.opensfm_rec_path,
                    'cores' : self.params.cores
                    }
            # run openmvs
            system.run('{bin} {prefix}/openmvs/scene.mvs  {cores}'.format(**kwargs))

        else:
            log.ODM_WARNING('Found a valid CMVS file in: %s' %
                            tree.openmvs_bundle)

        outputs.reconstruction = reconstruction

        if args.time:
            system.benchmark(start_time, tree.benchmarking, 'OpenMVS')

        log.ODM_INFO('Running ODM OpenMVS Cell - Finished')
        return ecto.OK if args.end_with != 'openmvs' else ecto.QUIT
