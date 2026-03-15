from probability4e import BayesNet, enumeration_ask
# Assumes probability4e.py is in the same directory

class Diagnostics:
    def __init__(self):
        # Define the Asia/Lung Cancer network structure and probabilities
        # Nodes: A=Asia, S=Smoker, T=TB, L=Cancer, B=Bronchitis,
        # TBorC=TB or Cancer, E=Xray, D=Dyspnea
        self.net = BayesNet([
            ('A', '', 0.01),
            ('S', '', 0.5),
            ('T', 'A', {True: 0.05, False: 0.01}),
            ('L', 'S', {True: 0.1, False: 0.01}),
            ('B', 'S', {True: 0.6, False: 0.3}),
            ('TBorC', 'T L', {
                (True, True): 1.0,
                (True, False): 1.0,
                (False, True): 1.0,
                (False, False): 0.0,
            }),
            ('E', 'TBorC', {True: 0.99, False: 0.05}),
            ('D', 'TBorC B', {
                (True, True): 0.9,
                (True, False): 0.7,
                (False, True): 0.8,
                (False, False): 0.1,
            }),
        ])

    def diagnose(self, visit_to_asia, smoking, xray_result, dyspnea):
        # Convert string inputs to evidence dictionary with booleans
        evidence = {}
        if visit_to_asia != "NA": evidence['A'] = (visit_to_asia == "Yes")
        if smoking != "NA": evidence['S'] = (smoking == "Yes")
        if xray_result != "NA": evidence['E'] = (xray_result == "Abnormal")
        if dyspnea != "NA": evidence['D'] = (dyspnea == "Present")

        # Calculate probabilities for each disease
        # P(T|evidence), P(L|evidence), P(B|evidence)
        tb_dist = enumeration_ask('T', evidence, self.net)
        cancer_dist = enumeration_ask('L', evidence, self.net)
        bronchitis_dist = enumeration_ask('B', evidence, self.net)

        # Get probability of 'True' for each
        p_tb = tb_dist[True]
        p_cancer = cancer_dist[True]
        p_bronchitis = bronchitis_dist[True]

        # Find max probability
        results = [("tb", p_tb), ("cancer", p_cancer), ("bronchitis", p_bronchitis)]
        best_disease = max(results, key=lambda x: x[1])

        return [best_disease[0], best_disease[1]]

# Example usage (as called by diagnostics_gui.py)
# diag = Diagnostics()
# print(diag.diagnose("Yes", "Yes", "Abnormal", "Present"))
