# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as onp
import scipy.stats as osp_stats

from ... import lax
from ...numpy.lax_numpy import _promote_args_like, _constant_like, _wraps, inf, where


@_wraps(osp_stats.pareto.logpdf)
def logpdf(x, b, loc=0, scale=1):
  x, b, loc, scale = _promote_args_like(osp_stats.pareto.logpdf, x, b, loc, scale)
  one = _constant_like(x, 1)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.div(scale, b))
  log_probs = lax.neg(lax.add(normalize_term, lax.mul(lax.add(b, one), lax.log(scaled_x))))
  return where(lax.lt(x, lax.add(loc, scale)), -inf, log_probs)

@_wraps(osp_stats.pareto.pdf)
def pdf(x, b, loc=0, scale=1):
  return lax.exp(logpdf(x, b, loc, scale))
