# Del I: Finans

VIKTIG: All kode må legges ved, og du må forsikre deg om at den kjører utenfor ditt utviklermiljø. Du kan forvente at bruker må installere pakker for å kjøre koden din. 

## Oppgave 1: prediker opsjonskurs

Data: [AEGON NV data](derivative.csv)
Informasjon om opsjonen: [AEGON NV info](info_option.csv)


### Problemstilling:
  * Lag daglige prediksjoner av opsjonskursen til AEGON NV.
  * Dere kan bruke python eller R.
  * Dere kan bruke maskinlæring eller øknometriske metoder.
  * Bruker dere maskinlæring må data deles i trenings- og testsett.
  * Bruker dere økonometriske metoder trenger dere ikke testsett, men dere må planlegge hvordan dere skal predikere før modellen anvendes for å unngå overtilpasning.
  * Resultatet spiller ingen rolle for karakter. En oppgave som ikke klarer å predikere kan få like høy karakter som en som klarer det. Det avgjørende er at dere har en god plan, beskriver godt hva dere har gjort og kalarer å dra konklusjoner ut fra resultatene

Besvarelsen trenger ikke være spesielt lang, men den skal inneholde:

### Innledning

  * Beskrivelse av problemstillingen og formålet med analysen. 
  * Sett arbeidet inn i en større sammenheng.
  * Hovedresultatene og konklusjonen skal presenteres kort.
  
### Metode og verktøy

  * Beskrivelse av metoden og verktøyene som er brukt.
  * Forklar hvorfor dere har valgt denne metoden, og valg dere har tatt underveis.
  * Forklar eventuelt hvorfor andre metoder ikke er brukt.
  
### Data
  * Beskrivelse av datasettet, variablene, opsjonen og underliggende aksje.

### Resultat
  * Presentasjon av resultatene.
  * Både grafisk og med tabeller
  * Oversiktlig og forståelig presentasjon av resultatene premieres
  * 
### Diskusjon
  * Forklar hovedfunnene
  * Hvilke konklusjoner kan trekkes?
  
  
## Oppgave 2: Pris et derivat

Data: valgfritt

### Problemstilling:

* Finn data på underliggende: 
  * Det må være noe som omsettes ofte
  * Det kan være alt fra eiendom, til kryptovaluta og aksjer. 
* Definer en kontrakt som gir en bestemt pris på et bestemt tidspunkt i fremtiden, avhengig av verdien på underliggende.
  * Det kan være en opsjon, men helst noe som gir en kontanstrømprofil. 
* Lag en funksjon som regner ut en risikonøytral sannsynlighetsfordeling for det underliggende, med følgende argumenter
  * Dagens verdi på underliggende
  * Tid til kontrakten utløper
  * Volatilitet
  * Rente
* Lagen en funksjon som priser kontrakten, med de samme argumentene som over ved hjelp av numerisk risikonøytral prising. 
* Det anbefales å bruke Python. 


Denne besvarelsen trenger heller ikke være spesielt lang, men den skal inneholde:

### Innledning

  * Hvorfor har du valgt denne kontrakten og dette underliggende?
  
### Metode og data

  * Beskriv hvordan du har funnet data og hvordan du har laget funksjonene.

### Resultat
  * Vis grafisk hvordan kontraktens verdi har utviklet seg over tid, og hvordan den endrer seg med endringer volatilitet og og underliggende.
  


# Vurderingskriterier

## Hovedkriterier


- **Metode**  
  Studenten skal vise evne til å velge og anvende hensiktsmessige metoder samt ha korrekt implementering av kode og analyseprosess.

- **Forståelse av konseptene**  
  Studenten skal demonstrere at de forstår relevante finansielle og statistiske teorier (f.eks. opsjonsprising, tidsserieanalyse, risikonøytral sannsynlighetsfordeling) og kan knytte disse til praktiske problemstillinger.

- **Argumentasjon og drøfting**  
  Studenten skal kunne begrunne valg av metoder og parametere, samt diskutere styrker og svakheter ved modellene, dataene og resultatene på en kritisk og reflektert måte.

## Karakterbeskrivelser

- **A (Fremragende)**: Studenten viser fullstendig mestring av metodene og en dyptgående forståelse av de teoretiske konseptene. Argumentasjonen er velbegrunnet og viser innsikt som går utover grunnleggende krav. Studenten demonstrerer en helhetlig og bred forståelse, samt evnen til å integrere ulike analyser på en sammenhengende måte.

- **B (Meget god)**: Studenten mestrer metodene fullt ut og viser god forståelse av de teoretiske aspektene. Argumentasjonen er godt fundert, og analysene er grundige, men mangler den dypere innsikten som kjennetegner en A-karakter.

- **C (God)**: Studenten gjennomfører metodene med få feil og viser en solid forståelse av de viktigste konseptene. Argumentasjonen er tilstrekkelig, men kan mangle dybde og nyanser.

- **D (Nokså god)**: Studenten behersker det meste av metodene og viser en viss forståelse av konseptene. Det kan være enkelte mangler i argumentasjonen og gjennomføringen av analysene, men helheten er akseptabel.

- **E (Tilstrekkelig)**: Studenten klarer å anvende noen av metodene og viser en grunnleggende, men begrenset forståelse av teorien. Argumentasjonen er enkel og mangler dybde. Analysene kan være ufullstendige eller overfladiske.

- **F (Ikke bestått)**: Studenten har betydelige feil i metodene eller unnlater å gjennomføre flere av de nødvendige analysene. Forståelsen av konseptene er svak eller fraværende, og argumentasjonen er mangelfull eller feilaktig.

### Tilleggskommentarer

- **Bruk av kilder**: Studenten forventes å benytte relevante kilder korrekt, og disse bør integreres for å styrke argumentasjonen og analysen.
- **Struktur og presentasjon**: Rapporten bør være godt strukturert, med klare avsnitt og tydelig fremstilling av analysene og resultatene.

En helhetlig vurdering vil bli gjort basert på hvordan studenten oppfyller kriteriene over.


