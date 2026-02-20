import requests
from bs4 import BeautifulSoup
import re
import time

# ==========================================
# 1. CONFIGURAZIONE (INSERISCI I TUOI DATI)
# ==========================================
url_corso = "https://didatticaeca.uniecampus.it/allievo/eroga_ua.aspx"

# ⚠️ AGGIORNA SEMPRE I COOKIE PRIMA DI AVVIARE
cookies = {
    'cto_lwid': 'YOURKEY', 
    'ASP.NET_SessionId': 'qpih2mgw42a5d1mdqfd0hz4z',
    '_shibsession_64696461747469636165636168747470733a2f2f6469646174746963616563612e756e696563616d7075732e69742f73686962626f6c657468': 'YOUR KEY',
    'autenticazione': 'YOUR KEY'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0 Safari/537.36',
    'Referer': url_corso,
    'Origin': 'https://didatticaeca.uniecampus.it'
}

session = requests.Session()

print("🚀 Inizio automazione massiva corso e-campus...\n")

# ==========================================
# 2. CICLO PRINCIPALE (ITERA SU TUTTO IL CORSO)
# ==========================================
while True:
    try:
        response = session.get(url_corso, headers=headers, cookies=cookies)
        
        if "login" in response.url.lower():
            print("❌ ERRORE CRITICO: Sei stato reindirizzato al login. Aggiorna i cookie!")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- ESTRAZIONE INFO LEZIONE ---
        cur_lesson_elem = soup.find('span', id='ContentPlaceHolder1_l_lezione_numerogrande')
        tot_lesson_elem = soup.find('span', id='ContentPlaceHolder1_l_lezione_numeropiccolo')
        
        cur_lesson = cur_lesson_elem.text.strip() if cur_lesson_elem else "?"
        tot_lesson = tot_lesson_elem.text.strip() if tot_lesson_elem else "?"
        
        print(f"📖 Analizzo la pagina... [Lezione {cur_lesson} di {tot_lesson}]")
        
        # --- ESTRAZIONE CODICI SICUREZZA ---
        viewstate_tag = soup.find('input', {'name': '__VIEWSTATE'})
        viewstate = viewstate_tag['value'] if viewstate_tag else ''
        
        viewstate_gen_tag = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
        viewstate_gen = viewstate_gen_tag['value'] if viewstate_gen_tag else ''
        
        event_validation_tag = soup.find('input', {'name': '__EVENTVALIDATION'})
        event_validation = event_validation_tag['value'] if event_validation_tag else ''

        # Cerchiamo un bottone non completato (spunta_maggiore.gif)
        bottone_da_cliccare = soup.find('input', {'type': 'image', 'src': re.compile(r'spunta_maggiore\.gif')}, disabled=False)
        
        # --- CASO A: NESSUN BOTTONE (LEZIONE FINITA) ---
        if not bottone_da_cliccare:
            print(f"\n🎉 Tutte le attività della Lezione {cur_lesson} completate!")
            print("[*] Invio il comando finale 'Dichiara come svolta'...")
            
            payload_finale = {
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$b_prossima',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstate_gen,
                '__EVENTVALIDATION': event_validation
            }
            
            resp_finale = session.post(url_corso, headers=headers, cookies=cookies, data=payload_finale)
            
            if resp_finale.status_code == 200:
                print(f"✅ Lezione {cur_lesson} dichiarata come svolta con successo!")
                
                # CONTROLLO FINE CORSO
                if cur_lesson == tot_lesson and cur_lesson != "?":
                    print("\n🎓 INCREDIBILE! Hai completato tutte le lezioni del corso!")
                    break  # Ferma lo script definitivamente
                else:
                    print(f"🔄 Passo alla lezione successiva... Ricarico la pagina in 3 secondi.\n")
                    time.sleep(3)
                    continue  # Ricomincia il ciclo While per la prossima lezione
            else:
                print(f"❌ Errore durante il click finale. Status: {resp_finale.status_code}")
                break
            
        # --- CASO B: C'È UN BOTTONE DA CLICCARE ---
        nome_bottone = bottone_da_cliccare.get('name')
        print(f"[+] Trovata attività da smarcare: {nome_bottone}")
        
        payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_gen,
            '__EVENTVALIDATION': event_validation,
            f'{nome_bottone}.x': '5',
            f'{nome_bottone}.y': '5'
        }
        
        post_resp = session.post(url_corso, headers=headers, cookies=cookies, data=payload)
        
        # Gestione del link pop-up con scudo per gli errori di Moodle
        match_popup = re.search(r"window\.open\('([^']+)'", post_resp.text)
        if match_popup:
            url_relativo = match_popup.group(1)
            url_popup = "https://didatticaeca.uniecampus.it" + url_relativo.replace('../', '/')
            print(f"[*] Simulo l'apertura del pop-up per validare...")
            
            try:
                session.get(url_popup, headers=headers, cookies=cookies, timeout=8)
            except requests.exceptions.RequestException:
                print(f"[!] Moodle è lento o ha chiuso la connessione. Ignoro e vado avanti!")
        
        print("[*] Attendo 7 secondi prima del prossimo click...\n")
        time.sleep(7)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRORE DI RETE: {e}")
        print("Riprovo tra 5 secondi...")
        time.sleep(5)
    except Exception as e:
        print(f"❌ ERRORE IMPREVISTO: {e}")
        break