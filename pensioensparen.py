RENTE_PENSIOENSPAREN = 0.03
RENTE_ETF = 0.08


def bereken_kapitaal(rente, jaarlijkse_inleg, jaren):
    kapitaal = 0
    for jaar in range(0, jaren):
        kapitaal *= (1 + rente)
        kapitaal += jaarlijkse_inleg
    return kapitaal

def pensioen_spaar(jaarlijkse_inleg, jaren):
    belastingvoordeel = 0.3*max(jaarlijkse_inleg, 1030)
    pensioen_kapitaal = bereken_kapitaal(RENTE_PENSIOENSPAREN, jaarlijkse_inleg, jaren)
    etf_kapitaal = bereken_kapitaal(0.08, belastingvoordeel, jaren)
    return pensioen_kapitaal + etf_kapitaal

kapitaal_pensioenspaar = pensioen_spaar(1030, 25)
kapitaal_etf = bereken_kapitaal(RENTE_ETF, 1030, 25)

print(f'kapitaal ETF-sparen: {kapitaal_etf}')
print(f'kapitaal pensioensparen: {kapitaal_pensioenspaar}')      
