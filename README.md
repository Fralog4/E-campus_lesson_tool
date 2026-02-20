# E-Campus Course Automator 🎓🤖

Questo script in Python automatizza il completamento delle videolezioni e la visualizzazione del materiale (PDF, slide) sulla piattaforma didattica E-Campus. 

Lo script simula la presenza dell'utente cliccando progressivamente su ogni attività (ottenendo la spunta verde ✅) e dichiarando automaticamente la lezione come "svolta" per passare a quella successiva, iterando su tutto il corso.

## ⚠️ Disclaimer Importante
**Questo progetto è stato realizzato a puro scopo didattico e di studio del web scraping e dell'automazione HTTP.** L'utilizzo di script automatici potrebbe violare i Termini di Servizio (TOS) della piattaforma universitaria. L'autore non si assume alcuna responsabilità per eventuali blocchi dell'account, provvedimenti disciplinari o malfunzionamenti derivanti dall'uso di questo codice. Usalo a tuo rischio e pericolo!

---

## 🛠️ Requisiti

Per eseguire lo script, devi avere installato sul tuo computer:
* **Python 3.x**
* Un browser web (Chrome, Edge, o Firefox)

Le librerie Python necessarie sono:
* `requests`
* `beautifulsoup4`

---

## 🚀 Installazione

1. **Clona il repository** (o scarica il file ZIP):
   ```bash
   git clone [https://github.com/TUO_USERNAME/NOME_REPO.git](https://github.com/TUO_USERNAME/NOME_REPO.git)
   cd NOME_REPO

```

2. **Crea e attiva un Virtual Environment** (consigliato):
* Su Windows:
```bash
python -m venv env
env\Scripts\activate

```


* Su macOS/Linux:
```bash
python3 -m venv env
source env/bin/activate

```




3. **Installa le dipendenze**:
```bash
pip install requests beautifulsoup4

```



---

## ⚙️ Configurazione (Fondamentale!)

Per far funzionare lo script, **devi fornirgli i tuoi cookie di sessione attivi**. Lo script non usa username e password, ma "prende in prestito" la tua sessione dal browser.

### Come recuperare i Cookie:

1. Apri il browser e fai il login sulla piattaforma E-Campus.
2. Vai sulla pagina principale del corso che vuoi automatizzare (la pagina con l'elenco delle lezioni).
3. Apri gli **Strumenti per Sviluppatori** premendo `F12` (o clic destro -> *Ispeziona*).
4. Vai sulla scheda **Application** (Chrome/Edge) o **Archiviazione** (Firefox).
5. Nel menu a sinistra, espandi la voce **Cookies** e clicca sull'URL della didattica (`https://didatticaeca.uniecampus.it`).
6. Cerca questi due cookie nella tabella e copia il loro **Valore** (Value):
* `ASP.NET_SessionId`
* `autenticazione`



### Inserisci i Cookie nello Script:

Apri il file `ecampus_bot.py` con un editor di testo e incolla i valori copiati all'interno del dizionario `cookies`, al posto delle stringhe segnaposto:

```python
cookies = {
    'cto_lwid': 'a4658357-4489-4e1f-bed3-15a473ca2704', 
    'ASP.NET_SessionId': 'INCOLLA_QUI_IL_TUO_VALORE',
    '_shibsession_...': '_10fc27cfc9dcf11235f13e3653ba39f6',
    'autenticazione': 'INCOLLA_QUI_IL_TUO_VALORE'
}

```

> **🛑 ATTENZIONE:** NON caricare MAI il file con i tuoi cookie personali su GitHub! Se fai dei commit, ricordati di rimuovere i valori o di usare un file `.env` separato (aggiungendolo al `.gitignore`).

---

## ▶️ Utilizzo

Una volta configurati i cookie, assicurati di essere nell'ambiente virtuale e lancia lo script:

```bash
python ecampus_bot.py

```

Lo script stamperà a schermo i log di debug, mostrandoti in tempo reale quale bottone sta cliccando e a quale lezione si trova. Quando avrà completato l'intero corso, si fermerà da solo.

### Risoluzione dei Problemi

* **"ERRORE CRITICO: Sei stato reindirizzato al login"**: I tuoi cookie sono scaduti (di solito durano qualche ora). Rifai il login sul browser, ripeti la procedura di configurazione per prendere i nuovi cookie e aggiorna lo script.
* **Moodle connection timeout / "Ignoro e vado avanti"**: È normale. Il server video a volte rifiuta connessioni troppo veloci. Lo script è progettato per ignorare questo errore e continuare a smarcare la lezione.