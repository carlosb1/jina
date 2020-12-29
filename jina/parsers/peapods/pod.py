from .pea import set_pea_parser
from ..base import set_base_parser
from ..helper import add_arg_group


def set_pod_parser(parser=None):
    from ...enums import PollingType, SchedulerType
    if not parser:
        parser = set_base_parser()
    set_pea_parser(parser)

    gp4 = add_arg_group(parser, 'pod replica arguments')
    gp4.add_argument('--parallel', '--shards', type=int, default=1,
                     help='number of parallel peas in the pod running at the same time, '
                          '`port_in` and `port_out` will be set to random, '
                          'and routers will be added automatically when necessary')
    gp4.add_argument('--polling', type=PollingType.from_string, choices=list(PollingType),
                     default=PollingType.ANY,
                     help='ANY: only one (whoever is idle) replica polls the message; '
                          'ALL: all workers poll the message (like a broadcast)')
    gp4.add_argument('--scheduling', type=SchedulerType.from_string, choices=list(SchedulerType),
                     default=SchedulerType.LOAD_BALANCE,
                     help='the strategy of scheduling workload among peas')
    gp4.add_argument('--uses-before', type=str,
                     help='the executor used before sending to all parallels, '
                          'accepted type follows "--uses"')
    gp4.add_argument('--uses-after', type=str,
                     help='the executor used after receiving from all parallels, '
                          'accepted type follows "--uses"')
    gp4.add_argument('--shutdown-idle', action='store_true', default=False,
                     help='shutdown this pod when all peas are idle')
    return parser
