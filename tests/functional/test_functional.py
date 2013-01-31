#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of the pymfony package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
"""
"""

from __future__ import absolute_import;

import os.path;

from pymfony.component.dependency import ContainerBuilder;
from pymfony.component.kernel import Kernel;
from pymfony.component.kernel import ConfigurableExtension;
from pymfony.component.config import ConfigurationInterface;
from pymfony.component.config import TreeBuilder;

class AppExtension(ConfigurableExtension):
    def _loadInternal(self, mergedConfig, container):
        assert isinstance(mergedConfig, dict);
        assert isinstance(container, ContainerBuilder);

        for name, value in mergedConfig.items():
            container.getParameterBag().set(self.getAlias()+'.'+name, value);

    def getAlias(self):
        return 'app';

class Configuration(ConfigurationInterface):
    def getConfigTreeBuilder(self):
        treeBuilder = TreeBuilder();
        rootNode = treeBuilder.root('app');

        node =  rootNode.children();
        node =      node.scalarNode('foo');
        node =          node.defaultValue("bar");
        node =      node.end();
        node =  node.end();

        return treeBuilder;

class AppKernel(Kernel):
    def registerContainerConfiguration(self, loader):
        loader.load("{0}/config/config_{1}.ini".format(
            os.path.dirname(__file__),
            self.getEnvironment(),
        ));












import unittest
import os.path as op;


class Test(unittest.TestCase):
    def setUp(self):
        self._kernel = AppKernel("test", True);
        self._kernel.boot();
        self.container = self._kernel.getContainer();


    def tearDown(self):
        self._kernel.shutdown();


    def testLocateResource(self):
        locator = self.container.get('file_locator');
        self.assertEqual(
            op.join(op.realpath(op.dirname(__file__)), "config/services.json").replace('\\', '/').lower(),
            self._kernel.locateResource("@App/config/services.json").replace('\\', '/').lower()
        );
        self.assertEqual(
            op.join(op.realpath(op.dirname(__file__)), "config/services.json").replace('\\', '/').lower(),
            locator.locate("@App/config/services.json").replace('\\', '/').lower()
        );
        self.assertEqual(
            op.join(op.realpath(op.dirname(__file__)), "config/services.json").replace('\\', '/').lower(),
            locator.locate("@App/config/services.json").replace('\\', '/').lower()
        );


    def testExtensionConfig(self):
        self.assertEqual(
            self.container.getParameter('app.foo'),
            'bar'
        );
        self.assertEqual(
            self.container.getParameter('locale'),
            'en'
        );


if __name__ == "__main__":
    unittest.main();
