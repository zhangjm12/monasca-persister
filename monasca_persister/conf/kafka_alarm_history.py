# (C) Copyright 2016-2017 Hewlett Packard Enterprise Development LP
# Copyright 2017 FUJITSU LIMITED
# (C) Copyright 2017 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy

from oslo_config import cfg

from monasca_persister.conf import kafka_common
from monasca_persister.conf import types

kafka_alarm_history_group = cfg.OptGroup(name='kafka_alarm_history',
                                         title='kafka_alarm_history')
kafka_alarm_history_opts = [
    cfg.BoolOpt('enabled',
                help='Enable alarm state history persister',
                default=False),
    # NOTE(czarneckia) default by reference does not work with ListOpt
    cfg.ListOpt('uri',
                help='Comma separated list of Kafka broker host:port',
                default=['127.0.0.1:9092'],
                item_type=types.HostAddressPortType()),
    cfg.StrOpt('group_id',
               help='Kafka Group from which persister get data',
               default='1_alarm-state-transitions'),
    cfg.StrOpt('topic',
               help='Kafka Topic from which persister get data',
               default='alarm-state-transitions'),
    cfg.StrOpt('zookeeper_path',
               help='Path in zookeeper for kafka consumer group partitioning algorithm',
               default='/persister_partitions/$kafka_alarm_history.topic'),
    cfg.IntOpt(
        'batch_size',
        help='Maximum number of alarm state history messages to buffer before writing to database',
        default=1),
]


# Replace Default OPt with reference to kafka group option
kafka_common_opts = copy.deepcopy(kafka_common.kafka_common_opts)
for opt in kafka_common_opts:
    opt.default = '$kafka.{}'.format(opt.name)


def register_opts(conf):
    conf.register_group(kafka_alarm_history_group)
    conf.register_opts(kafka_alarm_history_opts + kafka_common_opts,
                       kafka_alarm_history_group)


def list_opts():
    return kafka_alarm_history_group, kafka_alarm_history_opts + kafka_common_opts
