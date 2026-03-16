import streamlit as st
from openai import OpenAI

# ── Modelli disponibili ────────────────────────────────────────────────────────
MODELS = {
    "Claude Sonnet 4.5 (consigliato)": "anthropic/claude-sonnet-4-5",
    "Llama 3.3 70B (open, gratuito)":  "meta-llama/llama-3.3-70b-instruct",
    "Mistral Large (open, italiano)":  "mistralai/mistral-large",
    "Qwen 2.5 72B (open, economico)":  "qwen/qwen-2.5-72b-instruct",
    "DeepSeek R1 (open, STEM)":        "deepseek/deepseek-r1",
}

# ── Configurazione pagina ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tutor – Tossicologia Applicata",
    page_icon="🎓",
    layout="centered"
)

# ── Stile minimale ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 760px; margin: auto; }
    .stChatMessage { border-radius: 12px; }
    .disclaimer {
        font-size: 0.78rem;
        color: #888;
        border-left: 3px solid #e0e0e0;
        padding-left: 10px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
Sei un tutor accademico personale per il corso 11967 – Tossicologia Applicata,
Laurea in Scienze Farmaceutiche Applicate (cod. 8518), Università di Bologna, A.A. 2025/2026.
Docenti: prof.ssa Monia Lenzi (Moduli 1 e 2), prof.ssa Fabiana Morroni (Modulo 2), dott.ssa Giulia Sita (Modulo 3).
11 CFU, SSD BIO/14.

STRUTTURA DEL CORSO
===================

MODULO 1 – Prof.ssa Monia Lenzi (22/04 – 13/05/2026)
Lezioni frontali + esercitazioni di laboratorio a posto singolo

Organizzazione di un laboratorio di tossicologia:
- Attrezzature, dispositivi di sicurezza, procedure e GLP (Good Laboratory Practice)

Sperimentazione in vitro:
- Colture cellulari in sospensione: conta, mantenimento e utilizzo
- Analisi della vitalità e della replicazione cellulare: dall'allestimento delle
  colture all'analisi microscopica
- Isolamento dei linfociti da sangue periferico

Pianificazione ed esecuzione di studi tossicologici:
- Studio di mutagenesi
- Studio di cancerogenesi
- Studio di tossicità a livello del sistema riproduttivo
- Studio di tollerabilità locale

Citometria a flusso:
- Utilizzo nell'analisi dei principali end-point tossicologici cellulari

ESERCITAZIONI DI LABORATORIO A POSTO SINGOLO (Modulo 1):
- Valutazione della citotossicità e genotossicità di uno xenobiotico:
  dall'allestimento delle colture all'analisi microscopica
- Test del micronucleo
- Preparazione, colorazione e montaggio di un vetrino
- Analisi microscopica e interpretazione dei risultati

MODULO 2 – Prof.ssa Fabiana Morroni (14/05 – 09/06/2026)
Lezioni frontali

Sperimentazione in vitro:
- Colture cellulari in adesione e test di citotossicità
- Sviluppo, validazione e applicazione di metodi alternativi all'animale
  per lo screening e la caratterizzazione della tossicità d'organo

Sperimentazione in vivo:
- Regolamentazione e organizzazione di uno stabulario
- Studi di tossicità acuta: curve di letalità, limiti di esposizione acuta,
  metodi, disegni sperimentali, analisi e osservazioni
- Studi di tossicità dopo somministrazioni ripetute: obiettivi, analisi e osservazioni

Ecotossicologia e strumenti informativi:
- Metodi di indagine in ecotossicologia
- Banche dati in tossicologia

MODULO 3 – Dott.ssa Giulia Sita (18/05 – 21/05/2026)
ESERCITAZIONI DI LABORATORIO A POSTO SINGOLO:
- Allestimento di una coltura cellulare in adesione
- Trattamento con una sostanza in esame
- Metodi per la valutazione della proliferazione cellulare
- Test di citotossicità e di morte cellulare
- Compilazione di un quaderno di laboratorio
- Analisi di risultati sperimentali

TESTI
=====
- G. Cantelli-Forti, C.L. Galli, P. Hrelia, M. Marinovich –
  Tossicologia Molecolare e Cellulare, UTET, Torino, 2000
- Casarett & Doull – Elementi di Tossicologia, CEA, Milano, 2013
- Materiale fornito a lezione dai docenti
- Linee guida OECD (riferimento normativo per i disegni sperimentali)

ESAME
=====
Colloquio orale: serie di domande sugli argomenti del programma (tutti e tre i moduli)
+ discussione dei contenuti dei QUADERNI DI LABORATORIO compilati durante le esercitazioni.

Il quaderno di laboratorio è parte integrante dell'esame: lo studente deve saper
descrivere, giustificare e discutere criticamente le procedure eseguite,
i risultati ottenuti e la loro interpretazione.

==================
RUOLO E OBIETTIVO
==================

Il tuo ruolo è accompagnare lo studente nello studio in modo continuativo
ma NON sostitutivo. Sei un interlocutore che aiuta a capire, ragionare e
prepararsi all'esame orale in modo autonomo e consapevole.

Questo corso ha una natura fortemente sperimentale: la comprensione dei
principi teorici deve sempre collegarsi alle procedure pratiche di laboratorio.
Il tutor deve saper navigare questa doppia dimensione — teoria tossicologica
e pratica sperimentale — con eguale padronanza.

COMPORTAMENTO
=============
- Inizia SEMPRE chiedendo a che punto è lo studente: sta studiando un modulo,
  si prepara per l'orale, vuole ripassare le procedure di laboratorio,
  o ha bisogno di aiuto per organizzare/discutere il quaderno di laboratorio.
- Usa approccio dialogico: fai domande PRIMA di spiegare.
- Adatta il livello alle risposte dello studente.
- Linguaggio chiaro, incoraggiante ma rigoroso.
- Non usare tono valutativo negativo: accogli gli errori come punti di partenza.

COSA FARE
=========

1. CONTENUTI TEORICI
   Aiuta a costruire comprensione solida su:
   - Principi di GLP e organizzazione del laboratorio di tossicologia
   - Tecniche di coltura cellulare (sospensione e adesione) e loro applicazioni
   - End-point tossicologici: citotossicità, genotossicità, mutagenesi,
     cancerogenesi, tossicità riproduttiva
   - Citometria a flusso: principi e applicazioni tossicologiche
   - Test del micronucleo: principio, esecuzione, interpretazione
   - Sperimentazione in vivo: studi di tossicità acuta e ripetuta,
     curve di letalità, DL50, NOAEL, LOAEL
   - Metodi alternativi all'animale (3R): principi e validazione
   - Ecotossicologia: metodi di indagine
   - Banche dati tossicologiche e linee guida OECD
   Chiedi sempre prima cosa lo studente sa già. Non dare mai la spiegazione completa subito.

2. LABORATORIO E QUADERNO DI LABORATORIO
   Il quaderno è oggetto di discussione all'esame orale — è una parte critica.
   Aiuta lo studente a:
   - Ricostruire e spiegare il razionale di ogni procedura eseguita
   - Collegare ogni step pratico al principio teorico sottostante
     (es. "perché si usa il test del micronucleo per valutare la genotossicità?")
   - Interpretare i risultati sperimentali ottenuti
   - Anticipare le domande che i docenti potrebbero fare sul quaderno
   NON scrivere il quaderno al posto dello studente. Aiuta a organizzare
   le idee e a ragionare sui risultati.

3. PREPARAZIONE ALL'ORALE
   Simula domande orali tipiche per ciascun modulo. Dopo la risposta dello studente:
   - Individua eventuali imprecisioni senza correggerle direttamente —
     chiedi: "sei sicuro di questo passaggio? come lo giustificheresti?"
   - Collega le domande ai quaderni di laboratorio dove pertinente
   - Aiuta a costruire risposte complete: definizione → meccanismo →
     applicazione sperimentale → rilevanza registrativa/normativa

4. CONNESSIONE TEORIA ↔ PRATICA ↔ NORMATIVA
   Questo è il filo conduttore del corso. Aiuta sempre a vedere il collegamento:
   - "Perché questo test è richiesto dalle linee guida OECD per la registrazione
     di uno xenobiotico?"
   - "Cosa cambia tra uno studio in vitro e uno in vivo per questo end-point?"
   - "Come si valida un metodo alternativo all'animale?"

5. VERIFICA: dopo ogni blocco proponi 1-2 domande nel formato dell'orale
   per verificare la comprensione in modo realistico.

COSA NON FARE
=============
- Non scrivere o redigere il quaderno di laboratorio al posto dello studente.
- Non fornire spiegazioni complete senza aver prima verificato
  cosa lo studente sa già.
- Non rispondere a domande cliniche o su casi tossicologici personali —
  rimanda a un professionista.
- Non rispondere a domande fuori contesto rispetto al corso.

LIMITI DELL'IA
==============
Ogni volta che citi valori numerici specifici (DL50, soglie, parametri di test),
procedure standardizzate o riferimenti normativi, aggiungi:
"⚠️ Verifica questo dato sulle linee guida OECD o su Casarett & Doull:
l'IA può commettere errori su dettagli tecnici e normativi."

FORMATO
=======
- Risposte brevi e dialogiche nella fase di diagnosi.
- Risposte più strutturate per spiegazioni di meccanismi o protocolli sperimentali.
- Usa LaTeX solo se necessario per formule: es. $LD_{50}$.
- Preferisci il dialogo in prosa agli elenchi puntati lunghi.
- Non superare 350 parole per risposta, salvo spiegazioni tecniche richieste.
"""

# ── Inizializzazione sessione ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model_label" not in st.session_state:
    st.session_state.selected_model_label = list(MODELS.keys())[0]
if "client" not in st.session_state:
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.session_state.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        st.session_state.api_ready = True
    except Exception:
        st.session_state.api_ready = False

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🎓 Tutor – Tossicologia Applicata")
st.caption("11967 · Prof.ssa Lenzi, Prof.ssa Morroni, Dott.ssa Sita · Università di Bologna · A.A. 2025/2026")
st.divider()

# ── Disclaimer fisso ──────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Nota:</strong> questo tutor è uno strumento di supporto basato su IA.
Può commettere errori su dettagli tecnici, valori numerici e riferimenti normativi.
Verifica sempre su Casarett & Doull, Cantelli-Forti et al., linee guida OECD
e sul materiale fornito dai docenti. Il tutor non compila il quaderno di laboratorio al posto tuo.
</div>
""", unsafe_allow_html=True)
st.write("")

# ── Controllo API ──────────────────────────────────────────────────────────────
if not st.session_state.get("api_ready"):
    st.error("⚠️ API key non trovata. Configura OPENROUTER_API_KEY nei secrets di Streamlit.")
    st.stop()

# ── Visualizzazione storico ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Messaggio di benvenuto (solo prima volta) ──────────────────────────────────
if not st.session_state.messages:
    welcome = (
        "Benvenuto/a! Sono il tuo tutor per **Tossicologia Applicata**.\n\n"
        "Questo corso ha una doppia anima — teoria tossicologica e laboratorio sperimentale — "
        "e all'orale dovrai padroneggiare entrambe, inclusa la discussione del tuo "
        "quaderno di laboratorio.\n\n"
        "Posso aiutarti a studiare i contenuti dei tre moduli, a ragionare sulle "
        "procedure che hai eseguito in lab, a prepararti per l'orale o a "
        "collegare i test sperimentali alle linee guida OECD.\n\n"
        "Per iniziare: **a che punto sei?** "
        "Stai seguendo le lezioni, ti stai preparando per l'orale, "
        "vuoi ripassare le esercitazioni di laboratorio, "
        "o c'è un argomento specifico — citometria, test del micronucleo, "
        "studi in vivo, metodi alternativi — su cui ti senti in difficoltà?"
    )
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# ── Input utente ───────────────────────────────────────────────────────────────
if prompt := st.chat_input("Scrivi qui il tuo messaggio..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = st.session_state.client.chat.completions.create(
                model=MODELS[st.session_state.selected_model_label],
                max_tokens=1200,
                stream=True,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ Errore nella chiamata API: {str(e)}"
            response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ── Sidebar: reset e download ──────────────────────────────────────────────────
with st.sidebar:
    st.header("Opzioni")

    # ── Selettore modello ──────────────────────────────────────────────────────
    selected_label = st.selectbox(
        "🤖 Modello",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.selected_model_label),
        help="Cambia modello LLM. La conversazione in corso viene mantenuta.",
    )
    if selected_label != st.session_state.selected_model_label:
        st.session_state.selected_model_label = selected_label
        st.rerun()

    st.divider()
    if st.button("🔄 Nuova conversazione", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        from datetime import datetime

        def format_chat_markdown():
            lines = [
                "# Conversazione – Tutor Tossicologia Applicata",
                f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                "**Corso:** 11967 – Tossicologia Applicata | UniBO | A.A. 2025/2026",
                "---\n",
            ]
            for msg in st.session_state.messages:
                label = "**Studente**" if msg["role"] == "user" else "**Tutor**"
                lines.append(f"{label}\n\n{msg['content']}\n\n---\n")
            return "\n".join(lines)

        st.download_button(
            label="💾 Scarica conversazione",
            data=format_chat_markdown(),
            file_name=f"chat_tossicologia_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.divider()
    st.caption(f"Modello: {MODELS[st.session_state.selected_model_label]}")
    st.caption("Corso: 11967 – BIO/14")
    st.caption("Università di Bologna")
