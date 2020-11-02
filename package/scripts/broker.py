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

from common import kafkaHome, kafka_tar


class Broker(Script):
    def install(self, env):
        kafkaTmpDir = '/tmp/kafka'
        kafkaTarTmpPath = kafkaTmpDir + '/kafka.tar'

        Execute('mkdir -p {0}'.format(kafkaTmpDir))
        Execute('mkdir -p {0}'.format(kafkaHome))

        Execute('wget --no-check-certificate {0} -O {1}'.format(kafka_tar, kafkaTarTmpPath))

        Execute('tar -xf {0} -C {1} --strip-components=1'.format(kafkaTarTmpPath, kafkaHome))

        self.configure(env)

    def stop(self, env):
        Execute(kafkaHome + '/bin/kafka-server-stop.sh')

    def start(self, env):
        self.configure(self)
        Execute(kafkaHome + '/bin/kafka-server-start.sh ' + kafkaHome + '/config/connect-distributed.properties')

    def status(self, env):
        try:
            Execute(
                'export KAFKA_COUNT=`ps -ef |grep -v grep |grep "kafka.Kafka config/server.properties" | wc -l` && `if [ $KAFKA_COUNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        import socket
        from params import broker
        key_val_template = '{0}={1}\n'

        ipStr = socket.gethostbyname(socket.gethostname())
        ip = ipStr.replace(".", "")

        with open(kafkaHome + '/config/server.properties', 'w') as f:
            for key, value in broker.iteritems():
                f.write(key_val_template.format(key, value))
            f.write(key_val_template.format('broker.id', ip))


if __name__ == '__main__':
    Broker().execute()
