from pymatgen.ext.matproj import MPRester
import gzip
import json
from monty.json import MontyEncoder


def json_dump(o, fn, compress=True) -> None:
    if compress:
        with gzip.open(fn, 'wt', encoding='UTF-8') as zipfile:
            json.dump(o, zipfile, cls=MontyEncoder)
    else:
        with open(fn, "w") as f:
            json.dump(o, f, cls=MontyEncoder)

if __name__ == '__main__':
    mat_api_key = "YOUR_API_KEY_HERE"

    mpr = MPRester(mat_api_key)

    all_compounds = mpr.query({}, properties=["task_id", "pretty_formula", 'e_above_hull',
                                              'elements', 'volume', 'formation_energy_per_atom', 'band_gap',
                                              'nsites', 'unit_cell_formula'])

    json_dump(all_compounds, "mp.json.gz")
