## pragmaticflows

`pragmaticflows` is being used at [AmLight](https://www.amlight.net) to assess the conformance of OpenFlow version 1.3 on certain switch platforms focused on use cases for production networks pragmatically. `pragmaticflows` is a Ryu application which was forked from the classic [Ryu test suites](https://github.com/osrg/ryu/tree/master/ryu/tests/switch/of13).

## Enhancements

- Fully integrated with pytest for first-class test cases selection and HTML reports. You can select or troubleshoot/debug each test case individually thanks to pytest.
- All test cases written in json files have been refactored with actual variables so you can use with any OF1.3 switches regardless of their port numbers.
- Flowmods, PacketIns, PacketOuts and Errors are all logged to simplify the analysis, so just by analyzing the report you'll be able to figure out what happened.
- Removed miss tables checks, packet-ins are checked in instead, to reduce false positives.
- Removed all MPLS and PBB packets that were in several use cases since most vendors don't actually support these features.

### Report

Here's a screenshot of the report that you should expect when you run `pragmaticflows` with the `--html-report.html --self-contained-html` options:

![SS](./.ss.png "Report demo")

## Topology

- You'll need at least two links between the two OpenFlow switches. A third link is only necessary for advanced other more elaborated features such as multicast groups and QoS metering, which is not implemented yet on pragmaticflows yet.
- There are two switches involved, the one being under test the `target` switch and the `auxiliary`.
- Also, you'll need a controller running RYU to control these switches, as long as you have IP reachability that's all that matters.

```
------------------
    (1) -- (1)
 s1 (2) -- (2) s2
------------------
```

- `s1` and `s2` represent an OpenFlow 1.3 switch.
- The numbers `(1)` and `(2)` in the topology are the `of_port` numbers.

The topology is specified in a yml format, which is passed as an environment variable, see the Test Selection section bellow. Take a look on [topology.yml](./topology.yml) for example.

## Pre-requisites

Before running any test cases:

1. Make sure there aren't any type of unexpected network packets being sent on the interfaces being tested. This Ryu application relies on OpenFlow stats/counters/PacketIns/PacketOuts, so this is critical. For example, disable spanning tree, LLDP and other L2 multicast protocols. Ideally, you should run a sniffer on these interfaces for a few minutes before starting to verify this point.
2. Install Ryu, either `pip install requirements.txt` on a virtualenv or `docker-compose up` if you want run Ryu on Docker.
3. Figure out which test cases you want to run.
4. Figure out all the OpenFlow interface numbers on the `tester` (auxiliary switch) and `target` (device under test), and their datapath ids you'll need to pass them to ryu-manager.
5. Read [Ryu Official Test Tool](http://https://osrg.github.io/ryu-book/en/html/switch_test_tool.html#reference-transfer-path-of-the-applied-packet) page to understand how validation packets will be sent over these three links in the topology.
6. Configure the OpenFlow switches to point out to the RYU controller.

## Test Suites

These are the test suites, each folder has the .json files that specify the test cases. So, to add a new test case you have to either edit an existing json file, or if it makes sense create a new one. Currently, they're being grouped into folders, but folders doesn't not reduce the flexibility of the test selection thanks to pytest.

```
~/repos/pragmaticflows/tests master*
❯ tree -L 1
.
├── eth
├── in_port
├── ipv4
├── ipv6
├── lldp
├── qinq
├── test_all.py
└── vlan
```

## Test Selection

There's a pytest_args, where you can pass any pytest argument, so you can select tests or just collect them based on this variable.

## Collecting test cases

You can use the `--collect-only` argument, you can see bellow the `Functions` and the `id` of each test case. So typically you just collect first, narrow down a test case and run it.

```
❯ topo=topology_cnet.yml pytest_args="-v -s --collect-only --html=report.html --self-contained-html" ryu-manager --log-config-file logging.ini oftester/oftester.py
-----> 2018-06-15 10:22:57,055 INFO [ryu.base.app_manager]
loading app oftester/oftester.py
<Module 'tests/test_all.py'>
  <Function "test[match_ipv6_flowlabel.json_id_0_ethernet/ipv6(flow_label=100)/tcp-->'ipv6_flabel=100,actions=output:target_send_port_1']">
  <Function "test[match_ipv6_flowlabel.json_id_1_ethernet/ipv6(flow_label=100)/tcp-->'ipv6_flabel=100,actions=output:CONTROLLER']">
  <Function "test[match_ipv6_flowlabel.json_id_2_ethernet/ipv6(flow_label=203)/tcp-->'ipv6_flabel=100,actions=output:target_send_port_1']">
  <Function "test[match_ipv6_flowlabel.json_id_3_ethernet/vlan/ipv6(flow_label=100)/tcp-->'ipv6_flabel=100,actions=output:target_send_port_1']">
  <Function "test[match_ipv6_flowlabel.json_id_4_ethernet/vlan/ipv6(flow_label=100)/tcp-->'ipv6_flabel=100,actions=output:CONTROLLER']">
```

For example, if you want to target anything that is related to LLDP, you can use the `-k` parameter to pass a regex, as you can see there are just two test cases that test the matching capabilitities with LLDP:

```

❯ topo=topology_cnet.yml pytest_args="-v -s --collect-only -k lldp --html=report.html --self-contained-html" ryu-manager --log-config-file logging.ini oftester/oftester.py
<Module 'tests/test_all.py'>
  <Function "test[match_lldp.json_id_144_ethernet/lldp-->'eth_type=target_recv_port,actions=output:target_send_port_1']">
  <Function "test[match_lldp.json_id_145_ethernet/vlan/lldp-->'vlan_100/lldp=target_recv_port,actions=output:target_send_port_1']">
```

## Running just a subset of test cases

If we were to run just the LLDP test cases mentioned before, you just have to pass the regex without the `--collect-only` argument.

```
❯ topo=topology_cnet.yml pytest_args="-v -s -k lldp --html=report.html --self-contained-html" ryu-manager --log-config-file logging.ini oftester/oftester.py
-----> 2018-06-15 10:28:50,308 INFO [ryu.base.app_manager]
loading app oftester/oftester.py
10:28:50 [ryu.base.app_manager] [INFO] loading app ryu.controller.ofp_handler
10:28:50 [ryu.base.app_manager] [INFO] instantiating app oftester/oftester.py of OfTester
10:28:50 [OfTester] [INFO] Topology:{ 'switch_target': { 'dpid': '0000000000000003',
                     'of_version': 'openflow13',
                     'recv_port': 2,
                     'send_port_1': 3,
                     'send_port_2': 4},
  'switch_tester': { 'dpid': '0000000000000004',
                     'of_version': 'openflow13',
                     'recv_port_1': 3,
                     'recv_port_2': 4,
                     'send_port': 2}}
10:28:50 [ryu.base.app_manager] [INFO] instantiating app ryu.controller.ofp_handler of OFPHandler
Test session starts (platform: linux, Python 3.6.5, pytest 3.6.1, pytest-sugar 0.9.1)
rootdir: /home/arcanjo/repos/pragmaticflows, inifile:
plugins: sugar-0.9.1, metadata-1.7.0, html-1.19.0
10:28:50 [OfTester] [INFO] Waiting for switches connection...
10:28:51 [OfTester] [INFO] dpid=0000000000000004 : Join tester SW.
10:28:51 [OfTester] [INFO] dpid=0000000000000003 : Join target SW.
```

## Running all test cases, with HTML report:

Currently there are 190+ test cases, it takes almost 10 minutes to run:

```
topo=topology_cnet.yml pytest_args="-v -s --html=report.html --self-contained-html" ryu-manager --log-config-file logging.ini oftester/oftester.py
```


