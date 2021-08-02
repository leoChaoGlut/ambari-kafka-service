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

import ConfigParser
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(script_dir, 'download.ini')))

packageDir = os.path.dirname(script_dir)
serviceDir = os.path.dirname(packageDir)
serviceName = os.path.basename(serviceDir)

kafkaHomePrefix='/home/service/var/data1/kafka'

kafkaHome =kafkaHomePrefix+'/kafka'
kafkaTarUrl = config.get('download', 'kafka_tar_url')

jdk11Home = kafkaHomePrefix+'/jdk11/'
jdk11Url = config.get('download', 'jdk11_url')
jdk11TarName = jdk11Url.split('/')[-1]

exportJavaHomeAndPath = ' export JAVA_HOME=' + jdk11Home + ' && export PATH=${JAVA_HOME}/bin:$PATH '
