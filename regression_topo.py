#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mininet.topo import Topo


class RegressionTopo(Topo):
    "Regression topology"

    def __init__(self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__(self)

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add links
        self.addLink(s1, s2)
        self.addLink(s1, s2)
        self.addLink(s1, s2)


topos = {'regression_topo': RegressionTopo}
