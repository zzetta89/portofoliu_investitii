#  Aplicație pentru Gestionarea Portofoliului de Investiții

Aceasta este o aplicație web interactivă construită cu **Streamlit** și **Python**, menită să ajute utilizatorii să își gestioneze portofoliul de investiții (acțiuni, ETF-uri etc.). Aplicația preia automat prețurile curente ale activelor folosind **Yahoo Finance** și permite vizualizarea și exportul datelor.

##  Funcționalități Principale

* * Adăugare Investiții: Introduci simbolul activului (ex: `AAPL`, `TSLA`), cantitatea și prețul de achiziție, iar aplicația preia automat prețul curent la zi.
* * Ștergere Investiții: Elimină ușor activele pe care nu le mai deții.
* * Vizualizare Portofoliu:
    * Afișează un tabel detaliat cu toate investițiile.
    * Calculează valoarea totală a portofoliului și profitul/pierderea.
    * Suport multi-valută: Poți vizualiza portofoliul în **RON**, **EUR** sau **USD**.
    * Grafic interactiv (Bar chart) care arată ponderea fiecărui activ în funcție de valoarea totală.
* * Export în Excel: Descarcă întregul portofoliu într-un fișier `.xlsx` cu coloane auto-ajustate pentru un format curat.

##  Tehnologii Utilizate

* [Python](https://www.python.org/) - Limbajul de bază.
* [Streamlit](https://streamlit.io/) - Pentru interfața grafică web (GUI).
* [yfinance](https://pypi.org/project/yfinance/) - Pentru extragerea datelor financiare în timp real de pe Yahoo Finance.
* [Pandas](https://pandas.pydata.org/) - Pentru manipularea datelor.
* [Matplotlib](https://matplotlib.org/) - Pentru generarea graficelor.
* [Openpyxl](https://openpyxl.readthedocs.io/) - Pentru exportul datelor în format Excel.

