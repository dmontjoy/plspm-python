#!/usr/bin/python3
#
# Copyright (C) 2019 Google Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import plspm.config as c, pandas as pd, numpy as np


def _create_summary(data: pd.DataFrame):
    summary = pd.DataFrame(0, index=data.columns, columns=["original", "mean", "std.error", "perc.025", "perc.975"])
    summary.loc[:, "mean"] = data.mean(axis=0)
    summary.loc[:, "std.error"] = data.std(axis=0)
    summary.loc[:, "perc.025"] = data.quantile(0.025, axis=0)
    summary.loc[:, "perc.975"] = data.quantile(0.975, axis=0)
    return summary


class Bootstrap:
    def __init__(self, config: c.Config, data: pd.DataFrame, calculator, iterations: int):
        observations = data.shape[0]
        weights = pd.DataFrame(columns=data.columns)
        for i in range(1, iterations):
            boot_observations = np.random.randint(observations, size=observations)
            boot_data = config.treat(data.iloc[boot_observations, :])
            _final_data, _scores, _weights = calculator.calculate(boot_data)
            weights = weights.append(_weights.T, ignore_index=True)
        self.__weights = _create_summary(weights)

    def weights(self):
        return self.__weights
