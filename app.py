import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="Audit Comptable IA", layout="centered")

st.title("📊 Synthèse & Échéancier Financier")
st.write("Glissez votre fichier Excel ou CSV comptable ci-dessous pour générer l'analyse.")

# Champ pour la clé API
api_key = st.text_input("1. Collez votre clé API OpenAI ici :", type="password")

# Zone de dépôt du fichier
uploaded_file = st.file_uploader("2. Déposez le fichier du grand livre / balance", type=["xlsx", "csv"])

if uploaded_file and api_key:
    client = OpenAI(api_key=api_key)
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"Fichier bien reçu ! ({len(df)} lignes analysées)")

        if st.button("🚀 Générer le compte-rendu exécutif"):
            with st.spinner("L'IA examine les comptes et prépare la synthèse..."):
                sample_data = df.head(50).to_string()
                
                prompt = f"""
                Tu es expert-comptable. Voici un extrait de données comptables :
                {sample_data}

                Rédige un compte-rendu clair et structuré en français pour le dirigeant :
                1. Synthèse globale de l'avancement financier.
                2. Points d'attention et anomalies éventuelles.
                3. Frais et échéances à prévoir sous 30 à 60 jours.
                4. Recommandations prioritaires.
                Utilise des listes à puces claires et des montants précis.
                """

                reponse = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                rapport = reponse.choices[0].message.content
                st.subheader("📋 Rapport d'analyse financière")
                st.markdown(rapport)
                
                st.download_button("📥 Télécharger le compte-rendu (.txt)", rapport, file_name="compte_rendu.txt")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
