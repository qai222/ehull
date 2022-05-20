import inspect

from monty.json import MSONable


def normalize_stoi(formula_dictionary: dict[str, int]) -> dict[str, float]:
    natoms = sum(formula_dictionary.values())
    return {k: v / natoms for k, v in formula_dictionary.items()}


def is_close_to_zero(f: float, eps=1e-5):
    return abs(f) < eps


class Compound(MSONable):

    def __init__(
            self, normalized_formula: dict[str, float], formation_energy_per_atom: float,
            mpid: str = None, e_above_hull=None
    ):
        self.normalized_formula = normalized_formula
        self.formation_energy_per_atom = formation_energy_per_atom
        self.mpid = mpid
        self.e_above_hull = e_above_hull


    def __repr__(self):
        return self.normalized_formula.__repr__()

    @property
    def elements(self):
        return sorted(self.normalized_formula.keys())

    @classmethod
    def from_dict(cls, d: dict):
        keys = [k for k in inspect.signature(Compound.__init__).parameters.keys() if
                k != "self" and not k.startswith("_")]
        data = dict()
        for k in keys:
            if k == "normalized_formula" and k in d:
                data[k] = normalize_stoi(d[k])
            else:
                try:
                    data[k] = d[k]
                except KeyError:
                    continue
        return cls(**data)


def mpdata_to_compound(d: dict):
    data = {
        "normalized_formula": d["unit_cell_formula"],
        "formation_energy_per_atom": d["formation_energy_per_atom"],
        "mpid": d["task_id"],
        "e_above_hull": d["e_above_hull"],
    }
    return Compound.from_dict(data)


def load_mp_pairs(mpdata:list[dict]):
    from tqdm import tqdm

    compounds = [mpdata_to_compound(d) for d in mpdata]
    mpid_to_compound = {c.mpid: c for c in compounds}

    chemsys_to_mpids = dict()
    mpid_to_chemsys = dict()
    print("create mpid2chemsys...")
    for c in tqdm(compounds):
        try:
            chemsys_to_mpids[frozenset(c.elements)].append(c.mpid)
        except KeyError:
            chemsys_to_mpids[frozenset(c.elements)] = [c.mpid, ]
        mpid_to_chemsys[c.mpid] = frozenset(c.elements)

    chemsys_sets = [cs for cs in chemsys_to_mpids]

    chemsys_to_subsets = dict()
    print("create chemsys2subsets...")
    for i in tqdm(range(len(chemsys_sets))):
        chemsys_i = chemsys_sets[i]
        subsets = []
        for j in range(len(chemsys_sets)):
            chemsys_j = chemsys_sets[j]
            if chemsys_i.issuperset(chemsys_j):
                subsets.append(chemsys_j)
        chemsys_to_subsets[chemsys_i] = subsets

    pairs = []
    print("create pairs...")
    for c in tqdm(compounds):
        c_chemsys = mpid_to_chemsys[c.mpid]
        competing_phases = []
        for subset_chemsys in chemsys_to_subsets[c_chemsys]:
            competing_phases += chemsys_to_mpids[subset_chemsys]
        pairs.append((c, [mpid_to_compound[cpid] for cpid in competing_phases if cpid != c.mpid]))
    return pairs