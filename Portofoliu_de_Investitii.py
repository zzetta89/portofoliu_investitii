from io import BytesIO
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows


# Clasa PortofoliuInvestitii pentru gestionarea investitiilor
class PortofoliuInvestitii:
    def __init__(self):
        self.investitii = []  # Lista de investitii

    # Metodă pentru adăugarea unei noi investiții
    def adaugare_investitie(self, nume, cantitate, pret_cumparare, pret_curent_ron, pret_curent_eur, pret_curent_usd,
                            moneda):
        self.investitii.append({
            "Nume": nume,
            "Cantitate": cantitate,
            "Pret Cumparare": pret_cumparare,
            "Pret Curent RON": pret_curent_ron,
            "Pret Curent EUR": pret_curent_eur,
            "Pret Curent USD": pret_curent_usd,
            "Moneda": moneda
        })

    # Metodă pentru ștergerea unei investiții din portofoliu
    def stergere_investitie(self, nume):
        for i in self.investitii:
            if i["Nume"] == nume:
                self.investitii.remove(i)
                return True
        return False

    # Calcul valoare totală a portofoliului
    def calcul_valoare_totala(self, moneda_selectata):
        s = 0
        for i in self.investitii:
            pret_curent = i["Pret Curent RON"]
            if moneda_selectata == "EUR":
                pret_curent = i["Pret Curent EUR"]
            elif moneda_selectata == "USD":
                pret_curent = i["Pret Curent USD"]
            s += pret_curent * i["Cantitate"]
        return s

    # Calcul profit total pe baza diferenței dintre prețul curent și prețul de achiziție
    def calcul_profit(self, moneda_selectata):
        s = 0
        cursuri_de_schimb = obtine_cursuri_de_schimb()

        for i in self.investitii:
            pret_cumparare = i["Pret Cumparare"]
            pret_curent = i["Pret Curent RON"]

            if moneda_selectata == "EUR":
                pret_cumparare = pret_cumparare / cursuri_de_schimb["RON"]  # Convertim prețul de cumpărare în EUR
                pret_curent = i["Pret Curent EUR"]  # Folosim prețul curent în EUR
            elif moneda_selectata == "USD":
                pret_cumparare = pret_cumparare / cursuri_de_schimb["RON"] * cursuri_de_schimb[
                    "USD"]  # Convertim prețul de cumpărare în USD
                pret_curent = i["Pret Curent USD"]  # Folosim prețul curent în USD

            s += i["Cantitate"] * (pret_curent - pret_cumparare)

        return s

    # Obținem toate investițiile
    def get_investitii(self):
        return self.investitii


# Funcția pentru a obține prețul curent din Yahoo Finance folosind simbolul activului
def obtine_pret_curent(symbol):
    try:
        data = yf.Ticker(symbol)
        pret_curent = data.history(period="1d")["Close"].iloc[0]  # Obține prețul de închidere al zilei curente
        return pret_curent
    except Exception as e:
        print(f"Eroare la extragerea prețului curent: {e}")
        return None


# Funcția pentru a obține cursul de schimb între RON, EURO și DOLLAR
def obtine_cursuri_de_schimb():
    return {
        "RON": 4.8,  # Exemplu de conversie de la EURO la RON
        "USD": 1.1  # Exemplu de conversie de la EURO la USD
    }


# Creăm instanța portofoliului
if "portofoliu" not in st.session_state:
    st.session_state["portofoliu"] = PortofoliuInvestitii()

portofoliu = st.session_state["portofoliu"]

# Interfața aplicației
st.title("Aplicație pentru gestionarea portofoliului de investiții")

# Meniu lateral cu opțiuni
meniu = ["Adaugă investiție", "Șterge investiție", "Vizualizează portofoliu", "Exportă în Excel"]
alegere = st.sidebar.selectbox("Alege o opțiune", meniu)

# Adăugare investiție
if alegere == "Adaugă investiție":
    st.header("Adaugă o nouă investiție")
    nume = st.text_input("Numele activului")  # Introducerea numelui activului
    cantitate = st.number_input("Cantitate", min_value=0.0)  # Cantitatea activului
    pret_cumparare = st.number_input("Preț de achiziție (RON)", min_value=0.0)  # Prețul de achiziție în RON
    moneda = "RON"  # Se adaugă doar în RON
    # Obținem prețul curent din Yahoo Finance
    pret_curent_eur = obtine_pret_curent(nume)
    if pret_curent_eur:
        cursuri = obtine_cursuri_de_schimb()  # Obținem cursurile de schimb
        # Calculăm prețurile curente pentru fiecare monedă
        pret_curent_ron = pret_curent_eur * cursuri["RON"]
        pret_curent_usd = pret_curent_eur * cursuri["USD"]

        st.write(f"Prețul curent al activului {nume} este {pret_curent_eur:.2f} EURO")
        st.write(f"Prețul curent în RON este {pret_curent_ron:.2f} RON")
        st.write(f"Prețul curent în DOLLAR este {pret_curent_usd:.2f} USD")

    if st.button("Adaugă"):
        if pret_curent_eur:
            portofoliu.adaugare_investitie(nume, cantitate, pret_cumparare, pret_curent_ron, pret_curent_eur,
                                           pret_curent_usd, moneda)
            st.success(f"Investiția {nume} a fost adăugată!")
        else:
            st.error("Prețul curent nu a putut fi obținut.")

# Ștergere investiție
elif alegere == "Șterge investiție":
    st.header("Șterge o investiție")

    if not portofoliu.investitii:
        st.warning("Portofoliul este gol.")  # Dacă portofoliul este gol
    else:
        lista_nume_investitii = [investitie["Nume"] for investitie in portofoliu.investitii]
        nume = st.selectbox("Alege investiția pe care vrei să o ștergi", lista_nume_investitii)
        if st.button("Șterge"):
            if portofoliu.stergere_investitie(nume):
                st.success(f"Investiția {nume} a fost ștearsă!")
            else:
                st.error(f"Investiția {nume} nu se află în portofoliu!")

# Vizualizare portofoliu
elif alegere == "Vizualizează portofoliu":
    st.header("Portofoliu")
    moneda_selectata = st.selectbox("Selectează moneda pentru vizualizare", ["RON", "EUR", "USD"])

    if portofoliu.investitii:
        df = pd.DataFrame(portofoliu.investitii)

        # Calculăm prețul curent și prețul de cumpărare în funcție de moneda selectată
        if moneda_selectata == "RON":
            df['Pret Curent'] = df['Pret Curent RON']
            # Prețul de cumpărare rămâne neschimbat în RON
            df['Pret Cumparare'] = df['Pret Cumparare']  # Nu facem nicio conversie pentru RON
        elif moneda_selectata == "EUR":
            df['Pret Curent'] = df['Pret Curent EUR']
            df['Pret Cumparare'] = df['Pret Cumparare'] / obtine_cursuri_de_schimb()[
                'RON']  # Convertim prețul de cumpărare în EUR
        elif moneda_selectata == "USD":
            df['Pret Curent'] = df['Pret Curent USD']
            df['Pret Cumparare'] = df['Pret Cumparare'] / obtine_cursuri_de_schimb()['RON'] * \
                                   obtine_cursuri_de_schimb()['USD']  # Convertim prețul de cumpărare în USD

        # Calculăm valoarea totală în funcție de moneda selectată
        df['Valoare Totală'] = df['Cantitate'] * df['Pret Curent']

        # Eliminăm coloanele vechi (Pret Curent RON, Pret Curent EUR, Pret Curent USD)
        df = df.drop(columns=['Pret Curent RON', 'Pret Curent EUR', 'Pret Curent USD'])

        # Adăugăm un index la tabel
        df.insert(0, 'Index', range(1, len(df) + 1))

        # Formatarea numerelor la 2 zecimale
        df = df.round({"Pret Cumparare": 2, "Pret Curent": 2, "Valoare Totală": 2})

        # Afișăm tabelul cu investiții
        st.dataframe(df[['Index', 'Nume', 'Cantitate', 'Pret Cumparare', 'Pret Curent', 'Valoare Totală']])

        # Afișăm valoarea totală și profitul în moneda selectată
        st.subheader(f"Valoarea totală a portofoliului în {moneda_selectata}")
        st.metric(f"Valoare Totală", f"{portofoliu.calcul_valoare_totala(moneda_selectata):.2f} {moneda_selectata}")

        # Afișăm profitul în moneda selectată
        profit = portofoliu.calcul_profit(moneda_selectata)
        culoare_profit = "green" if profit > 0 else "red"
        st.subheader(f"Profit total în {moneda_selectata}")
        st.markdown(f"<h3 style='color:{culoare_profit};'>{profit:.2f} {moneda_selectata}</h3>", unsafe_allow_html=True)

        # Creăm graficul cu achizițiile din portofoliu
        fig, ax = plt.subplots()
        ax.bar(df['Nume'], df['Valoare Totală'], color='skyblue')

        ax.set_xlabel('Activ')
        ax.set_ylabel(f'Valoare Totală în {moneda_selectata}')
        ax.set_title(f'Grafic Achiziții din Portofoliu ({moneda_selectata})')
        plt.xticks(rotation=45, ha="right")

        # Afișăm graficul
        st.pyplot(fig)

    else:
        st.warning("Portofoliul este gol.")  # Dacă portofoliul este gol

# Export în Excel
elif alegere == "Exportă în Excel":
    st.header("Exportă portofoliul în Excel")

    if portofoliu.investitii:
        df = pd.DataFrame(portofoliu.investitii)

        # Calculăm valoarea totală în RON pentru a o adăuga în Excel
        df['Valoare Totală'] = df['Cantitate'] * df['Pret Curent RON']

        # Creăm un fișier Excel din DataFrame
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Investitii')

            # Obținem foaia de lucru
            workbook = writer.book
            sheet = workbook['Investitii']

            # Ajustăm lățimea coloanelor
            for col in sheet.columns:
                max_length = 0
                column = col[0].column_letter  # obținem litera coloanei
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)  # Adăugăm un mic spațiu pentru fiecare coloană
                sheet.column_dimensions[column].width = adjusted_width

        excel_file.seek(0)

        # Permitem utilizatorului să descarce fișierul Excel
        st.download_button(
            label="Descarcă fișierul Excel",
            data=excel_file,
            file_name="portofoliu_investitii.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Portofoliul este gol. Nu se poate exporta.")