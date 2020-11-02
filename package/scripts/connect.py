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

from common import kafkaHome


class Connect(Script):
    def install(self, env):
        try:
            Execute(
                'export CONNECT_SCRIPT_COUNT=`ls {0}/bin |grep "connect-distributed.sh" | wc -l` && `if [ $CONNECT_SCRIPT_COUNT -ne 0 ];then exit 0;else exit 3;fi `'.format(
                    kafkaHome)
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotInstall")
            else:
                raise ef

        self.configure(env)

    def stop(self, env):
        Execute(
            'ps -ef |grep -v grep |grep "org.apache.kafka.connect.cli.ConnectDistributed config/connect-distributed.properties" |awk \'{print $2}\'|xargs kill -9'
        )

    def start(self, env):
        self.configure(self)
        Execute(
            'cd ' + kafkaHome + ' && nohup bin/connect-distributed.sh config/connect-distributed.properties > connect.out 2>&1 &')

    def status(self, env):
        try:
            Execute(
                'export CONNECT_COUNT=`ps -ef |grep -v grep |grep "org.apache.kafka.connect.cli.ConnectDistributed config/connect-distributed.properties" | wc -l` && `if [ $CONNECT_COUNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import connect
        key_val_template = '{0}={1}\n'

        with open(kafkaHome + '/config/connect-distributed.properties', 'w') as f:
            for key, value in connect.iteritems():
                f.write(key_val_template.format(key, value))


if __name__ == '__main__':
    Connect().execute()
