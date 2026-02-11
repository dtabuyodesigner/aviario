from itertools import product
from collections import defaultdict
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

            # Buscar coincidencia exacta (o disciplinada)
            for allele_name in locus.alleles:
                a = allele_name.lower()
                if a == name: # Changed from 'in' to '==' for precision
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
    # Filter W for dominance check
    check_alleles = [a for a in alleles if a != "W"]
    
    dom = locus.alleles
    best = "wild"
    best_dom = -1
    
    # Find most dominant allele
    for a in check_alleles:
        val = dom.get(a, 0)
        if val > best_dom:
            best = a
            best_dom = val
            
    # If best is wild, we might be Split (Portador)
    if best == "wild":
        carriers = [a for a in check_alleles if a != "wild"]
        if carriers:
             carrier_str = " + ".join([f"Portador de {c}" for c in set(carriers)])
             return "Ancestral", carrier_str

        return "Ancestral", "Ancestral"

    # If Visual (best != wild)
    geno_list = []
    normalized = [a for a in alleles if a != "W"]
    counts = {x: normalized.count(x) for x in normalized}
    
    for a, ct in counts.items():
        if a == "wild": continue
        if "W" in alleles:
            geno_list.append(f"{a}")
        else:
            if ct == 2:
                geno_list.append(f"{a} (DF)")
            else:
                geno_list.append(f"{a} (SF)")
    
    geno = " + ".join(geno_list) or best
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

                pheno_parts = [p for p in [c1["phenotype"], c2["phenotype"]] if p != "Ancestral"]
                pheno = " + ".join(pheno_parts) or "Ancestral"

                geno_parts = [g for g in [c1["genotype"], c2["genotype"]] if g != "Ancestral"]
                if geno_parts:
                    geno = " + ".join(geno_parts)
                    geno = geno.replace("/", "Portador de ")
                    geno = geno.replace("Portador de  ", "Portador de ")
                else:
                    geno = "Ancestral"

                new_combined.append({
                    "sex": sex,
                    "phenotype": pheno,
                    "genotype": geno,
                    "pheno_list": pheno_parts
                })

        combined = new_combined

    return combined

def apply_combinations(result, combinations):
    if not combinations: return result
    phenos = result.get("pheno_list", [])
    if len(phenos) < 2: return result
    
    for i in range(len(phenos)):
        for j in range(i + 1, len(phenos)):
            pair = tuple(sorted([phenos[i].lower(), phenos[j].lower()]))
            if pair in combinations:
                result["phenotype"] = combinations[pair]
                return result
    return result


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def calculate_genetics(male_mutations, female_mutations, loci, combinations=None):

    logging.info(f"INPUT Male: {male_mutations}")
    logging.info(f"INPUT Female: {female_mutations}")
    
    male_gen = build_parent_genotype(male_mutations, loci, "M")
    female_gen = build_parent_genotype(female_mutations, loci, "H")
    
    # print("GENOTIPO MACHO:", male_gen)
    # print("GENOTIPO HEMBRA:", female_gen)

    active_loci_names = []
    for lname in loci:
        m_a = male_gen[lname]
        f_a = female_gen[lname]
        is_m_wild = (m_a == ('wild', 'wild'))
        is_f_wild = (f_a == ('wild', 'wild') or f_a == ('wild', 'W'))
        
        if not is_m_wild or not is_f_wild:
            active_loci_names.append(lname)

    locus_results = []
    for locus_name in active_loci_names:
        locus = loci[locus_name] 
        crosses = crossover_locus(locus, male_gen[locus_name], female_gen[locus_name])
        analyzed = []
        for child in crosses:
            pheno, geno = resolve_phenotype(locus, child["alleles"])
            analyzed.append({
                "sex": child["sex"],
                "phenotype": pheno,
                "genotype": geno
            })
        locus_results.append(analyzed)

    combined = combine_results(locus_results)
    
    if not combined:
        combined = [{'sex': 'Any', 'phenotype': 'Ancestral', 'genotype': 'Ancestral'}]

    if combinations:
        combined = [apply_combinations(c, combinations) for c in combined]

    # Apply specific species logic (Ninfas/Agapornis)
    # Whiteface/Blue masks Psittacine (Yellow/Red)
    # Ino masks Melanin
    combined = [apply_phenotype_rules(c) for c in combined]

    # Probabilidades
    expanded = []
    for c in combined:
        if c["sex"] == "Any" or not c["sex"]:
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


def apply_phenotype_rules(result):
    """
    Apply complex phenotype rules like masking (Epistasis).
    Especially for Ninfas (Cockatiels) and Agapornis.
    """
    pheno_list = [p.lower() for p in result.get("pheno_list", [])]
    original_pheno = result["phenotype"]
    
    # 1. Albino Logic (Lutino + Whiteface/Blue)
    # Check for Ino (Lutino) AND Blue (Cara blanca / Whiteface)
    has_ino = any('lutino' in p or 'ino' in p for p in pheno_list) 
    has_blue = any('cara blanca' in p or 'whiteface' in p or 'azul' in p or 'turquesa' in p for p in pheno_list)
    has_canela = any('canela' in p or 'cinnamon' in p for p in pheno_list)
    has_perlado = any('perlado' in p or 'opaline' in p or 'pearl' in p for p in pheno_list)
    has_pied = any('pied' in p or 'manchado' in p or 'arlequín' in p for p in pheno_list)
    
    # --- Renaming/Combination Logic ---
    
    # Albino (Priority)
    if has_ino and has_blue:
        if 'albino' not in original_pheno.lower():
            original_pheno = original_pheno.replace("Lutino", "").replace("Cara blanca", "").replace("Carablanca", "").replace("Blue", "").replace(" + ", " ").strip()
            original_pheno = "Albino " + original_pheno
            
    # Cinnamon Pearl
    if has_canela and has_perlado:
        if 'cinnamon pearl' not in original_pheno.lower():
             # Replace individual parts with combined name
             # Careful not to duplicate if source has multiples
             original_pheno = original_pheno.replace("Canela", "").replace("Perlado", "").replace("Opalino", "").replace("Cinnamon", "").replace("Pearl", "").replace(" + ", " ").strip()
             original_pheno = "Cinnamon Pearl " + original_pheno

    # Whiteface Pied (Naming preference)
    if has_blue and has_pied:
        if 'whiteface pied' not in original_pheno.lower():
            if "Cara blanca" in original_pheno:
               original_pheno = original_pheno.replace("Cara blanca", "Whiteface")
            original_pheno = original_pheno.replace("Whiteface + Pied", "Whiteface Pied")

    # Lutino Pied
    if has_ino and has_pied:
        original_pheno = original_pheno.replace("Lutino + Pied", "Lutino Pied")
        
    # --- New Combinations from User List ---
    
    # Pearl Pied
    if has_perlado and has_pied:
        original_pheno = original_pheno.replace("Perlado + Pied", "Pearl Pied").replace("Opalino + Arlequín", "Pearl Pied")
        
    # Cinnamon Pied
    if has_canela and has_pied:
        original_pheno = original_pheno.replace("Canela + Pied", "Cinnamon Pied")

    # Whiteface Cinnamon
    if has_blue and has_canela:
         original_pheno = original_pheno.replace("Cara blanca + Canela", "Whiteface Cinnamon").replace("Canela + Cara blanca", "Whiteface Cinnamon")

    # Whiteface Pearl
    if has_blue and has_perlado:
         original_pheno = original_pheno.replace("Cara blanca + Perlado", "Whiteface Pearl").replace("Perlado + Cara blanca", "Whiteface Pearl")

    # Whiteface Cinnamon Pearl (Tri-combo)
    if has_blue and has_canela and has_perlado:
        # Check if already partially combined into "Whiteface Cinnamon" or "Cinnamon Pearl" or "Whiteface Pearl"
        # We want "Whiteface Cinnamon Pearl"
        
        # Simplest: If we have all three components, force the name.
        # But we must preserve any OTHER traits (like Pied).
        
        # Strategy: Remove the 3 components from string, prepend "Whiteface Cinnamon Pearl"
        # Components to remove: Whiteface, Cinnamon, Pearl, Canela, Perlado, Cara blanca, Cinnamon Pearl, Whiteface Cinnamon, etc.
        
        # We already ran Cinnamon Pearl logic above, so "Cinnamon Pearl" might be present.
        # We ran Whiteface logic? Not really, just replacements.
        
        # Let's clean up
        temp = original_pheno
        temp = temp.replace("Whiteface Cinnamon", "").replace("Whiteface Pearl", "").replace("Cinnamon Pearl", "")
        temp = temp.replace("Cara blanca", "").replace("Canela", "").replace("Perlado", "")
        temp = temp.replace("Whiteface", "").replace("Cinnamon", "").replace("Pearl", "")
        temp = temp.replace(" + ", " ").strip()
        
        original_pheno = "Whiteface Cinnamon Pearl " + temp

    # Pastel Pied
    has_pastel = any('pastel' in p for p in pheno_list)
    if has_pastel and has_pied:
        original_pheno = original_pheno.replace("Pastel + Pied", "Pastel Pied")

    # Silver Pied
    has_silver = any('silver' in p or 'plateado' in p for p in pheno_list)
    if has_silver and has_pied:
        original_pheno = original_pheno.replace("Silver + Pied", "Silver Pied").replace("Plateado + Pied", "Silver Pied")

    # Clean up
    original_pheno = " ".join(original_pheno.split())
    original_pheno = original_pheno.replace(" + ", " ") # Remove stray pluses
    original_pheno = original_pheno.replace("  ", " ")
    
    result["phenotype"] = original_pheno
    
    return result
