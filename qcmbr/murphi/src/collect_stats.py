import numpy as np
import pickle
from util import *
with open ("build/stats.pkl", "rb") as f:
  res_file_stats = pickle.load(f)
print(res_file_stats.keys())
arr = np.array(res_file_stats['completed'], dtype=float)
print('count', len(arr))
print('avg', float(np.mean(arr)) if len(arr) else 'nan')
print('min', float(np.min(arr)) if len(arr) else 'nan')
print('max', float(np.max(arr)) if len(arr) else 'nan')

for ff in res_file_stats['unknow_ff']:
  r = get_res_file(ff, "")
# res_file_stats  = get_file_stats()
farr = []
# with open ("build/ff.txt", "r") as f:
#   for line in f:
#     farr.append(line[1:-1])
# print(res_file_stats, farr)
cnt = 0
print(res_file_stats['completed_ff'][0])
arr = res_file_stats['completed_ff']
print(type(arr[0]))
for f in farr:
  fnd = False
  for itm in res_file_stats['completed_ff']:
    if f in str(itm):
      fnd = True
      break
  if not fnd:
    print("==>", f)
    cnt += 1
print("MISS ", cnt) 
# print(res_file_stats)
for k, v in res_file_stats.items():
  print(k, len(v))
  if k == "unknow_ff":
    arr = [itm for itm in v if itm in res_file_stats['completed_ff'] or itm in res_file_stats['undetermined_ff']]
    print(k, len(arr), arr)
    continue
  if not "ff" in k:
    nparr = np.array(v)
    if len(nparr) == 0:
      continue
    print("\t mean: ", np.mean(nparr))
    print("\t std: ", np.std(nparr))
    print("\t max: ", np.max(nparr), res_file_stats[k + "_ff"][np.argmax(nparr)])
    print("\t min: ", np.min(nparr))

completed_arr = np.array(res_file_stats.get('completed', []), dtype=float)
undetermined_arr = np.array(res_file_stats.get('undetermined', []), dtype=float)

combined_arr = np.concatenate((completed_arr, undetermined_arr))
print('combined_count(completed+undetermined)', len(combined_arr))
print('combined_avg(completed+undetermined)', float(np.mean(combined_arr)) if len(combined_arr) else 'nan')
capped_combined_arr = np.minimum(combined_arr, 600.0)
print('capped_combined_avg(max=600)', float(np.mean(capped_combined_arr)) if len(capped_combined_arr) else 'nan')
arr2 = combined_arr[combined_arr > 600.0]
print('arr2_count(>600)', len(arr2))
print('arr2_avg(>600)', float(np.mean(arr2)) if len(arr2) else 'nan')

