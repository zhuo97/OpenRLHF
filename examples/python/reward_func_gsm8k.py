# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Adapt from: https://github.com/volcengine/verl/blob/main/verl/utils/reward_score/gsm8k.py

import torch
import re


def extract_solution(solution_str):
    # this also tests the formatting of the model
    solution = re.search("#### (\\-?[0-9\\.\\,]+)", solution_str)
    if solution is None:
        final_answer = None
    else:
        final_answer = solution.group(0)
        final_answer = final_answer.split("#### ")[1].replace(",", "").replace("$", "")

    return final_answer

        
def reward_func(queries, prompts, labels, **kwargs):
    results = []
    for i in range(len(queries)):
        answer = extract_solution(queries[i])
        ground_truth = labels[i]
        if answer is None:
            results.append(0.0)
        else:
            if answer == ground_truth:
                results.append(1.0)
            else:
                results.append(0.0)
    
    return torch.tensor(results)
