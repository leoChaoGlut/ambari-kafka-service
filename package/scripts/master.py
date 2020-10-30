# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script

from common import kuduHome, KUDU_RPM, KUDU_MASTER_RPM


class Master(Script):
    def install(self, env):
        kuduTmpDir = '/tmp/kudu'
        kuduRpmPath = kuduTmpDir + '/kudu.rpm'
        kuduMasterRpmPath = kuduTmpDir + '/kudu-master.rpm'

        Execute('mkdir -p {0}'.format(kuduHome))
        Execute('mkdir -p {0}'.format(kuduTmpDir))

        Execute('wget --no-check-certificate {0} -O {1}'.format(KUDU_RPM, kuduRpmPath))
        Execute('wget --no-check-certificate {0} -O {1}'.format(KUDU_MASTER_RPM, kuduMasterRpmPath))

        Execute('rpm -ivh --force {0}'.format(kuduRpmPath))
        Execute('rpm -ivh --force {0}'.format(kuduMasterRpmPath))

        self.configure(env)

    def stop(self, env):
        Execute('service kudu-master stop')

    def start(self, env):
        self.configure(self)
        Execute('service kudu-master start')

    def status(self, env):
        try:
            Execute('service kudu-master status')
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import kudu_master, master_gflagfile
        key_val_template = '{0}={1}\n'
        export_kv_tmpl = 'export {0}={1}\n'

        walDir = master_gflagfile['--fs_wal_dir']
        dataDirs = master_gflagfile['--fs_data_dirs']
        metaDir = master_gflagfile['--fs_metadata_dir']
        logDir = kudu_master['FLAGS_log_dir']

        Execute('mkdir -p {0}'.format(walDir))
        Execute('mkdir -p {0}'.format(dataDirs))
        Execute('mkdir -p {0}'.format(metaDir))
        Execute('mkdir -p {0}'.format(logDir))

        Execute('chown kudu:kudu {0}'.format(walDir))
        Execute('chown kudu:kudu {0}'.format(dataDirs))
        Execute('chown kudu:kudu {0}'.format(metaDir))
        Execute('chown kudu:kudu {0}'.format(logDir))
        Execute('chown kudu:kudu {0}'.format(kuduHome))

        with open('/etc/kudu/conf/master.gflagfile', 'w') as f:
            for key, value in master_gflagfile.iteritems():
                f.write(key_val_template.format(key, value))

        with open('/etc/default/kudu-master', 'w') as f:
            for key, value in kudu_master.iteritems():
                f.write(export_kv_tmpl.format(key, value))


if __name__ == '__main__':
    Master().execute()
