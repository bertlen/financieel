RENTE_PENSIOENSPAREN = 0.03
RENTE_ETF = 0.08
JAREN = 25
MAANDELIJKS = 1000
JAARLIJKSE_PENSIOENSPAAR = 1030

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

kapitaal_pensioenspaar = pensioen_spaar(JAARLIJKSE_PENSIOENSPAAR, 25)
kapitaal_etf_als_pensioenspaar = bereken_kapitaal(RENTE_ETF, JAARLIJKSE_PENSIOENSPAAR, 25)
kapitaal_etf = bereken_kapitaal(RENTE_ETF, 12*MAANDELIJKS, 25)

print(f'ETF i.p.v. pensioensparen na {JAREN} jaar: {kapitaal_etf_als_pensioenspaar}')
print(f'pensioensparen + belastingvoordeel als ETF na {JAREN} jaar: {kapitaal_pensioenspaar}')    
print(f'Maandelijks {MAANDELIJKS} in ETF na {JAREN} jaar: {kapitaal_etf}')    
  
