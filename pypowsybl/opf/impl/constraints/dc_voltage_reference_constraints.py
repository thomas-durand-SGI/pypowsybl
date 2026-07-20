# Copyright (c) 2026, SuperGrid Institute (http://www.supergrid-institute.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
#
import pyoptinterface as poi

from pypowsybl.opf.impl.model.constraints import Constraints
from pypowsybl.opf.impl.model.model import Model
from pypowsybl.opf.impl.model.model_parameters import ModelParameters
from pypowsybl.opf.impl.model.network_cache import NetworkCache
from pypowsybl.opf.impl.model.variable_context import VariableContext

class DcVoltageReferenceConstraints(Constraints):
    def add(self, parameters: ModelParameters, network_cache: NetworkCache, variable_context: VariableContext,
            model: Model) -> None:
        grounded_dc_node_ids = set(network_cache.dc_grounds["dc_node_id"])

        for dc_component, component_nodes in network_cache.dc_nodes.groupby("dc_component", sort=True):
            component_node_ids = component_nodes.index

            # A ground already fixes the voltage reference
            if any(node_id in grounded_dc_node_ids for node_id in component_node_ids):
                continue

            reference_eq = poi.ExprBuilder()

            for node_id in component_node_ids:
                node_num = network_cache.dc_nodes.index.get_loc(node_id)
                reference_eq += variable_context.v_dc_vars[node_num]

            model.add_linear_constraint(reference_eq, poi.Eq, 0.0)
 
