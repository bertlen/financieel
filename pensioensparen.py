import matplotlib.pyplot as plt

RENDEMENT_REFERENTIE = 0.08  # Referentie rendement wereld ETF
RENDEMENT_PENSIOENFONDS_ARGENTA = 0.08 # jaarlijks rendement
KOSTEN_PENSIOENFONDS_ARGENTA = 1.44e-2  # jaarlijkse kosten
BELASTINGSVOORDEEL_PENSIOENSPAREN = 0.3  # Belastingsvoordeel bij inleg
BELASTING_PENSIOENSPAREN = 0.08  # Belastingpercentage bij opname (op inleg gedaan voor de 60ste verjaardag)


class Pensioenfonds:
    FISCAAL_MAXIMUM = 1030  # Fiscaal maximum voor jaarlijkse inleg pensioensparen
    
    def __init__(self, rendement, kosten, belastingsvoordeel=30e-2, belasting_opname=0.08):
        """
        Initialiseer een pensioenfonds.

        :param rente: Jaarlijkse rente in procent (bijv. 0.03 voor 3%)
        :param kosten: Jaarlijkse kosten in procent (bijv. 0.01 voor 1%)
        :param belastingsvoordeel: Belastingsvoordeel in procent (bijv. 0.3 voor 30%)
        :param belasting_opname: Belastingpercentage dat wordt afgehouden bij opname (bijv. 0.2 voor 20%), enkel van toepassing als de inleg voor de 60ste verjaardag is gedaan.
        """
        self.rendement = rendement
        self.kosten = kosten
        self.belastingsvoordeel = belastingsvoordeel
        self.belasting_opname = belasting_opname

    def opbrengst(self, leeftijd_inleg, leeftijd_afname, bruto_inleg=FISCAAL_MAXIMUM):
        """
        Bereken de opbrengst, netto inleg, totaal rendement en gemiddeld rendement per jaar.

        :param bruto_inleg: Het bedrag dat wordt ingelegd.
        :param leeftijd_inleg: De leeftijd waarop de inleg plaatsvindt.
        :param leeftijd_afname: De leeftijd waarop het kapitaal wordt opgenomen.
        :return: Een dict met netto 'opbrengst', 'inleg', 'rendement' en 'rendement_per_jaar'.
        """
        netto_inleg = bruto_inleg * (1 - self.belastingsvoordeel) # Dit is wat we werkelijk betalen, na aftrek belastingsvoordeel
        jaren = leeftijd_afname - leeftijd_inleg
        
        kapitaal = bruto_inleg
        for _ in range(jaren):
            kapitaal *= (1 + self.rendement - self.kosten)

        opbrengst_bruto = kapitaal

        # Belasting bij opname alleen toepassen als de inleg voor de 60ste verjaardag is gedaan
        if leeftijd_inleg < 60:
            opbrengst_netto = opbrengst_bruto * (1 - self.belasting_opname)
        else:
            opbrengst_netto = opbrengst_bruto

        netto_rendement = opbrengst_netto - netto_inleg
        netto_rendement_per_jaar = (opbrengst_netto / netto_inleg) ** (1 / jaren) - 1

        return {
            "opbrengst": opbrengst_netto,
            "inleg": netto_inleg,
            "rendement": netto_rendement,
            "rendement_per_jaar": netto_rendement_per_jaar
        }
    def plot_rendement(self, leeftijden_inleg_afname_pairs, referentie=RENDEMENT_REFERENTIE):
        """
        Genereer een plot van de opbrengsten en netto rendement per jaar voor meerdere combinaties van leeftijden van inleg en opname.

        :param leeftijden_inleg_afname_pairs: Een lijst van tuples, waarbij elke tuple bestaat uit een range van leeftijden voor inleg en een leeftijd voor opname.
        """
        plt.figure(figsize=(12, 8))

        kleuren = plt.cm.tab10.colors  # Gebruik een colormap voor consistente kleuren
        for idx, (leeftijden_inleg, leeftijd_afname) in enumerate(leeftijden_inleg_afname_pairs):
            opbrengsten = []
            rendementen_per_jaar = []

            for leeftijd in leeftijden_inleg:
                resultaat = self.opbrengst(leeftijd_inleg=leeftijd, leeftijd_afname=leeftijd_afname)
                opbrengsten.append(resultaat["opbrengst"])
                rendementen_per_jaar.append(resultaat["rendement_per_jaar"])

            # Plot voor opbrengsten
            plt.subplot(2, 1, 1)
            plt.plot(leeftijden_inleg, opbrengsten, label=f"Opname op {leeftijd_afname} jaar", color=kleuren[idx])

            # Gebruik netto inleg voor referentie opbrengst
            netto_inleg = self.FISCAAL_MAXIMUM * (1 - self.belastingsvoordeel)
            referentie_opbrengsten = []
            for leeftijd in leeftijden_inleg:
                jaren = leeftijd_afname - leeftijd
                referentie_kapitaal = netto_inleg
                for _ in range(jaren):
                    referentie_kapitaal *= (1 + referentie)
                referentie_opbrengsten.append(referentie_kapitaal)
            plt.plot(leeftijden_inleg, referentie_opbrengsten, linestyle='--', color=kleuren[idx], label=f"Referentie opname op {leeftijd_afname} jaar")

        # Configuratie voor opbrengsten plot
        plt.subplot(2, 1, 1)
        plt.xlabel("Leeftijd inleg")
        plt.ylabel("Opbrengst (€)")
        plt.title(f"Opbrengst van {netto_inleg:.2f} € netto inleg")
        plt.grid(True)
        plt.legend()

        # Netto rendement per jaar
        plt.subplot(2, 1, 2)
        for idx, (leeftijden_inleg, leeftijd_afname) in enumerate(leeftijden_inleg_afname_pairs):
            rendementen_per_jaar = []
            for leeftijd in leeftijden_inleg:
                resultaat = self.opbrengst(leeftijd_inleg=leeftijd, leeftijd_afname=leeftijd_afname)
                rendementen_per_jaar.append(resultaat["rendement_per_jaar"])
            plt.semilogy(leeftijden_inleg, rendementen_per_jaar, label=f"Opname op {leeftijd_afname} jaar", color=kleuren[idx])

        plt.xlabel("Leeftijd inleg")
        plt.ylabel("Netto rendement per jaar (%)")
        plt.title("Gemiddeld rendement per jaar")
        plt.axhline(y=referentie, color='r', linestyle='--', label=f"Referentie rendement ({referentie * 100:.2f}%)")
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend()

        plt.tight_layout()
        plt.show()

pensioenfondsArgenta = Pensioenfonds(rendement=RENDEMENT_PENSIOENFONDS_ARGENTA, kosten=KOSTEN_PENSIOENFONDS_ARGENTA)
pensioenfondsArgenta.plot_rendement([(range(30, 60), 60), (range(30, 67), 67)])

# leeftijden_inleg_60 = range(30, 60)  # Mogelijke leeftijden voor inleg tot 60 jaar
# leeftijden_inleg_67 = range(30, 67)  # Mogelijke leeftijden voor inleg tot 67 jaar
# opbrengsten_60 = []
# opbrengsten_67 = []
# rendementen_per_jaar_60 = []
# rendementen_per_jaar_67 = []

# for leeftijd in leeftijden_inleg_60:
#     resultaat_60 = pensioenfondsArgenta.opbrengst(leeftijd_inleg=leeftijd, leeftijd_afname=60)
#     opbrengsten_60.append(resultaat_60["opbrengst"])
#     rendementen_per_jaar_60.append(resultaat_60["rendement_per_jaar"])

# for leeftijd in leeftijden_inleg_67:
#     resultaat_67 = pensioenfondsArgenta.opbrengst(leeftijd_inleg=leeftijd, leeftijd_afname=67)
#     opbrengsten_67.append(resultaat_67["opbrengst"])
#     rendementen_per_jaar_67.append(resultaat_67["rendement_per_jaar"])

# plt.figure(figsize=(12, 8))

# # Plot voor opbrengsten
# plt.subplot(2, 1, 1)
# plt.plot(leeftijden_inleg_60, opbrengsten_60, label="Opname op 60 jaar")
# plt.plot(leeftijden_inleg_67, opbrengsten_67, label="Opname op 67 jaar")
# plt.xlabel("Leeftijd inleg")
# plt.ylabel("Opbrengst (€)")
# plt.title(f"Opbrengst van {resultaat_60["inleg"]} € netto inleg")
# plt.grid(True)
# plt.legend()

# # Plot voor netto rendement per jaar
# plt.subplot(2, 1, 2)
# plt.plot(leeftijden_inleg_60, rendementen_per_jaar_60, label="Opname op 60 jaar")
# plt.plot(leeftijden_inleg_67, rendementen_per_jaar_67, label="Opname op 67 jaar")
# plt.xlabel("Leeftijd inleg")
# plt.ylabel("Netto rendement per jaar (%)")
# plt.title("Gemiddeld rendement per jaar")
# plt.grid(True)
# plt.legend()

# plt.tight_layout()
# plt.show()
