Inconsistent `e_above_hull`
--

This notebook shows some values of `e_above_hull` from `Materials Project` appear to be different 
from the ones computed using `get_decomp_and_e_above_hull`. The latter should be preferred. 

You would need `pymatgen` to run the notebook. 
The code only looked at one chemical system, but it can be extended to others.

### note on `mp-778012`
- The formation energy retrieved using `MPRester` for `mp-778012` is -13.5686 eV/atom which seems abnormal. 
- As of 2022-11-16T17:19:59+00:00 the formation energy shown in [Materials Explorer](https://materialsproject.org/materials/mp-778012) is -1.889 eV/atom.
- The same page captured on 20220527 (from [wayback machine](https://web.archive.org/web/20220000000000*/https://materialsproject.org/materials/mp-778012?material_ids=mp-778012)) shows the formation energy is -13.5686 eV/atom.
