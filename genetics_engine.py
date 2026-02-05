from itertools import product
from collections import defaultdict

# =====================================================
# 1. CORE LOGIC (No DB, No Flask)
# =====================================================

import logging

# Config logging to file
logging.basicConfig(filename='genetics_debug.log', level=logging.INFO, filemode='w')

class Locus:
    def __init__(self, name, sex_linked=False):
        self.name = name
        self.sex_linked = sex_linked
        self.alleles = {}  # allele_name -> dominance

    def add_allele(self, name, dominance):
        self.alleles[name] = dominance


# =====================================================
# GENERAR GENOTIPO PADRES
# =====================================================

def build_parent_genotype(selected_mutations, loci, sex):

    genotype = {}

    for locus_name, locus in loci.items():

        allele = "wild"
        factor = None

        for m in selected_mutations:
            raw_name = m.get("nombre") or m.get("name") or ""
            name = raw_name.lower()
            factor = m.get("factor")

            # Buscar coincidencia flexible
            for allele_name in locus.alleles:

                a = allele_name.lower()

                if a in name or name in a:
                    if allele_name != "wild":
                        allele = allele_name
                        break

            if allele != "wild":
                break

        # --- Construcción genotipo ---

        if locus.sex_linked and sex == "H":
            genotype[locus_name] = (allele, "W") if allele != "wild" else ("wild", "W")

        else:

            wild_dom = locus.alleles.get("wild", 0)
            mut_dom = locus.alleles.get(allele, 0)

            if allele == "wild":
                genotype[locus_name] = ("wild", "wild")

            elif factor == "Portador":
                genotype[locus_name] = (allele, "wild")

            elif factor == "DF":
                genotype[locus_name] = (allele, allele)

            else:
                # Visual automático según dominancia
                if mut_dom > wild_dom:
                    genotype[locus_name] = (allele, "wild")
                else:
                    genotype[locus_name] = (allele, allele)

    return genotype


# =====================================================
# CRUCE POR LOCUS
# =====================================================

def crossover_locus(locus, male_alleles, female_alleles):

    results = []

    for gm in male_alleles:
        for gf in female_alleles:

            if locus.sex_linked:
                sex = "H" if gf == "W" else "M"
            else:
                sex = "Any"

            results.append({
                "sex": sex,
                "alleles": (gm, gf),
                "locus": locus
            })

    return results


# =====================================================
# FENOTIPO
# =====================================================

def resolve_phenotype(locus, alleles):
    # Determine dominant allele
    # This assumes 'alleles' contains names like ("Turquesa", "wild") or ("Turquesa", "Turquesa")
    
    # Sex linked 'W' handling
    # If W is present, the other allele determines phenotype (hemizygous)
    # But effectively, if we have (Mut, W), Mut is expressed. 
    # If (wild, W), Wild is expressed.
    
    # Filter W for dominance check
    check_alleles = [a for a in alleles if a != "W"]
    
    dom = locus.alleles
    best = "wild"
    best_dom = -1
    
    # Find most dominant allele
    for a in check_alleles:
        # Default dominance if not in map?
        # User defined logic: Wild=2, Rec=0.
        # But we must be careful. 
        # If we rely on locus.alleles having 'wild':2...
        val = dom.get(a, 0)
        if val > best_dom:
            best = a
            best_dom = val
            
    # If best is wild, we might be Split (Portador)
    if best == "wild":
        # Check carriers
        carriers = [a for a in check_alleles if a != "wild"]
        if carriers:
             # E.g. "Portador de Aqua"
             # Join if multiple? (Unlikely for one locus but good practice)
             carrier_str = " + ".join([f"Portador de {c}" for c in set(carriers)])
             return "Ancestral", carrier_str

        return "Ancestral", "Ancestral"

    # If Visual (best != wild)
    # Consult genotype string
    geno_list = []
    # Count alleles including W?
    # For (Mut, W), we say "Mut".
    # For (Mut, Mut), we say "Mut (DF)"
    # For (Mut, Wild) and Mut is Dominant -> "Mut (SF)"
    
    # Re-eval counts from full alleles tuple
    normalized = [a for a in alleles if a != "W"] # W doesn't count for DF/SF usually
    
    counts = {x: normalized.count(x) for x in normalized}
    
    for a, ct in counts.items():
        if a == "wild": continue
        
        # Determine label
        # If Sex Linked and Female (W present in original 'alleles') -> Just Name (Hembra)
        if "W" in alleles:
            geno_list.append(f"{a}")
        else:
            # Autosomal or Male SL
            if ct == 2:
                geno_list.append(f"{a} (DF)")
            else:
                # Single Factor
                geno_list.append(f"{a} (SF)")
    
    geno = " + ".join(geno_list) or best # Fallback to name if list empty?
    
    # Aesthetic Fix: Ensure standard notation
    geno = geno.replace("/ ", "Portador de ").replace("/", "Portador de ")
    
    return best, geno


# =====================================================
# COMBINAR LOCI
# =====================================================

def combine_results(locus_results):

    if not locus_results: return []

    combined = locus_results[0]

    for next_locus in locus_results[1:]:

        new_combined = []

        for c1 in combined:
            for c2 in next_locus:

                # Sexo
                sex = "Any"

                if c1["sex"] != "Any" and c2["sex"] != "Any":
                    if c1["sex"] != c2["sex"]:
                        continue
                    sex = c1["sex"]
                elif c1["sex"] != "Any":
                    sex = c1["sex"]
                elif c2["sex"] != "Any":
                    sex = c2["sex"]

                pheno = " + ".join(
                    p for p in [c1["phenotype"], c2["phenotype"]] if p != "Ancestral"
                ) or "Ancestral"

                geno_parts = [g for g in [c1["genotype"], c2["genotype"]] if g != "Ancestral"]
                
                if geno_parts:
                    geno = " + ".join(geno_parts)
                    # Cleanup weird slashes just in case
                    geno = " + ".join(geno_parts)
                    # Cleanup weird slashes just in case - Aggressive
                    geno = geno.replace("/", "Portador de ")
                    geno = geno.replace("Portador de  ", "Portador de ") # Clean double spaces
                else:
                    geno = "Ancestral"

                new_combined.append({
                    "sex": sex,
                    "phenotype": pheno,
                    "genotype": geno
                })

        combined = new_combined

    return combined


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def calculate_genetics(male_mutations, female_mutations, loci):

    logging.info(f"INPUT Male: {male_mutations}")
    logging.info(f"INPUT Female: {female_mutations}")
    logging.info(f"LOCI AVAILABLE: {list(loci.keys())}")
    
    male_gen = build_parent_genotype(male_mutations, loci, "M")
    female_gen = build_parent_genotype(female_mutations, loci, "H")
    
    logging.info(f"GENOTIPO MACHO: {male_gen}")
    logging.info(f"GENOTIPO HEMBRA: {female_gen}")
    # Also print to stdout just in case
    print("GENOTIPO MACHO:", male_gen)
    print("GENOTIPO HEMBRA:", female_gen)

    # Filter active loci (mutated in at least one parent)
    active_loci_names = []
    for lname in loci:
        m_a = male_gen[lname]
        f_a = female_gen[lname]
        
        # Check if Wild
        # Male Wild: ('wild', 'wild')
        # Female Wild: ('wild', 'wild') or ('wild', 'W')
        
        is_m_wild = (m_a == ('wild', 'wild'))
        is_f_wild = (f_a == ('wild', 'wild') or f_a == ('wild', 'W'))
        
        if not is_m_wild or not is_f_wild:
            active_loci_names.append(lname)
            
    logging.info(f"ACTIVE LOCI: {active_loci_names}")

    locus_results = []
    
    # If no active loci, return wildtype immediately
    if not active_loci_names:
         # Need to handle sex dist?
         # Just return basic Ancestral
         pass # let the logic flow, but active_loci is empty.

    for locus_name in active_loci_names:
        locus = loci[locus_name] 

        crosses = crossover_locus(
            locus,
            male_gen[locus_name],
            female_gen[locus_name]
        )

        analyzed = []

        for child in crosses:
            pheno, geno = resolve_phenotype(locus, child["alleles"])
            logging.info(f"RESOLVE LOCUS {locus_name} ALLELES {child['alleles']} -> PHENO: {pheno}")
            
            analyzed.append({
                "sex": child["sex"],
                
                "phenotype": pheno,
                "genotype": geno
            })
            
        locus_results.append(analyzed)

    combined = combine_results(locus_results)
    
    # If no results (e.g. all wild), add default Ancestral
    if not combined:
        logging.info("No active loci, returning Ancestral default.")
        combined = [{'sex': 'Any', 'phenotype': 'Ancestral', 'genotype': 'Ancestral'}]

    if combined:
        logging.info(f"DEBUG COMBINED SAMPLE: {combined[0]}")

    # Probabilidades
    expanded = []

    for c in combined:
        if c["sex"] == "Any":
            expanded.append({**c, "sex": "M"})
            expanded.append({**c, "sex": "H"})
        else:
            expanded.append(c)
            
    if not expanded: return []

    total = len(expanded)
    counts = defaultdict(int)

    for c in expanded:
        key = (c["sex"], c["phenotype"], c["genotype"])
        counts[key] += 1

    results = []

    for key, count in counts.items():
        sex, pheno, geno = key
        prob = (count / total) * 100

        results.append({
            "sex": sex,
            "phenotype": pheno,
            "genotype": geno,
            "probability": round(prob, 1)
        })

    return sorted(results, key=lambda x: (x["sex"], -x["probability"]))
